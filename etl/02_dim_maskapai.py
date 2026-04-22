"""
02_dim_maskapai.py — Generate Dim_Maskapai dari BAB II CSV
ETL Pipeline v3.2 (Clean Rewrite)

Output:
  - output/dim_maskapai.csv

Sumber: BAB II — Perusahaan Angkutan Udara (CSV Berjadwal + CSV Asing, 2020-2024)
Kolom output: maskapai_id, nama_maskapai, kategori_maskapai, jenis_kegiatan, negara_asal
"""

import csv
import sys
import os
import glob

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from etl.config import OUTPUT_DIR, BAB_II_DIR, TAHUN_RANGE, ensure_output_dir
from etl.utils import standardize_maskapai, normalize_jenis_kegiatan, MASKAPAI_NEGARA_FILL

# Log standarisasi: (raw, standardized)
STANDARDIZATION_LOG = []


def find_csv_by_keyword(folder, *keywords):
    """Cari file CSV di folder yang mengandung semua keywords (case-insensitive)."""
    if not os.path.isdir(folder):
        return None
    for f in os.listdir(folder):
        if not f.lower().endswith('.csv'):
            continue
        f_upper = f.upper()
        if all(kw.upper() in f_upper for kw in keywords):
            return os.path.join(folder, f)
    return None


def read_csv_auto(filepath):
    """Baca CSV dengan auto-detect encoding (utf-8 → latin-1 fallback)."""
    for enc in ['utf-8-sig', 'utf-8', 'latin-1', 'cp1252']:
        try:
            with open(filepath, 'r', encoding=enc, newline='') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                return rows, reader.fieldnames
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot read {filepath} with any supported encoding")


def extract_nasional(tahun):
    """Extract maskapai nasional dari CSV Berjadwal per tahun."""
    folder = os.path.join(BAB_II_DIR, str(tahun))
    filepath = find_csv_by_keyword(folder, 'BERJADWAL')

    if filepath is None:
        print(f"  ⚠️ Tidak ditemukan CSV Berjadwal untuk tahun {tahun}")
        return []

    rows, fieldnames = read_csv_auto(filepath)
    print(f"  📄 Nasional {tahun}: {os.path.basename(filepath)} — {len(rows)} baris")

    # Detect kolom nama maskapai
    nama_col = None
    jenis_col = None
    for col in fieldnames:
        col_upper = col.strip().upper()
        if 'NAMA' in col_upper and ('BADAN' in col_upper or 'USAHA' in col_upper or 'PERUSAHAAN' in col_upper):
            nama_col = col
        elif 'JENIS' in col_upper and 'KEGIATAN' in col_upper:
            jenis_col = col

    if nama_col is None or jenis_col is None:
        print(f"    ⚠️ Kolom tidak terdeteksi. fieldnames={fieldnames}")
        return []

    results = []
    for row in rows:
        nama_raw = row.get(nama_col, '').strip()
        jenis_raw = row.get(jenis_col, '').strip()

        if not nama_raw:
            continue

        nama = standardize_maskapai(nama_raw)
        if nama_raw.upper().strip() != nama:
            STANDARDIZATION_LOG.append((nama_raw.strip(), nama, 'NASIONAL', tahun))
        jenis = normalize_jenis_kegiatan(jenis_raw)

        results.append({
            'nama_maskapai': nama,
            'kategori_maskapai': 'NASIONAL',
            'jenis_kegiatan': jenis,
            'negara_asal': 'INDONESIA',
        })

    return results


def extract_asing(tahun):
    """Extract maskapai asing dari CSV Asing per tahun."""
    folder = os.path.join(BAB_II_DIR, str(tahun))

    # Coba beberapa variasi nama file
    filepath = (
        find_csv_by_keyword(folder, 'ASING')
        or find_csv_by_keyword(folder, 'PERWAKILAN')
    )

    if filepath is None:
        print(f"  ⚠️ Tidak ditemukan CSV Asing untuk tahun {tahun}")
        return []

    rows, fieldnames = read_csv_auto(filepath)
    print(f"  📄 Asing {tahun}: {os.path.basename(filepath)} — {len(rows)} baris")

    # Detect kolom
    nama_col = None
    jenis_col = None
    negara_col = None

    for col in fieldnames:
        col_upper = col.strip().upper()
        if 'NAMA' in col_upper:
            nama_col = col
        elif 'JENIS' in col_upper and 'KEGIATAN' in col_upper:
            jenis_col = col
        elif 'NEGARA' in col_upper:
            negara_col = col

    if nama_col is None or jenis_col is None:
        print(f"    ⚠️ Kolom tidak terdeteksi. fieldnames={fieldnames}")
        return []

    results = []
    for row in rows:
        nama_raw = row.get(nama_col, '').strip()
        jenis_raw = row.get(jenis_col, '').strip()
        negara_raw = row.get(negara_col, '').strip() if negara_col else ''

        if not nama_raw:
            continue

        nama = standardize_maskapai(nama_raw)
        if nama_raw.upper().strip() != nama:
            STANDARDIZATION_LOG.append((nama_raw.strip(), nama, 'ASING', tahun))
        jenis = normalize_jenis_kegiatan(jenis_raw)
        negara = negara_raw.strip().upper() if negara_raw else ''

        results.append({
            'nama_maskapai': nama,
            'kategori_maskapai': 'ASING',
            'jenis_kegiatan': jenis,
            'negara_asal': negara if negara else '',
        })

    return results


def deduplicate_maskapai(all_records):
    """
    Deduplikasi by nama_maskapai.
    Jika satu maskapai muncul di beberapa tahun dengan jenis_kegiatan berbeda,
    ambil jenis_kegiatan yang paling sering muncul.
    Jika muncul sebagai NASIONAL dan ASING, prioritaskan yang paling sering.
    """
    from collections import Counter

    # Group by nama_maskapai
    groups = {}
    for rec in all_records:
        key = rec['nama_maskapai']
        if key not in groups:
            groups[key] = []
        groups[key].append(rec)

    results = []
    for nama, records in sorted(groups.items()):
        # Ambil kategori maskapai yang paling sering
        kat_counter = Counter(r['kategori_maskapai'] for r in records)
        kategori = kat_counter.most_common(1)[0][0]

        # Ambil jenis kegiatan terbaru (asumsi: records diurutkan per tahun)
        # Atau yang paling sering
        jenis_counter = Counter(r['jenis_kegiatan'] for r in records)
        jenis = jenis_counter.most_common(1)[0][0]

        # Ambil negara (untuk asing)
        negara_list = [r['negara_asal'] for r in records if r['negara_asal']]
        negara = Counter(negara_list).most_common(1)[0][0] if negara_list else ''

        # Untuk nasional, override negara
        if kategori == 'NASIONAL':
            negara = 'INDONESIA'

        results.append({
            'nama_maskapai': nama,
            'kategori_maskapai': kategori,
            'jenis_kegiatan': jenis,
            'negara_asal': negara,
        })

    return results


def main():
    print("=" * 60)
    print("02_dim_maskapai.py — Generate Dimensi Maskapai")
    print("=" * 60)

    ensure_output_dir()

    all_records = []

    # Collect dari semua tahun
    for tahun in TAHUN_RANGE:
        print(f"\n{'─' * 40}")
        print(f"📅 Tahun {tahun}")
        print(f"{'─' * 40}")

        nasional = extract_nasional(tahun)
        asing = extract_asing(tahun)

        print(f"  → Nasional: {len(nasional)}, Asing: {len(asing)}")
        all_records.extend(nasional)
        all_records.extend(asing)

    print(f"\n{'─' * 40}")
    print(f"Total raw records: {len(all_records)}")

    # Deduplikasi
    unique = deduplicate_maskapai(all_records)
    print(f"Unique maskapai setelah dedup: {len(unique)}")

    # Fill missing negara dari MASKAPAI_NEGARA_FILL
    negara_filled = 0
    for rec in unique:
        if not rec['negara_asal'] and rec['nama_maskapai'] in MASKAPAI_NEGARA_FILL:
            rec['negara_asal'] = MASKAPAI_NEGARA_FILL[rec['nama_maskapai']]
            negara_filled += 1
            print(f"  🔧 Fill negara: {rec['nama_maskapai']} → {rec['negara_asal']}")
    if negara_filled:
        print(f"  Filled {negara_filled} missing negara values")

    # Flag maskapai yang masih tanpa negara
    still_missing = [r for r in unique if not r['negara_asal'] and r['kategori_maskapai'] == 'ASING']
    if still_missing:
        print(f"\n  ⚠️ Masih ada {len(still_missing)} maskapai asing tanpa negara:")
        for r in still_missing:
            print(f"     - {r['nama_maskapai']}")

    # Assign surrogate key
    for i, rec in enumerate(unique, start=1):
        rec['maskapai_id'] = i

    # Write CSV
    out_path = OUTPUT_DIR / "dim_maskapai.csv"
    fieldnames = ['maskapai_id', 'nama_maskapai', 'kategori_maskapai',
                  'jenis_kegiatan', 'negara_asal']

    with open(out_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(unique)

    print(f"\n  ✅ dim_maskapai.csv — {len(unique)} baris")

    # Validasi
    nasional_count = sum(1 for r in unique if r['kategori_maskapai'] == 'NASIONAL')
    asing_count = sum(1 for r in unique if r['kategori_maskapai'] == 'ASING')
    null_kategori = sum(1 for r in unique if not r['kategori_maskapai'])
    null_jenis = sum(1 for r in unique if not r['jenis_kegiatan'])
    null_negara = sum(1 for r in unique if not r['negara_asal'])

    print(f"\n📊 Breakdown:")
    print(f"  Nasional: {nasional_count}")
    print(f"  Asing: {asing_count}")
    print(f"  NULL kategori_maskapai: {null_kategori}")
    print(f"  NULL jenis_kegiatan: {null_jenis}")
    print(f"  NULL negara_asal: {null_negara}")

    # Assertions
    assert null_kategori == 0, "Ada maskapai tanpa kategori_maskapai!"
    assert null_jenis == 0, "Ada maskapai tanpa jenis_kegiatan!"

    # Show sample
    print(f"\n📋 Sample (10 pertama):")
    for rec in unique[:10]:
        print(f"  {rec['maskapai_id']:3d} | {rec['nama_maskapai']:<45s} | "
              f"{rec['kategori_maskapai']:<9s} | {rec['jenis_kegiatan']:<20s} | "
              f"{rec['negara_asal']}")

    # Write catatan standarisasi
    write_catatan(unique)

    print("\n✅ 02_dim_maskapai.py SELESAI")


def write_catatan(unique):
    """Tulis catatan standarisasi ke dim_maskapai.txt"""
    catatan_path = OUTPUT_DIR / "dim_maskapai.txt"
    with open(catatan_path, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("CATATAN STANDARISASI DIM_MASKAPAI\n")
        f.write("Generated by 02_dim_maskapai.py\n")
        f.write("=" * 80 + "\n\n")

        # Section 1: Ringkasan
        nasional = sum(1 for r in unique if r['kategori_maskapai'] == 'NASIONAL')
        asing = sum(1 for r in unique if r['kategori_maskapai'] == 'ASING')
        f.write(f"RINGKASAN:\n")
        f.write(f"  Total raw records (sebelum standarisasi): {len(STANDARDIZATION_LOG) + len(unique)} approx\n")
        f.write(f"  Total unique maskapai (setelah standarisasi): {len(unique)}\n")
        f.write(f"  Nasional: {nasional}\n")
        f.write(f"  Asing: {asing}\n\n")

        # Section 2: Nama yang di-standarisasi
        f.write("=" * 80 + "\n")
        f.write("STANDARISASI NAMA (raw → canonical)\n")
        f.write("=" * 80 + "\n\n")

        # Group by canonical name
        from collections import defaultdict
        groups = defaultdict(set)
        for raw, canonical, kat, tahun in STANDARDIZATION_LOG:
            groups[canonical].add(raw)

        for canonical in sorted(groups.keys()):
            variants = sorted(groups[canonical])
            if len(variants) >= 1:
                f.write(f"  → {canonical}\n")
                for v in variants:
                    f.write(f"      ← \"{v}\"\n")
                f.write("\n")

        # Section 3: Jenis standarisasi yang diterapkan
        f.write("=" * 80 + "\n")
        f.write("JENIS STANDARISASI YANG DITERAPKAN\n")
        f.write("=" * 80 + "\n\n")
        f.write("  1. GREEK → LATIN: Karakter Yunani diganti Latin\n")
        f.write("       Contoh: ΟΜΑΝ AIR → OMAN AIR, ΧΙΑΜΕN AIRLINES → XIAMEN AIRLINES\n\n")
        f.write("  2. LEGAL SUFFIX STRIP: Hapus suffix legal entity tidak konsisten\n")
        f.write("       Suffix: PTY LTD, SDN BHD, CO. LTD, INC, BERHAD, BERHARD, dll\n")
        f.write("       Contoh: QANTAS AIRWAYS LIMITED → QANTAS AIRWAYS\n\n")
        f.write("  3. CANONICAL MAPPING: Merge varian nama ke 1 nama standar\n")
        f.write("       Contoh: AIR ASIA BERHARD / AIRASIA BERHAD / AIRASIA → AIRASIA\n\n")
        f.write("  4. TYPO FIX: Koreksi salah ketik\n")
        f.write("       Contoh: SHENZEN → SHENZHEN, WORD CARGO → WORLD CARGO\n")
        f.write("       Contoh: PHILIPINE → PHILIPPINE, SEVICE → SERVICE\n\n")
        f.write("  5. PT. → PT: Hapus titik setelah PT\n")
        f.write("       Contoh: PT. GARUDA INDONESIA → PT GARUDA INDONESIA\n\n")
        f.write("  6. ASTERISK STRIP: Hapus marker * dan **\n")
        f.write("       Contoh: CEBU PACIFIC** → CEBU PACIFIC\n\n")
        f.write("  7. NEGARA FILL: Isi negara_asal yang kosong (asing 2020 tanpa kolom NEGARA)\n")
        f.write("       Dari: MASKAPAI_NEGARA_FILL dict di utils.py\n\n")

        # Section 4: Daftar final
        f.write("=" * 80 + "\n")
        f.write("DAFTAR MASKAPAI FINAL\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"{'ID':<4s} | {'NAMA MASKAPAI':<45s} | {'KAT':<9s} | {'JENIS':<20s} | NEGARA\n")
        f.write("-" * 110 + "\n")
        for rec in unique:
            f.write(f"{rec['maskapai_id']:<4d} | {rec['nama_maskapai']:<45s} | "
                    f"{rec['kategori_maskapai']:<9s} | {rec['jenis_kegiatan']:<20s} | "
                    f"{rec['negara_asal']}\n")

    print(f"  📝 Catatan standarisasi → {catatan_path}")


if __name__ == "__main__":
    main()
