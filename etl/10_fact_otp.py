"""
10_fact_otp.py — Generate Fact_OTP
ETL Pipeline v3.2 (Clean Rewrite)

Output:
  - output/fact_otp.csv

Sumber: BAB XII (OTP 2024 single file)
Kolom: waktu_id, maskapai_id, otp_value
"""

import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from etl.config import OUTPUT_DIR, BAB_XII_CSV, ensure_output_dir
from etl.utils import standardize_maskapai


def load_dim_maskapai():
    maskapai_path = OUTPUT_DIR / "dim_maskapai.csv"
    m_map = {}
    with open(maskapai_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # OTP only for Nasional
            if row['kategori_maskapai'] == 'NASIONAL':
                m_map[row['nama_maskapai']] = int(row['maskapai_id'])
    return m_map


def parse_otp_val(val):
    if not val:
        return None
    val = str(val).strip().replace('%', '')
    if val in ('-', '', 'nan', 'NaN'):
        return None
    
    # European decimal
    if ',' in val:
        val = val.replace(',', '.')
    
    try:
        f = float(val) / 100.0
        return round(f, 4)
    except:
        return None


def main():
    print("=" * 60)
    print("10_fact_otp.py — Generate Fact OTP")
    print("=" * 60)

    ensure_output_dir()
    maskapai_map = load_dim_maskapai()
    print(f"  Loaded dim_maskapai (Nasional): {len(maskapai_map)}")

    if not BAB_XII_CSV.exists():
        print(f"  ❌ File not found: {BAB_XII_CSV}")
        return

    records = []
    
    # BAB XII has single file
    with open(BAB_XII_CSV, 'r', encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        
        # Check years we care about: 2020-2024
        target_years = ['2020', '2021', '2022', '2023', '2024']
        
        for row in reader:
            bu_raw = row.get('BADAN USAHA', '').strip()
            if not bu_raw or bu_raw.upper() == 'TOTAL/RATA-RATA':
                continue
            
            nama_std = standardize_maskapai(bu_raw)
            m_id = maskapai_map.get(nama_std)
            
            if not m_id:
                # Try partial match if exactly standard fails
                candidates = [v for k,v in maskapai_map.items() if nama_std in k or k in nama_std]
                if candidates:
                    m_id = candidates[0]
                else:
                    print(f"    ⚠️ Maskapai ID not found for: {bu_raw} -> {nama_std}")
                    continue
            
            for yr in target_years:
                val_raw = row.get(yr)
                val = parse_otp_val(val_raw)
                if val is not None:
                    records.append({
                        'waktu_id': int(yr),
                        'maskapai_id': m_id,
                        'otp_percentage': val
                    })

    out_path = OUTPUT_DIR / "fact_otp_maskapai.csv"
    fieldnames = ['waktu_id', 'maskapai_id', 'otp_percentage']
    with open(out_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"  ✅ fact_otp_maskapai.csv — {len(records)} baris")
    print("\n✅ 10_fact_otp.py SELESAI")

if __name__ == "__main__":
    main()
