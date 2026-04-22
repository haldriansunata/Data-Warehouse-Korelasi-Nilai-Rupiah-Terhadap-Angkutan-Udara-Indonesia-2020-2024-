"""
03_dim_bandara.py — Generate Dim_Bandara dari BAB VII + IATA dari BAB III/VI
ETL Pipeline v3.2 (Clean Rewrite)

Output:
  - output/dim_bandara.csv

Phase A: Fondasi dari BAB VII (nama_bandara, kota, provinsi, negara)
Phase B: Perkaya dengan kode IATA dari BAB III/VI + BANDARA_IATA_MAP

Kolom output: bandara_id, kode_iata, nama_bandara, kota, provinsi, negara
"""

import csv
import re
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from etl.config import (OUTPUT_DIR, BAB_III_DIR, BAB_VI_DIR, BAB_VII_CSV,
                         TAHUN_RANGE, ensure_output_dir)
from etl.utils import parse_airport_name, BANDARA_IATA_MAP, IATA_KOTA_MAP


def read_csv_auto(filepath):
    """Baca CSV dengan auto-detect encoding."""
    for enc in ['utf-8-sig', 'utf-8', 'latin-1', 'cp1252']:
        try:
            with open(filepath, 'r', encoding=enc, newline='') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                return rows, reader.fieldnames
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot read {filepath}")


def clean_provinsi(raw: str) -> str:
    """Standardisasi nama provinsi."""
    p = raw.strip().upper()
    # Hapus prefix PROPINSI/PROVINSI
    p = re.sub(r'^PROP?INSI\s+', '', p)
    # Normalisasi spasi "R I A U" → "RIAU"
    if re.match(r'^[A-Z](\s[A-Z])+$', p):
        p = p.replace(' ', '')
    return p.strip()


# =========================================================================
# PHASE A: Fondasi dari BAB VII
# =========================================================================

def phase_a():
    """
    Extract bandara unik dari BAB VII CSV.
    Returns: dict keyed by (nama_bandara, kota) → {provinsi, negara, kategori_set}
    """
    print("\n--- PHASE A: Extract Bandara dari BAB VII ---")

    rows, _ = read_csv_auto(str(BAB_VII_CSV))
    print(f"  Total baris BAB VII: {len(rows)}")

    bandara_map = {}  # key: (nama_bandara_upper, kota_upper) → info

    for row in rows:
        airport_raw = row.get('airport_name', '').strip()
        provinsi_raw = row.get('propinsi_name', '').strip()

        if not airport_raw:
            continue

        nama_bandara, kota, kategori = parse_airport_name(airport_raw)
        nama_bandara = nama_bandara.strip().upper()
        kota = kota.strip().upper()
        provinsi = clean_provinsi(provinsi_raw)

        key = (nama_bandara, kota)
        if key not in bandara_map:
            bandara_map[key] = {
                'nama_bandara': nama_bandara,
                'kota': kota,
                'provinsi': provinsi,
                'negara': 'INDONESIA',
                'kategori_set': set(),
            }
        bandara_map[key]['kategori_set'].add(kategori)

    print(f"  Bandara unik (nama+kota): {len(bandara_map)}")

    # Debug: show some examples
    sample = list(bandara_map.values())[:5]
    for s in sample:
        print(f"    - {s['nama_bandara']} | {s['kota']} | {s['provinsi']} | {s['kategori_set']}")

    return bandara_map


# =========================================================================
# PHASE B: Extract IATA dari BAB III + BAB VI
# =========================================================================

def extract_iata_from_bab3_and_bab6():
    """
    Scan semua CSV di BAB III dan BAB VI untuk extract kota↔IATA pairs.
    Returns: dict kota_upper → set of IATA codes
    """
    print("\n--- PHASE B: Extract IATA dari BAB III + BAB VI ---")

    kota_iata = defaultdict(set)  # kota → {IATA codes}

    # Pattern: "Jakarta (CGK)" or "Jakarta(CGK)"
    pattern_kota_iata = re.compile(r'([^()]+?)\s*\(([A-Z]{3}\*?)\)')

    def scan_csv_for_iata(filepath, label):
        """Scan CSV untuk pattern kota(IATA)."""
        count = 0
        try:
            rows, fieldnames = read_csv_auto(filepath)
        except Exception as e:
            print(f"    ⚠️ Gagal baca {label}: {e}")
            return 0

        for row in rows:
            for col in (fieldnames or []):
                val = row.get(col, '').strip()
                if not val:
                    continue
                # Find all kota(IATA) patterns
                matches = pattern_kota_iata.findall(val)
                for kota, iata in matches:
                    kota = kota.strip().upper()
                    iata = iata.strip().rstrip('*').upper()
                    if len(iata) == 3 and iata.isalpha():
                        kota_iata[kota].add(iata)
                        count += 1

                # Also handle pure "CGK-DPS" format
                if re.match(r'^[A-Z]{3}\s*[-–]\s*[A-Z]{3}$', val.strip()):
                    parts = re.split(r'\s*[-–]\s*', val.strip())
                    for p in parts:
                        p = p.strip()
                        if len(p) == 3 and p.isalpha() and p.isupper():
                            # Pure IATA — no kota info, but track existence
                            kota_iata[f'__IATA_{p}__'].add(p)
                            count += 1
        return count

    # Scan BAB III
    bab3_count = 0
    for tahun in TAHUN_RANGE:
        tahun_dir = os.path.join(BAB_III_DIR, str(tahun))
        if not os.path.isdir(tahun_dir):
            continue
        for f in os.listdir(tahun_dir):
            if not f.lower().endswith('.csv'):
                continue
            fp = os.path.join(tahun_dir, f)
            n = scan_csv_for_iata(fp, f"BAB III/{tahun}/{f[:40]}")
            bab3_count += n

    # Scan BAB VI
    bab6_count = 0
    for tahun in TAHUN_RANGE:
        tahun_dir = os.path.join(BAB_VI_DIR, str(tahun))
        if not os.path.isdir(tahun_dir):
            continue
        for f in os.listdir(tahun_dir):
            if not f.lower().endswith('.csv'):
                continue
            fp = os.path.join(tahun_dir, f)
            n = scan_csv_for_iata(fp, f"BAB VI/{tahun}/{f[:40]}")
            bab6_count += n

    print(f"  BAB III: {bab3_count} kota↔IATA matches")
    print(f"  BAB VI: {bab6_count} kota↔IATA matches")
    print(f"  Total unique kota keys: {len(kota_iata)}")

    # Show sample
    sample_items = [(k, v) for k, v in sorted(kota_iata.items()) if not k.startswith('__')][:10]
    for kota, iatas in sample_items:
        print(f"    {kota} → {iatas}")

    return kota_iata


def match_iata_to_bandara(bandara_map, kota_iata):
    """
    Match IATA codes ke bandara menggunakan 3-pass approach.
    Returns: bandara_map with 'kode_iata' added.
    """
    print("\n--- PHASE B: Match IATA → Bandara ---")

    matched = 0
    unmatched = []

    for key, info in bandara_map.items():
        nama_bandara = info['nama_bandara']
        kota = info['kota']

        # Pass 1: Exact match dari BANDARA_IATA_MAP (manual dict)
        if nama_bandara in BANDARA_IATA_MAP:
            info['kode_iata'] = BANDARA_IATA_MAP[nama_bandara]
            matched += 1
            continue

        # Pass 2: Match kota dari BAB III/VI data
        iata_found = None

        # Try exact kota match
        if kota and kota in kota_iata:
            codes = kota_iata[kota]
            if len(codes) == 1:
                iata_found = list(codes)[0]
            else:
                # Multiple IATA for same kota (e.g. JAKARTA → CGK, HLP)
                # Pick the most common one (heuristic)
                iata_found = sorted(codes)[0]  # alphabetical first

        # Try kota variations
        if not iata_found and kota:
            # Try without dashes: "SIBORONG-BORONG" → "SIBORONG BORONG"
            kota_alt = kota.replace('-', ' ')
            if kota_alt in kota_iata:
                codes = kota_iata[kota_alt]
                iata_found = list(codes)[0]

            # Try first word: "PADANG KEMILING" → "PADANG"
            if not iata_found:
                first_word = kota.split()[0] if kota.split() else ''
                if first_word and first_word in kota_iata and len(kota_iata[first_word]) == 1:
                    iata_found = list(kota_iata[first_word])[0]

        if iata_found:
            info['kode_iata'] = iata_found
            matched += 1
        else:
            info['kode_iata'] = ''
            unmatched.append((nama_bandara, kota))

    print(f"  Matched: {matched}/{len(bandara_map)}")
    print(f"  Unmatched: {len(unmatched)}")
    if unmatched:
        print(f"\n  Unmatched bandara (top 20):")
        for nama, kota in sorted(unmatched)[:20]:
            print(f"    - {nama} | {kota}")

    return bandara_map


# =========================================================================
# PHASE B2: Add foreign airports from BAB III/VI international routes
# =========================================================================

def add_foreign_airports(bandara_map, kota_iata):
    """
    Bandara asing yang muncul di rute internasional tapi tidak ada di BAB VII.
    Tambah sebagai baris baru dengan provinsi=NULL.
    """
    print("\n--- PHASE B2: Foreign Airports dari Rute Internasional ---")

    # Collect all IATA codes already in bandara_map
    existing_iata = set()
    for info in bandara_map.values():
        if info.get('kode_iata'):
            existing_iata.add(info['kode_iata'])

    # Collect all IATA codes from kota_iata that are NOT in existing
    foreign_count = 0
    for kota_key, iata_set in kota_iata.items():
        if kota_key.startswith('__'):
            continue
        for iata in iata_set:
            if iata not in existing_iata:
                # This is likely a foreign airport
                key = (f"FOREIGN_{iata}", kota_key)
                if key not in bandara_map:
                    bandara_map[key] = {
                        'nama_bandara': kota_key.title(),  # Best guess
                        'kota': kota_key.title(),
                        'provinsi': '',
                        'negara': '',  # Not Indonesia
                        'kode_iata': iata,
                        'kategori_set': {'INTERNASIONAL'},
                    }
                    existing_iata.add(iata)
                    foreign_count += 1

    print(f"  Foreign airports added: {foreign_count}")
    return bandara_map


# =========================================================================
# MAIN
# =========================================================================

def main():
    print("=" * 60)
    print("03_dim_bandara.py — Generate Dimensi Bandara")
    print("=" * 60)

    ensure_output_dir()

    # Phase A: Extract from BAB VII
    bandara_map = phase_a()

    # Phase B: Extract IATA and match
    kota_iata = extract_iata_from_bab3_and_bab6()
    bandara_map = match_iata_to_bandara(bandara_map, kota_iata)

    # Phase B2: Add foreign airports
    bandara_map = add_foreign_airports(bandara_map, kota_iata)

    # Build final list, sorted
    records = []
    for key, info in sorted(bandara_map.items()):
        records.append({
            'kode_iata': info.get('kode_iata', ''),
            'nama_bandara': info['nama_bandara'],
            'kota': info['kota'],
            'provinsi': info['provinsi'],
            'negara': info['negara'],
        })

    # Assign surrogate key
    for i, rec in enumerate(records, start=1):
        rec['bandara_id'] = i

    # Write CSV
    out_path = OUTPUT_DIR / "dim_bandara.csv"
    fieldnames = ['bandara_id', 'kode_iata', 'nama_bandara', 'kota', 'provinsi', 'negara']
    with open(out_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    # Stats
    total = len(records)
    with_iata = sum(1 for r in records if r['kode_iata'])
    indonesia = sum(1 for r in records if r['negara'] == 'INDONESIA')
    foreign = sum(1 for r in records if r['negara'] != 'INDONESIA')
    null_prov_indo = sum(1 for r in records if r['negara'] == 'INDONESIA' and not r['provinsi'])

    print(f"\n{'=' * 60}")
    print(f"HASIL:")
    print(f"  Total bandara: {total}")
    print(f"  Dengan IATA: {with_iata} ({with_iata*100//total}%)")
    print(f"  Indonesia: {indonesia}")
    print(f"  Foreign: {foreign}")
    print(f"  Indonesia tanpa provinsi: {null_prov_indo}")

    # Validasi
    if null_prov_indo > 0:
        print(f"\n  ⚠️ Ada {null_prov_indo} bandara Indonesia tanpa provinsi!")
        for r in records:
            if r['negara'] == 'INDONESIA' and not r['provinsi']:
                print(f"     - {r['nama_bandara']} | {r['kota']}")

    print(f"\n  ✅ dim_bandara.csv — {total} baris")
    print("\n✅ 03_dim_bandara.py SELESAI")


if __name__ == "__main__":
    main()
