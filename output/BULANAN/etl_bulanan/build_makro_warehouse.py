"""
build_makro_warehouse.py — Merge fact_kurs + makro tambahan ke fact_makro_bulanan,
                          dan enrich dim_waktu_bulanan dengan covid_phase, has_lebaran, dll.

Input (intermediate dari 01_dim_waktu + 05_fact_kurs):
  - _tmp/dim_waktu_bulanan.csv      (basic, 6 kolom)
  - _tmp/fact_kurs_bulanan.csv      (60 baris)
Input (data_tambahan):
  - BPS/BI RATE/BI_RATE_2020-2024.csv
  - BPS/Inflasi Bulanan (M-to-M) (Persen)/inflasi_indonesia_mtm_bps.csv
  - BPS/Survei Harga Konsumen ... /harga-konsumen-nasional-beberapa-barang-dan-jasa(2020-2024).csv
  - BI/Data Inflasi.xlsx
  - BRENT/Brent Oil Futures Historical Data.csv

Output:
  - output/BULANAN/fact_makro_bulanan.csv
  - output/BULANAN/dim_waktu_bulanan.csv   (versi enriched, menimpa hasil 01_dim_waktu)

Catatan: pandas to_csv dipaksa pakai lineterminator='\\n' supaya output LF
(byte-identical dengan file BULANAN lama yang dibuat di sandbox Linux).
"""
import os
import sys
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import (TMP_DIR, OUTPUT_DIR,
                    BI_RATE_CSV, INFLASI_MTM_CSV, TARIF_IHK_CSV,
                    INFLASI_YOY_XLSX, BRENT_CSV, ensure_dirs)


BULAN_FULL = {
    'Januari': 1, 'Februari': 2, 'Maret': 3, 'April': 4,
    'Mei': 5, 'Juni': 6, 'Juli': 7, 'Agustus': 8,
    'September': 9, 'Oktober': 10, 'November': 11, 'Desember': 12,
}
BULAN_SHORT = {
    'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'Mei': 5, 'Jun': 6,
    'Jul': 7, 'Ags': 8, 'Agu': 8, 'Sep': 9, 'Okt': 10, 'Nov': 11, 'Des': 12,
}

LEBARAN_MONTHS = {202005, 202105, 202205, 202304, 202404}

HARI_LIBUR = {
    202001:2,202002:0,202003:2,202004:1,202005:5,202006:1,202007:1,202008:2,202009:0,202010:1,202011:0,202012:1,
    202101:1,202102:1,202103:2,202104:1,202105:5,202106:1,202107:1,202108:2,202109:0,202110:1,202111:0,202112:1,
    202201:1,202202:1,202203:1,202204:1,202205:4,202206:1,202207:1,202208:1,202209:0,202210:1,202211:0,202212:1,
    202301:2,202302:1,202303:1,202304:3,202305:3,202306:2,202307:1,202308:1,202309:1,202310:0,202311:0,202312:1,
    202401:1,202402:2,202403:2,202404:2,202405:4,202406:2,202407:1,202408:1,202409:1,202410:0,202411:0,202412:1,
}


def melt_wide(df, year_col, value_name, month_map):
    cols = [c for c in df.columns if c in month_map]
    long = df.melt(id_vars=year_col, value_vars=cols,
                   var_name='nama_bulan', value_name=value_name)
    long['bulan']    = long['nama_bulan'].map(month_map)
    long['waktu_id'] = long[year_col].astype(int) * 100 + long['bulan']
    return long[['waktu_id', value_name]].sort_values('waktu_id').reset_index(drop=True)


def covid_phase(wid):
    if wid <= 202002: return 'pre_pandemic'
    if wid <= 202109: return 'lockdown'
    if wid <= 202212: return 'transisi'
    return 'recovery'


def main():
    print("=" * 60)
    print("build_makro_warehouse.py — Fact Makro + Enrich Dim Waktu")
    print("=" * 60)
    ensure_dirs()

    dim_waktu = pd.read_csv(TMP_DIR / 'dim_waktu_bulanan.csv')
    fact_kurs = pd.read_csv(TMP_DIR / 'fact_kurs_bulanan.csv')

    bi       = pd.read_csv(BI_RATE_CSV)
    bi_long  = melt_wide(bi, 'Tahun', 'bi_rate', BULAN_FULL)

    mtm      = pd.read_csv(INFLASI_MTM_CSV)
    mtm_long = melt_wide(mtm, 'Tahun', 'inflasi_mtm', BULAN_SHORT)

    tarif    = pd.read_csv(TARIF_IHK_CSV)
    tarif_long = melt_wide(
        tarif[['Tahun/Year'] + [c for c in tarif.columns if c in BULAN_SHORT]],
        'Tahun/Year', 'tarif_tiket_ihk', BULAN_SHORT,
    )

    yoy_raw = pd.read_excel(
        INFLASI_YOY_XLSX, sheet_name=0, skiprows=5, header=None,
        names=['No', 'Periode', 'inflasi_str', '_extra'],
    ).dropna(subset=['Periode', 'inflasi_str'])

    def parse_periode(s):
        parts = str(s).strip().split()
        if len(parts) != 2 or parts[0] not in BULAN_FULL:
            return None
        return int(parts[1]) * 100 + BULAN_FULL[parts[0]]
    yoy_raw['waktu_id']    = yoy_raw['Periode'].apply(parse_periode)
    yoy_raw['inflasi_yoy'] = (yoy_raw['inflasi_str'].astype(str)
                              .str.replace('%', '', regex=False).str.strip().astype(float))
    yoy_long = (yoy_raw.dropna(subset=['waktu_id'])
                       .assign(waktu_id=lambda d: d['waktu_id'].astype(int))
                       [['waktu_id', 'inflasi_yoy']]
                       .sort_values('waktu_id').reset_index(drop=True))

    brent = pd.read_csv(BRENT_CSV, encoding='utf-8-sig')
    brent['Date']     = pd.to_datetime(brent['Date'], format='%m/%d/%Y')
    brent['waktu_id'] = brent['Date'].dt.year * 100 + brent['Date'].dt.month
    brent_long = (brent[['waktu_id', 'Price', 'High', 'Low']]
                  .rename(columns={'Price': 'brent_usd_bbl',
                                   'High':  'brent_high',
                                   'Low':   'brent_low'})
                  .sort_values('waktu_id').reset_index(drop=True))

    fact_makro = (fact_kurs
                  .merge(tarif_long, on='waktu_id', how='left')
                  .merge(yoy_long,   on='waktu_id', how='left')
                  .merge(mtm_long,   on='waktu_id', how='left')
                  .merge(bi_long,    on='waktu_id', how='left')
                  .merge(brent_long, on='waktu_id', how='left'))
    fact_makro = fact_makro[[
        'waktu_id',
        'avg_kurs_jual', 'avg_kurs_beli', 'avg_kurs_tengah',
        'min_kurs_tengah', 'max_kurs_tengah', 'jumlah_hari_trading',
        'tarif_tiket_ihk', 'inflasi_yoy', 'inflasi_mtm', 'bi_rate',
        'brent_usd_bbl', 'brent_high', 'brent_low',
    ]]
    out_makro = OUTPUT_DIR / 'fact_makro_bulanan.csv'
    fact_makro.to_csv(out_makro, index=False, lineterminator='\n')
    print(f"  [OK] {out_makro.name} — {len(fact_makro)} baris")

    dim_waktu['covid_phase']       = dim_waktu['waktu_id'].apply(covid_phase)
    dim_waktu['has_lebaran']       = dim_waktu['waktu_id'].isin(LEBARAN_MONTHS).astype(int)
    dim_waktu['has_natal']         = (dim_waktu['bulan'] == 12).astype(int)
    dim_waktu['is_peak_season']    = (dim_waktu['has_lebaran'].eq(1)
                                      | dim_waktu['bulan'].isin([6, 7, 12])).astype(int)
    dim_waktu['jumlah_hari_libur'] = dim_waktu['waktu_id'].map(HARI_LIBUR)

    out_waktu = OUTPUT_DIR / 'dim_waktu_bulanan.csv'
    dim_waktu.to_csv(out_waktu, index=False, lineterminator='\n')
    print(f"  [OK] {out_waktu.name} — {len(dim_waktu)} baris (enriched)")


if __name__ == "__main__":
    main()
