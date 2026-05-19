"""
Bab 4 / WS5 — Hubungan kontinyu jumlah_hari_libur × penumpang.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _utils import monthly_pax, linreg_summary, COVID_PHASE_COLORS

import numpy as np
import matplotlib.pyplot as plt

OUT = Path(__file__).parent
df = monthly_pax()

x = df["jumlah_hari_libur"].values
y = df["jumlah_penumpang"].values
res = linreg_summary(x, y)

with open(OUT / "metrics.txt", "w", encoding="utf-8") as f:
    f.write("Bab 4 / WS5 — Hari Libur × Penumpang\n")
    f.write(f"slope = {res['slope']:,.2f} (pax per 1 hari libur tambahan)\n")
    f.write(f"R² = {res['r2']:.4f}\n")
    f.write(f"p-value = {res['p']:.6f}\n")

fig, ax = plt.subplots(figsize=(9, 6))
for phase, color in COVID_PHASE_COLORS.items():
    sub = df[df["covid_phase"] == phase]
    ax.scatter(sub["jumlah_hari_libur"] + np.random.uniform(-0.15, 0.15, len(sub)),
               sub["jumlah_penumpang"]/1e6,
               s=70, alpha=0.7, color=color, label=phase, edgecolor="white", lw=0.8)
xline = np.linspace(0, 6, 100)
ax.plot(xline, (res["intercept"] + res["slope"]*xline)/1e6, "k--", lw=1.5, alpha=0.7)
ax.set_xlabel("Jumlah hari libur nasional (per bulan)")
ax.set_ylabel("Penumpang (juta)")
ax.set_title(f"Hari Libur × Penumpang  |  R²={res['r2']:.3f}, slope={res['slope']:,.0f}")
ax.legend()
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(OUT / "plot.png", dpi=120, bbox_inches="tight")
plt.close()
print("WS5 Bab4 — Hari Libur")
print(f"  R² = {res['r2']:.4f}, slope = {res['slope']:,.2f}")
