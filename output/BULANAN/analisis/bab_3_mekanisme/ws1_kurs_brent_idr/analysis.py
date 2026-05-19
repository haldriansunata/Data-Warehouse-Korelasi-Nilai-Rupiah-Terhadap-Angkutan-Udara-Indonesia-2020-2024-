"""
Bab 3 / WS1 — Kurs × Brent_IDR_per_bbl (double shock).
Channel 1 Step A.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _utils import monthly_pax, linreg_summary, COVID_PHASE_COLORS

import numpy as np
import matplotlib.pyplot as plt

OUT = Path(__file__).parent
df = monthly_pax()
df["brent_idr_per_bbl"] = df["brent_usd_bbl"] * df["avg_kurs_tengah"]

x = df["avg_kurs_tengah"].values
y = df["brent_idr_per_bbl"].values
res = linreg_summary(x, y)

with open(OUT / "metrics.txt", "w", encoding="utf-8") as f:
    f.write("Bab 3 / WS1 — Kurs × Brent (in IDR)\n")
    f.write(f"slope = {res['slope']:,.2f} (IDR/bbl per 1 IDR kurs)\n")
    f.write(f"R² = {res['r2']:.4f}\n")
    f.write(f"p-value = {res['p']:.6f}\n")
    f.write(f"\nBrent IDR range: {df['brent_idr_per_bbl'].min():,.0f} - {df['brent_idr_per_bbl'].max():,.0f}\n")

fig, ax = plt.subplots(figsize=(9, 6))
for phase, color in COVID_PHASE_COLORS.items():
    sub = df[df["covid_phase"] == phase]
    ax.scatter(sub["avg_kurs_tengah"], sub["brent_idr_per_bbl"]/1e3,
               s=70, alpha=0.75, color=color, label=phase, edgecolor="white", lw=0.8)
xline = np.linspace(x.min(), x.max(), 100)
ax.plot(xline, (res["intercept"] + res["slope"]*xline)/1e3, "k--", lw=1.5, alpha=0.7)

ax.set_xlabel("Kurs IDR/USD")
ax.set_ylabel("Brent dalam IDR per barrel (ribu IDR)")
ax.set_title(f"Channel 1 Step A: Kurs × Brent IDR  |  R²={res['r2']:.3f}, p={res['p']:.2e}")
ax.legend()
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(OUT / "plot.png", dpi=120, bbox_inches="tight")
plt.close()

# Save calculated field reference
df[["waktu_id", "tanggal", "avg_kurs_tengah", "brent_usd_bbl", "brent_idr_per_bbl"]].to_csv(
    OUT / "brent_idr_per_bbl.csv", index=False)

print("WS1 Bab3 — Kurs × Brent IDR")
print(f"  Brent IDR range: {df['brent_idr_per_bbl'].min():,.0f} - {df['brent_idr_per_bbl'].max():,.0f}")
print(f"  R² = {res['r2']:.4f}")
print(f"  slope = {res['slope']:,.2f}")
