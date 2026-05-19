"""
Bab 4 / WS3 — Efek Lebaran pada penumpang DOMESTIK (median per rute).
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
dom = df[df["kategori"] == "DOMESTIK"].copy()

summary = dom.groupby("has_lebaran")["jumlah_penumpang"].agg(
    n="count", median="median", mean="mean", sum="sum").reset_index()
summary.to_csv(OUT / "summary.csv", index=False)

# Statistical test: Mann-Whitney U (non-parametric, no normality assumption)
group_0 = dom.loc[dom["has_lebaran"] == 0, "jumlah_penumpang"].values
group_1 = dom.loc[dom["has_lebaran"] == 1, "jumlah_penumpang"].values
u_stat, p_val = stats.mannwhitneyu(group_1, group_0, alternative="greater")

with open(OUT / "metrics.txt", "w", encoding="utf-8") as f:
    f.write("Bab 4 / WS3 — Lebaran Effect (DOMESTIK)\n")
    f.write(f"Median penumpang non-Lebaran: {summary.loc[0,'median']:,.0f}\n")
    f.write(f"Median penumpang Lebaran: {summary.loc[1,'median']:,.0f}\n")
    f.write(f"Boost ratio: {summary.loc[1,'median']/summary.loc[0,'median']:.2f}×\n")
    f.write(f"Mann-Whitney U test: U={u_stat:.0f}, p={p_val:.6f}\n")

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Bar chart medians
axes[0].bar([0, 1], summary["median"], color=["#4C72B0", "#C44E52"], width=0.5)
axes[0].set_xticks([0, 1])
axes[0].set_xticklabels(["Bulan biasa", "Bulan Lebaran"])
axes[0].set_ylabel("Median penumpang per rute")
axes[0].set_title(f"Median per rute  |  boost {summary.loc[1,'median']/summary.loc[0,'median']:.2f}×")
for i, v in enumerate(summary["median"]):
    axes[0].text(i, v + 200, f"{v:,.0f}", ha="center", fontsize=10)

# Box plot
axes[1].boxplot([group_0/1000, group_1/1000], labels=["Bulan biasa", "Bulan Lebaran"], showfliers=False)
axes[1].set_ylabel("Penumpang (ribu)")
axes[1].set_title(f"Distribusi  |  Mann-Whitney p={p_val:.2e}")
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig(OUT / "plot.png", dpi=120, bbox_inches="tight")
plt.close()
print(f"WS3 Bab4 — Lebaran effect (DOM)")
print(summary.to_string(index=False))
print(f"Mann-Whitney U p={p_val:.6f}")
