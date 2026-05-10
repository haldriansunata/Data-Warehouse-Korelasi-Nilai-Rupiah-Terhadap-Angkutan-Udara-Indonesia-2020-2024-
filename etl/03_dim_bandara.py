"""
03_dim_bandara.py — Generate Dim_Bandara
ETL Pipeline v3.2 (Clean Rewrite)

Output:
  - output/dim_bandara.csv

Sumber:
  - Ekstraksi IATA unik dari BAB III dan BAB VI (Data Rute).
  - Data nama, kota, provinsi diperkaya menggunakan internet/airportsdata.
Kolom output: bandara_id, nama_bandara, iata, kota, provinsi, negara
"""

import csv
import os
import sys
import re
import urllib.request
import json
import airportsdata

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from etl.config import OUTPUT_DIR, BAB_III_DIR, BAB_VI_DIR, ensure_output_dir


def extract_iata_from_datasets():
    print("  Mengumpulkan kode IATA unik dari BAB III & BAB VI...")
    iata_map = {}
    
    # Regex to capture "City Name(IATA)" or just IATAs
    # This regex looks for (XXX) where XXX is 3 uppercase letters
    regex_with_parens = re.compile(r'([A-Za-z\s\-\.]+)\(([A-Z]{3})\)')
    # Regex for just standalone IATAs
    regex_standalone = re.compile(r'\b([A-Z]{3})\b')
    
    block_list = {'DAN', 'KE', 'DARI', 'PER', 'KAB', 'KEC', 'PRO', 'PP', 
                  'JAN', 'FEB', 'MAR', 'APR', 'MEI', 'JUN', 'JUL', 'AGU', 
                  'SEP', 'OKT', 'NOV', 'DES', 'MAY', 'AUG', 'OCT', 'DEC', 
                  'DOM', 'INT', 'AIR', 'JET', 'POS', 'LTD'}

    def process_val(val):
        pairs = regex_with_parens.findall(val)
        found = False
        for city, iata in pairs:
            city = city.replace('-', '').strip()
            if iata not in block_list:
                if iata not in iata_map: iata_map[iata] = set()
                if len(city) > 2: iata_map[iata].add(city)
                found = True
        
        # If no parens found, try standalone
        if not found:
            iatas = regex_standalone.findall(val)
            for iata in iatas:
                if iata not in block_list:
                    if iata not in iata_map: iata_map[iata] = set()

    for d in [BAB_III_DIR, BAB_VI_DIR]:
        for root, dirs, files in os.walk(d):
            for f in files:
                if f.endswith('.csv'):
                    try:
                        with open(os.path.join(root, f), 'r', encoding='utf-8-sig') as file:
                            reader = csv.reader(file)
                            for row in reader:
                                for cell in row:
                                    if 'RUTE' in cell.upper() or 'TOTAL' in cell.upper() or 'KARGO' in cell.upper():
                                        continue
                                    process_val(cell)
                    except Exception:
                        pass
    
    return iata_map

# Custom overrides for specific Indonesian airports mapping that airportsdata might have slightly wrong or missing
CUSTOM_MAPPINGS = {
    'HLP': {'name': 'Halim Perdanakusuma International Airport', 'city': 'Jakarta', 'subd': 'DKI Jakarta', 'country': 'ID'},
    'KJT': {'name': 'Kertajati International Airport', 'city': 'Majalengka', 'subd': 'Jawa Barat', 'country': 'ID'},
    'YIA': {'name': 'Yogyakarta International Airport', 'city': 'Yogyakarta', 'subd': 'DI Yogyakarta', 'country': 'ID'},
    'AAP': {'name': 'Aji Pangeran Tumenggung Pranoto International Airport', 'city': 'Samarinda', 'subd': 'Kalimantan Timur', 'country': 'ID'},
    'BDO': {'name': 'Husein Sastranegara International Airport', 'city': 'Bandung', 'subd': 'Jawa Barat', 'country': 'ID'},
    'JOG': {'name': 'Adisutjipto International Airport', 'city': 'Yogyakarta', 'subd': 'DI Yogyakarta', 'country': 'ID'},
    'SRG': {'name': 'Achmad Yani International Airport', 'city': 'Semarang', 'subd': 'Jawa Tengah', 'country': 'ID'},
    'SOC': {'name': 'Adisumarmo International Airport', 'city': 'Solo', 'subd': 'Jawa Tengah', 'country': 'ID'},
    'BDJ': {'name': 'Syamsudin Noor International Airport', 'city': 'Banjarmasin', 'subd': 'Kalimantan Selatan', 'country': 'ID'},
    'PKY': {'name': 'Tjilik Riwut Airport', 'city': 'Palangkaraya', 'subd': 'Kalimantan Tengah', 'country': 'ID'},
    'TRT': {'name': 'Toraja Airport', 'city': 'Makale', 'subd': 'Sulawesi Selatan', 'country': 'ID'},
    'KRC': {'name': 'Depati Parbo Airport', 'city': 'Kerinci', 'subd': 'Jambi', 'country': 'ID'},
    'PUM': {'name': 'Sangia Nibandera Airport', 'city': 'Kolaka', 'subd': 'Sulawesi Tenggara', 'country': 'ID'},
    'KXB': {'name': 'Sangia Nibandera Airport', 'city': 'Kolaka', 'subd': 'Sulawesi Tenggara', 'country': 'ID'},
    'TFY': {'name': 'Taufiq Kiemas Airport', 'city': 'Krui', 'subd': 'Lampung', 'country': 'ID'},
    'LLJ': {'name': 'Silampari Airport', 'city': 'Lubuklinggau', 'subd': 'Sumatera Selatan', 'country': 'ID'},
    'PXA': {'name': 'Atung Bungsu Airport', 'city': 'Pagar Alam', 'subd': 'Sumatera Selatan', 'country': 'ID'},
    'PWL': {'name': 'Jenderal Besar Sudirman Airport', 'city': 'Purbalingga', 'subd': 'Jawa Tengah', 'country': 'ID'},
    'CPF': {'name': 'Ngloram Airport', 'city': 'Blora', 'subd': 'Jawa Tengah', 'country': 'ID'},
    'KWB': {'name': 'Dewadaru Airport', 'city': 'Karimunjawa', 'subd': 'Jawa Tengah', 'country': 'ID'},
    'TSY': {'name': 'Wiriadinata Airport', 'city': 'Tasikmalaya', 'subd': 'Jawa Barat', 'country': 'ID'},
    'CJN': {'name': 'Nusawiru Airport', 'city': 'Pangandaran', 'subd': 'Jawa Barat', 'country': 'ID'},
    'SQN': {'name': 'Emalamo Airport', 'city': 'Sanana', 'subd': 'Maluku Utara', 'country': 'ID'},
    'PGQ': {'name': 'Buli Airport', 'city': 'Maba', 'subd': 'Maluku Utara', 'country': 'ID'},
    'KAZ': {'name': 'Kao Airport', 'city': 'Kao', 'subd': 'Maluku Utara', 'country': 'ID'},
    'GLX': {'name': 'Gamar Malamo Airport', 'city': 'Galela', 'subd': 'Maluku Utara', 'country': 'ID'},
    'OTI': {'name': 'Leo Wattimena Airport', 'city': 'Morotai', 'subd': 'Maluku Utara', 'country': 'ID'},
    'NAM': {'name': 'Namlea Airport', 'city': 'Namlea', 'subd': 'Maluku', 'country': 'ID'},
    'NRE': {'name': 'Namrole Airport', 'city': 'Namrole', 'subd': 'Maluku', 'country': 'ID'},
    'DOB': {'name': 'Rar Gwamar Airport', 'city': 'Dobo', 'subd': 'Maluku', 'country': 'ID'},
    'LUV': {'name': 'Dumatubun Airport', 'city': 'Langgur', 'subd': 'Maluku', 'country': 'ID'},
    'SXK': {'name': 'Mathilda Batlayeri Airport', 'city': 'Saumlaki', 'subd': 'Maluku', 'country': 'ID'},
    'MNA': {'name': 'Melonguane Airport', 'city': 'Melonguane', 'subd': 'Sulawesi Utara', 'country': 'ID'},
    'NAH': {'name': 'Naha Airport', 'city': 'Tahuna', 'subd': 'Sulawesi Utara', 'country': 'ID'},
    'IAX': {'name': 'Melonguane Airport', 'city': 'Talaud', 'subd': 'Sulawesi Utara', 'country': 'ID'},
    'UOL': {'name': 'Pogogul Airport', 'city': 'Buol', 'subd': 'Sulawesi Tengah', 'country': 'ID'},
    'TLI': {'name': 'Sultan Bantilan Airport', 'city': 'Tolitoli', 'subd': 'Sulawesi Tengah', 'country': 'ID'},
    'PSJ': {'name': 'Kasiguncu Airport', 'city': 'Poso', 'subd': 'Sulawesi Tengah', 'country': 'ID'},
    'MOH': {'name': 'Maleo Airport', 'city': 'Morowali', 'subd': 'Sulawesi Tengah', 'country': 'ID'},
    'OJU': {'name': 'Tanjung Api Airport', 'city': 'Ampana', 'subd': 'Sulawesi Tengah', 'country': 'ID'},
    'LUW': {'name': 'Syukuran Aminuddin Amir Airport', 'city': 'Luwuk', 'subd': 'Sulawesi Tengah', 'country': 'ID'},
    'MJU': {'name': 'Tampa Padang Airport', 'city': 'Mamuju', 'subd': 'Sulawesi Barat', 'country': 'ID'},
    'RAQ': {'name': 'Sugimanuru Airport', 'city': 'Muna', 'subd': 'Sulawesi Tenggara', 'country': 'ID'},
    'BTW': {'name': 'Bersujud Airport', 'city': 'Batulicin', 'subd': 'Kalimantan Selatan', 'country': 'ID'},
    'SMQ': {'name': 'H. Asan Airport', 'city': 'Sampit', 'subd': 'Kalimantan Tengah', 'country': 'ID'},
    'PKN': {'name': 'Iskandar Airport', 'city': 'Pangkalan Bun', 'subd': 'Kalimantan Tengah', 'country': 'ID'},
    'KTG': {'name': 'Rahadi Oesman Airport', 'city': 'Ketapang', 'subd': 'Kalimantan Barat', 'country': 'ID'},
    'SQG': {'name': 'Tebelian Airport', 'city': 'Sintang', 'subd': 'Kalimantan Barat', 'country': 'ID'},
    'PSU': {'name': 'Pangsuma Airport', 'city': 'Putussibau', 'subd': 'Kalimantan Barat', 'country': 'ID'},
    'LNU': {'name': 'Robert Atty Bessing Airport', 'city': 'Malinau', 'subd': 'Kalimantan Utara', 'country': 'ID'},
    'NNX': {'name': 'Nunukan Airport', 'city': 'Nunukan', 'subd': 'Kalimantan Utara', 'country': 'ID'},
    'TJS': {'name': 'Tanjung Harapan Airport', 'city': 'Tanjung Selor', 'subd': 'Kalimantan Utara', 'country': 'ID'},
    'BEJ': {'name': 'Kalimarau Airport', 'city': 'Tanjung Redeb', 'subd': 'Kalimantan Timur', 'country': 'ID'},
    'GHS': {'name': 'Melalan Airport', 'city': 'Melak', 'subd': 'Kalimantan Timur', 'country': 'ID'},
    'NTI': {'name': 'Bintuni Airport', 'city': 'Bintuni', 'subd': 'Papua Barat', 'country': 'ID'},
    'BXB': {'name': 'Babo Airport', 'city': 'Babo', 'subd': 'Papua Barat', 'country': 'ID'},
    'FKQ': {'name': 'Fakfak Torea Airport', 'city': 'Fakfak', 'subd': 'Papua Barat', 'country': 'ID'},
    'KNG': {'name': 'Utarom Airport', 'city': 'Kaimana', 'subd': 'Papua Barat', 'country': 'ID'},
    'NBX': {'name': 'Douw Aturure Airport', 'city': 'Nabire', 'subd': 'Papua Tengah', 'country': 'ID'},
    'TIM': {'name': 'Mozes Kilangin Airport', 'city': 'Timika', 'subd': 'Papua Tengah', 'country': 'ID'},
    'ZRI': {'name': 'Stevanus Rumbewas Airport', 'city': 'Serui', 'subd': 'Papua', 'country': 'ID'},
    'OKL': {'name': 'Oksibil Airport', 'city': 'Oksibil', 'subd': 'Papua Pegunungan', 'country': 'ID'},
    'WMX': {'name': 'Wamena Airport', 'city': 'Wamena', 'subd': 'Papua Pegunungan', 'country': 'ID'},
    'DEX': {'name': 'Nop Goliat Dekai Airport', 'city': 'Yahukimo', 'subd': 'Papua Pegunungan', 'country': 'ID'},
    'KEI': {'name': 'Kepi Airport', 'city': 'Kepi', 'subd': 'Papua Selatan', 'country': 'ID'},
    'TMH': {'name': 'Tanah Merah Airport', 'city': 'Tanah Merah', 'subd': 'Papua Selatan', 'country': 'ID'},
    'GTO': {'name': 'Jalaluddin Airport', 'city': 'Gorontalo', 'subd': 'Gorontalo', 'country': 'ID'},
    'FLZ': {'name': 'Ferdinand Lumban Tobing Airport', 'city': 'Sibolga', 'subd': 'Sumatera Utara', 'country': 'ID'},
    'AEG': {'name': 'Aek Godang Airport', 'city': 'Padang Sidempuan', 'subd': 'Sumatera Utara', 'country': 'ID'},
    'GNS': {'name': 'Binaka Airport', 'city': 'Gunungsitoli', 'subd': 'Sumatera Utara', 'country': 'ID'},
    'SNB': {'name': 'Lasikin Airport', 'city': 'Sinabang', 'subd': 'Aceh', 'country': 'ID'},
    'MEQ': {'name': 'Cut Nyak Dhien Airport', 'city': 'Nagan Raya', 'subd': 'Aceh', 'country': 'ID'},
    'LSW': {'name': 'Malikus Saleh Airport', 'city': 'Lhokseumawe', 'subd': 'Aceh', 'country': 'ID'},
    'TXE': {'name': 'Rembele Airport', 'city': 'Takengon', 'subd': 'Aceh', 'country': 'ID'},
    'NTX': {'name': 'Ranai Airport', 'city': 'Natuna', 'subd': 'Kepulauan Riau', 'country': 'ID'},
    'MWK': {'name': 'Matak Airport', 'city': 'Anambas', 'subd': 'Kepulauan Riau', 'country': 'ID'},
    'LMU': {'name': 'Letung Airport', 'city': 'Anambas', 'subd': 'Kepulauan Riau', 'country': 'ID'},
    'SIQ': {'name': 'Dabo Airport', 'city': 'Singkep', 'subd': 'Kepulauan Riau', 'country': 'ID'},
    'TMC': {'name': 'Tambolaka Airport', 'city': 'Tambolaka', 'subd': 'Nusa Tenggara Timur', 'country': 'ID'},
    'WGP': {'name': 'Umbu Mehang Kunda Airport', 'city': 'Waingapu', 'subd': 'Nusa Tenggara Timur', 'country': 'ID'},
    'ENE': {'name': 'H. Hasan Aroeboesman Airport', 'city': 'Ende', 'subd': 'Nusa Tenggara Timur', 'country': 'ID'},
    'LWE': {'name': 'Wunopito Airport', 'city': 'Lewoleba', 'subd': 'Nusa Tenggara Timur', 'country': 'ID'},
    'LKA': {'name': 'Gewayantana Airport', 'city': 'Larantuka', 'subd': 'Nusa Tenggara Timur', 'country': 'ID'},
    'ARD': {'name': 'Mali Airport', 'city': 'Alor', 'subd': 'Nusa Tenggara Timur', 'country': 'ID'},
    'SAU': {'name': 'Tardamu Airport', 'city': 'Sabu', 'subd': 'Nusa Tenggara Timur', 'country': 'ID'},
    'RTI': {'name': 'David Constantijn Saudale Airport', 'city': 'Rote', 'subd': 'Nusa Tenggara Timur', 'country': 'ID'},
    'ABU': {'name': 'Haliwen Airport', 'city': 'Atambua', 'subd': 'Nusa Tenggara Timur', 'country': 'ID'},
    'BJW': {'name': 'Turelelo Soa Airport', 'city': 'Bajawa', 'subd': 'Nusa Tenggara Timur', 'country': 'ID'},
    'RTG': {'name': 'Frans Sales Lega Airport', 'city': 'Ruteng', 'subd': 'Nusa Tenggara Timur', 'country': 'ID'},
    'SWQ': {'name': 'Sultan Muhammad Kaharuddin III Airport', 'city': 'Sumbawa Besar', 'subd': 'Nusa Tenggara Barat', 'country': 'ID'},
    'BMU': {'name': 'Sultan Muhammad Salahudin Airport', 'city': 'Bima', 'subd': 'Nusa Tenggara Barat', 'country': 'ID'},
    'JBB': {'name': 'Notohadinegoro Airport', 'city': 'Jember', 'subd': 'Jawa Timur', 'country': 'ID'},
    'SUP': {'name': 'Trunojoyo Airport', 'city': 'Sumenep', 'subd': 'Jawa Timur', 'country': 'ID'},
    'PCB': {'name': 'Pondok Cabe Airport', 'city': 'Tangerang Selatan', 'subd': 'Banten', 'country': 'ID'},
}

def main():
    print("=" * 60)
    print("03_dim_bandara.py — Generate Dim_Bandara (IATA-Based)")
    print("=" * 60)

    ensure_output_dir()
    
    iata_map = extract_iata_from_datasets()
    print(f"  Berhasil mengekstrak {len(iata_map)} IATA unik.")

    ad_db = airportsdata.load('IATA')
    
    records = []
    bandara_id = 1
    
    # Iterate and build
    for iata in sorted(iata_map.keys()):
        # Determine best city name from datasets if available, else fallback to API
        cities = list(iata_map[iata])
        city_extracted = cities[0] if cities else ''
        
        # Override with CUSTOM_MAPPINGS or fallback to airportsdata
        if iata in CUSTOM_MAPPINGS:
            info = CUSTOM_MAPPINGS[iata]
            name = info['name']
            city = city_extracted if city_extracted else info['city']
            provinsi = info['subd']
            negara = info['country']
        elif iata in ad_db:
            info = ad_db[iata]
            name = info['name']
            city = city_extracted if city_extracted else info['city']
            provinsi = info['subd']
            negara = info['country']
        else:
            name = f"Airport {iata}"
            city = city_extracted if city_extracted else "Unknown"
            provinsi = "Unknown"
            negara = "Unknown"
            
        # Format Negara
        if negara == 'ID':
            negara = 'INDONESIA'
        elif len(negara) == 2:
            # We can leave as Country Code or map it. Let's just use the code or map common ones.
            common_countries = {
                'MY': 'MALAYSIA', 'SG': 'SINGAPURA', 'TH': 'THAILAND', 'VN': 'VIETNAM',
                'PH': 'FILIPINA', 'CN': 'CHINA', 'JP': 'JEPANG', 'KR': 'KOREA SELATAN',
                'TW': 'TAIWAN', 'HK': 'HONG KONG', 'AU': 'AUSTRALIA', 'NZ': 'SELANDIA BARU',
                'IN': 'INDIA', 'LK': 'SRI LANKA', 'AE': 'UNI EMIRAT ARAB', 'QA': 'QATAR',
                'SA': 'ARAB SAUDI', 'TR': 'TURKI', 'GB': 'INGGRIS', 'NL': 'BELANDA',
                'US': 'AMERIKA SERIKAT', 'TL': 'TIMOR LESTE', 'BN': 'BRUNEI'
            }
            negara = common_countries.get(negara, negara)

        records.append({
            'bandara_id': bandara_id,
            'nama_bandara': name.upper(),
            'iata': iata,
            'kota': city.upper(),
            'provinsi': provinsi.upper() if provinsi else "UNKNOWN",
            'negara': negara.upper()
        })
        bandara_id += 1

    out_path = OUTPUT_DIR / "dim_bandara.csv"
    fieldnames = ['bandara_id', 'nama_bandara', 'iata', 'kota', 'provinsi', 'negara']
    
    with open(out_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"  ✅ dim_bandara.csv — {len(records)} baris")
    print("\n✅ 03_dim_bandara.py SELESAI")

if __name__ == "__main__":
    main()
