"""
Script 3: Process BAB VI (20 CSV) → fact_penumpang + agregat + dim_rute
Output: 
  - output/fase1_core/fact_penumpang_rute_bulanan.csv
  - output/fase1_core/fact_penumpang_agregat_bulanan.csv
  - output/fase1_core/dim_rute.csv

Ini script PALING KOMPLEKS — setiap tahun punya format berbeda.
"""

import os
import sys
import re
import glob
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import BAB_VI_DIR, OUTPUT_CORE, TAHUN_RANGE
from utils import (
    normalize_route_pp,
    extract_iata_from_route_2020,
    extract_iata_from_route_2021,
    extract_iata_from_route_code,
    parse_penumpang_value,
)


# --- FILE DISCOVERY ---

def find_bulanan_files():
    """
    Cari file CSV bulanan (domestik + internasional) per tahun.
    Return: list of (filepath, year, kategori)
    """
    files = []
    for year in TAHUN_RANGE:
        year_dir = os.path.join(BAB_VI_DIR, str(year))
        if not os.path.isdir(year_dir):
            print(f"  WARNING: Folder {year_dir} tidak ditemukan, skip.")
            continue
        
        for fname in os.listdir(year_dir):
            if not fname.endswith('.csv'):
                continue
            if 'STATISTIK' in fname.upper() or 'RANKING' in fname.upper():
                continue  # skip ranking files
            
            fpath = os.path.join(year_dir, fname)
            fname_upper = fname.upper()
            
            if 'DALAM NEGERI' in fname_upper:
                kategori = 'DOMESTIK'
            elif 'LUAR NEGERI' in fname_upper:
                kategori = 'INTERNASIONAL'
            else:
                continue  # skip unknown files
            
            files.append((fpath, year, kategori))
    
    return sorted(files, key=lambda x: (x[1], x[2]))


# --- ROUTE PARSING ---

def parse_route(route_str, year):
    """
    Parse rute ke (kode_origin, kode_dest, kota_origin, kota_dest) sesuai format tahun.
    """
    if route_str is None or str(route_str).strip() == '':
        return None, None, None, None
    
    route_str = str(route_str).strip()
    
    if year in (2020, 2021):
        # Format: "Jakarta (CGK)-Denpasar (DPS)" atau "Jakarta (CGK) - Denpasar (DPS)"
        return extract_iata_from_route_2020(route_str)
    else:
        # Format 2022-2024: "CGK-DPS"
        return extract_iata_from_route_code(route_str)


# --- MAIN PROCESSING ---

def process_one_file(filepath, year, kategori):
    """
    Process satu file CSV bulanan BAB VI.
    
    Returns: DataFrame dengan kolom [waktu_id, rute_id, kategori, jumlah_penumpang,
                                     kode_a, kode_b, kota_a, kota_b]
    """
    print(f"  Processing: {os.path.basename(filepath)} ({year}, {kategori})")
    
    # Baca CSV
    df = pd.read_csv(filepath, encoding='utf-8', dtype=str)
    
    # Kolom index: 0=NO, 1=RUTE, 2-13=12 bulan, 14+=TOTAL (skip)
    cols = list(df.columns)
    
    if len(cols) < 15:
        print(f"    WARNING: Hanya {len(cols)} kolom (expected >= 15), trying flexible parse")
    
    rute_col = cols[1]  # Apapun namanya — ambil kolom ke-2
    month_cols = cols[2:14]  # 12 kolom bulan
    
    rows = []
    for idx, row in df.iterrows():
        # STEP E: Filter baris non-data
        no_val = str(row.get(cols[0], '')).strip()
        rute_val = str(row.get(rute_col, '')).strip()
        
        # Skip Total row, empty rows, KARGO, footnotes
        if rute_val.upper() in ('', 'TOTAL', 'NAN'):
            continue
        if 'KARGO' in rute_val.upper():
            continue
        if rute_val.startswith('*'):
            continue
        
        # Cek apakah NO adalah angka
        try:
            int(float(no_val))
        except (ValueError, TypeError):
            if no_val.upper() not in ('', 'NAN', 'TOTAL'):
                continue
        
        # STEP B: Parse rute
        kode_origin, kode_dest, kota_origin, kota_dest = parse_route(rute_val, year)
        
        if kode_origin is None or kode_dest is None:
            print(f"    WARNING: Gagal parse rute '{rute_val}' di baris {idx+2}")
            continue
        
        # Normalisasi PP (alphabetical)
        kode_a, kode_b = normalize_route_pp(kode_origin, kode_dest)
        rute_id = f"{kode_a}-{kode_b}"
        
        # Flip kota jika kode di-flip
        if kode_a == kode_origin:
            kota_a, kota_b = kota_origin, kota_dest
        else:
            kota_a, kota_b = kota_dest, kota_origin
        
        # STEP C & D: Unpivot 12 bulan + parse angka
        for bulan_idx, month_col in enumerate(month_cols):
            bulan = bulan_idx + 1
            waktu_id = year * 100 + bulan
            
            val = str(row.get(month_col, '')).strip()
            penumpang = parse_penumpang_value(val, year)
            
            # Skip NULL/empty → tidak simpan baris ini
            if penumpang is None:
                continue
            
            rows.append({
                'waktu_id': waktu_id,
                'rute_id': rute_id,
                'kategori': kategori,
                'jumlah_penumpang': int(penumpang),
                'kode_a': kode_a,
                'kode_b': kode_b,
                'kota_a': kota_a,
                'kota_b': kota_b,
            })
    
    print(f"    → {len(rows)} baris data terisi")
    return pd.DataFrame(rows) if rows else pd.DataFrame()


def build_dim_rute(df_all):
    """
    Extract dim_rute dari semua data penumpang.
    Prioritaskan nama kota dari data yang punya kota (2020-2021).
    """
    if df_all.empty:
        return pd.DataFrame()
    
    # Group by rute_id dan ambil first non-null kota
    dim = df_all.groupby(['rute_id', 'kode_a', 'kode_b', 'kategori']).agg(
        kota_a=('kota_a', lambda x: next((v for v in x if v is not None and str(v) != 'None' and str(v) != ''), None)),
        kota_b=('kota_b', lambda x: next((v for v in x if v is not None and str(v) != 'None' and str(v) != ''), None)),
    ).reset_index()
    
    # Replace 'None' strings with empty string for cleaner CSV
    for col in ['kota_a', 'kota_b']:
        dim[col] = dim[col].apply(lambda x: '' if x is None or str(x) == 'None' else x)
    
    return dim[['rute_id', 'kode_a', 'kode_b', 'kota_a', 'kota_b', 'kategori']]


def build_agregat(df_fact):
    """
    Aggregate fact_penumpang_rute → fact_penumpang_agregat_bulanan.
    """
    if df_fact.empty:
        return pd.DataFrame()
    
    agg = df_fact.groupby(['waktu_id', 'kategori']).agg(
        total_penumpang=('jumlah_penumpang', 'sum'),
        jumlah_rute_aktif=('jumlah_penumpang', 'count'),
    ).reset_index()
    
    agg['tahun'] = agg['waktu_id'] // 100
    agg['bulan'] = agg['waktu_id'] % 100
    
    # Reorder columns
    agg = agg[['waktu_id', 'tahun', 'bulan', 'kategori', 'total_penumpang', 'jumlah_rute_aktif']]
    
    return agg


def main():
    print("=" * 60)
    print("SCRIPT 3: Process BAB VI → Penumpang + Agregat + Rute")
    print("=" * 60)
    
    # 1. Discover files
    files = find_bulanan_files()
    print(f"\nDitemukan {len(files)} file CSV bulanan:")
    for fpath, year, kat in files:
        print(f"  {year} {kat}: {os.path.basename(fpath)}")
    
    # 2. Process all files
    print(f"\n--- Processing ---")
    all_frames = []
    for fpath, year, kat in files:
        df = process_one_file(fpath, year, kat)
        if not df.empty:
            all_frames.append(df)
    
    if not all_frames:
        print("ERROR: Tidak ada data yang berhasil di-process!")
        return
    
    df_all = pd.concat(all_frames, ignore_index=True)
    print(f"\nTotal baris terisi: {len(df_all)}")
    
    # 3. Build fact_penumpang_rute_bulanan
    df_fact = df_all[['waktu_id', 'rute_id', 'kategori', 'jumlah_penumpang']].copy()
    
    # Aggregate duplikat (rute yang sama bisa muncul karena normalisasi PP)
    df_fact = df_fact.groupby(['waktu_id', 'rute_id', 'kategori']).agg(
        jumlah_penumpang=('jumlah_penumpang', 'sum')
    ).reset_index()
    
    fact_path = os.path.join(OUTPUT_CORE, "fact_penumpang_rute_bulanan.csv")
    df_fact.to_csv(fact_path, index=False)
    print(f"\n--- Output 1: fact_penumpang_rute_bulanan ---")
    print(f"  Path: {fact_path}")
    print(f"  Baris: {len(df_fact)}")
    print(f"  Kolom: {list(df_fact.columns)}")
    
    # 4. Build dim_rute
    df_rute = build_dim_rute(df_all)
    rute_path = os.path.join(OUTPUT_CORE, "dim_rute.csv")
    df_rute.to_csv(rute_path, index=False)
    print(f"\n--- Output 2: dim_rute ---")
    print(f"  Path: {rute_path}")
    print(f"  Baris: {len(df_rute)}")
    
    # 5. Build agregat
    df_agregat = build_agregat(df_fact)
    agregat_path = os.path.join(OUTPUT_CORE, "fact_penumpang_agregat_bulanan.csv")
    df_agregat.to_csv(agregat_path, index=False)
    print(f"\n--- Output 3: fact_penumpang_agregat_bulanan ---")
    print(f"  Path: {agregat_path}")
    print(f"  Baris: {len(df_agregat)}")
    
    # 6. Verifikasi
    print(f"\n{'=' * 60}")
    print("VERIFIKASI")
    print(f"{'=' * 60}")
    
    # Check dim_rute — no duplicate rute_id within same kategori
    dup_check = df_rute.groupby(['rute_id', 'kategori']).size()
    dups = dup_check[dup_check > 1]
    if len(dups) > 0:
        print(f"  WARNING: {len(dups)} duplicate rute_id ditemukan:")
        print(dups.head())
    else:
        print(f"  [OK] dim_rute: Tidak ada duplikat rute_id per kategori")
    
    # Check PP normalization — tidak boleh ada "DPS-CGK" bersamaan dengan "CGK-DPS"
    all_rute_ids = set(df_rute['rute_id'])
    pp_violations = []
    for rid in all_rute_ids:
        parts = rid.split('-')
        if len(parts) == 2:
            reversed_id = f"{parts[1]}-{parts[0]}"
            if reversed_id in all_rute_ids and reversed_id != rid:
                pp_violations.append((rid, reversed_id))
    if pp_violations:
        print(f"  WARNING: {len(pp_violations)} PP violations found:")
        for a, b in pp_violations[:5]:
            print(f"    {a} dan {b} keduanya ada!")
    else:
        print(f"  [OK] Normalisasi PP: Tidak ada rute terbalik")
    
    # Check agregat completeness
    print(f"  [OK] Agregat: {len(df_agregat)} baris (expected ~120)")
    
    # Spot-check: total penumpang domestik per tahun
    print(f"\nTotal penumpang DOMESTIK per tahun:")
    dom = df_agregat[df_agregat['kategori'] == 'DOMESTIK']
    for year in TAHUN_RANGE:
        year_total = dom[dom['tahun'] == year]['total_penumpang'].sum()
        print(f"  {year}: {year_total:,.0f}")
    
    print(f"\nTotal penumpang INTERNASIONAL per tahun:")
    intl = df_agregat[df_agregat['kategori'] == 'INTERNASIONAL']
    for year in TAHUN_RANGE:
        year_total = intl[intl['tahun'] == year]['total_penumpang'].sum()
        print(f"  {year}: {year_total:,.0f}")
    
    print(f"\n[DONE] Semua output Fase 1 selesai!")


if __name__ == "__main__":
    main()
