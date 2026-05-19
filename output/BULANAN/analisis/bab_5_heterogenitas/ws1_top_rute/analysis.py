"""
Bab 5 / WS1 — Top 15 rute by total penumpang 2020-2024.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _utils import joined_full

import pandas as pd
import matplotlib.pyplot as plt

OUT = Path(__file__).parent
df = joined_full()

top = (df.groupby(["kode_rute", "kategori"])["jumlah_penumpang"]
         .sum().reset_index()
         .sort_values("jumlah_penumpang", ascending=False)
         .head(15))
top.to_csv(OUT / "top15_rute.csv", index=False)

fig, ax = plt.subplots(figsize=(10, 7))
colors = top["kategori"].map({"DOMESTIK": "#4C72B0", "INTERNASIONAL": "#C44E52"})
ax.barh(top["kode_rute"][::-1], top["jumlah_penumpang"][::-1]/1e6,
        color=colors[::-1])
ax.set_xlabel("Total penumpang 2020-2024 (juta)")
ax.set_title("Top 15 Rute by Total Penumpang Bulanan (60 bulan)")
ax.grid(alpha=0.3, axis="x")
for i, v in enumerate(top["jumlah_penumpang"][::-1]/1e6):
    ax.text(v + 0.5, i, f"{v:.1f}M", va="center", fontsize=9)
# Legend
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color="#4C72B0", label="DOMESTIK"),
                   Patch(color="#C44E52", label="INTERNASIONAL")],
          loc="lower right")
plt.tight_layout()
plt.savefig(OUT / "plot.png", dpi=120, bbox_inches="tight")
plt.close()

print("WS1 Bab5 — Top 15 rute:")
print(top.to_string(index=False))
