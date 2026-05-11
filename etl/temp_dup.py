import csv
with open('output/dim_bandara.csv', 'r', encoding='utf-8') as f: rows = list(csv.DictReader(f))
no_iata = [r for r in rows if not r['kode_iata']]
has_iata = [r for r in rows if r['kode_iata']]
for n in no_iata:
    kota_n = n['kota'].upper()
    nama_n = n['nama_bandara'].upper()
    for h in has_iata:
        kota_h = h['kota'].upper() if h['kota'] else ''
        nama_h = h['nama_bandara'].upper()
        if (kota_n and kota_n in kota_h) or (kota_h and kota_h in kota_n):
            if kota_n != '':
                print(f'{nama_n} ({kota_n}) NO IATA  ----  {nama_h} ({kota_h}) HAS IATA {h[\
kode_iata\]}')
