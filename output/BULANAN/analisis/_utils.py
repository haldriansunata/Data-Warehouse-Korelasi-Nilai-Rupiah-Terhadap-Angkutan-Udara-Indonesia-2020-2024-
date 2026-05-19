"""
Helper bersama untuk seluruh analisis bab/WS.
"""
from pathlib import Path
import pandas as pd
import numpy as np

ANALISIS_DIR = Path(__file__).resolve().parent
BULANAN_DIR  = ANALISIS_DIR.parent

PATHS = {
    "pax":     BULANAN_DIR / "fact_penumpang_rute.csv",
    "makro":   BULANAN_DIR / "fact_makro_bulanan.csv",
    "waktu":   BULANAN_DIR / "dim_waktu_bulanan.csv",
    "rute":    BULANAN_DIR / "dim_rute.csv",
    "bandara": BULANAN_DIR / "dim_bandara.csv",
}


def load_dim():
    waktu = pd.read_csv(PATHS["waktu"])
    rute  = pd.read_csv(PATHS["rute"])
    band  = pd.read_csv(PATHS["bandara"])
    makro = pd.read_csv(PATHS["makro"])
    return waktu, rute, band, makro


def load_pax():
    return pd.read_csv(PATHS["pax"])


def monthly_pax(filter_kategori=None):
    """
    Total penumpang per bulan (60 baris) + semua makro digabung.
    filter_kategori: None | 'DOMESTIK' | 'INTERNASIONAL'
    """
    pax, rute = load_pax(), pd.read_csv(PATHS["rute"])
    waktu = pd.read_csv(PATHS["waktu"])
    makro = pd.read_csv(PATHS["makro"])
    df = pax.merge(rute[["rute_id", "kategori"]], on="rute_id", how="left")
    if filter_kategori:
        df = df[df["kategori"] == filter_kategori]
    monthly = df.groupby("waktu_id", as_index=False)["jumlah_penumpang"].sum()
    monthly = monthly.merge(waktu, on="waktu_id").merge(makro, on="waktu_id")
    monthly = monthly.sort_values("waktu_id").reset_index(drop=True)
    # tanggal proper untuk plotting
    monthly["tanggal"] = pd.to_datetime(monthly["waktu_id"].astype(str), format="%Y%m")
    return monthly


def joined_full():
    """
    Grain (waktu_id, rute_id) – 17.118 baris. Semua dim + makro digabung.
    """
    pax, rute, band, makro = load_pax(), pd.read_csv(PATHS["rute"]), pd.read_csv(PATHS["bandara"]), pd.read_csv(PATHS["makro"])
    waktu = pd.read_csv(PATHS["waktu"])

    bo = band.add_prefix("o_").rename(columns={"o_bandara_id": "bandara_1_id"})
    bd = band.add_prefix("d_").rename(columns={"d_bandara_id": "bandara_2_id"})

    df = (pax
          .merge(waktu, on="waktu_id")
          .merge(makro, on="waktu_id")
          .merge(rute,  on="rute_id")
          .merge(bo,    on="bandara_1_id")
          .merge(bd,    on="bandara_2_id"))
    df["tanggal"] = pd.to_datetime(df["waktu_id"].astype(str), format="%Y%m")
    return df


def linreg_summary(x, y):
    """Linear regression sederhana: slope, intercept, r, r2, p. Pakai scipy."""
    from scipy import stats
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    mask = ~(np.isnan(x) | np.isnan(y))
    res = stats.linregress(x[mask], y[mask])
    return dict(
        slope=res.slope,
        intercept=res.intercept,
        r=res.rvalue,
        r2=res.rvalue**2,
        p=res.pvalue,
        n=int(mask.sum()),
    )


def pearson(x, y):
    """Pearson correlation."""
    from scipy import stats
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    mask = ~(np.isnan(x) | np.isnan(y))
    r, p = stats.pearsonr(x[mask], y[mask])
    return dict(r=r, r2=r**2, p=p, n=int(mask.sum()))


# Tanggal event yang dipakai untuk reference line
EVENT_DATES = [
    ("2020-03-01", "PSBB"),
    ("2021-07-01", "PPKM Darurat"),
    ("2022-02-01", "Rusia-Ukraina"),
    ("2022-05-01", "VOA dibuka"),
    ("2023-01-01", "PPKM dicabut"),
    ("2024-04-01", "Rupiah > 16K"),
]

COVID_PHASE_COLORS = {
    "pre_pandemic": "#4C72B0",
    "lockdown":     "#C44E52",
    "transisi":     "#DD8452",
    "recovery":     "#55A868",
}
