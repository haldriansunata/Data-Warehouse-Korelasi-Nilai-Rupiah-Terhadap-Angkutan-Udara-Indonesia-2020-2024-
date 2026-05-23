# Bab 2 / WS2 — Scatter Kurs × Penumpang INTERNASIONAL

## Tujuan
Apakah hubungan kurs–penumpang lebih kuat di segmen INTERNASIONAL dibanding total/domestik? Secara teori harusnya iya, karena tiket INT dalam USD.

## Pendekatan
Sama dengan WS1 (OLS linear regression + scatter), tapi data difilter ke rute `kategori = INTERNASIONAL` saja sebelum agregat bulanan.

## Hasil

| Metrik | Nilai | vs Total (WS1) |
|---|---:|---|
| Slope | +1.176 pax/IDR | Lebih kecil dalam magnitude absolut |
| **R²** | **0,486** | **Lebih tinggi dari Total (0,347)** ✓ |
| Pearson r | +0,697 | Lebih kuat |
| p-value | 6 × 10⁻¹⁰ | Lebih signifikan |
| n | 60 | sama |

## Makna Angka

- **R² lebih tinggi (0,49 vs 0,35)** = pergerakan kurs lebih banyak menjelaskan variasi penumpang INT daripada penumpang total. Ini *konsisten dengan teori* meskipun arahnya masih spurious.
- **Slope positif lagi** = artefak COVID yang sama (lockdown menutup penerbangan internasional, recovery membukanya — bersamaan dengan tren depresiasi rupiah).

### Insight tambahan
Travel internasional **lebih sensitif terhadap rezim COVID** daripada domestik:
- Saat lockdown (Mar 2020–Sep 2021), penerbangan INT hampir mati total (pembatasan VOA).
- Saat reopening (Mei 2022), demand INT meledak.

Itu sebabnya R² INT > Total — karena COVID mempengaruhi INT lebih ekstrem daripada DOM, sehingga COVID-as-confounder menghasilkan korelasi yang lebih ketat (semu) di INT.

## Output
- `plot.png`, `metrics.txt`

## Target Tableau — Step by Step

### Langkah Pembuatan Sheet
1. **Klik kanan tab worksheet `Bab2_WS1_ScatterTotal` → Duplicate**. Rename hasil duplikat menjadi `Bab2_WS2_ScatterINT`.
2. **Tambah filter kategori**:
   - Drag `kategori` (dari Data pane → dim_rute) ke kotak **Filters**.
   - Di dialog yang muncul, centang **hanya `INTERNASIONAL`** → OK.
3. **Update title sheet**: klik 2× di title chart → ubah ke "Scatter Kurs × Penumpang INTERNASIONAL".
4. **Lihat R² baru**: hover ke trend line → tooltip akan tampilkan R² yang berbeda.

### Cross-check ke Python
File `metrics.txt`:
- slope = **1.175,53**
- R-squared = **0,4862**
- p-value = **6 × 10⁻¹⁰**
- Pearson r = **0,6973**

**R² lebih tinggi dari WS1 (0,49 vs 0,35)** — segmen internasional memang lebih sensitif terhadap dinamika makro/COVID.

### Catatan Khusus
- Filter `kategori = INTERNASIONAL` akan mempengaruhi `SUM(jumlah_penumpang)` saja, tidak mempengaruhi `AVG(avg_kurs_tengah)` (karena kurs sama untuk semua rute di bulan tersebut).
- Slope tetap **POSITIF** (+1.176) — spurious yang sama, akan dijelaskan di Bab 4.

---

## ⚙️ Update — Catatan Implementasi Tableau

**Masalah `covid_phase` memecah trend line** → solusi sama dengan WS1:
1. Klik kanan trend line → **Edit Trend Lines**.
2. Uncheck `[ ] Allow a trend line per color`.
3. OK. Trend line jadi 1, titik tetap berwarna.

Lihat `output/BULANAN/analisis/masalah/solusi_masalah.md` Solusi #1.
