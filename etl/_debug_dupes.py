import csv
from collections import Counter

with open(r'D:\Kuliah\projek_dw\output\dim_bandara.csv', 'r', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

keys = [(r['nama_bandara'], r['kota']) for r in rows]
c = Counter(keys)
for k, cnt in c.items():
    if cnt > 1:
        print(f"DUPE ({cnt}x): nama={k[0]}, kota={k[1]}")
        for r in rows:
            if (r['nama_bandara'], r['kota']) == k:
                print(f"  id={r['bandara_id']} iata={r['kode_iata']} prov={r['provinsi']} negara={r['negara']}")
