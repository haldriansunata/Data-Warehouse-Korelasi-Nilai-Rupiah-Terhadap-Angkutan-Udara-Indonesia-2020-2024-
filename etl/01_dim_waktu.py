"""
01_dim_waktu.py — Generate Dim_Waktu_Bulanan + Dim_Waktu_Tahunan
ETL Pipeline v3.2 (Clean Rewrite)

Output:
  - output/dim_waktu_bulanan.csv (60 baris: 2020-2024 × 12 bulan)
  - output/dim_waktu_tahunan.csv (5 baris: 2020-2024)

Sumber: Generate manual (tidak dari CSV).
"""

import csv
import math
import sys
import os

# Tambah parent dir ke path agar bisa import config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from etl.config import OUTPUT_DIR, TAHUN_RANGE, NAMA_BULAN, ensure_output_dir


def generate_dim_waktu_bulanan():
    """Generate dim_waktu_bulanan.csv — 60 baris."""
    rows = []
    for tahun in TAHUN_RANGE:
        for bulan in range(1, 13):
            waktu_id = tahun * 100 + bulan
            nama_bulan = NAMA_BULAN[bulan]
            kuartal = math.ceil(bulan / 3)
            semester = 1 if bulan <= 6 else 2
            rows.append({
                'waktu_id': waktu_id,
                'tahun': tahun,
                'bulan': bulan,
                'nama_bulan': nama_bulan,
                'kuartal': kuartal,
                'semester': semester,
            })

    out_path = OUTPUT_DIR / "dim_waktu_bulanan.csv"
    with open(out_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'waktu_id', 'tahun', 'bulan', 'nama_bulan', 'kuartal', 'semester'
        ])
        writer.writeheader()
        writer.writerows(rows)

    print(f"  ✅ dim_waktu_bulanan.csv — {len(rows)} baris")
    return rows


def generate_dim_waktu_tahunan():
    """Generate dim_waktu_tahunan.csv — 5 baris."""
    rows = []
    for tahun in TAHUN_RANGE:
        rows.append({
            'waktu_id': tahun,
            'tahun': tahun,
        })

    out_path = OUTPUT_DIR / "dim_waktu_tahunan.csv"
    with open(out_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['waktu_id', 'tahun'])
        writer.writeheader()
        writer.writerows(rows)

    print(f"  ✅ dim_waktu_tahunan.csv — {len(rows)} baris")
    return rows


def main():
    print("=" * 60)
    print("01_dim_waktu.py — Generate Dimensi Waktu")
    print("=" * 60)

    ensure_output_dir()

    bulanan = generate_dim_waktu_bulanan()
    tahunan = generate_dim_waktu_tahunan()

    # Validasi
    assert len(bulanan) == 60, f"Expected 60 baris, got {len(bulanan)}"
    assert len(tahunan) == 5, f"Expected 5 baris, got {len(tahunan)}"
    assert bulanan[0]['waktu_id'] == 202001
    assert bulanan[-1]['waktu_id'] == 202412
    assert tahunan[0]['waktu_id'] == 2020
    assert tahunan[-1]['waktu_id'] == 2024

    print("\n✅ 01_dim_waktu.py SELESAI")


if __name__ == "__main__":
    main()
