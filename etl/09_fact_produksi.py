"""
09_fact_produksi.py — Generate Fact_Produksi
ETL Pipeline v3.2 (Clean Rewrite)

Output:
  - output/fact_produksi.csv

Sumber: BAB IV (96 file CSV produksi per maskapai)
Kolom: waktu_id, maskapai_id, kategori_rute, aircraft_km, aircraft_departure...
"""

import csv
import os
import sys
import re
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from etl.config import OUTPUT_DIR, BASE_DIR, TAHUN_RANGE, ensure_output_dir
from etl.utils import parse_angka_indonesia, standardize_maskapai


def load_dim_maskapai():
    maskapai_path = OUTPUT_DIR / "dim_maskapai.csv"
    m_map = {}
    with open(maskapai_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cat = row.get('kategori_maskapai', 'NASIONAL')
            m_map[(row['nama_maskapai'], cat)] = int(row['maskapai_id'])
    return m_map


def parse_produksi_val(val):
    if not val:
        return 0.0
    val = str(val).strip()
    if val in ('-', '', 'nan', 'NaN'):
        return 0.0
    
    # Handle Aircraft Hours: "114282:49"
    if ':' in val:
        parts = val.split(':')
        try:
            return float(parts[0]) + (float(parts[1])/60.0)
        except:
            pass
            
    # Percentage
    if ',' in val and '.' not in val:
        try: return float(val.replace(',', '.'))
        except: return 0.0
        
    num = parse_angka_indonesia(val)
    if num is not None:
        return float(num)
    return 0.0


def main():
    print("=" * 60)
    print("09_fact_produksi.py — Generate Fact Produksi")
    print("=" * 60)

    ensure_output_dir()
    maskapai_map = load_dim_maskapai()
    print(f"  Loaded dim_maskapai: {len(maskapai_map)} maskapai")

    BAB_IV_DIR = BASE_DIR / "DJPU" / "Table_Pilihan" / "BAB IV — Produksi"

    # Folders mapping
    folder_mappings = [
        ('CSV_Produksi Angkutan Udara Niaga Berjadwal Dalam Negeri 2020-2024', 'DOMESTIK', 'NASIONAL'),
        ('CSV_PRODUKSI ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI 2020 - 2024 BADAN USAHA ANGKUTAN UDARA NASIONAL', 'INTERNASIONAL', 'NASIONAL'),
        ('CSV_PRODUKSI ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI 2020 - 2024 PERUSAHAAN ANGKUTAN UDARA ASING', 'INTERNASIONAL', 'ASING')
    ]

    records = []

    # Target mapping
    metrics_map = {
        '1': 'aircraft_km',
        '2': 'aircraft_departure',
        '3': 'aircraft_hours',
        '4': 'passenger_carried',
        '5': 'freight_carried',
        '6': 'passenger_km',
        '7': 'available_seat_km',
        '8': 'passenger_load_factor',
        '9A': 'ton_km_passenger',
        '9B': 'ton_km_freight',
        '9C': 'ton_km_mail',
        '9D': 'ton_km_total',
        '10': 'available_ton_km',
        '11': 'weight_load_factor'
    }

    for folder, kategori_rute, flag_nasional in folder_mappings:
        fdir = BAB_IV_DIR / folder
        if not fdir.exists():
            continue
            
        print(f"\n  📁 Scanning: {folder}")
        
        for fname in os.listdir(fdir):
            if not fname.lower().endswith('.csv'):
                continue
            
            # Use absolute path with prefix for long paths on Windows
            abs_path = os.path.abspath(os.path.join(str(fdir), fname))
            if os.name == 'nt' and not abs_path.startswith('\\\\?\\'):
                abs_path = '\\\\?\\' + abs_path
            
            # Extract name from filename 
            name_raw = fname.upper().replace('.CSV', '')
            name_raw = re.sub(r'^PRODUKSI ANGKUTAN UDARA NIAGA BERJADWAL.*?2024\s*', '', name_raw)
            name_raw = re.sub(r'^PERUSAHAAN ANGKUTAN UDARA ASING\s*', '', name_raw)
            name_raw = re.sub(r'^BADAN USAHA ANGKUTAN UDARA NASIONAL\s*', '', name_raw)
            name_raw = name_raw.strip()
            
            nama_std = standardize_maskapai(name_raw)
            
            # Find ID
            m_id = None
            if (nama_std, flag_nasional) in maskapai_map:
                m_id = maskapai_map[(nama_std, flag_nasional)]
            else:
                # Try finding by just name
                candidates = [v for k, v in maskapai_map.items() if k[0] == nama_std]
                if candidates:
                    m_id = candidates[0]
            
            if not m_id:
                # Try partial match as fallback
                candidates_partial = [v for k, v in maskapai_map.items() if nama_std in k[0] or k[0] in nama_std]
                if candidates_partial:
                    m_id = candidates_partial[0]
                else:
                    print(f"    ⚠️ Maskapai ID not found for: {fname} -> {nama_std} ({flag_nasional})")
                    continue
                
            # Dictionary year -> metrics
            data_per_year = {
                2020: {}, 2021: {}, 2022: {}, 2023: {}, 2024: {}
            }
            
            try:
                # We can't use 'with open(abs_path)' directly with \\?\ prefix in some python versions/setups
                # but in modern Python 3.x on Windows it should work if using os.open or just open()
                with open(abs_path, 'r', encoding='utf-8-sig', newline='') as f:
                    reader = csv.reader(f)
                    try:
                        headers = next(reader, [])
                    except StopIteration:
                        continue
                    
                    # identify year column index
                    yr_cols = {}
                    for i, col in enumerate(headers):
                        cstr = col.strip()
                        if cstr in ['2020', '2021', '2022', '2023', '2024']:
                            yr_cols[int(cstr)] = i
                    
                    for row in reader:
                        if not row: continue
                        no = str(row[0]).strip().upper()
                        if no in metrics_map:
                            col_name = metrics_map[no]
                            for yr, y_idx in yr_cols.items():
                                if y_idx < len(row):
                                    data_per_year[yr][col_name] = parse_produksi_val(row[y_idx])
            except Exception as e:
                print(f"    ❌ Error reading {fname}: {e}")
                continue

            # Flush to records
            for yr in range(2020, 2025):
                mdata = data_per_year.get(yr, {})
                if not mdata:
                    continue
                    
                # Skip if totally empty
                if all(val == 0.0 for val in mdata.values()):
                    continue
                    
                rec = {
                    'waktu_id': yr,
                    'maskapai_id': m_id,
                    'kategori_rute': kategori_rute
                }
                for mm in metrics_map.values():
                    rec[mm] = mdata.get(mm, 0.0)
                records.append(rec)

    print(f"\n  Total records: {len(records)} baris output")
    
    out_path = OUTPUT_DIR / "fact_produksi_maskapai.csv"
    fieldnames = ['waktu_id', 'maskapai_id', 'kategori_rute'] + list(metrics_map.values())
    with open(out_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"  ✅ fact_produksi_maskapai.csv — {len(records)} baris")
    print("\n✅ 09_fact_produksi.py SELESAI")

if __name__ == "__main__":
    main()
