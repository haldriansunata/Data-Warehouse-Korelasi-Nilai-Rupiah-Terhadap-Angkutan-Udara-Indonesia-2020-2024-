"""
08_fact_lalu_lintas.py — Generate Fact_Lalu_Lintas
ETL Pipeline v3.2 (Clean Rewrite)

Output:
  - output/fact_lalu_lintas.csv

Sumber: BAB VII
Kolom output: waktu_id, bandara_id, kategori_lalu_lintas, 
              pesawat_dtg, pesawat_brk, pesawat_total, ... (19 metrics total)
"""

import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from etl.config import OUTPUT_DIR, BAB_VII_CSV, TAHUN_RANGE, ensure_output_dir
from etl.utils import parse_angka_indonesia, parse_airport_name


def load_dim_bandara():
    bandara_path = OUTPUT_DIR / "dim_bandara.csv"
    b_map = {}
    with open(bandara_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            b_map[(row['nama_bandara'], row['kota'])] = int(row['bandara_id'])
    return b_map

def main():
    print("=" * 60)
    print("08_fact_lalu_lintas.py — Generate Fact Lalu Lintas")
    print("=" * 60)

    ensure_output_dir()
    b_map = load_dim_bandara()

    # Metrics cols (16 metrics) + 1 transit
    metric_cols = [
        'pesawat_dtg', 'pesawat_brk', 'pesawat_total',
        'penumpang_dtg', 'penumpang_brk', 'penumpang_total', 'penumpang_tra',
        'bagasi_dtg', 'bagasi_brk', 'bagasi_total',
        'barang_dtg', 'barang_brk', 'barang_total',
        'pos_dtg', 'pos_brk', 'pos_total'
    ]

    records = []
    
    with open(BAB_VII_CSV, 'r', encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            airport_raw = row.get('airport_name', '').strip()
            if not airport_raw:
                continue

            nama_bandara, kota, kategori = parse_airport_name(airport_raw)
            nama_bandara = nama_bandara.strip().upper()
            kota = kota.strip().upper()
            
            key = (nama_bandara, kota)
            if key not in b_map:
                continue
                
            bandara_id = b_map[key]
            
            try:
                tahun = int(str(row.get('year', '')).strip())
            except:
                continue
                
            if tahun not in TAHUN_RANGE:
                continue
            
            rec = {
                'waktu_id': tahun,
                'bandara_id': bandara_id,
                'kategori': kategori
            }
            
            # loop columns and parse
            for m in metric_cols:
                v = row.get(m, '')
                # Note: bagasi, barang, pos format can use european decimal (,) or dot.
                # BAB VII mainly uses dots for thousands and dashes for 0.
                if v == '-' or str(v).strip() == '':
                    rec[m] = 0.0 if m in ('bagasi_dtg','bagasi_brk','bagasi_total','barang_dtg','barang_brk','barang_total','pos_dtg','pos_brk','pos_total') else 0
                else:
                    val = parse_angka_indonesia(v)
                    rec[m] = val if val is not None else 0
                    
            records.append(rec)

    out_path = OUTPUT_DIR / "fact_lalu_lintas_bandara.csv"
    fieldnames = ['waktu_id', 'bandara_id', 'kategori'] + metric_cols
    with open(out_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"  ✅ fact_lalu_lintas_bandara.csv — {len(records)} baris")
    print("\n✅ 08_fact_lalu_lintas.py SELESAI")

if __name__ == "__main__":
    main()
