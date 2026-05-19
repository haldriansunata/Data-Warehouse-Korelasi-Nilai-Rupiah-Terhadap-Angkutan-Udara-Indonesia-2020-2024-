"""
Bab 1 / WS4 — Heatmap musiman: tahun × bulan, value = total penumpang.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _utils import monthly_pax

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

OUT = Path(__file__).parent
df = monthly_pax()

pivot = df.pivot_table(index="tahun", columns="bulan", values="jumlah_penumpang", aggfunc="sum")
pivot.columns = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]
pivot.to_csv(OUT / "pivot_pax_tahun_bulan.csv")

fig, ax = plt.subplots(figsize=(10, 4))
im = ax.imshow(pivot.values / 1e6, aspect="auto", cmap="YlOrRd")

# Labels
ax.set_xticks(range(12))
ax.set_xticklabels(pivot.columns)
ax.set_yticks(range(len(pivot.index)))
ax.set_yticklabels(pivot.index)
ax.set_xlabel("Bulan")
ax.set_ylabel("Tahun")
ax.set_title("Heatmap Total Penumpang Nasional (juta) — Tahun × Bulan")

# Cell annotations
for i in range(pivot.shape[0]):
    for j in range(pivot.shape[1]):
        val = pivot.values[i, j] / 1e6
        ax.text(j, i, f"{val:.1f}", ha="center", va="center",
                fontsize=8, color="black" if val < 5 else "white")

fig.colorbar(im, ax=ax, label="Juta penumpang")
plt.tight_layout()
plt.savefig(OUT / "plot.png", dpi=120, bbox_inches="tight")
plt.close()

print("WS4 — Seasonal heatmap")
print("\nPivot (juta penumpang):")
print((pivot / 1e6).round(2).to_string())
print(f"\n  Cell minimum: {pivot.values.min():,.0f} ({pivot.stack().idxmin()})")
print(f"  Cell maximum: {pivot.values.max():,.0f} ({pivot.stack().idxmax()})")
print(f"\n  Plot disimpan: {OUT/'plot.png'}")
