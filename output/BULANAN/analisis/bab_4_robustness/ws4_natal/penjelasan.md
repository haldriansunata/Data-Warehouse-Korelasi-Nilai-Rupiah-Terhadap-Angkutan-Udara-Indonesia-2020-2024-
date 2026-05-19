# Bab 4 / WS4 — Efek Natal (Bulan Desember)

## Tujuan
Sama dengan WS3, tapi untuk flag `has_natal` (semua bulan Desember).

## Hasil

| Group | n | Median | Mean | Sum |
|---|---:|---:|---:|---:|
| has_natal=0 | 15.647 | 5.839 | 18.497 | 289 jt |
| has_natal=1 | 1.471 | **7.704** | 21.726 | 32 jt |
| **Boost ratio (median)** | — | **1,32×** | — | — |

## Makna

**Natal effect SIGNIFIKAN dan KUAT**: boost 32% di median per-rute. Berbeda dengan Lebaran karena:
1. Natal terjadi di Des 2020, 2021, 2022, 2023, 2024 — hanya Des 2020 yang masih lockdown ringan; sisanya transisi/recovery.
2. Bulan Desember selalu mencakup Tahun Baru + libur sekolah → demand ganda.

### Implikasi
Flag `has_natal` adalah seasonal predictor yang **valid**. Kalau di Tableau kamu plot bar chart `has_natal` vs median, harus ada selisih jelas (5.839 → 7.704).

Kamu bisa kombinasi dengan `is_peak_season` (yang mencakup Juni-Juli libur sekolah + Lebaran + Desember) untuk control musim lebih komprehensif.

## Target Tableau
- Columns: `has_natal` (Discrete)
- Rows: `MEDIAN(jumlah_penumpang)`
- (tanpa filter kategori — Natal berlaku universal)

Hasil: bar 5.839 vs 7.704.
