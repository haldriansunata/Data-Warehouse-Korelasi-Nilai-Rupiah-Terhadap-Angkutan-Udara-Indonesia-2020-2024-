"""
07_fact_statistik_rute.py — Generate Fact_Statistik_Rute
ETL Pipeline v3.2 (Clean Rewrite)

Output:
  - output/fact_statistik_rute.csv

Sumber: BAB VI (10 file CSV: "STATISTIK PER RUTE...")
Kolom output: waktu_id, rute_id, kategori_rute, jumlah_penerbangan, 
              jumlah_penumpang, kapasitas_seat, jumlah_barang_kg, 
              jumlah_pos_kg, load_factor_pct
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

def normalize_col_name(c):
    c = c.upper().strip()
    if 'PENERBANGAN' in c: return 'JUMLAH_PENERBANGAN'
    if 'KAPASITAS' in c: return 'KAPASITAS_SEAT'
    if 'BARANG' in c: return 'JUMLAH_BARANG'
    if 'POS' in c: return 'JUMLAH_POS'
    if 'L/F' in c or 'LF' in c or 'LOAD' in c: return 'LOAD_FACTOR'
    if 'PENUMPANG' in c: return 'JUMLAH_PENUMPANG'
    return c

def parse_float_indonesia(val):
    if not val:
        return 0.0
    val = str(val).strip().replace('%', '')
    if val in ('-', '', 'nan', 'NaN'):
        return 0.0
    if ',' in val and '.' not in val:
        try: return float(val.replace(',', '.'))
        except: return 0.0
    try:
        return float(val)
    except:
        return 0.0

def process_file(tahun, tag_kategori, filepath, rute_map):
    rows, fieldnames = read_csv_auto(filepath)
    if not fieldnames:
        return []

    # Mapping header
    col_mapping = {}
    rute_col = None
    for col in fieldnames:
        norm = normalize_col_name(col)
        if 'RUTE' in norm:
            rute_col = col
        else:
            col_mapping[norm] = col

    if not rute_col:
        return []

    records = []
    
    for row in rows:
        val_rute = row.get(rute_col, '').strip()
        if not val_rute or val_rute.upper() == 'TOTAL' or 'KARGO' in val_rute.upper() or 'RATA' in val_rute.upper():
            continue
            
        kode_rute = extract_route_iata_pair(val_rute)
        if not kode_rute or kode_rute not in rute_map:
            continue
            
        rute_id = rute_map[kode_rute]
        
        jml_penerbangan = parse_angka_indonesia(row.get(col_mapping.get('JUMLAH_PENERBANGAN'))) or 0
        jml_penumpang = parse_angka_indonesia(row.get(col_mapping.get('JUMLAH_PENUMPANG'))) or 0
        kapasitas = parse_angka_indonesia(row.get(col_mapping.get('KAPASITAS_SEAT'))) or 0
        jml_barang = parse_float_indonesia(row.get(col_mapping.get('JUMLAH_BARANG')))
        jml_pos = parse_float_indonesia(row.get(col_mapping.get('JUMLAH_POS')))
        lf = parse_float_indonesia(row.get(col_mapping.get('LOAD_FACTOR')))
        
        if jml_penerbangan == 0 and jml_penumpang == 0 and kapasitas == 0:
            continue

        records.append({
            'waktu_id': tahun,
            'rute_id': rute_id,
            'kategori_rute': tag_kategori,
            'jumlah_penerbangan': jml_penerbangan,
            'jumlah_penumpang': jml_penumpang,
            'kapasitas_seat': kapasitas,
            'jumlah_barang_kg': round(jml_barang, 2),
            'jumlah_pos_kg': round(jml_pos, 2),
            'load_factor_pct': round(lf, 2)
        })
    return records


def main():
    print("=" * 60)
    print("07_fact_statistik_rute.py — Generate Fact Statistik Rute")
    print("=" * 60)

    ensure_output_dir()
    rute_map = load_dim_rute()
    print(f"  Loaded dim_rute: {len(rute_map)} routes")

    files_dom = find_csv_files(BAB_VI_DIR, ['STATISTIK', 'DALAM NEGERI'])
    files_int = find_csv_files(BAB_VI_DIR, ['STATISTIK', 'LUAR NEGERI'])
    
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

    # Note: Sama seperti 06, rute bisa double di raw data.
    # Kita groupby waktu_id dan rute_id dan sum / (recalc LF) just in case.
    from collections import defaultdict
    agg = {}
    for r in all_records:
        k = (r['waktu_id'], r['rute_id'])
        if k not in agg:
            agg[k] = {
                'jumlah_penerbangan': 0, 'jumlah_penumpang': 0, 
                'kapasitas_seat': 0, 'jumlah_barang_kg': 0.0, 'jumlah_pos_kg': 0.0
            }
        agg[k]['jumlah_penerbangan'] += r['jumlah_penerbangan']
        agg[k]['jumlah_penumpang'] += r['jumlah_penumpang']
        agg[k]['kapasitas_seat'] += r['kapasitas_seat']
        agg[k]['jumlah_barang_kg'] += r['jumlah_barang_kg']
        agg[k]['jumlah_pos_kg'] += r['jumlah_pos_kg']
        
    final_records = []
    for k, v in sorted(agg.items()):
        lf = 0.0
        if v['kapasitas_seat'] > 0:
            lf = (v['jumlah_penumpang'] / v['kapasitas_seat']) * 100.0
            
        final_records.append({
            'waktu_id': k[0],
            'rute_id': k[1],
            'jumlah_penerbangan': v['jumlah_penerbangan'],
            'jumlah_penumpang': v['jumlah_penumpang'],
            'kapasitas_seat': v['kapasitas_seat'],
            'jumlah_barang_kg': round(v['jumlah_barang_kg'], 2),
            'jumlah_pos_kg': round(v['jumlah_pos_kg'], 2),
            'load_factor_pct': round(lf, 2)
        })
        
    out_path = OUTPUT_DIR / "fact_statistik_rute.csv"
    fieldnames = ['waktu_id', 'rute_id', 'jumlah_penerbangan', 
                  'jumlah_penumpang', 'kapasitas_seat', 'jumlah_barang_kg', 
                  'jumlah_pos_kg', 'load_factor_pct']
    with open(out_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(final_records)
        
    print(f"\n  ✅ fact_statistik_rute.csv — {len(final_records)} baris")
    print("\n✅ 07_fact_statistik_rute.py SELESAI")

if __name__ == "__main__":
    main()
