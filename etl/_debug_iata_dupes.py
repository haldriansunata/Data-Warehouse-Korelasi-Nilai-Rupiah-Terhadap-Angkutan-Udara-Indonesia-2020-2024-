import csv
from collections import Counter

with open(r'D:\Kuliah\projek_dw\output\dim_bandara.csv', 'r', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

iatas = [r['kode_iata'] for r in rows if r['kode_iata']]
c = Counter(iatas)
for k, v in c.items():
    if v > 1:
        print(f"DUP IATA: {k}")
        for r in rows:
            if r['kode_iata'] == k:
                print(f"  id={r['bandara_id']} nama={r['nama_bandara']} kota={r['kota']} prov={r['provinsi']} negara={r['negara']}")
