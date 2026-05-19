"""
Bab 5 / WS5 — Ranking provinsi origin by total penumpang.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _utils import joined_full

import pandas as pd
import matplotlib.pyplot as plt

OUT = Path(__file__).parent
df = joined_full()
dom = df[df["kategori"] == "DOMESTIK"]

# Ranking provinsi sebagai origin
prov = (dom.groupby("o_provinsi")["jumlah_penumpang"].sum()
        .nlargest(15).reset_index())
prov.columns = ["provinsi", "total_penumpang"]
prov.to_csv(OUT / "top15_provinsi.csv", index=False)

fig, ax = plt.subplots(figsize=(10, 7))
ax.barh(prov["provinsi"][::-1], prov["total_penumpang"][::-1]/1e6, color="#55A868")
ax.set_xlabel("Total penumpang (juta) — sebagai provinsi asal")
ax.set_title("Top 15 Provinsi by Total Penumpang Domestik 2020-2024")
ax.grid(alpha=0.3, axis="x")
for i, v in enumerate(prov["total_penumpang"][::-1]/1e6):
    ax.text(v + 0.5, i, f"{v:.1f}M", va="center", fontsize=9)
plt.tight_layout()
plt.savefig(OUT / "plot.png", dpi=120, bbox_inches="tight")
plt.close()

print("WS5 Bab5 — Top 15 provinsi origin (DOM):")
print(prov.to_string(index=False))
