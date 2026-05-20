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

## Target Tableau — Step by Step

### Prasyarat
Pastikan default aggregation `brent_idr_per_bbl` dan `tarif_tiket_ihk` sudah di-set ke **Average** (lihat Bab 3 WS1 untuk langkah set default agg).

### Langkah Pembuatan Sheet
1. **Buat worksheet baru** `Bab3_WS2_BrentIDR_Tarif`.
2. **Drag `brent_idr_per_bbl` ke Columns**. Pil `AVG(brent_idr_per_bbl)`, hijau.
3. **Drag `tarif_tiket_ihk` ke Rows**. Pil `AVG(tarif_tiket_ihk)`. (Pastikan AVG, bukan SUM.)
4. **Drag `waktu_id` ke Detail** → klik kanan → **Dimension**.
5. **Marks**: Circle.
6. **Drag `covid_phase` ke Color**.
7. **Trend Line**: Analytics → Linear.

### Catatan: Alternatif dengan Calculated Field
Kalau dataset belum punya kolom `brent_idr_per_bbl`, buat calculated field di Tableau:
```
Brent IDR per Bbl = AVG([brent_usd_bbl]) * AVG([avg_kurs_tengah])
```
Hasil R² dan slope identik dengan versi native.

### Cross-check ke Python
File `metrics.txt`:
- slope = **0,000277** poin IHK per 1 IDR Brent
- R² = **0,3521**

Interpretasi: kenaikan Brent IDR sebesar Rp 1.000.000 per barel diasosiasikan dengan kenaikan indeks tarif sebesar **+277 poin**.

### Catatan Khusus
- R² = 0,35 → 35% variasi tarif tiket dijelaskan oleh biaya BBM dalam IDR. Sisanya (65%) dijelaskan faktor lain: gaji crew, biaya bandara, retribusi, faktor non-BBM.
- Slope kecil dalam angka absolute (0,000277) karena Brent IDR dalam ratusan ribu sedangkan tarif IHK dalam ribuan. Jangan terkecoh angka kecil — interpretasi yang benar pakai range.
