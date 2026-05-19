"""
Bab 5 / WS4 — OD Matrix: Top 10 origin × Top 10 destination IATA.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _utils import joined_full

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

OUT = Path(__file__).parent
df = joined_full()

# Top 10 IATA by total penumpang (sum as origin or destination)
all_iata_o = df.groupby("o_iata")["jumlah_penumpang"].sum()
all_iata_d = df.groupby("d_iata")["jumlah_penumpang"].sum()
combined = all_iata_o.add(all_iata_d, fill_value=0).nlargest(10).index.tolist()
print(f"  Top 10 IATA: {combined}")

filt = df[df["o_iata"].isin(combined) & df["d_iata"].isin(combined)]
matrix = filt.pivot_table(index="o_iata", columns="d_iata",
                          values="jumlah_penumpang", aggfunc="sum", fill_value=0)
matrix = matrix.reindex(index=combined, columns=combined, fill_value=0)
matrix.to_csv(OUT / "od_matrix.csv")

fig, ax = plt.subplots(figsize=(8, 7))
im = ax.imshow(matrix.values / 1e6, cmap="YlOrRd", aspect="auto")
ax.set_xticks(range(len(combined)))
ax.set_xticklabels(combined, rotation=45)
ax.set_yticks(range(len(combined)))
ax.set_yticklabels(combined)
ax.set_xlabel("Destination (IATA)")
ax.set_ylabel("Origin (IATA)")
ax.set_title("OD Matrix — Total Penumpang 2020-2024 (juta)\nTop 10 IATA × Top 10 IATA")

for i in range(len(combined)):
    for j in range(len(combined)):
        val = matrix.values[i, j] / 1e6
        if val > 0.01:
            color = "white" if val > 3 else "black"
            ax.text(j, i, f"{val:.1f}", ha="center", va="center", fontsize=8, color=color)

fig.colorbar(im, ax=ax, label="Juta penumpang")
plt.tight_layout()
plt.savefig(OUT / "plot.png", dpi=120, bbox_inches="tight")
plt.close()

print("WS4 Bab5 — OD Matrix (juta):")
print((matrix/1e6).round(2).to_string())
