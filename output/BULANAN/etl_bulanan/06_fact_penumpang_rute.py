"""
06_fact_penumpang_rute.py — Fact_Penumpang_Rute bulanan (BAB VI).

Output: output/BULANAN/fact_penumpang_rute.csv
Depend: output/BULANAN/dim_rute.csv
"""
import csv
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import OUTPUT_DIR, BAB_VI_DIR, TAHUN_RANGE, ensure_dirs
from utils import parse_angka_indonesia, extract_iata_from_route


def read_csv_auto(filepath):
    for enc in ['utf-8-sig', 'utf-8', 'latin-1', 'cp1252']:
        try:
            with open(filepath, 'r', encoding=enc, newline='') as f:
                r = csv.DictReader(f)
                rows = list(r)
                return rows, r.fieldnames
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot read {filepath}")


def find_csv_files(base_dir, kw_include, kw_exclude=None):
    out = []
    for tahun in TAHUN_RANGE:
        d = os.path.join(base_dir, str(tahun))
        if not os.path.isdir(d):
            continue
        for f in os.listdir(d):
            if not f.lower().endswith('.csv'):
                continue
            U = f.upper()
            if all(k.upper() in U for k in kw_include):
                if kw_exclude and any(k.upper() in U for k in kw_exclude):
                    continue
                out.append((tahun, os.path.join(d, f), f))
    return out


def load_dim_rute():
    p = OUTPUT_DIR / "dim_rute.csv"
    m = {}
    with open(p, 'r', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            m[row['kode_rute']] = int(row['rute_id'])
    return m


def route_to_kode(val):
    a, b, _, _ = extract_iata_from_route(val)
    if a and b and len(a) == 3 and len(b) == 3:
        p = sorted([a.upper(), b.upper()])
        return f"{p[0]}-{p[1]}"
    return None


def month_from_col(col):
    cu = col.upper().strip()
    for i, p in enumerate(['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']):
        if cu.startswith(p):
            return i + 1
    for i, p in enumerate(['JAN','FEB','MAR','APR','MEI','JUN','JUL','AGU','SEP','OKT','NOV','DES']):
        if cu.startswith(p):
            return i + 1
    return None


def process_file(tahun, kategori, filepath, rute_map):
    rows, fields = read_csv_auto(filepath)
    if not fields:
        return []

    rute_col = next((c for c in fields if 'RUTE' in c.upper()), None)
    if not rute_col:
        return []

    month_cols = {c: m for c in fields if (m := month_from_col(c))}

    out = []
    for row in rows:
        v = row.get(rute_col, '').strip()
        if not v or v.upper() == 'TOTAL' or 'KARGO' in v.upper():
            continue
        kode = route_to_kode(v)
        if not kode or kode not in rute_map:
            continue
        rid = rute_map[kode]
        for col, bln in month_cols.items():
            num = parse_angka_indonesia(row.get(col))
            if num is not None and num > 0:
                out.append({
                    'waktu_id':         tahun * 100 + bln,
                    'rute_id':          rid,
                    'kategori_rute':    kategori,
                    'jumlah_penumpang': num,
                })
    return out


def main():
    print("=" * 60)
    print("06_fact_penumpang_rute.py — Fact Penumpang Rute Bulanan")
    print("=" * 60)
    ensure_dirs()
    rute_map = load_dim_rute()
    print(f"  dim_rute: {len(rute_map)} rute")

    files_dom = find_csv_files(BAB_VI_DIR, ['JUMLAH', 'DALAM NEGERI'], ['STATISTIK'])
    files_int = find_csv_files(BAB_VI_DIR, ['JUMLAH', 'LUAR NEGERI'], ['STATISTIK'])

    all_recs = []
    print("  Processing Domestik...")
    for t, fp, fn in files_dom:
        recs = process_file(t, 'DOMESTIK', fp, rute_map)
        print(f"    {t}: {len(recs)} records  ({fn[:40]})")
        all_recs.extend(recs)
    print("  Processing Internasional...")
    for t, fp, fn in files_int:
        recs = process_file(t, 'INTERNASIONAL', fp, rute_map)
        print(f"    {t}: {len(recs)} records  ({fn[:40]})")
        all_recs.extend(recs)

    # Aggregate duplikat (sum bila satu (waktu_id, rute_id) muncul dari banyak baris)
    agg = defaultdict(int)
    for r in all_recs:
        agg[(r['waktu_id'], r['rute_id'])] += r['jumlah_penumpang']

    final = [{'waktu_id': k[0], 'rute_id': k[1], 'jumlah_penumpang': v}
             for k, v in sorted(agg.items())]

    out_path = OUTPUT_DIR / "fact_penumpang_rute.csv"
    fields = ['waktu_id', 'rute_id', 'jumlah_penumpang']
    with open(out_path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(final)

    print(f"  [OK] {out_path.name} — {len(final)} baris")


if __name__ == "__main__":
    main()
