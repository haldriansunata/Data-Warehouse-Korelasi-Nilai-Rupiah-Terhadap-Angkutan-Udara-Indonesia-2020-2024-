"""
Script 4 (Fase 2): Build dim_maskapai.csv
Input:  BAB IV filenames + BAB XII column + BAB II reference
Output: output/fase2_enrichment/dim_maskapai.csv

Master list maskapai unik dengan nama standar.
"""

import os
import sys
import re
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import BAB_IV_DIR, BAB_XII_DIR, BAB_II_DIR, OUTPUT_ENRICHMENT
from utils import standardize_maskapai, maskapai_to_id


def extract_names_from_bab_iv():
    """Extract nama maskapai dari nama file BAB IV."""
    names = []
    prefix = "PRODUKSI ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI 2020-2024 "
    
    for fname in os.listdir(BAB_IV_DIR):
        if not fname.endswith('.csv'):
            continue
        # Strip prefix and .csv
        name = fname.replace(prefix, '').replace('.csv', '').strip()
        if name:
            names.append(name)
    
    return names


def extract_names_from_bab_xii():
    """Extract nama maskapai dari kolom BADAN USAHA di BAB XII."""
    csv_files = [f for f in os.listdir(BAB_XII_DIR) if f.endswith('.csv')]
    if not csv_files:
        return []
    
    fpath = os.path.join(BAB_XII_DIR, csv_files[0])
    df = pd.read_csv(fpath, encoding='utf-8', dtype=str)
    
    names = []
    for _, row in df.iterrows():
        name = str(row.get('BADAN USAHA', '')).strip()
        no = str(row.get('NO', '')).strip()
        # Skip Total row
        if no == '-' or 'Total' in name or 'Rata' in name:
            continue
        if name and name != 'nan':
            names.append(name)
    
    return names


def main():
    print("=" * 60)
    print("SCRIPT 4 (Fase 2): Build dim_maskapai.csv")
    print("=" * 60)
    
    # 1. Collect all names
    names_iv = extract_names_from_bab_iv()
    print(f"\nBAB IV: {len(names_iv)} maskapai dari filename")
    
    names_xii = extract_names_from_bab_xii()
    print(f"BAB XII: {len(names_xii)} maskapai dari kolom BADAN USAHA")
    
    # 2. Union all names
    all_names = set(names_iv + names_xii)
    print(f"Union: {len(all_names)} nama unik (sebelum standardisasi)")
    
    # 3. Standardize and deduplicate
    rows = []
    seen_ids = set()
    
    for raw_name in sorted(all_names):
        nama_standar = standardize_maskapai(raw_name)
        mid = maskapai_to_id(raw_name)
        
        if mid in seen_ids:
            continue
        seen_ids.add(mid)
        
        # Nama pendek: strip PT prefix
        nama_pendek = nama_standar
        if nama_pendek.upper().startswith("PT "):
            nama_pendek = nama_pendek[3:]
        
        rows.append({
            'maskapai_id': mid,
            'nama_maskapai': nama_standar,
            'nama_pendek': nama_pendek,
        })
    
    df = pd.DataFrame(rows).sort_values('maskapai_id').reset_index(drop=True)
    
    # 4. Output
    output_path = os.path.join(OUTPUT_ENRICHMENT, "dim_maskapai.csv")
    df.to_csv(output_path, index=False)
    
    print(f"\nOutput: {output_path}")
    print(f"Jumlah baris: {len(df)}")
    print(f"\nDaftar maskapai:")
    for _, row in df.iterrows():
        print(f"  {row['maskapai_id']:40s} | {row['nama_maskapai']}")
    
    print(f"\n[OK] dim_maskapai.csv berhasil dibuat ({len(df)} maskapai)")


if __name__ == "__main__":
    main()
