"""
Bab 1 / WS3 — Inflasi YoY & MtM dengan background COVID phase.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _utils import monthly_pax, COVID_PHASE_COLORS

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

OUT = Path(__file__).parent
df = monthly_pax()

# Summary per fase
phase_summary = df.groupby("covid_phase").agg(
    n_bulan=("waktu_id", "count"),
    inflasi_yoy_mean=("inflasi_yoy", "mean"),
    inflasi_mtm_mean=("inflasi_mtm", "mean"),
    bi_rate_mean=("bi_rate", "mean"),
).reset_index()
phase_summary.to_csv(OUT / "phase_summary.csv", index=False)

fig, ax1 = plt.subplots(figsize=(12, 5))

# Background COVID phase shading
phase_change = df["covid_phase"].ne(df["covid_phase"].shift()).cumsum()
for _, group in df.groupby(phase_change):
    phase = group["covid_phase"].iloc[0]
    start, end = group["tanggal"].iloc[0], group["tanggal"].iloc[-1]
    ax1.axvspan(start, end, alpha=0.10, color=COVID_PHASE_COLORS[phase], label=f"_{phase}")

# Inflasi YoY (axis kiri)
ax1.plot(df["tanggal"], df["inflasi_yoy"], color="#C44E52", lw=2, label="Inflasi YoY (%)")
ax1.set_ylabel("Inflasi YoY (%)", color="#C44E52")
ax1.tick_params(axis="y", labelcolor="#C44E52")
ax1.set_ylim(bottom=0)

# Inflasi MtM (axis kanan)
ax2 = ax1.twinx()
ax2.plot(df["tanggal"], df["inflasi_mtm"], color="#4C72B0", lw=1.5, alpha=0.7, label="Inflasi MtM (%)")
ax2.axhline(0, color="black", lw=0.5)
ax2.set_ylabel("Inflasi MtM (%)", color="#4C72B0")
ax2.tick_params(axis="y", labelcolor="#4C72B0")

ax1.set_title("Inflasi YoY (merah, kiri) & MtM (biru, kanan) dengan Background COVID Phase")
ax1.grid(alpha=0.3)

# Legend custom untuk phase
from matplotlib.patches import Patch
phase_legend = [Patch(facecolor=COVID_PHASE_COLORS[p], alpha=0.30, label=p)
                for p in ["pre_pandemic", "lockdown", "transisi", "recovery"]]
ax1.legend(handles=phase_legend, loc="upper left", fontsize=8)

ax1.xaxis.set_major_locator(mdates.YearLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

plt.tight_layout()
plt.savefig(OUT / "plot.png", dpi=120, bbox_inches="tight")
plt.close()

print("WS3 — Inflasi & COVID phase")
print("\nRata-rata per fase:")
print(phase_summary.to_string(index=False))
print(f"\n  Plot disimpan: {OUT/'plot.png'}")
