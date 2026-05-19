# Bab 4 / WS3 — Efek Lebaran pada Domestik (Median per Rute)

## Tujuan
Validasi flag `has_lebaran`: apakah bulan Lebaran benar-benar boost penumpang di rute domestik (mudik)?

## Pendekatan
Bandingkan **median** penumpang per rute (DOMESTIK) antara `has_lebaran=0` vs `has_lebaran=1`. Pakai median karena distribusi penumpang per rute *right-skewed* (rute besar mendistorsi mean). Uji statistik: **Mann-Whitney U test** (non-parametric, tidak butuh asumsi normality).

## Perhitungan
```python
group_0 = penumpang_rute[has_lebaran == 0]  # baseline
group_1 = penumpang_rute[has_lebaran == 1]  # Lebaran
median_0 = np.median(group_0)
median_1 = np.median(group_1)
boost = median_1 / median_0
u, p = scipy.stats.mannwhitneyu(group_1, group_0, alternative="greater")
```

## Hasil

| Group | n | Median | Mean | Sum |
|---|---:|---:|---:|---:|
| has_lebaran=0 | 12.534 | 5.338 | 17.987 | 225 jt |
| has_lebaran=1 | 985 | 5.621 | 19.344 | 19 jt |
| **Boost ratio (median)** | — | **1,05×** | — | — |
| Mann-Whitney p | — | — | — | **0,697** |

## Makna — Surprising!

**Boost Lebaran hanya 1,05× dan TIDAK signifikan (p=0,70).**

Kenapa? Karena bulan Lebaran di dataset adalah:
- **Mei 2020** (lockdown puncak — pax SANGAT rendah, jauh dari typical Lebaran)
- **Mei 2021** (Delta wave incoming — pax tertekan)
- **Mei 2022** (transisi awal)
- **April 2023, 2024** (recovery normal)

3 dari 5 bulan Lebaran terjadi di periode COVID, sehingga pull-down median Lebaran. Mean (mass-weighted) lebih informatif: 19.344 vs 17.987 = boost 1,08×.

## Cara Mengisolasi Efek Lebaran Lebih Baik

1. **Filter ke recovery only**: lihat 2023 (April) dan 2024 (April) saja.
2. **Diff-in-diff**: bandingkan rute domestik Mei vs April Mei tahun yang sama (control bulan), tahun-tahun pasca-COVID.

## Pesan untuk Paper

Hindari over-claim efek Lebaran berdasarkan median per rute. Yang lebih kuat: total nasional April 2024 (8,58 juta) > rata-rata bulan non-libur 2024 → boost ~12-15%. Tapi ini juga butuh kontrol Lebaran-bulan-shift.

## Target Tableau
- Columns: `has_lebaran` (Discrete, 0/1)
- Rows: `MEDIAN(jumlah_penumpang)` per rute (Detail = `kode_rute`)
- Filter: `kategori` = DOMESTIK

Hasil di Tableau akan match dengan angka median di atas.
