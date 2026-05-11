import csv
import os

OUTPUT_DIR = r'd:\Kuliah\projek_dw\output'

def load_csv(filename, key_col):
    data = {}
    with open(os.path.join(OUTPUT_DIR, filename), 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data[row[key_col]] = row
    return data

def load_csv_list(filename):
    data = []
    with open(os.path.join(OUTPUT_DIR, filename), 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data

# Load all
dim_waktu = load_csv('dim_waktu_bulanan.csv', 'waktu_id')
dim_bandara = load_csv('dim_bandara.csv', 'bandara_id')
dim_rute = load_csv('dim_rute.csv', 'rute_id')
fact_kurs = load_csv('fact_kurs_bulanan.csv', 'waktu_id')
fact_penumpang = load_csv_list('fact_penumpang_rute.csv')

# Look for CGK-DPS in Jan 2023
target_waktu = '202301'
target_rute_kode = 'CGK-DPS'

# Find rute_id for CGK-DPS
target_rute_id = None
for r_id, r_data in dim_rute.items():
    if r_data['kode_rute'] == target_rute_kode:
        target_rute_id = r_id
        break

print(f"1. Pencarian Rute '{target_rute_kode}' -> rute_id: {target_rute_id}")

# Join for the specific fact
found_fact = None
for fact in fact_penumpang:
    if fact['waktu_id'] == target_waktu and fact['rute_id'] == target_rute_id:
        found_fact = fact
        break

print(f"2. Pencarian Fakta (Waktu={target_waktu}, Rute={target_rute_id}) -> {found_fact}")

if found_fact:
    waktu_info = dim_waktu[found_fact['waktu_id']]
    rute_info = dim_rute[found_fact['rute_id']]
    bandara1_info = dim_bandara[rute_info['bandara_1_id']]
    bandara2_info = dim_bandara[rute_info['bandara_2_id']]
    kurs_info = fact_kurs.get(found_fact['waktu_id'], {})

    print("\n--- HASIL MERGING (SKEMA BINTANG) ---")
    print(f"Bulan-Tahun   : {waktu_info['nama_bulan']} {waktu_info['tahun']}")
    print(f"Rute (IATA)   : {rute_info['kode_rute']} ({rute_info['kategori']})")
    print(f"Bandara 1     : {bandara1_info['nama_bandara']} ({bandara1_info['kota']})")
    print(f"Bandara 2     : {bandara2_info['nama_bandara']} ({bandara2_info['kota']})")
    print(f"Jumlah Pnp    : {found_fact['jumlah_penumpang']} orang")
    print(f"Kurs Tengah   : Rp {float(kurs_info.get('avg_kurs_tengah', 0)):,.2f}")
