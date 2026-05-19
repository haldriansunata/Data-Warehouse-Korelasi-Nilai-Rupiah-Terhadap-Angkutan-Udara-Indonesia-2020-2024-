"""
Bab 3 / WS2 — Brent_IDR × Tarif Tiket IHK (channel 1 step B: cost-push BBM → harga tiket; Brent IDR adalah proxy upstream untuk biaya avtur — kita tidak punya data avtur langsung).
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

x = df["brent_idr_per_bbl"].values
y = df["tarif_tiket_ihk"].values
res = linreg_summary(x, y)

with open(OUT / "metrics.txt", "w", encoding="utf-8") as f:
    f.write("Bab 3 / WS2 — Brent IDR × Tarif Tiket IHK\n")
    f.write(f"slope = {res['slope']:.6f} (poin IHK per 1 IDR brent)\n")
    f.write(f"R² = {res['r2']:.4f}\n")
    f.write(f"p-value = {res['p']:.6f}\n")

fig, ax = plt.subplots(figsize=(9, 6))
for phase, color in COVID_PHASE_COLORS.items():
    sub = df[df["covid_phase"] == phase]
    ax.scatter(sub["brent_idr_per_bbl"]/1e3, sub["tarif_tiket_ihk"],
               s=70, alpha=0.75, color=color, label=phase, edgecolor="white", lw=0.8)
xline = np.linspace(x.min(), x.max(), 100)
ax.plot(xline/1e3, res["intercept"] + res["slope"]*xline, "k--", lw=1.5, alpha=0.7)

ax.set_xlabel("Brent IDR per barrel (ribu IDR)")
ax.set_ylabel("Tarif Tiket IHK (indeks)")
ax.set_title(f"Channel 1 Step B: Brent IDR × Tarif Tiket  |  R²={res['r2']:.3f}, p={res['p']:.2e}")
ax.legend()
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(OUT / "plot.png", dpi=120, bbox_inches="tight")
plt.close()

print("WS2 Bab3 — Brent IDR × Tarif")
print(f"  R² = {res['r2']:.4f}")
print(f"  slope = {res['slope']:.6f} IHK per IDR brent")
