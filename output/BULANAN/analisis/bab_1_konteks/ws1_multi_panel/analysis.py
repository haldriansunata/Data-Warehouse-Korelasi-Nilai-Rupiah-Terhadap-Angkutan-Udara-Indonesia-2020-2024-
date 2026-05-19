"""
Bab 1 / WS1 — Multi-panel time series: Penumpang, Kurs, Brent, BI Rate (60 bulan).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _utils import monthly_pax, EVENT_DATES

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

OUT = Path(__file__).parent
df = monthly_pax()  # 60 baris

# Save data tabel
df[["waktu_id", "tanggal", "jumlah_penumpang",
    "avg_kurs_tengah", "brent_usd_bbl", "bi_rate"]].to_csv(
    OUT / "data_4panel.csv", index=False)

fig, axes = plt.subplots(4, 1, figsize=(12, 10), sharex=True)

# Panel 1: Penumpang
axes[0].plot(df["tanggal"], df["jumlah_penumpang"] / 1e6, color="#2E86AB", lw=1.8)
axes[0].set_ylabel("Penumpang (juta)")
axes[0].set_title("Total Penumpang Nasional per Bulan")
axes[0].grid(alpha=0.3)

# Panel 2: Kurs
axes[1].plot(df["tanggal"], df["avg_kurs_tengah"], color="#A23B72", lw=1.8)
axes[1].set_ylabel("Kurs IDR/USD")
axes[1].set_title("Kurs Tengah IDR/USD")
axes[1].grid(alpha=0.3)

# Panel 3: Brent
axes[2].plot(df["tanggal"], df["brent_usd_bbl"], color="#F18F01", lw=1.8)
axes[2].set_ylabel("USD per barrel")
axes[2].set_title("Brent Crude (USD/bbl)")
axes[2].grid(alpha=0.3)

# Panel 4: BI Rate
axes[3].plot(df["tanggal"], df["bi_rate"], color="#3E7B27", lw=1.8)
axes[3].set_ylabel("% per tahun")
axes[3].set_title("BI Rate")
axes[3].grid(alpha=0.3)

# Reference lines untuk events
for ax in axes:
    for d, lab in EVENT_DATES:
        ax.axvline(x=pd.Timestamp(d), color="grey", ls="--", alpha=0.5, lw=0.8)

# Annotate events di panel atas
for d, lab in EVENT_DATES:
    axes[0].annotate(lab, xy=(pd.Timestamp(d), axes[0].get_ylim()[1]*0.95),
                     fontsize=7, rotation=90, va="top", ha="right",
                     color="dimgray")

axes[-1].xaxis.set_major_locator(mdates.YearLocator())
axes[-1].xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
axes[-1].set_xlabel("Tanggal")

plt.tight_layout()
plt.savefig(OUT / "plot.png", dpi=120, bbox_inches="tight")
plt.close()

# Print ringkasan
print("WS1 — Multi-panel time series")
print(f"  Penumpang min={df['jumlah_penumpang'].min():,.0f} (Apr 2020 = COVID dip)")
print(f"  Penumpang max={df['jumlah_penumpang'].max():,.0f}")
print(f"  Kurs min={df['avg_kurs_tengah'].min():,.0f}, max={df['avg_kurs_tengah'].max():,.0f}")
print(f"  Brent min={df['brent_usd_bbl'].min():.2f}, max={df['brent_usd_bbl'].max():.2f}")
print(f"  BI rate min={df['bi_rate'].min():.2f}%, max={df['bi_rate'].max():.2f}%")
print(f"  Plot disimpan: {OUT/'plot.png'}")
