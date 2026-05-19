# Bab 3 / WS2 — Channel 1 Step B: Brent IDR × Tarif Tiket IHK

## Tujuan
Step kedua: apakah kenaikan biaya BBM dalam IDR ter-pass-through ke harga tiket pesawat (proxy: indeks tarif tiket BPS)?

## Hasil

| Metrik | Nilai |
|---|---:|
| R² | **0,352** |
| Slope | 0,000277 poin IHK per 1 IDR brent |
| p-value | <0,001 (signifikan) |

## Makna

R² = 0,35 → **35% variasi tarif tiket dijelaskan oleh biaya BBM dalam IDR**. Hubungan moderate.

Slope: setiap kenaikan Brent IDR sebesar **1.000.000 IDR/bbl** (1 juta), indeks tarif naik **+277 poin**. Mengingat range Brent IDR 400K–1.689K (delta ~1.300K), perkiraan kontribusi: **~360 poin** kenaikan IHK dari channel BBM saja. Cocok dengan kenyataan: tarif IHK naik dari ~1.248 (2020) ke ~1.788 (2024), delta 540 poin — sebagian besar (~67%) dijelaskan oleh BBM, sisanya oleh faktor lain (gaji, retribusi, dll).

### Catatan
- Pass-through tidak instan — ada lag (biasanya 1–2 bulan) karena maskapai hedge BBM dan penyesuaian harga butuh persetujuan regulator.
- Pemerintah membatasi tarif batas atas, yang membatasi pass-through sebenarnya. Industri mengeluh tarif batas atas dibuat 2019 dengan asumsi Brent jauh lebih rendah → ini eksplisit dijelaskan oleh Dirut Garuda.

## Target Tableau
Columns: `Brent IDR per Bbl` (calculated). Rows: `AVG(tarif_tiket_ihk)`. Detail: `waktu_id`. Color: `covid_phase`. Trend linear.
