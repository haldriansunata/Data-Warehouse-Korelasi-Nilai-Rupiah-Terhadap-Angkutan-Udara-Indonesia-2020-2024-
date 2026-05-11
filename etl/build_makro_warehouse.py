"""
build_makro_warehouse.py
========================

Membangun dua file untuk data warehouse "korelasi rupiah vs angkutan udara":

  1. fact_makro_bulanan.csv     — gabungan kurs + tarif tiket + inflasi YoY/MtM
                                  + BI rate + harga Brent (per bulan, nasional)
  2. dim_waktu_bulanan.csv      — dim waktu lama + atribut baru:
                                  covid_phase, has_lebaran, has_natal,
                                  is_peak_season, jumlah_hari_libur

INPUT (taruh semua di folder UPLOADS):
  - dim_waktu_bulanan.csv
  - fact_kurs_bulanan.csv
  - BI_RATE_2020-2024.csv
  - inflasi_indonesia_mtm_bps.csv
  - harga-konsumen-nasional-beberapa-barang-dan-jasa_2020-2024_.csv
  - Data_Inflasi.xlsx
  - Brent_Oil_Futures_Historical_Data.csv

OUTPUT: ditulis ke folder OUTPUTS.

Cara pakai:
    python build_makro_warehouse.py
atau atur path di bagian KONFIGURASI di bawah.
"""
from pathlib import Path
import pandas as pd

# ==========================================================
# KONFIGURASI — ganti dua path ini sesuai lokasi file kamu
# ==========================================================
UPLOADS = Path('/mnt/user-data/uploads')
OUTPUTS = Path('/mnt/user-data/outputs')
OUTPUTS.mkdir(parents=True, exist_ok=True)

# ==========================================================
# MAPPING BULAN
# ==========================================================
BULAN_FULL = {
    'Januari': 1, 'Februari': 2, 'Maret': 3, 'April': 4,
    'Mei': 5, 'Juni': 6, 'Juli': 7, 'Agustus': 8,
    'September': 9, 'Oktober': 10, 'November': 11, 'Desember': 12,
}
BULAN_SHORT = {
    'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'Mei': 5, 'Jun': 6,
    'Jul': 7, 'Ags': 8, 'Agu': 8, 'Sep': 9, 'Okt': 10, 'Nov': 11, 'Des': 12,
}

def melt_wide_year_month(df, year_col, value_name, month_map):
    """Wide (year × month) → long dengan waktu_id."""
    month_cols = [c for c in df.columns if c in month_map]
    long = df.melt(id_vars=year_col, value_vars=month_cols,
                   var_name='nama_bulan', value_name=value_name)
    long['bulan'] = long['nama_bulan'].map(month_map)
    long['waktu_id'] = long[year_col].astype(int) * 100 + long['bulan']
    return long[['waktu_id', value_name]].sort_values('waktu_id').reset_index(drop=True)


# ==========================================================
# 1. LOAD TABEL YANG SUDAH ADA
# ==========================================================
dim_waktu = pd.read_csv(UPLOADS / 'dim_waktu_bulanan.csv')
fact_kurs = pd.read_csv(UPLOADS / 'fact_kurs_bulanan.csv')

# ==========================================================
# 2. BI RATE (wide: Tahun × Januari..Desember)
# ==========================================================
bi = pd.read_csv(UPLOADS / 'BI_RATE_2020-2024.csv')
bi_long = melt_wide_year_month(bi, year_col='Tahun', value_name='bi_rate',
                               month_map=BULAN_FULL)

# ==========================================================
# 3. INFLASI MoM (BPS) — wide: Tahun × Jan..Des
# ==========================================================
mtm = pd.read_csv(UPLOADS / 'inflasi_indonesia_mtm_bps.csv')
mtm_long = melt_wide_year_month(mtm, year_col='Tahun', value_name='inflasi_mtm',
                                month_map=BULAN_SHORT)

# ==========================================================
# 4. TARIF TIKET IHK (BPS) — wide: Tahun/Year × Jan..Des
# ==========================================================
tarif = pd.read_csv(UPLOADS / 'harga-konsumen-nasional-beberapa-barang-dan-jasa_2020-2024_.csv')
tarif_long = melt_wide_year_month(
    tarif[['Tahun/Year'] + [c for c in tarif.columns if c in BULAN_SHORT]],
    year_col='Tahun/Year', value_name='tarif_tiket_ihk',
    month_map=BULAN_SHORT,
)

# ==========================================================
# 5. INFLASI YoY (BI) — xlsx long format dgn "Periode" = "Desember 2024"
# ==========================================================
yoy_raw = pd.read_excel(
    UPLOADS / 'Data_Inflasi.xlsx', sheet_name=0,
    skiprows=5, header=None,
    names=['No', 'Periode', 'inflasi_str', '_extra'],
)
yoy_raw = yoy_raw.dropna(subset=['Periode', 'inflasi_str'])

def parse_periode(s):
    parts = str(s).strip().split()
    if len(parts) != 2 or parts[0] not in BULAN_FULL:
        return None
    return int(parts[1]) * 100 + BULAN_FULL[parts[0]]

yoy_raw['waktu_id'] = yoy_raw['Periode'].apply(parse_periode)
yoy_raw['inflasi_yoy'] = (
    yoy_raw['inflasi_str'].astype(str).str.replace('%', '', regex=False).str.strip().astype(float)
)
yoy_long = (yoy_raw.dropna(subset=['waktu_id'])
                   .assign(waktu_id=lambda d: d['waktu_id'].astype(int))
                   [['waktu_id', 'inflasi_yoy']]
                   .sort_values('waktu_id').reset_index(drop=True))

# ==========================================================
# 6. BRENT OIL — bulanan, format MM/DD/YYYY, Price = close bulanan
# ==========================================================
brent = pd.read_csv(UPLOADS / 'Brent_Oil_Futures_Historical_Data.csv',
                    encoding='utf-8-sig')
brent['Date'] = pd.to_datetime(brent['Date'], format='%m/%d/%Y')
brent['waktu_id'] = brent['Date'].dt.year * 100 + brent['Date'].dt.month
brent_long = (brent[['waktu_id', 'Price', 'High', 'Low']]
              .rename(columns={'Price': 'brent_usd_bbl',
                               'High':  'brent_high',
                               'Low':   'brent_low'})
              .sort_values('waktu_id').reset_index(drop=True))

# ==========================================================
# 7. MERGE → fact_makro_bulanan
# ==========================================================
fact_makro = (fact_kurs
              .merge(tarif_long, on='waktu_id', how='left')
              .merge(yoy_long,   on='waktu_id', how='left')
              .merge(mtm_long,   on='waktu_id', how='left')
              .merge(bi_long,    on='waktu_id', how='left')
              .merge(brent_long, on='waktu_id', how='left'))

# Urutkan kolom yang rapi
fact_makro = fact_makro[[
    'waktu_id',
    # kurs
    'avg_kurs_jual', 'avg_kurs_beli', 'avg_kurs_tengah',
    'min_kurs_tengah', 'max_kurs_tengah', 'jumlah_hari_trading',
    # makro tambahan
    'tarif_tiket_ihk', 'inflasi_yoy', 'inflasi_mtm', 'bi_rate',
    # energi
    'brent_usd_bbl', 'brent_high', 'brent_low',
]]

fact_makro.to_csv(OUTPUTS / 'fact_makro_bulanan.csv', index=False)

# ==========================================================
# 8. ENRICH dim_waktu_bulanan
# ==========================================================

# COVID phase — patokan kebijakan PSBB/PPKM
def covid_phase(wid):
    if wid <= 202002: return 'pre_pandemic'   # sebelum kasus pertama di Indonesia (2 Mar 2020)
    if wid <= 202109: return 'lockdown'       # PSBB → puncak Delta wave (PPKM Darurat Jul-Sep 2021)
    if wid <= 202212: return 'transisi'       # PPKM level menurun, VOA dibuka bertahap
    return 'recovery'                          # PPKM dicabut 30 Des 2022 → normalisasi

# Bulan yang berisi hari raya Idul Fitri (Lebaran) di Indonesia
LEBARAN_MONTHS = {
    202005,  # 24-25 Mei 2020
    202105,  # 13-14 Mei 2021
    202205,  # 2-3  Mei 2022
    202304,  # 22-23 April 2023
    202404,  # 10-11 April 2024
}

# Approx jumlah hari libur nasional per bulan
# (libur nasional resmi, tidak termasuk cuti bersama yang lebih variabel)
HARI_LIBUR = {
    # 2020
    202001: 2, 202002: 0, 202003: 2, 202004: 1, 202005: 5, 202006: 1,
    202007: 1, 202008: 2, 202009: 0, 202010: 1, 202011: 0, 202012: 1,
    # 2021
    202101: 1, 202102: 1, 202103: 2, 202104: 1, 202105: 5, 202106: 1,
    202107: 1, 202108: 2, 202109: 0, 202110: 1, 202111: 0, 202112: 1,
    # 2022
    202201: 1, 202202: 1, 202203: 1, 202204: 1, 202205: 4, 202206: 1,
    202207: 1, 202208: 1, 202209: 0, 202210: 1, 202211: 0, 202212: 1,
    # 2023
    202301: 2, 202302: 1, 202303: 1, 202304: 3, 202305: 3, 202306: 2,
    202307: 1, 202308: 1, 202309: 1, 202310: 0, 202311: 0, 202312: 1,
    # 2024
    202401: 1, 202402: 2, 202403: 2, 202404: 2, 202405: 4, 202406: 2,
    202407: 1, 202408: 1, 202409: 1, 202410: 0, 202411: 0, 202412: 1,
}

dim_waktu['covid_phase']      = dim_waktu['waktu_id'].apply(covid_phase)
dim_waktu['has_lebaran']      = dim_waktu['waktu_id'].isin(LEBARAN_MONTHS).astype(int)
dim_waktu['has_natal']        = (dim_waktu['bulan'] == 12).astype(int)
dim_waktu['is_peak_season']   = (
    dim_waktu['has_lebaran'].eq(1) |
    dim_waktu['bulan'].isin([6, 7, 12])  # libur sekolah Jun-Jul + Des Natal/TBN
).astype(int)
dim_waktu['jumlah_hari_libur'] = dim_waktu['waktu_id'].map(HARI_LIBUR)

dim_waktu.to_csv(OUTPUTS / 'dim_waktu_bulanan.csv', index=False)

# ==========================================================
# REPORT
# ==========================================================
print('=== fact_makro_bulanan.csv ===')
print(f'rows  : {len(fact_makro)}')
print(f'cols  : {list(fact_makro.columns)}')
print(f'NA/col:\n{fact_makro.isna().sum().to_string()}')
print()
print('=== dim_waktu_bulanan.csv ===')
print(f'rows  : {len(dim_waktu)}')
print(f'cols  : {list(dim_waktu.columns)}')
print(f'covid_phase distribution:\n{dim_waktu["covid_phase"].value_counts().to_string()}')
print()
print('Output:')
for p in sorted(OUTPUTS.iterdir()):
    print(f'  {p.name}  ({p.stat().st_size:,} bytes)')
