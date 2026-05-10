"""
04_dim_rute.py — Generate Dim_Rute
ETL Pipeline v3.2 (Clean Rewrite)

Output:
  - output/dim_rute.csv

Sumber: BAB III (Rute & Bandara)
Kolom output: rute_id, kode_rute, bandara_1_id, bandara_2_id, kategori
"""

import csv
import os
import sys
import re

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from etl.config import OUTPUT_DIR, BAB_III_DIR, TAHUN_RANGE, ensure_output_dir


def load_dim_bandara():
    bandara_path = OUTPUT_DIR / "dim_bandara.csv"
    b_map = {}
    with open(bandara_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            b_map[row['iata']] = int(row['bandara_id'])
    return b_map


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

def extract_iatas_from_route(route_str):
    # This regex looks for 3 uppercase letters
    iatas = re.findall(r'\b[A-Z]{3}\b', route_str.upper())
    
    # filter out bad words
    valid_iatas = [i for i in iatas if i not in ['DAN', 'KE', 'DARI', 'PER', 'KAB', 'KEC', 'PRO', 'PP', 'DOM', 'INT']]
    
    if len(valid_iatas) >= 2:
        return valid_iatas[0], valid_iatas[1]
    return None, None


def main():
    print("=" * 60)
    print("04_dim_rute.py — Generate Dim Rute (IATA-Based)")
    print("=" * 60)

    ensure_output_dir()
    b_map = load_dim_bandara()
    print(f"  Loaded dim_bandara: {len(b_map)} IATAs")

    files_dom = find_csv_files(BAB_III_DIR, ['DALAM NEGERI', 'RUTE'], ['KOTA'])
    files_int = find_csv_files(BAB_III_DIR, ['LUAR NEGERI', 'RUTE'], ['KOTA'])

    unique_routes = {}

    def process_file(filepath, kategori):
        try:
            with open(filepath, 'r', encoding='utf-8-sig') as f:
                reader = csv.reader(f)
                headers = next(reader, [])
                
                # Cek tipe format
                if len(headers) >= 3 and 'RUTE (ASAL)' in headers[1]:
                    # Format lama: NO, RUTE (ASAL), RUTE (TUJUAN)
                    for row in reader:
                        if len(row) < 3: continue
                        iata1, _ = extract_iatas_from_route(row[1])
                        iata2, _ = extract_iatas_from_route(row[2])
                        if iata1 and iata2:
                            pair = sorted([iata1, iata2])
                            kode_rute = f"{pair[0]}-{pair[1]}"
                            unique_routes[kode_rute] = kategori
                else:
                    # Format baru (2022+): NO, RUTE (ASAL - TUJUAN)
                    for row in reader:
                        if len(row) < 2: continue
                        iata1, iata2 = extract_iatas_from_route(row[1])
                        if iata1 and iata2:
                            pair = sorted([iata1, iata2])
                            kode_rute = f"{pair[0]}-{pair[1]}"
                            unique_routes[kode_rute] = kategori
        except Exception as e:
            print(f"    ❌ Error reading {filepath}: {e}")

    print("\n  Processing International...")
    for t, fp, fn in files_int:
        process_file(fp, 'INTERNASIONAL')

    print("\n  Processing Domestic...")
    for t, fp, fn in files_dom:
        process_file(fp, 'DOMESTIK')
        
    print(f"\n  Total unique routes: {len(unique_routes)}")
    
    records = []
    rute_id = 1
    skipped = 0
    
    for kode_rute, kategori in sorted(unique_routes.items()):
        iata1, iata2 = kode_rute.split('-')
        if iata1 in b_map and iata2 in b_map:
            records.append({
                'rute_id': rute_id,
                'kode_rute': kode_rute,
                'bandara_1_id': b_map[iata1],
                'bandara_2_id': b_map[iata2],
                'kategori': kategori
            })
            rute_id += 1
        else:
            skipped += 1
            if iata1 not in b_map: print(f"    ⚠️ Missing IATA in dim_bandara: {iata1}")
            if iata2 not in b_map: print(f"    ⚠️ Missing IATA in dim_bandara: {iata2}")

    print(f"\n  Routes with valid FK: {len(records)}")
    print(f"  Routes skipped (missing FK): {skipped}")

    out_path = OUTPUT_DIR / "dim_rute.csv"
    fieldnames = ['rute_id', 'kode_rute', 'bandara_1_id', 'bandara_2_id', 'kategori']
    with open(out_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"  ✅ dim_rute.csv — {len(records)} baris")
    print("\n✅ 04_dim_rute.py SELESAI")

if __name__ == "__main__":
    main()
