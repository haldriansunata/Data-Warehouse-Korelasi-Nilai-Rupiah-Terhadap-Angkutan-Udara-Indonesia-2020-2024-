"""
Konfigurasi path dan konstanta untuk ETL pipeline.
Data Warehouse: Korelasi Nilai Rupiah terhadap Angkutan Udara Indonesia (2020-2024)
"""

import os

# Base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Input paths
KURS_CSV = os.path.join(BASE_DIR, "KURS", "BI.csv")
BAB_II_DIR = os.path.join(BASE_DIR, "DJPU", "Table_Pilihan", "BAB II — Perusahaan Angkutan Udara")
BAB_IV_DIR = os.path.join(BASE_DIR, "DJPU", "Table_Pilihan", "BAB IV — Produksi")
BAB_VI_DIR = os.path.join(BASE_DIR, "DJPU", "Table_Pilihan", "BAB VI — Penumpang Per Rute")
BAB_VII_DIR = os.path.join(BASE_DIR, "DJPU", "Table_Pilihan", "BAB VII — Lalu Lintas Bandara")
BAB_XII_DIR = os.path.join(BASE_DIR, "DJPU", "Table_Pilihan", "BAB XII — On Time Performance")

# Output paths
OUTPUT_CORE = os.path.join(BASE_DIR, "output", "fase1_core")
OUTPUT_ENRICHMENT = os.path.join(BASE_DIR, "output", "fase2_enrichment")

# Tahun analisis
TAHUN_MULAI = 2020
TAHUN_AKHIR = 2024
TAHUN_RANGE = range(TAHUN_MULAI, TAHUN_AKHIR + 1)

# Nama bulan Indonesia
NAMA_BULAN = {
    1: "Januari", 2: "Februari", 3: "Maret", 4: "April",
    5: "Mei", 6: "Juni", 7: "Juli", 8: "Agustus",
    9: "September", 10: "Oktober", 11: "November", 12: "Desember"
}
