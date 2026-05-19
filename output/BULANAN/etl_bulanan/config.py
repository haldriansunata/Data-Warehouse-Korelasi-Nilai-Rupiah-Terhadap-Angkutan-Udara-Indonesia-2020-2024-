"""
Konfigurasi path & konstanta untuk ETL Bulanan.
Pipeline khusus topik: Korelasi Nilai Rupiah terhadap Angkutan Udara Indonesia (2020-2024).
Layout:
  - Script di:  output/BULANAN/etl_bulanan/
  - Final CSV: output/BULANAN/         (dim_bandara, dim_rute, dim_waktu_bulanan, fact_penumpang_rute, fact_makro_bulanan)
  - Tmp CSV:   output/BULANAN/etl_bulanan/_tmp/   (dim_waktu basic + fact_kurs intermediate)

Override lokasi output via env var BULANAN_OUTPUT=<path> (untuk verifikasi/sandbox).
"""
import os
from pathlib import Path

SCRIPT_DIR  = Path(__file__).resolve().parent          # output/BULANAN/etl_bulanan
BULANAN_DIR = SCRIPT_DIR.parent                        # output/BULANAN
BASE_DIR    = BULANAN_DIR.parent.parent                # projek_dw root

_override = os.environ.get("BULANAN_OUTPUT")
if _override:
    OUTPUT_DIR = Path(_override).resolve()
    TMP_DIR    = OUTPUT_DIR / "_tmp"
else:
    OUTPUT_DIR = BULANAN_DIR
    TMP_DIR    = SCRIPT_DIR / "_tmp"

# === INPUT ===
KURS_CSV    = BASE_DIR / "KURS" / "BI.csv"
BAB_III_DIR = BASE_DIR / "DJPU" / "Table_Pilihan" / "BAB III — Rute & Bandara"
BAB_VI_DIR  = BASE_DIR / "DJPU" / "Table_Pilihan" / "BAB VI — Penumpang Per Rute"

DT_DIR           = BASE_DIR / "data_tambahan"
BI_RATE_CSV      = DT_DIR / "BPS" / "BI RATE" / "BI_RATE_2020-2024.csv"
INFLASI_MTM_CSV  = DT_DIR / "BPS" / "Inflasi Bulanan (M-to-M) (Persen)" / "inflasi_indonesia_mtm_bps.csv"
TARIF_IHK_CSV    = (DT_DIR / "BPS"
                    / "Survei Harga Konsumen (SHK) bulanan di 150 kabupatenkota (38 ibukota provinsi dan 112 kabupatenkota lainnya)"
                    / "harga-konsumen-nasional-beberapa-barang-dan-jasa(2020-2024).csv")
INFLASI_YOY_XLSX = DT_DIR / "BI" / "Data Inflasi.xlsx"
BRENT_CSV        = DT_DIR / "BRENT" / "Brent Oil Futures Historical Data.csv"

# === KONSTANTA ===
TAHUN_MULAI = 2020
TAHUN_AKHIR = 2024
TAHUN_RANGE = range(TAHUN_MULAI, TAHUN_AKHIR + 1)

NAMA_BULAN = {
    1: "Januari", 2: "Februari", 3: "Maret", 4: "April",
    5: "Mei", 6: "Juni", 7: "Juli", 8: "Agustus",
    9: "September", 10: "Oktober", 11: "November", 12: "Desember",
}


def ensure_dirs():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    TMP_DIR.mkdir(parents=True, exist_ok=True)
