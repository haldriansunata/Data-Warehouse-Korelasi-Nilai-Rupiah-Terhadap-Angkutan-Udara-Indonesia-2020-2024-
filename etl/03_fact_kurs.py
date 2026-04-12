"""
Script 2: Process KURS/BI.csv → fact_kurs_bulanan.csv
Output: output/fase1_core/fact_kurs_bulanan.csv (60 baris)

Agregasi kurs harian → rata-rata bulanan.
"""

import os
import sys
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import KURS_CSV, OUTPUT_CORE, TAHUN_MULAI, TAHUN_AKHIR


def load_and_process_kurs():
    """Load KURS/BI.csv dan agregasi ke bulanan."""
    
    print(f"📂 Membaca: {KURS_CSV}")
    
    # BI.csv structure:
    # Baris 1: "Kurs Transaksi USD, ..." (skip)
    # Baris 2: kosong (skip)
    # Baris 3: NO,Nilai,Kurs Jual,Kurs Beli,Tanggal ← actual header
    # Baris 4+: data
    df = pd.read_csv(KURS_CSV, skiprows=2, encoding='utf-8')
    
    print(f"   Raw rows: {len(df)}")
    print(f"   Columns: {list(df.columns)}")
    
    # Rename columns to standardized names
    df.columns = [c.strip() for c in df.columns]
    
    # Parse tanggal: "M/D/YYYY 12:00:00 AM" → datetime
    df['Tanggal'] = pd.to_datetime(df['Tanggal'], format='mixed')
    
    # Parse kurs values (should be clean numbers)
    df['Kurs Jual'] = pd.to_numeric(df['Kurs Jual'], errors='coerce')
    df['Kurs Beli'] = pd.to_numeric(df['Kurs Beli'], errors='coerce')
    
    # Hitung kurs tengah
    df['kurs_tengah'] = (df['Kurs Jual'] + df['Kurs Beli']) / 2
    
    # Filter tahun 2020-2024
    df['tahun'] = df['Tanggal'].dt.year
    df['bulan'] = df['Tanggal'].dt.month
    df = df[(df['tahun'] >= TAHUN_MULAI) & (df['tahun'] <= TAHUN_AKHIR)]
    
    print(f"   Rows after filter {TAHUN_MULAI}-{TAHUN_AKHIR}: {len(df)}")
    
    # Aggregate per bulan
    agg = df.groupby(['tahun', 'bulan']).agg(
        avg_kurs_jual=('Kurs Jual', 'mean'),
        avg_kurs_beli=('Kurs Beli', 'mean'),
        avg_kurs_tengah=('kurs_tengah', 'mean'),
        min_kurs_tengah=('kurs_tengah', 'min'),
        max_kurs_tengah=('kurs_tengah', 'max'),
        jumlah_hari_trading=('kurs_tengah', 'count'),
    ).reset_index()
    
    # Generate waktu_id
    agg['waktu_id'] = agg['tahun'] * 100 + agg['bulan']
    
    # Round to 2 decimal places
    for col in ['avg_kurs_jual', 'avg_kurs_beli', 'avg_kurs_tengah', 
                'min_kurs_tengah', 'max_kurs_tengah']:
        agg[col] = agg[col].round(2)
    
    # Reorder columns
    agg = agg[['waktu_id', 'avg_kurs_jual', 'avg_kurs_beli', 'avg_kurs_tengah',
               'min_kurs_tengah', 'max_kurs_tengah', 'jumlah_hari_trading']]
    
    return agg


def main():
    print("=" * 60)
    print("SCRIPT 2: Process KURS/BI.csv → fact_kurs_bulanan.csv")
    print("=" * 60)
    
    df = load_and_process_kurs()
    
    output_path = os.path.join(OUTPUT_CORE, "fact_kurs_bulanan.csv")
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
    assert df['avg_kurs_tengah'].notna().all(), "No NULL values should exist in kurs tengah"
    assert (df['avg_kurs_tengah'] > 10000).all(), "All kurs values should be > 10.000"
    assert (df['avg_kurs_tengah'] < 20000).all(), "All kurs values should be < 20.000"
    
    print("\n✅ Verifikasi passed: 60 baris, range valid, semua kurs masuk akal")
    
    # Spot-check: tampilkan range kurs per tahun
    print("\n📊 Range kurs per tahun:")
    for year in range(2020, 2025):
        year_data = df[df['waktu_id'].between(year*100+1, year*100+12)]
        print(f"   {year}: Rp {year_data['avg_kurs_tengah'].min():,.0f} - Rp {year_data['avg_kurs_tengah'].max():,.0f}")


if __name__ == "__main__":
    main()
