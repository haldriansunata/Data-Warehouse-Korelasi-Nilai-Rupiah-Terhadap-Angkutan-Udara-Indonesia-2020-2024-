"""
Bab 4 / WS1 — Faceted scatter kurs × penumpang per covid_phase.
Tujuan: lihat slope SETELAH dikontrol COVID phase.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _utils import monthly_pax, linreg_summary, COVID_PHASE_COLORS

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

OUT = Path(__file__).parent
df = monthly_pax()

phases = ["pre_pandemic", "lockdown", "transisi", "recovery"]
results = []
fig, axes = plt.subplots(1, 4, figsize=(16, 4.5), sharey=True)

for ax, phase in zip(axes, phases):
    sub = df[df["covid_phase"] == phase]
    if len(sub) < 3:
        ax.text(0.5, 0.5, f"n={len(sub)}\ntoo few", ha="center", va="center",
                transform=ax.transAxes, fontsize=12)
        ax.set_title(f"{phase} (n={len(sub)})")
        results.append({"phase": phase, "n": len(sub), "slope": None, "r2": None, "p": None})
        continue
    x = sub["avg_kurs_tengah"].values
    y = sub["jumlah_penumpang"].values
    res = linreg_summary(x, y)
    results.append({"phase": phase, "n": res["n"], "slope": res["slope"],
                    "r2": res["r2"], "p": res["p"]})

    ax.scatter(x, y/1e6, s=70, alpha=0.75, color=COVID_PHASE_COLORS[phase],
               edgecolor="white", lw=0.8)
    if res["n"] >= 3:
        xline = np.linspace(x.min(), x.max(), 100)
        ax.plot(xline, (res["intercept"] + res["slope"]*xline)/1e6,
                "k--", lw=1.5, alpha=0.7)
    ax.set_title(f"{phase}\nslope={res['slope']:,.0f}, R²={res['r2']:.2f}, n={res['n']}",
                 fontsize=10)
    ax.set_xlabel("Kurs IDR/USD")
    ax.grid(alpha=0.3)
axes[0].set_ylabel("Penumpang (juta)")
fig.suptitle("Scatter Kurs × Penumpang per COVID Phase (Faceted)", fontsize=12)
plt.tight_layout()
plt.savefig(OUT / "plot.png", dpi=120, bbox_inches="tight")
plt.close()

pd.DataFrame(results).to_csv(OUT / "slope_per_phase.csv", index=False)
print("WS1 Bab4 — Slope per COVID phase:")
print(pd.DataFrame(results).to_string(index=False))
