"""
05_fact_kurs.py — Generate Fact_Kurs_Bulanan dan Fact_Kurs_Tahunan
ETL Pipeline v3.2 (Clean Rewrite)

Output:
  - output/fact_kurs_bulanan.csv
  - output/fact_kurs_tahunan.csv

Sumber: KURS/BI.csv
Kolom output bulanan: waktu_id, avg_kurs_jual, avg_kurs_beli, avg_kurs_tengah, min_kurs_tengah, max_kurs_tengah, jumlah_hari_trading
Kolom output tahunan: waktu_id, avg_kurs_jual, avg_kurs_beli, avg_kurs_tengah, min_kurs_tengah, max_kurs_tengah, jumlah_hari_trading
"""

import csv
import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from etl.config import KURS_CSV, OUTPUT_DIR, TAHUN_RANGE, ensure_output_dir


def main():
    print("=" * 60)
    print("05_fact_kurs.py — Generate Fact Kurs (Bulanan & Tahunan)")
    print("=" * 60)

    ensure_output_dir()

    # Data structures untuk agregasi
    # Key = (tahun, bulan)
    bulanan = {}
    # Key = (tahun)
    tahunan = {}

    print(f"  Reading: {KURS_CSV.name}...")
    
    # 1. Baca dan filter CSV
    with open(KURS_CSV, 'r', encoding='utf-8-sig', newline='') as f:
        reader = csv.reader(f)
        # Skip baris 1-3: "Kurs Transaksi", blank, "NO,Nilai,Kurs Jual,Kurs Beli,Tanggal"
        for _ in range(3):
            next(reader, None)

        rows_read = 0
        rows_filtered = 0
        
        for row in reader:
            if not row or len(row) < 5:
                continue
            
            rows_read += 1
            
            try:
                # Kolom: [NO, Nilai, Kurs Jual, Kurs Beli, Tanggal]
                jual = float(row[2].replace(',', '.'))
                beli = float(row[3].replace(',', '.'))
                tengah = (jual + beli) / 2.0
                
                # Parse tgl: "12/31/2024 12:00:00 AM"
                # date format: %m/%d/%Y %I:%M:%S %p
                tgl_str = row[4].strip()
                tgl = datetime.datetime.strptime(tgl_str, "%m/%d/%Y %I:%M:%S %p")
                
                tahun = tgl.year
                bulan = tgl.month
                
            except ValueError as e:
                # if row is broken
                continue

            if tahun not in TAHUN_RANGE:
                continue
                
            rows_filtered += 1

            # Agregasi Bulanan
            k_bulan = (tahun, bulan)
            if k_bulan not in bulanan:
                bulanan[k_bulan] = {
                    'sum_jual': 0.0, 'sum_beli': 0.0, 'sum_tengah': 0.0,
                    'min_tg': float('inf'), 'max_tg': float('-inf'),
                    'count': 0
                }
            bm = bulanan[k_bulan]
            bm['sum_jual'] += jual
            bm['sum_beli'] += beli
            bm['sum_tengah'] += tengah
            bm['min_tg'] = min(bm['min_tg'], tengah)
            bm['max_tg'] = max(bm['max_tg'], tengah)
            bm['count'] += 1

            # Agregasi Tahunan
            k_tahun = tahun
            if k_tahun not in tahunan:
                tahunan[k_tahun] = {
                    'sum_jual': 0.0, 'sum_beli': 0.0, 'sum_tengah': 0.0,
                    'min_tg': float('inf'), 'max_tg': float('-inf'),
                    'count': 0
                }
            tm = tahunan[k_tahun]
            tm['sum_jual'] += jual
            tm['sum_beli'] += beli
            tm['sum_tengah'] += tengah
            tm['min_tg'] = min(tm['min_tg'], tengah)
            tm['max_tg'] = max(tm['max_tg'], tengah)
            tm['count'] += 1

    print(f"  Rows read: {rows_read}")
    print(f"  Rows in range (2020-2024): {rows_filtered}")

    # =========================================================================
    # 2. Output Fact_Kurs_Bulanan
    # =========================================================================
    records_bulanan = []
    for (t, b), m in sorted(bulanan.items()):
        c = m['count']
        if c == 0: continue
        waktu_id = t * 100 + b
        records_bulanan.append({
            'waktu_id': waktu_id,
            'avg_kurs_jual': round(m['sum_jual'] / c, 2),
            'avg_kurs_beli': round(m['sum_beli'] / c, 2),
            'avg_kurs_tengah': round(m['sum_tengah'] / c, 2),
            'min_kurs_tengah': round(m['min_tg'], 2),
            'max_kurs_tengah': round(m['max_tg'], 2),
            'jumlah_hari_trading': c
        })

    out_bulanan = OUTPUT_DIR / "fact_kurs_bulanan.csv"
    fieldnames_b = ['waktu_id', 'avg_kurs_jual', 'avg_kurs_beli', 
                    'avg_kurs_tengah', 'min_kurs_tengah', 'max_kurs_tengah', 'jumlah_hari_trading']
    with open(out_bulanan, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames_b)
        writer.writeheader()
        writer.writerows(records_bulanan)
    print(f"  ✅ fact_kurs_bulanan.csv — {len(records_bulanan)} baris")

    # =========================================================================
    # 3. Output Fact_Kurs_Tahunan
    # =========================================================================
    records_tahunan = []
    for t, m in sorted(tahunan.items()):
        c = m['count']
        if c == 0: continue
        records_tahunan.append({
            'waktu_id': t,
            'avg_kurs_jual': round(m['sum_jual'] / c, 2),
            'avg_kurs_beli': round(m['sum_beli'] / c, 2),
            'avg_kurs_tengah': round(m['sum_tengah'] / c, 2),
            'min_kurs_tengah': round(m['min_tg'], 2),
            'max_kurs_tengah': round(m['max_tg'], 2),
            'jumlah_hari_trading': c
        })

    out_tahunan = OUTPUT_DIR / "fact_kurs_tahunan.csv"
    fieldnames_t = ['waktu_id', 'avg_kurs_jual', 'avg_kurs_beli', 
                    'avg_kurs_tengah', 'min_kurs_tengah', 'max_kurs_tengah', 'jumlah_hari_trading']
    with open(out_tahunan, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames_t)
        writer.writeheader()
        writer.writerows(records_tahunan)
    print(f"  ✅ fact_kurs_tahunan.csv — {len(records_tahunan)} baris")

    print("\n✅ 05_fact_kurs.py SELESAI")

if __name__ == "__main__":
    main()
