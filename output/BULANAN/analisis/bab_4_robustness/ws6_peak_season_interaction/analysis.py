"""
Bab 4 / WS6 — Interaksi is_peak_season × kurs.
Apakah peak season lebih/kurang sensitif ke kurs?
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _utils import monthly_pax, linreg_summary

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

OUT = Path(__file__).parent
df = monthly_pax()

results = []
for ps in [0, 1]:
    sub = df[df["is_peak_season"] == ps]
    x, y = sub["avg_kurs_tengah"].values, sub["jumlah_penumpang"].values
    res = linreg_summary(x, y)
    res["is_peak_season"] = ps
    results.append(res)
pd.DataFrame(results).to_csv(OUT / "slope_by_peak.csv", index=False)

with open(OUT / "metrics.txt", "w", encoding="utf-8") as f:
    f.write("Bab 4 / WS6 — Interaksi is_peak_season × Kurs\n")
    for r in results:
        f.write(f"\nis_peak_season={r['is_peak_season']} (n={r['n']}):\n")
        f.write(f"  slope = {r['slope']:,.2f}\n  R² = {r['r2']:.4f}\n  p = {r['p']:.6f}\n")

fig, ax = plt.subplots(figsize=(10, 6))
colors = {0: "#4C72B0", 1: "#C44E52"}
labels = {0: "Non-peak season", 1: "Peak season (Lebaran/Jun-Jul/Des)"}
for ps in [0, 1]:
    sub = df[df["is_peak_season"] == ps]
    ax.scatter(sub["avg_kurs_tengah"], sub["jumlah_penumpang"]/1e6,
               s=70, alpha=0.7, color=colors[ps], label=labels[ps],
               edgecolor="white", lw=0.8)
    r = next(rr for rr in results if rr["is_peak_season"] == ps)
    xline = np.linspace(sub["avg_kurs_tengah"].min(), sub["avg_kurs_tengah"].max(), 100)
    ax.plot(xline, (r["intercept"] + r["slope"]*xline)/1e6,
            "--", color=colors[ps], lw=2,
            label=f"  slope={r['slope']:,.0f}, R²={r['r2']:.2f}")

ax.set_xlabel("Kurs IDR/USD")
ax.set_ylabel("Penumpang (juta)")
ax.set_title("Interaksi: Sensitivitas Kurs Berbeda di Peak vs Non-peak Season")
ax.legend(fontsize=9)
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(OUT / "plot.png", dpi=120, bbox_inches="tight")
plt.close()
print("WS6 Bab4 — Peak season interaction:")
for r in results:
    print(f"  is_peak={r['is_peak_season']} (n={r['n']}): slope={r['slope']:,.0f}, R²={r['r2']:.3f}")
