"""
Konfigurasi path dan konstanta untuk ETL Pipeline v3.2
Data Warehouse: Korelasi Nilai Rupiah terhadap Angkutan Udara Indonesia (2020-2024)
Sumber kebenaran: Master_DWH_Blueprint_dan_Strategi_ETL.md
"""

import os
from pathlib import Path

# === BASE PATHS ===
BASE_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTPUT_DIR = BASE_DIR / "output"

# === INPUT PATHS ===
KURS_CSV = BASE_DIR / "KURS" / "BI.csv"

BAB_II_DIR = BASE_DIR / "DJPU" / "Table_Pilihan" / "BAB II \u2014 Perusahaan Angkutan Udara"
BAB_III_DIR = BASE_DIR / "DJPU" / "Table_Pilihan" / "BAB III \u2014 Rute & Bandara"
BAB_IV_DIR = BASE_DIR / "DJPU" / "Table_Pilihan" / "BAB IV \u2014 Produksi"
BAB_VI_DIR = BASE_DIR / "DJPU" / "Table_Pilihan" / "BAB VI \u2014 Penumpang Per Rute"
BAB_VII_CSV = (
    BASE_DIR / "DJPU" / "Table_Pilihan" / "BAB VII \u2014 Lalu Lintas Bandara"
    / "DATA LALU LINTAS ANGKUTAN UDARA DI BANDAR UDARA TAHUN 2020 - 2024.csv"
)
BAB_XII_CSV = (
    BASE_DIR / "DJPU" / "Table_Pilihan" / "BAB XII \u2014 On Time Performance"
    / "TINGKAT KETEPATAN WAKTU (ON TIME PERFORMANCE) BADAN USAHA ANGKUTAN UDARA NIAGA PENERBANGAN NIAGA BERJADWAL DALAM NEGERI 2024.csv"
)

# === CONSTANTS ===
TAHUN_MULAI = 2020
TAHUN_AKHIR = 2024
TAHUN_RANGE = range(TAHUN_MULAI, TAHUN_AKHIR + 1)  # [2020, 2021, 2022, 2023, 2024]

NAMA_BULAN = {
    1: "Januari", 2: "Februari", 3: "Maret", 4: "April",
    5: "Mei", 6: "Juni", 7: "Juli", 8: "Agustus",
    9: "September", 10: "Oktober", 11: "November", 12: "Desember"
}


def ensure_output_dir():
    """Buat folder output/ jika belum ada."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
