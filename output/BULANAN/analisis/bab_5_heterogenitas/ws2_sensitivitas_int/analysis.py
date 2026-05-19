"""
Bab 5 / WS2 — Sensitivitas slope per rute INTERNASIONAL (top 10).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _utils import joined_full, linreg_summary

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

OUT = Path(__file__).parent
df = joined_full()
df_int = df[df["kategori"] == "INTERNASIONAL"]

# Top 10 rute INT
top10 = (df_int.groupby("kode_rute")["jumlah_penumpang"].sum()
         .nlargest(10).index.tolist())

results = []
for kode in top10:
    sub = df_int[df_int["kode_rute"] == kode]
    monthly = sub.groupby("waktu_id").agg(
        pax=("jumlah_penumpang", "sum"),
        kurs=("avg_kurs_tengah", "first")
    ).reset_index()
    if len(monthly) < 5:
        continue
    res = linreg_summary(monthly["kurs"], monthly["pax"])
    res["kode_rute"] = kode
    res["total_pax"] = monthly["pax"].sum()
    results.append(res)

result_df = pd.DataFrame(results).sort_values("slope")
result_df.to_csv(OUT / "sensitivity_per_int_route.csv", index=False)

fig, ax = plt.subplots(figsize=(10, 6))
colors = ["red" if s < 0 else "steelblue" for s in result_df["slope"]]
ax.barh(result_df["kode_rute"], result_df["slope"], color=colors)
ax.axvline(0, color="black", lw=1)
ax.set_xlabel("Slope (pax per 1 IDR pelemahan kurs)")
ax.set_title("Sensitivitas Slope Kurs → Penumpang per Rute INTERNASIONAL (Top 10)\n(merah = slope negatif sesuai teori; biru = positif spurious)")
for i, (s, r2) in enumerate(zip(result_df["slope"], result_df["r2"])):
    ax.text(s + np.sign(s)*5, i, f"R²={r2:.2f}", va="center", fontsize=8)
ax.grid(alpha=0.3, axis="x")
plt.tight_layout()
plt.savefig(OUT / "plot.png", dpi=120, bbox_inches="tight")
plt.close()

print("WS2 Bab5 — Sensitivitas per rute INT (sorted by slope):")
print(result_df[["kode_rute", "slope", "r2", "p"]].round(4).to_string(index=False))
