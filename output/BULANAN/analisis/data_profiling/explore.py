"""
Data profiling: profil tiap kolom (range, statistik, sampel).
Output: profil_raw_stats.txt (dipakai sebagai bahan baku data_profiling.md).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _utils import load_dim, load_pax, joined_full, monthly_pax  # noqa

import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)
pd.set_option("display.float_format", "{:,.4f}".format)

waktu, rute, band, makro = load_dim()
pax = load_pax()

OUT = Path(__file__).parent / "profil_raw_stats.txt"
with open(OUT, "w", encoding="utf-8") as f:
    def w(s=""):
        print(s)
        f.write(str(s) + "\n")

    w("=" * 78)
    w("PROFIL DATA BULANAN")
    w("=" * 78)

    for name, df in [("dim_waktu_bulanan", waktu),
                     ("dim_rute", rute),
                     ("dim_bandara", band),
                     ("fact_makro_bulanan", makro),
                     ("fact_penumpang_rute", pax)]:
        w(f"\n### {name}  ({len(df):,} baris, {len(df.columns)} kolom)")
        w(f"Kolom: {list(df.columns)}")
        w(f"\nDtype:\n{df.dtypes.to_string()}")
        w(f"\nDescribe (numeric):\n{df.describe(include='number').to_string()}")
        if df.select_dtypes(include='object').shape[1] > 0:
            w(f"\nObject kolom — sample unique:")
            for c in df.select_dtypes(include='object').columns:
                u = df[c].unique()
                w(f"  {c}: nunique={len(u)}, sample={list(u[:6])}")
        w(f"\nKepala (5 baris):\n{df.head(5).to_string(index=False)}")
        w("-" * 78)

    # cek satuan Brent
    w("\n### Cek satuan Brent (apakah USD/bbl atau IDR/bbl?)")
    s = makro["brent_usd_bbl"].describe()
    w(f"Brent range: min={s['min']:.2f}, mean={s['mean']:.2f}, max={s['max']:.2f}")
    w("Catatan: Brent historis biasanya 20-130 USD/bbl. Kalau IDR/bbl harusnya 6-digit (jutaan).")
    w(f"-> Brent di data ini jelas USD/bbl, BUKAN IDR.")

    # cek satuan kurs
    w("\n### Cek satuan kurs")
    s = makro["avg_kurs_tengah"].describe()
    w(f"avg_kurs_tengah range: min={s['min']:.2f}, max={s['max']:.2f}")
    w("-> 5 digit, jelas IDR per 1 USD.")

    # cek satuan tarif_tiket_ihk
    w("\n### Cek satuan tarif_tiket_ihk")
    s = makro["tarif_tiket_ihk"].describe()
    w(f"tarif_tiket_ihk range: min={s['min']:.2f}, max={s['max']:.2f}")
    w("-> Ini adalah INDEKS Harga Konsumen tarif tiket pesawat (BPS, base = 100 di tahun referensi).")
    w("   Angka 1000-1500 menunjukkan harga tiket relatif terhadap base year.")

    # cek bi_rate
    w("\n### Cek satuan bi_rate")
    s = makro["bi_rate"].describe()
    w(f"bi_rate range: min={s['min']:.2f}, max={s['max']:.2f}")
    w("-> Persen (%). 3.5% = 3.5, bukan 0.035.")

    # cek inflasi
    w("\n### Cek satuan inflasi_yoy, inflasi_mtm")
    for col in ["inflasi_yoy", "inflasi_mtm"]:
        s = makro[col].describe()
        w(f"{col}: min={s['min']:.2f}, max={s['max']:.2f}")
    w("-> Persen (%). inflasi_yoy = inflasi tahunan, inflasi_mtm = month-to-month.")

    # cek jumlah_penumpang
    w("\n### Cek satuan jumlah_penumpang")
    s = pax["jumlah_penumpang"].describe()
    w(f"jumlah_penumpang per (waktu_id, rute_id): min={s['min']:.0f}, max={s['max']:,.0f}")
    monthly_total = pax.groupby("waktu_id")["jumlah_penumpang"].sum()
    w(f"Total penumpang per bulan (sum across all routes): min={monthly_total.min():,.0f}, max={monthly_total.max():,.0f}")
    w("-> Satuan: orang.")

print(f"\nProfil disimpan ke: {OUT}")
