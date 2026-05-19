"""
Bab 3 / WS4 — Kurs × BI Rate (channel 2: respons moneter).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _utils import monthly_pax, linreg_summary, COVID_PHASE_COLORS

import numpy as np
import matplotlib.pyplot as plt

OUT = Path(__file__).parent
df = monthly_pax()

x = df["avg_kurs_tengah"].values
y = df["bi_rate"].values
res = linreg_summary(x, y)

with open(OUT / "metrics.txt", "w", encoding="utf-8") as f:
    f.write("Bab 3 / WS4 — Kurs × BI Rate\n")
    f.write(f"slope = {res['slope']:.6f} (% per 1 IDR pelemahan)\n")
    f.write(f"R² = {res['r2']:.4f}\n")
    f.write(f"p-value = {res['p']:.6f}\n")
    f.write("\nInterpretasi: setiap 1.000 IDR pelemahan, BI rate naik {0:.2f}%.\n".format(res['slope']*1000))

fig, ax = plt.subplots(figsize=(9, 6))
for phase, color in COVID_PHASE_COLORS.items():
    sub = df[df["covid_phase"] == phase]
    ax.scatter(sub["avg_kurs_tengah"], sub["bi_rate"],
               s=70, alpha=0.75, color=color, label=phase, edgecolor="white", lw=0.8)
xline = np.linspace(x.min(), x.max(), 100)
ax.plot(xline, res["intercept"] + res["slope"]*xline, "k--", lw=1.5, alpha=0.7)

ax.set_xlabel("Kurs IDR/USD")
ax.set_ylabel("BI Rate (% per tahun)")
ax.set_title(f"Channel 2: Kurs × BI Rate  |  R²={res['r2']:.3f}, p={res['p']:.2e}")
ax.legend()
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(OUT / "plot.png", dpi=120, bbox_inches="tight")
plt.close()

print("WS4 Bab3 — Kurs × BI Rate")
print(f"  R² = {res['r2']:.4f}")
print(f"  slope = {res['slope']:.6f} %/IDR ({res['slope']*1000:.2f}% per 1000 IDR)")
