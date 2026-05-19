"""
05_fact_kurs.py — Agregasi kurs harian (BI.csv) → fact_kurs_bulanan (60 baris).

Output: _tmp/fact_kurs_bulanan.csv  (intermediate)
        Dipakai oleh build_makro_warehouse.py untuk menyusun fact_makro_bulanan.
"""
import csv
import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import KURS_CSV, TMP_DIR, TAHUN_RANGE, ensure_dirs


def main():
    print("=" * 60)
    print("05_fact_kurs.py — Fact Kurs Bulanan")
    print("=" * 60)
    ensure_dirs()

    bulanan = {}
    print(f"  Reading: {KURS_CSV.name}...")
    with open(KURS_CSV, 'r', encoding='utf-8-sig', newline='') as f:
        reader = csv.reader(f)
        # Skip 3 baris header non-standar
        for _ in range(3):
            next(reader, None)

        rows_read = 0
        rows_filtered = 0
        for row in reader:
            if not row or len(row) < 5:
                continue
            rows_read += 1
            try:
                jual = float(row[2].replace(',', '.'))
                beli = float(row[3].replace(',', '.'))
                tengah = (jual + beli) / 2.0
                tgl = datetime.datetime.strptime(row[4].strip(), "%m/%d/%Y %I:%M:%S %p")
            except ValueError:
                continue
            tahun, bulan = tgl.year, tgl.month
            if tahun not in TAHUN_RANGE:
                continue
            rows_filtered += 1
            k = (tahun, bulan)
            if k not in bulanan:
                bulanan[k] = {'sum_jual': 0.0, 'sum_beli': 0.0, 'sum_tengah': 0.0,
                              'min_tg': float('inf'), 'max_tg': float('-inf'), 'count': 0}
            bm = bulanan[k]
            bm['sum_jual']  += jual
            bm['sum_beli']  += beli
            bm['sum_tengah'] += tengah
            bm['min_tg'] = min(bm['min_tg'], tengah)
            bm['max_tg'] = max(bm['max_tg'], tengah)
            bm['count'] += 1

    print(f"  Rows read: {rows_read}  |  In range: {rows_filtered}")

    records = []
    for (t, b), m in sorted(bulanan.items()):
        c = m['count']
        if c == 0:
            continue
        records.append({
            'waktu_id':           t * 100 + b,
            'avg_kurs_jual':      round(m['sum_jual'] / c, 2),
            'avg_kurs_beli':      round(m['sum_beli'] / c, 2),
            'avg_kurs_tengah':    round(m['sum_tengah'] / c, 2),
            'min_kurs_tengah':    round(m['min_tg'], 2),
            'max_kurs_tengah':    round(m['max_tg'], 2),
            'jumlah_hari_trading': c,
        })

    out_path = TMP_DIR / "fact_kurs_bulanan.csv"
    fields = ['waktu_id', 'avg_kurs_jual', 'avg_kurs_beli', 'avg_kurs_tengah',
              'min_kurs_tengah', 'max_kurs_tengah', 'jumlah_hari_trading']
    with open(out_path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(records)

    print(f"  [OK] {out_path.name} — {len(records)} baris")


if __name__ == "__main__":
    main()
