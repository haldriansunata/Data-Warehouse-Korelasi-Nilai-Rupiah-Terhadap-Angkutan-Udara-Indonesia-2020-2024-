"""
extract_pdf.py
==============
Script untuk mengekstrak tabel dari PDF Statistik Angkutan Udara
(DJPU Kemenhub) 2020-2024 secara otomatis.

Alur kerja:
  1. Scan semua PDF → temukan halaman tiap bab via keyword
  2. Kelompokkan halaman yang berurutan jadi satu range
  3. Extract tabel dari tiap range → simpan ke CSV

Cara pakai:
    python extract_pdf.py
"""

import pdfplumber
import pandas as pd
from pathlib import Path

# ==============================================================
# CONFIG
# ==============================================================

PDF_DIR    = r"D:\Kuliah\projek_dw\DJPU\Statistik Angkutan Udara"
OUTPUT_DIR = r"D:\Kuliah\projek_dw\Statistik Angkutan Udara(extracted)"

# Halaman awal yang dilewati (sampul + daftar isi).
# Dinaikkan ke 15 agar daftar isi (s.d. hal ~14) tidak ikut ke-scan.
SKIP_HALAMAN_AWAL = 15

# Keyword per bab — semua keyword dalam satu list harus muncul
# di halaman yang sama (kondisi AND).
KEYWORDS = {
    "maskapai"              : ["Badan Usaha Angkutan Udara Niaga Berjadwal"],
    "rute_bandara"          : ["Rute Angkutan Udara Niaga Berjadwal"],
    "produksi"              : ["Produksi Angkutan Udara Niaga Berjadwal"],
    "market_share"          : ["Market Share Penumpang"],
    # 2020-2023: judul tabel "Statistik Per Rute Penerbangan Domestik/International"
    "penumpang_rute_dn"     : ["Statistik Per Rute", "Domestik"],
    "penumpang_rute_ln"     : ["Statistik Per Rute", "International"],
    # 2024: terminologi berubah jadi "Dalam Negeri" / "Luar Negeri"
    "penumpang_rute_dn_2024": ["Statistik Per Rute", "Dalam Negeri"],
    "penumpang_rute_ln_2024": ["Statistik Per Rute", "Luar Negeri"],
    "lalu_lintas_bandara"   : ["Lalu Lintas Angkutan Udara di Bandar Udara"],
    # Tambah "Badan Usaha" agar tidak menangkap halaman lain yang hanya
    # menyebut "On Time Performance" di judul bab saja
    "otp"                   : ["On Time Performance", "Badan Usaha"],
}

# ==============================================================


def scan_halaman(path: str, keywords: list, skip: int) -> list:
    """
    Scan PDF halaman per halaman.
    Kembalikan list nomor halaman (1-based) yang mengandung
    SEMUA keyword (kondisi AND).
    """
    hasil = []
    with pdfplumber.open(path) as pdf:
        for i, page in enumerate(pdf.pages):
            if i < skip:
                continue
            teks = (page.extract_text() or "").lower()
            if all(kw.lower() in teks for kw in keywords):
                hasil.append(i + 1)
    return hasil


def kelompokkan_range(halaman: list, toleransi: int = 2) -> list:
    """
    Ubah list halaman jadi list range (mulai, selesai).
    Halaman berurutan (dengan toleransi gap) digabung jadi satu range.

    Contoh: [45,46,47,50,51] toleransi=2 → [(45,51)]
             [45,46,60,61]   toleransi=2 → [(45,46),(60,61)]

    toleransi: gap halaman yang masih dianggap satu blok.
    Berguna untuk tabel yang diselingi halaman kosong atau grafik.
    """
    if not halaman:
        return []

    halaman = sorted(set(halaman))
    ranges  = []
    mulai   = halaman[0]
    sblmnya = halaman[0]

    for h in halaman[1:]:
        if h - sblmnya <= toleransi + 1:
            sblmnya = h
        else:
            ranges.append((mulai, sblmnya))
            mulai   = h
            sblmnya = h

    ranges.append((mulai, sblmnya))
    return ranges


def extract_tabel_range(path: str, mulai: int, selesai: int):
    """
    Extract semua tabel dari halaman mulai s.d. selesai.
    Gabungkan seluruh baris jadi satu DataFrame.
    Kembalikan DataFrame atau None jika tidak ada tabel.
    """
    semua_baris = []

    with pdfplumber.open(path) as pdf:
        selesai_aman = min(selesai, len(pdf.pages))

        for nomor in range(mulai, selesai_aman + 1):
            page   = pdf.pages[nomor - 1]
            tables = page.extract_tables()
            if not tables:
                continue
            for tbl in tables:
                bersih = [b for b in tbl if any(sel is not None for sel in b)]
                semua_baris.extend(bersih)

    if not semua_baris:
        return None

    df = pd.DataFrame(semua_baris)

    # Jadikan baris pertama sebagai header jika semuanya tidak kosong
    if df.iloc[0].notna().all():
        df.columns = df.iloc[0]
        df = df[1:].reset_index(drop=True)

    return df


def proses_satu_pdf(path: str) -> list:
    """
    Proses lengkap satu file PDF:
    scan → deteksi range → extract → simpan CSV.
    """
    nama_file = Path(path).stem
    tahun = "unknown"
    for t in ["2020", "2021", "2022", "2023", "2024"]:
        if t in nama_file:
            tahun = t
            break

    print(f"\n{'='*65}")
    print(f"  FILE : {Path(path).name}")
    print(f"  TAHUN: {tahun}")
    print(f"{'='*65}")

    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    ringkasan = []

    for nama_bab, kws in KEYWORDS.items():

        # Skip variasi 2024 untuk tahun lain, dan sebaliknya
        if "2024" in nama_bab and tahun != "2024":
            continue
        if nama_bab in ("penumpang_rute_dn", "penumpang_rute_ln") and tahun == "2024":
            continue

        halaman_cocok = scan_halaman(path, kws, skip=SKIP_HALAMAN_AWAL)

        if not halaman_cocok:
            print(f"  [!] {nama_bab:<30} → tidak ditemukan")
            ringkasan.append({
                "file_pdf": Path(path).name, "tahun": tahun,
                "bab": nama_bab, "status": "tidak ditemukan",
                "halaman": "-", "baris": "-", "kolom": "-", "file_csv": "-"
            })
            continue

        ranges = kelompokkan_range(halaman_cocok)

        for idx, (mulai, selesai) in enumerate(ranges):
            label        = f"hal {mulai}–{selesai}" if mulai != selesai else f"hal {mulai}"
            nama_output  = f"{nama_bab}_{tahun}"
            if len(ranges) > 1:
                nama_output += f"_part{idx + 1}"

            df = extract_tabel_range(path, mulai, selesai)

            if df is None or df.empty:
                print(f"  [!] {nama_bab:<30} → {label} | tabel tidak terbaca")
                ringkasan.append({
                    "file_pdf": Path(path).name, "tahun": tahun,
                    "bab": nama_bab, "status": "tabel tidak terbaca",
                    "halaman": label, "baris": "-", "kolom": "-", "file_csv": "-"
                })
                continue

            output_path = Path(OUTPUT_DIR) / f"{nama_output}.csv"
            df.to_csv(output_path, index=False, encoding="utf-8-sig")

            print(f"  [✓] {nama_bab:<30} → {label} | "
                  f"{len(df)} baris | {len(df.columns)} kolom → {output_path.name}")
            ringkasan.append({
                "file_pdf": Path(path).name, "tahun": tahun,
                "bab": nama_bab, "status": "OK",
                "halaman": label, "baris": len(df),
                "kolom": len(df.columns), "file_csv": output_path.name
            })

    return ringkasan


def proses_semua_pdf():
    """
    Proses semua PDF di PDF_DIR, cetak dan simpan ringkasan akhir.
    """
    pdf_files = sorted(Path(PDF_DIR).glob("*.pdf"))

    if not pdf_files:
        print(f"[!] Tidak ada file PDF di: {PDF_DIR}")
        return

    semua_ringkasan = []
    for pdf_path in pdf_files:
        hasil = proses_satu_pdf(str(pdf_path))
        semua_ringkasan.extend(hasil)

    df_ringkasan  = pd.DataFrame(semua_ringkasan)
    ringkasan_path = Path(OUTPUT_DIR) / "ringkasan_ekstraksi.csv"
    df_ringkasan.to_csv(ringkasan_path, index=False, encoding="utf-8-sig")

    ok    = len(df_ringkasan[df_ringkasan["status"] == "OK"])
    gagal = len(df_ringkasan[df_ringkasan["status"] != "OK"])

    print(f"\n{'='*65}")
    print(f"  SELESAI")
    print(f"  CSV berhasil dibuat  : {ok}")
    print(f"  Tidak ditemukan/gagal: {gagal}")
    print(f"  Ringkasan lengkap    : {ringkasan_path}")
    print(f"{'='*65}")


# ==============================================================
# JALANKAN
# ==============================================================

if __name__ == "__main__":
    proses_semua_pdf()