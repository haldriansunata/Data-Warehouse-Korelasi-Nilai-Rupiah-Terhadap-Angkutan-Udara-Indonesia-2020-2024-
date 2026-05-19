"""
Bab 1 / WS2 — Kurs band: avg + min/max sebagai band per bulan.
Menunjukkan volatilitas bulanan, bukan cuma level.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _utils import monthly_pax, EVENT_DATES

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

OUT = Path(__file__).parent
df = monthly_pax()
df["spread"] = df["max_kurs_tengah"] - df["min_kurs_tengah"]

# Top 5 bulan paling volatil
top5 = df.nlargest(5, "spread")[["tanggal", "min_kurs_tengah", "max_kurs_tengah", "spread"]]
top5.to_csv(OUT / "top5_volatile_months.csv", index=False)

fig, ax = plt.subplots(figsize=(12, 5))
ax.fill_between(df["tanggal"], df["min_kurs_tengah"], df["max_kurs_tengah"],
                color="#A23B72", alpha=0.25, label="Range harian (min–max)")
ax.plot(df["tanggal"], df["avg_kurs_tengah"], color="#A23B72", lw=2, label="Rata-rata harian")
ax.set_ylabel("Kurs IDR/USD")
ax.set_title("Kurs Tengah IDR/USD — Rata-rata + Range Harian per Bulan")
ax.grid(alpha=0.3)
ax.legend(loc="upper left")

for d, lab in EVENT_DATES:
    ax.axvline(x=pd.Timestamp(d), color="grey", ls="--", alpha=0.5, lw=0.8)
    ax.annotate(lab, xy=(pd.Timestamp(d), ax.get_ylim()[1]*0.97),
                fontsize=7, rotation=90, va="top", ha="right", color="dimgray")

ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

plt.tight_layout()
plt.savefig(OUT / "plot.png", dpi=120, bbox_inches="tight")
plt.close()

print("WS2 — Kurs band")
print(f"  Spread rata-rata: {df['spread'].mean():.0f} IDR")
print(f"  Spread max: {df['spread'].max():.0f} IDR")
print(f"  5 bulan paling volatil:")
print(top5.to_string(index=False))
print(f"  Plot disimpan: {OUT/'plot.png'}")
