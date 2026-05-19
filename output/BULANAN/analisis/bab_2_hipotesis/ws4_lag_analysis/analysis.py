"""
Bab 2 / WS4 — Lag analysis: kurs t-k × penumpang t untuk k = 0..6 bulan.
Mencari lag dengan R² puncak.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _utils import monthly_pax, linreg_summary

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

OUT = Path(__file__).parent

def lag_table(df_subset, label):
    out = []
    for lag in range(0, 7):
        shifted = df_subset["avg_kurs_tengah"].shift(lag)
        mask = shifted.notna()
        x = shifted[mask].values
        y = df_subset.loc[mask, "jumlah_penumpang"].values
        res = linreg_summary(x, y)
        res["lag_bulan"] = lag
        res["segment"] = label
        out.append(res)
    return pd.DataFrame(out)

frames = []
for kat, label in [(None, "TOTAL"),
                   ("INTERNASIONAL", "INT"),
                   ("DOMESTIK", "DOM")]:
    df = monthly_pax(filter_kategori=kat)
    frames.append(lag_table(df, label))

result = pd.concat(frames, ignore_index=True)
result.to_csv(OUT / "lag_r2.csv", index=False)

# Plot: R² per lag, 3 garis (TOTAL/INT/DOM)
fig, ax = plt.subplots(figsize=(9, 5))
colors = {"TOTAL": "#2E86AB", "INT": "#C44E52", "DOM": "#55A868"}
for seg in ["TOTAL", "INT", "DOM"]:
    sub = result[result["segment"] == seg]
    ax.plot(sub["lag_bulan"], sub["r2"], "o-", color=colors[seg], lw=2,
            label=f"{seg}", markersize=8)
    # Annotate puncak
    peak = sub.loc[sub["r2"].idxmax()]
    ax.annotate(f"peak lag={int(peak['lag_bulan'])}, R²={peak['r2']:.2f}",
                xy=(peak["lag_bulan"], peak["r2"]),
                xytext=(5, 5), textcoords="offset points",
                fontsize=8, color=colors[seg])

ax.set_xlabel("Lag (bulan): kurs t-k → penumpang t")
ax.set_ylabel("R²")
ax.set_title("Lag Analysis Kurs → Penumpang (R² per Lag)")
ax.set_xticks(range(0, 7))
ax.legend()
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(OUT / "plot.png", dpi=120, bbox_inches="tight")
plt.close()

print("WS4 — Lag analysis")
print(result.pivot(index="lag_bulan", columns="segment", values="r2").round(4))
print(f"\nDetail: {OUT/'lag_r2.csv'}")
