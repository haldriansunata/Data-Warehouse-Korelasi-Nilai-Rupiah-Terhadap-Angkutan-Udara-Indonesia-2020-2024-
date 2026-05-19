"""
Bab 2 / WS2 — Scatter kurs × penumpang INTERNASIONAL.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _utils import monthly_pax, linreg_summary, COVID_PHASE_COLORS

import numpy as np
import matplotlib.pyplot as plt

OUT = Path(__file__).parent
df = monthly_pax(filter_kategori="INTERNASIONAL")

x = df["avg_kurs_tengah"].values
y = df["jumlah_penumpang"].values

res = linreg_summary(x, y)

with open(OUT / "metrics.txt", "w", encoding="utf-8") as f:
    f.write("Bab 2 / WS2 — Kurs × Penumpang INTERNASIONAL\n")
    f.write(f"n = {res['n']}\n")
    f.write(f"slope = {res['slope']:,.2f} (pax / 1 IDR pelemahan)\n")
    f.write(f"R-squared = {res['r2']:.4f}\n")
    f.write(f"Pearson r = {res['r']:.4f}\n")
    f.write(f"p-value = {res['p']:.6f}\n")

fig, ax = plt.subplots(figsize=(9, 6))
for phase, color in COVID_PHASE_COLORS.items():
    sub = df[df["covid_phase"] == phase]
    ax.scatter(sub["avg_kurs_tengah"], sub["jumlah_penumpang"]/1e6,
               s=70, alpha=0.75, color=color, label=phase, edgecolor="white", lw=0.8)

xline = np.linspace(x.min(), x.max(), 100)
yline = res["intercept"] + res["slope"]*xline
ax.plot(xline, yline/1e6, "k--", lw=1.5, alpha=0.7,
        label=f"OLS slope={res['slope']:.0f}/IDR")

ax.set_xlabel("Kurs IDR/USD")
ax.set_ylabel("Penumpang INT (juta)")
ax.set_title(f"Kurs × Penumpang INTERNASIONAL  |  R²={res['r2']:.3f}, p={res['p']:.3e}")
ax.legend(loc="upper left", fontsize=9)
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(OUT / "plot.png", dpi=120, bbox_inches="tight")
plt.close()

print("WS2 — INT")
for k, v in res.items():
    print(f"  {k}: {v}")
