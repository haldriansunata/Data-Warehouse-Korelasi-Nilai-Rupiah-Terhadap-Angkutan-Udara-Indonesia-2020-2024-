"""
04_dim_rute.py — Generate Dim_Rute dari BAB III + BAB VI route data
ETL Pipeline v3.2 (Clean Rewrite)

Output:
  - output/dim_rute.csv

Sumber: BAB III (rute domestik+internasional) + BAB VI (jumlah+statistik per rute)
Kolom output: rute_id, kode_rute, bandara_1_id, bandara_2_id, kategori
"""

import csv
import re
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from etl.config import (OUTPUT_DIR, BAB_III_DIR, BAB_VI_DIR,
                         TAHUN_RANGE, ensure_output_dir)
from etl.utils import extract_iata_from_route


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


def load_dim_bandara():
    """Load dim_bandara.csv dan buat lookup maps."""
    bandara_path = OUTPUT_DIR / "dim_bandara.csv"
    with open(bandara_path, 'r', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))

    # Lookup: IATA → bandara_id
    iata_to_id = {}
    for row in rows:
        if row['kode_iata']:
            iata_to_id[row['kode_iata'].upper()] = int(row['bandara_id'])

    print(f"  Loaded dim_bandara: {len(rows)} bandara, {len(iata_to_id)} with IATA")
    return iata_to_id


def find_csv_files(base_dir, keywords_include=None, keywords_exclude=None):
    """Find CSV files in year subdirectories matching keywords."""
    results = []
    for tahun in TAHUN_RANGE:
        tahun_dir = os.path.join(base_dir, str(tahun))
        if not os.path.isdir(tahun_dir):
            continue
        for f in os.listdir(tahun_dir):
            if not f.lower().endswith('.csv'):
                continue
            f_upper = f.upper()
            if keywords_include and not all(kw.upper() in f_upper for kw in keywords_include):
                continue
            if keywords_exclude and any(kw.upper() in f_upper for kw in keywords_exclude):
                continue
            results.append((tahun, os.path.join(tahun_dir, f), f))
    return results


def extract_route_iata_pair(val: str) -> tuple[str, str] | None:
    """
    Extract a sorted IATA pair from a route string.
    Returns: (IATA_1, IATA_2) sorted alphabetically, or None.
    """
    iata1, iata2, _, _ = extract_iata_from_route(val)
    if iata1 and iata2 and len(iata1) == 3 and len(iata2) == 3:
        # Sort alphabetically to normalize PP routes (CGK-DPS == DPS-CGK)
        return tuple(sorted([iata1.upper(), iata2.upper()]))
    return None


def extract_all_routes():
    """
    Scan BAB III (rute CSVs) and BAB VI (jumlah+statistik CSVs) 
    to collect all unique routes with their categori (DOMESTIK/INTERNASIONAL).
    Returns: dict {(IATA1, IATA2): kategori}
    """
    print("\n--- Extract Routes dari BAB III + BAB VI ---")

    routes = {}  # (IATA1, IATA2) → kategori

    # === BAB III: RUTE CSVs ===
    rute_dom_files = find_csv_files(BAB_III_DIR, ['RUTE', 'DALAM NEGERI'])
    rute_int_files = find_csv_files(BAB_III_DIR, ['RUTE', 'LUAR NEGERI'])

    for tahun, fp, fname in rute_dom_files:
        rows, fieldnames = read_csv_auto(fp)
        count = 0
        for row in rows:
            # BAB III format: RUTE (ASAL) + RUTE (TUJUAN) or RUTE (PP)
            if 'RUTE (PP)' in (fieldnames or []):
                val = row.get('RUTE (PP)', '').strip()
                pair = extract_route_iata_pair(val)
                if pair:
                    routes[pair] = 'DOMESTIK'
                    count += 1
            else:
                asal = row.get('RUTE (ASAL)', '').strip()
                tujuan = row.get('RUTE (TUJUAN)', '').strip()
                if asal and tujuan:
                    combined = f"{asal}-{tujuan}"
                    pair = extract_route_iata_pair(combined)
                    if pair:
                        routes[pair] = 'DOMESTIK'
                        count += 1
        print(f"  BAB III DOM {tahun}: {count} routes from {fname[:50]}")

    for tahun, fp, fname in rute_int_files:
        rows, fieldnames = read_csv_auto(fp)
        count = 0
        for row in rows:
            if 'RUTE (PP)' in (fieldnames or []):
                val = row.get('RUTE (PP)', '').strip()
                pair = extract_route_iata_pair(val)
                if pair:
                    routes[pair] = 'INTERNASIONAL'
                    count += 1
            else:
                asal = row.get('RUTE (ASAL)', '').strip()
                tujuan = row.get('RUTE (TUJUAN)', '').strip()
                if asal and tujuan:
                    combined = f"{asal}-{tujuan}"
                    pair = extract_route_iata_pair(combined)
                    if pair:
                        routes[pair] = 'INTERNASIONAL'
                        count += 1
        print(f"  BAB III INT {tahun}: {count} routes from {fname[:50]}")

    # === BAB VI: JUMLAH + STATISTIK CSVs ===
    jum_dom_files = find_csv_files(BAB_VI_DIR, ['JUMLAH', 'DALAM NEGERI'])
    jum_int_files = find_csv_files(BAB_VI_DIR, ['JUMLAH', 'LUAR NEGERI'])
    stat_dom_files = find_csv_files(BAB_VI_DIR, ['STATISTIK', 'DALAM NEGERI'])
    stat_int_files = find_csv_files(BAB_VI_DIR, ['STATISTIK', 'LUAR NEGERI'])

    def scan_route_column(files, kategori, label):
        for tahun, fp, fname in files:
            rows, fieldnames = read_csv_auto(fp)
            count = 0
            # Find route column (RUTE PP or RUTE (PP))
            rute_col = None
            for col in (fieldnames or []):
                if 'RUTE' in col.upper():
                    rute_col = col
                    break
            if not rute_col:
                continue
            for row in rows:
                val = row.get(rute_col, '').strip()
                pair = extract_route_iata_pair(val)
                if pair:
                    routes[pair] = kategori
                    count += 1
            print(f"  BAB VI {label} {tahun}: {count} routes")

    scan_route_column(jum_dom_files, 'DOMESTIK', 'JUM DOM')
    scan_route_column(jum_int_files, 'INTERNASIONAL', 'JUM INT')
    scan_route_column(stat_dom_files, 'DOMESTIK', 'STAT DOM')
    scan_route_column(stat_int_files, 'INTERNASIONAL', 'STAT INT')

    print(f"\n  Total unique routes: {len(routes)}")
    dom = sum(1 for v in routes.values() if v == 'DOMESTIK')
    intl = sum(1 for v in routes.values() if v == 'INTERNASIONAL')
    print(f"  Domestik: {dom}, Internasional: {intl}")

    return routes


def main():
    print("=" * 60)
    print("04_dim_rute.py — Generate Dimensi Rute")
    print("=" * 60)

    ensure_output_dir()

    # Load dim_bandara for FK lookup
    iata_to_id = load_dim_bandara()

    # Extract all routes
    routes = extract_all_routes()

    # Build records with FK
    records = []
    fk_miss = 0

    for (iata1, iata2), kategori in sorted(routes.items()):
        kode_rute = f"{iata1}-{iata2}"
        bandara_1_id = iata_to_id.get(iata1, '')
        bandara_2_id = iata_to_id.get(iata2, '')

        if not bandara_1_id or not bandara_2_id:
            fk_miss += 1
            missing_iatas = []
            if not bandara_1_id:
                missing_iatas.append(iata1)
            if not bandara_2_id:
                missing_iatas.append(iata2)
            # Skip routes where we can't find either airport
            # (these are likely foreign airports not in our dim)
            continue

        records.append({
            'kode_rute': kode_rute,
            'bandara_1_id': bandara_1_id,
            'bandara_2_id': bandara_2_id,
            'kategori': kategori,
        })

    print(f"\n  Routes with valid FK: {len(records)}")
    print(f"  Routes skipped (missing FK): {fk_miss}")

    # Check for duplicate kode_rute
    rute_codes = [r['kode_rute'] for r in records]
    dupes = len(rute_codes) - len(set(rute_codes))
    if dupes > 0:
        print(f"  ⚠️ {dupes} duplicate kode_rute found! Deduplicating...")
        seen = set()
        deduped = []
        for r in records:
            if r['kode_rute'] not in seen:
                seen.add(r['kode_rute'])
                deduped.append(r)
        records = deduped

    # Assign surrogate key
    for i, rec in enumerate(records, start=1):
        rec['rute_id'] = i

    # Write CSV
    out_path = OUTPUT_DIR / "dim_rute.csv"
    fieldnames = ['rute_id', 'kode_rute', 'bandara_1_id', 'bandara_2_id', 'kategori']
    with open(out_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    # Stats
    dom = sum(1 for r in records if r['kategori'] == 'DOMESTIK')
    intl = sum(1 for r in records if r['kategori'] == 'INTERNASIONAL')

    print(f"\n{'=' * 60}")
    print(f"HASIL:")
    print(f"  Total rute: {len(records)}")
    print(f"  Domestik: {dom}")
    print(f"  Internasional: {intl}")
    print(f"  Duplikat kode_rute: 0")

    # Show sample
    print(f"\n  Sample (5 pertama):")
    for rec in records[:5]:
        print(f"    {rec['rute_id']:3d} | {rec['kode_rute']:<8s} | "
              f"b1={rec['bandara_1_id']:<4d} b2={rec['bandara_2_id']:<4d} | "
              f"{rec['kategori']}")

    # Validate FK
    all_bandara_ids = set(iata_to_id.values())
    invalid_fk1 = sum(1 for r in records if int(r['bandara_1_id']) not in all_bandara_ids)
    invalid_fk2 = sum(1 for r in records if int(r['bandara_2_id']) not in all_bandara_ids)
    assert invalid_fk1 == 0, f"Invalid bandara_1_id FK: {invalid_fk1}"
    assert invalid_fk2 == 0, f"Invalid bandara_2_id FK: {invalid_fk2}"

    print(f"\n  ✅ dim_rute.csv — {len(records)} baris")
    print("\n✅ 04_dim_rute.py SELESAI")


if __name__ == "__main__":
    main()
