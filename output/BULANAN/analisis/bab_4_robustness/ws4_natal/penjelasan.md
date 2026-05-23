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

## Target Tableau — Step by Step

### Langkah Pembuatan Sheet
1. **Buat worksheet baru** `Bab4_WS4_NatalEffect`. ATAU duplicate `Bab4_WS3_LebaranEffect` dan rename.
2. **HAPUS filter kategori** kalau sebelumnya ada (Natal berlaku universal, tidak khusus DOM).
3. **Drag `has_natal` ke Columns**. Klik kanan → **Discrete** (pil biru). 2 kolom: 0, 1.
4. **Drag `jumlah_penumpang` ke Rows**. Ubah ke **MEDIAN** (klik kanan pil → Measure → Median).
5. **Marks**: Bar.
6. **Drag `MEDIAN(jumlah_penumpang)` ke Label**.
7. **Color**: `has_natal` (2 warna).

### Cross-check ke Python
File `summary.csv`:
- Median has_natal=0: **5.839**
- Median has_natal=1: **7.704**
- Boost ratio: **1,32×** (SIGNIFIKAN, p < 0,001)

### Catatan
- **Berbeda dengan Lebaran (WS3) yang tidak signifikan**, efek Natal **SIGNIFIKAN** karena bulan Desember 2020–2024 mayoritas di luar lockdown puncak.
- Annotation manual: "Median Natal **1,32× lebih tinggi** dari bulan biasa (Mann-Whitney p < 0,001). Konsisten karena Desember bertepatan dengan libur sekolah + Tahun Baru + Natal."
- Ini bisa jadi sheet pendamping WS3 saat presentasi — kontraskan "Lebaran terkontaminasi COVID" vs "Natal robust".

---

## ⚙️ Update — Catatan Implementasi Tableau

**`has_natal` Dimension vs Measure**: sama dengan WS3 Lebaran — nilainya 0/1, convert ke **Dimension** sudah BENAR.

Lihat `solusi_masalah.md` Solusi #3.
