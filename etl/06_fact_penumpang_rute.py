"""
06_fact_penumpang_rute.py — Generate Fact_Penumpang_Rute
ETL Pipeline v3.2 (Clean Rewrite)

Output:
  - output/fact_penumpang_rute.csv

Sumber: BAB VI (20 file CSV: "JUMLAH PENUMPANG PER RUTE...")
Kolom output: waktu_id, rute_id, kategori_rute, jumlah_penumpang
"""

import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from etl.config import OUTPUT_DIR, BAB_VI_DIR, TAHUN_RANGE, ensure_output_dir
from etl.utils import parse_angka_indonesia, extract_iata_from_route


def read_csv_auto(filepath):
    """Baca CSV dengan auto-detect encoding."""
    for enc in ['utf-8-sig', 'utf-8', 'latin-1', 'cp1252']:
        try:
            with open(filepath, 'r', encoding=enc, newline='') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                return rows, reader.fieldnames
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot read {filepath}")


def find_csv_files(base_dir, keywords_include, keywords_exclude=None):
    results = []
    for tahun in TAHUN_RANGE:
        tahun_dir = os.path.join(base_dir, str(tahun))
        if not os.path.isdir(tahun_dir):
            continue
        for f in os.listdir(tahun_dir):
            if not f.lower().endswith('.csv'):
                continue
            f_upper = f.upper()
            if all(kw.upper() in f_upper for kw in keywords_include):
                if keywords_exclude and any(kw.upper() in f_upper for kw in keywords_exclude):
                    continue
                results.append((tahun, os.path.join(tahun_dir, f), f))
    return results


def load_dim_rute():
    # Load rute_id mapping (kode_rute -> rute_id)
    rute_path = OUTPUT_DIR / "dim_rute.csv"
    rute_map = {}
    with open(rute_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rute_map[row['kode_rute']] = int(row['rute_id'])
    return rute_map

def extract_route_iata_pair(val: str) -> str | None:
    iata1, iata2, _, _ = extract_iata_from_route(val)
    if iata1 and iata2 and len(iata1) == 3 and len(iata2) == 3:
        pair = sorted([iata1.upper(), iata2.upper()])
        return f"{pair[0]}-{pair[1]}"
    return None

MONTH_PREFIXES = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'MEI', 'JUN', 'JUL', 'AUG', 'AGU', 'SEP', 'OCT', 'OKT', 'NOV', 'DEC', 'DES']

def extract_month_from_col(col_name: str) -> int | None:
    cu = col_name.upper().strip()
    # Paling gampang: cek prefix 3 digit
    for i, p in enumerate(['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']):
        if cu.startswith(p):
            return i + 1
    for i, p in enumerate(['JAN', 'FEB', 'MAR', 'APR', 'MEI', 'JUN', 'JUL', 'AGU', 'SEP', 'OKT', 'NOV', 'DES']):
        if cu.startswith(p):
            return i + 1
    return None

def process_file(tahun, tag_kategori, filepath, rute_map):
    rows, fieldnames = read_csv_auto(filepath)
    if not fieldnames:
        return []

    rute_col = None
    # Cari kolom rute
    for col in fieldnames:
        if 'RUTE' in col.upper():
            rute_col = col
            break
            
    if not rute_col:
        return []

    # Cari kolom bulan
    month_cols = {} # index -> month (1-12)
    for col in fieldnames:
        m = extract_month_from_col(col)
        if m:
            month_cols[col] = m

    records = []
    
    for row in rows:
        val_rute = row.get(rute_col, '').strip()
        if not val_rute or val_rute.upper() == 'TOTAL' or 'KARGO' in val_rute.upper():
            continue
            
        kode_rute = extract_route_iata_pair(val_rute)
        if not kode_rute or kode_rute not in rute_map:
            continue
            
        rute_id = rute_map[kode_rute]
        
        for col, bulan in month_cols.items():
            val = row.get(col)
            num = parse_angka_indonesia(val)
            if num is not None and num > 0:
                # Add to record
                waktu_id = (tahun * 100) + bulan
                records.append({
                    'waktu_id': waktu_id,
                    'rute_id': rute_id,
                    'kategori_rute': tag_kategori,
                    'jumlah_penumpang': num
                })
    return records


def main():
    print("=" * 60)
    print("06_fact_penumpang_rute.py — Generate Fact Penumpang Rute")
    print("=" * 60)

    ensure_output_dir()
    rute_map = load_dim_rute()
    print(f"  Loaded dim_rute: {len(rute_map)} routes")

    files_dom = find_csv_files(BAB_VI_DIR, ['JUMLAH', 'DALAM NEGERI'], ['STATISTIK'])
    files_int = find_csv_files(BAB_VI_DIR, ['JUMLAH', 'LUAR NEGERI'], ['STATISTIK'])
    
    all_records = []
    
    print("\n  Processing Domestic...")
    for t, fp, fn in files_dom:
        recs = process_file(t, 'DOMESTIK', fp, rute_map)
        print(f"    {t} | {fn[:40]:<40} -> {len(recs)} records")
        all_records.extend(recs)
        
    print("\n  Processing International...")
    for t, fp, fn in files_int:
        recs = process_file(t, 'INTERNASIONAL', fp, rute_map)
        print(f"    {t} | {fn[:40]:<40} -> {len(recs)} records")
        all_records.extend(recs)

    # Note: Rute yang sama bisa muncul di dataset domestik (penerbangan domestik CGK-DPS)
    # atau internasional. Tapi jumlah rute bisa jadi diagregasi ganda jika kita nggak hati2?
    # Berdasarkan schema: dim_waktu + dim_rute grain. 
    # Kita groupby waktu_id dan rute_id dan sum if duplications exist from multiple lines?
    
    # Aggregating just in case a file had duplicated rute
    from collections import defaultdict
    agg = defaultdict(int)
    for r in all_records:
        k = (r['waktu_id'], r['rute_id'])
        agg[k] += r['jumlah_penumpang']
        
    final_records = []
    for k, v in sorted(agg.items()):
        final_records.append({
            'waktu_id': k[0],
            'rute_id': k[1],
            'jumlah_penumpang': v
        })
        
    out_path = OUTPUT_DIR / "fact_penumpang_rute.csv"
    fieldnames = ['waktu_id', 'rute_id', 'jumlah_penumpang']
    with open(out_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(final_records)
        
    print(f"\n  ✅ fact_penumpang_rute.csv — {len(final_records)} baris")
    print("\n✅ 06_fact_penumpang_rute.py SELESAI")

if __name__ == "__main__":
    main()
