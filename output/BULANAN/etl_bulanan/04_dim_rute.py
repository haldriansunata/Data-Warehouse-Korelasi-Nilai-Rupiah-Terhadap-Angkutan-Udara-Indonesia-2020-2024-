"""
04_dim_rute.py — Dim_Rute (kategori domestik/internasional, FK ke dim_bandara).

Output: output/BULANAN/dim_rute.csv
Depend: output/BULANAN/dim_bandara.csv
"""
import csv
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import OUTPUT_DIR, BAB_III_DIR, TAHUN_RANGE, ensure_dirs


def load_dim_bandara():
    p = OUTPUT_DIR / "dim_bandara.csv"
    m = {}
    with open(p, 'r', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            m[row['iata']] = int(row['bandara_id'])
    return m


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


def extract_iatas_from_route(s):
    iatas = re.findall(r'\b[A-Z]{3}\b', s.upper())
    valid = [i for i in iatas if i not in ['DAN','KE','DARI','PER','KAB','KEC','PRO','PP','DOM','INT']]
    if len(valid) >= 2:
        return valid[0], valid[1]
    return None, None


def main():
    print("=" * 60)
    print("04_dim_rute.py — Dim Rute (IATA-based)")
    print("=" * 60)
    ensure_dirs()
    b_map = load_dim_bandara()
    print(f"  dim_bandara: {len(b_map)} IATA")

    files_dom = find_csv_files(BAB_III_DIR, ['DALAM NEGERI', 'RUTE'], ['KOTA'])
    files_int = find_csv_files(BAB_III_DIR, ['LUAR NEGERI', 'RUTE'], ['KOTA'])

    unique_routes = {}

    def process_file(filepath, kategori):
        try:
            with open(filepath, 'r', encoding='utf-8-sig') as f:
                reader = csv.reader(f)
                headers = next(reader, [])
                if len(headers) >= 3 and 'RUTE (ASAL)' in headers[1]:
                    # Format lama: NO, RUTE (ASAL), RUTE (TUJUAN)
                    for row in reader:
                        if len(row) < 3:
                            continue
                        a, _ = extract_iatas_from_route(row[1])
                        b, _ = extract_iatas_from_route(row[2])
                        if a and b:
                            pair = sorted([a, b])
                            unique_routes[f"{pair[0]}-{pair[1]}"] = kategori
                else:
                    # Format baru (2022+): NO, RUTE (ASAL - TUJUAN)
                    for row in reader:
                        if len(row) < 2:
                            continue
                        a, b = extract_iatas_from_route(row[1])
                        if a and b:
                            pair = sorted([a, b])
                            unique_routes[f"{pair[0]}-{pair[1]}"] = kategori
        except Exception as e:
            print(f"  [ERR] {filepath}: {e}")

    print("  Processing Internasional...")
    for _, fp, _ in files_int:
        process_file(fp, 'INTERNASIONAL')
    print("  Processing Domestik...")
    for _, fp, _ in files_dom:
        process_file(fp, 'DOMESTIK')

    print(f"  Total unique routes: {len(unique_routes)}")

    records = []
    rute_id = 1
    skipped = 0
    for kode, kat in sorted(unique_routes.items()):
        a, b = kode.split('-')
        if a in b_map and b in b_map:
            records.append({
                'rute_id':      rute_id,
                'kode_rute':    kode,
                'bandara_1_id': b_map[a],
                'bandara_2_id': b_map[b],
                'kategori':     kat,
            })
            rute_id += 1
        else:
            skipped += 1

    print(f"  Routes valid: {len(records)}  |  skipped (FK miss): {skipped}")

    out_path = OUTPUT_DIR / "dim_rute.csv"
    fields = ['rute_id', 'kode_rute', 'bandara_1_id', 'bandara_2_id', 'kategori']
    with open(out_path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(records)

    print(f"  [OK] {out_path.name} — {len(records)} baris")


if __name__ == "__main__":
    main()
