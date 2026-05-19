"""
Bab 5 / WS3 — Sensitivitas slope per negara destinasi (rute INT).
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
df_int = df[df["kategori"] == "INTERNASIONAL"].copy()

# Destinasi = bandara yang BUKAN INDONESIA (untuk rute INT)
df_int["negara_asing"] = np.where(df_int["o_negara"] != "INDONESIA",
                                   df_int["o_negara"], df_int["d_negara"])
df_int = df_int[df_int["negara_asing"] != "INDONESIA"]

# Pilih negara dengan total penumpang signifikan
total_per_negara = df_int.groupby("negara_asing")["jumlah_penumpang"].sum()
top_neg = total_per_negara[total_per_negara > 500_000].index.tolist()
print(f"  Negara dianalisis (total pax > 500K): {top_neg}")

results = []
for neg in top_neg:
    sub = df_int[df_int["negara_asing"] == neg]
    monthly = sub.groupby("waktu_id").agg(
        pax=("jumlah_penumpang", "sum"),
        kurs=("avg_kurs_tengah", "first")
    ).reset_index()
    if len(monthly) < 12:
        continue
    res = linreg_summary(monthly["kurs"], monthly["pax"])
    res["negara"] = neg
    res["total_pax"] = monthly["pax"].sum()
    res["n_bulan"] = len(monthly)
    results.append(res)

result_df = pd.DataFrame(results).sort_values("slope")
result_df.to_csv(OUT / "sensitivity_per_negara.csv", index=False)

fig, ax = plt.subplots(figsize=(10, 7))
colors = ["red" if s < 0 else "steelblue" for s in result_df["slope"]]
ax.barh(result_df["negara"], result_df["slope"], color=colors)
ax.axvline(0, color="black", lw=1)
ax.set_xlabel("Slope (pax per 1 IDR pelemahan kurs)")
ax.set_title("Sensitivitas Slope per Negara Destinasi (Rute INT)\nmerah = negatif sesuai teori")
for i, (s, r2, n) in enumerate(zip(result_df["slope"], result_df["r2"], result_df["total_pax"])):
    ax.text(s + np.sign(s)*max(abs(result_df["slope"]))*0.02, i,
            f"R²={r2:.2f}, total={n/1e6:.1f}M", va="center", fontsize=8)
ax.grid(alpha=0.3, axis="x")
plt.tight_layout()
plt.savefig(OUT / "plot.png", dpi=120, bbox_inches="tight")
plt.close()

print("WS3 Bab5 — Sensitivitas per negara:")
print(result_df[["negara", "slope", "r2", "p", "total_pax"]].round(4).to_string(index=False))
