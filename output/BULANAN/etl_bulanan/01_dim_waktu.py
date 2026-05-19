"""
01_dim_waktu.py — Basic Dim_Waktu_Bulanan (60 baris).

Output: _tmp/dim_waktu_bulanan.csv  (versi belum di-enrich)
        Akan ditimpa oleh build_makro_warehouse.py menjadi versi final
        di output/BULANAN/dim_waktu_bulanan.csv (dengan covid_phase, has_lebaran, dll).
"""
import csv
import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import TMP_DIR, TAHUN_RANGE, NAMA_BULAN, ensure_dirs


def main():
    print("=" * 60)
    print("01_dim_waktu.py — Basic Dim Waktu Bulanan")
    print("=" * 60)

    ensure_dirs()

    rows = []
    for tahun in TAHUN_RANGE:
        for bulan in range(1, 13):
            rows.append({
                'waktu_id':   tahun * 100 + bulan,
                'tahun':      tahun,
                'bulan':      bulan,
                'nama_bulan': NAMA_BULAN[bulan],
                'kuartal':    math.ceil(bulan / 3),
                'semester':   1 if bulan <= 6 else 2,
            })

    out_path = TMP_DIR / "dim_waktu_bulanan.csv"
    with open(out_path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=[
            'waktu_id', 'tahun', 'bulan', 'nama_bulan', 'kuartal', 'semester'
        ])
        w.writeheader()
        w.writerows(rows)

    assert len(rows) == 60
    print(f"  [OK] {out_path.name} — {len(rows)} baris (basic, akan di-enrich oleh build_makro)")


if __name__ == "__main__":
    main()
