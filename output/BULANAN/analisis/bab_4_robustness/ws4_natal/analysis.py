"""
Bab 4 / WS4 — Efek Natal pada penumpang (median per rute, total dom+int).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _utils import joined_full

import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

OUT = Path(__file__).parent
df = joined_full()

summary = df.groupby("has_natal")["jumlah_penumpang"].agg(
    n="count", median="median", mean="mean", sum="sum").reset_index()
summary.to_csv(OUT / "summary.csv", index=False)

g0 = df.loc[df["has_natal"] == 0, "jumlah_penumpang"].values
g1 = df.loc[df["has_natal"] == 1, "jumlah_penumpang"].values
u, p = stats.mannwhitneyu(g1, g0, alternative="greater")

with open(OUT / "metrics.txt", "w", encoding="utf-8") as f:
    f.write("Bab 4 / WS4 — Natal Effect (semua segmen)\n")
    f.write(f"Median non-Natal: {summary.loc[0,'median']:,.0f}\n")
    f.write(f"Median Natal:     {summary.loc[1,'median']:,.0f}\n")
    f.write(f"Boost: {summary.loc[1,'median']/summary.loc[0,'median']:.2f}×\n")
    f.write(f"Mann-Whitney p = {p:.6f}\n")

fig, ax = plt.subplots(figsize=(8, 5))
ax.bar([0, 1], summary["median"], color=["#4C72B0", "#3E7B27"], width=0.5)
ax.set_xticks([0, 1])
ax.set_xticklabels(["Bukan Desember", "Bulan Desember (Natal)"])
ax.set_ylabel("Median penumpang per rute")
ax.set_title(f"Efek Natal  |  boost {summary.loc[1,'median']/summary.loc[0,'median']:.2f}×  |  p={p:.2e}")
for i, v in enumerate(summary["median"]):
    ax.text(i, v + 200, f"{v:,.0f}", ha="center", fontsize=10)
ax.grid(alpha=0.3, axis="y")
plt.tight_layout()
plt.savefig(OUT / "plot.png", dpi=120, bbox_inches="tight")
plt.close()
print(f"WS4 Bab4 — Natal effect")
print(summary.to_string(index=False))
