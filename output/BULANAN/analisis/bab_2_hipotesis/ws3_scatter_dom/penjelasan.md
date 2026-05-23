# Bab 2 / WS3 — Scatter Kurs × Penumpang DOMESTIK

## Hasil

| Metrik | Nilai | vs INT (WS2) |
|---|---:|---|
| Slope | +1.119 pax/IDR | mirip |
| R² | **0,226** | jauh lebih rendah |
| Pearson r | +0,475 | lebih lemah |
| p-value | 1,25 × 10⁻⁴ | masih signifikan |

## Makna

R² DOMESTIK paling rendah (0,23) dari ketiga sheet (Total 0,35, INT 0,49). Maknanya: variasi penumpang DOM kurang dijelaskan oleh kurs.

Ini sesuai ekspektasi teoritis:
- Travel **domestik** tidak ter-denominasi USD secara langsung.
- Channel pengaruh kurs ke DOM melalui *cost-push* lewat biaya bahan bakar penerbangan (USD-denominated, di-proksi dengan Brent crude oil karena data avtur langsung tidak tersedia), tapi pass-through-nya tidak penuh (regulasi tarif batas atas membatasi).
- Lebih banyak faktor lokal (Lebaran, libur sekolah, kondisi ekonomi domestik) yang mempengaruhi DOM.

## Sintesis Bab 2 (WS1+WS2+WS3)

| Segmen | R² naive | Slope |
|---|---:|---:|
| Total | 0,347 | +2.294 |
| INT | **0,486** | +1.176 |
| DOM | 0,226 | +1.119 |

**Ranking sensitivitas (R²)**: INT > Total > DOM ✓ Sesuai teori.

**Tapi**: semua slope positif karena confounder COVID. Hubungan sebenarnya menanti di Bab 4 (kontrol per covid_phase).

## Target Tableau — Step by Step

### Langkah Pembuatan Sheet
1. **Klik kanan tab worksheet `Bab2_WS1_ScatterTotal` → Duplicate**. Rename menjadi `Bab2_WS3_ScatterDOM`.
2. **Tambah filter kategori**:
   - Drag `kategori` ke **Filters**.
   - Centang **hanya `DOMESTIK`** → OK.
3. **Update title sheet** ke "Scatter Kurs × Penumpang DOMESTIK".
4. **Hover Trend Line** untuk verifikasi metrik.

### Cross-check ke Python
File `metrics.txt`:
- slope = **1.118,94**
- R-squared = **0,2257**
- p-value = **0,000125**
- Pearson r = **0,4750**

R² DOMESTIK paling rendah dari 3 sheet (Total 0,35, INT 0,49) — konsisten dengan teori bahwa rute domestik kurang ter-USD-kan dibanding internasional.

### Catatan Khusus untuk Presentasi
Susun ketiga sheet (WS1, WS2, WS3) di satu **Dashboard** baru bernama `Bab2_Dashboard_HipotesisUtama`:
1. Buat Dashboard baru (icon dashboard di bawah, sebelah icon worksheet).
2. Drag ketiga sheet ke layout horizontal/grid.
3. Tambah Text box di atas untuk title: "Korelasi Naive Kurs × Penumpang per Segmen".
4. Tambah Text box di bawah dengan ringkasan: "R² ranking: INT (0,49) > Total (0,35) > DOM (0,23). Slope semua POSITIF — akan dijelaskan di Bab 4."

---

## ⚙️ Update — Catatan Implementasi Tableau

**Masalah `covid_phase` memecah trend line** → solusi sama dengan WS1:
1. Klik kanan trend line → **Edit Trend Lines**.
2. Uncheck `[ ] Allow a trend line per color`.
3. OK. Trend line jadi 1, titik tetap berwarna.

Lihat `output/BULANAN/analisis/masalah/solusi_masalah.md` Solusi #1.
