"""
Script 1: Generate dim_waktu.csv
Output: output/fase1_core/dim_waktu.csv (60 baris)

Tabel dimensi waktu — generated, bukan dari CSV.
Rentang: Januari 2020 s/d Desember 2024.
"""

import os
import sys
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import OUTPUT_CORE, TAHUN_RANGE, NAMA_BULAN


def generate_dim_waktu():
    """Generate dimensi waktu: 60 baris (5 tahun × 12 bulan)."""
    
    rows = []
    for tahun in TAHUN_RANGE:
        for bulan in range(1, 13):
            waktu_id = tahun * 100 + bulan
            rows.append({
                'waktu_id': waktu_id,
                'tahun': tahun,
                'bulan': bulan,
                'nama_bulan': NAMA_BULAN[bulan],
                'kuartal': (bulan - 1) // 3 + 1,
                'semester': 1 if bulan <= 6 else 2,
            })
    
    df = pd.DataFrame(rows)
    return df


def main():
    print("=" * 60)
    print("SCRIPT 1: Generate dim_waktu.csv")
    print("=" * 60)
    
    df = generate_dim_waktu()
    
    output_path = os.path.join(OUTPUT_CORE, "dim_waktu.csv")
    df.to_csv(output_path, index=False)
    
    print(f"\n✅ Output: {output_path}")
    print(f"   Jumlah baris: {len(df)}")
    print(f"   Kolom: {list(df.columns)}")
    print(f"\nPreview (5 baris pertama):")
    print(df.head().to_string(index=False))
    print(f"\nPreview (5 baris terakhir):")
    print(df.tail().to_string(index=False))
    
    # Verifikasi
    assert len(df) == 60, f"Expected 60 rows, got {len(df)}"
    assert df['waktu_id'].min() == 202001, f"Min waktu_id should be 202001"
    assert df['waktu_id'].max() == 202412, f"Max waktu_id should be 202412"
    assert df['waktu_id'].nunique() == 60, "All waktu_id should be unique"
    
    print("\n✅ Verifikasi passed: 60 baris, range 202001-202412, semua unique")


if __name__ == "__main__":
    main()
