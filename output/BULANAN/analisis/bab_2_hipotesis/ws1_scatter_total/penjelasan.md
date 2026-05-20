# Bab 2 / WS1 — Scatter Kurs × Total Penumpang

## Tujuan
Menguji hipotesis utama: apakah ada hubungan signifikan antara kurs IDR/USD dan jumlah penumpang nasional?

## Pendekatan
**Scatter plot + OLS linear regression**. Setiap titik = satu bulan (60 titik). Sumbu X = kurs, sumbu Y = total penumpang. Trend line linear dan koefisien dihitung untuk mendapat *slope*, *R²*, dan *p-value*.

## Perhitungan
Model: `y = a + b·x + ε`
dimana:
- `y` = jumlah penumpang (orang)
- `x` = kurs (IDR/USD)
- `b` = slope (berapa penumpang berubah per 1 IDR pelemahan kurs)
- `a` = intercept (penumpang teoritis jika kurs = 0, biasanya tidak interpretable)

Pearson correlation: `r = Cov(x,y) / (σ_x · σ_y)`
R² = `r²` = proporsi variasi y yang dijelaskan oleh x.
p-value: probabilitas slope = 0 (no relationship) dari uji t.

```python
from scipy import stats
res = stats.linregress(x, y)
# res.slope, res.intercept, res.rvalue, res.pvalue
```

## Hasil dari Data Kamu

| Metrik | Nilai | Interpretasi |
|---|---:|---|
| Slope | **+2.294** | Setiap pelemahan kurs 1 IDR, penumpang **bertambah** 2.294 orang |
| R² | 0,347 | 35% variasi penumpang dijelaskan oleh kurs |
| Pearson r | +0,589 | Korelasi positif moderate |
| p-value | 7,3 × 10⁻⁷ | **Sangat signifikan** (p < 0,001) |
| n | 60 | 60 bulan observasi |

## Makna Angka — TWIST PENTING!

**Slope-nya POSITIF**, padahal teori ekonomi memprediksi **NEGATIF** (kurs melemah → tiket mahal → demand turun).

### Kenapa demikian?

Karena hubungan didominasi oleh **structural break COVID**, bukan elastisitas kurs:
- **Jan 2020** (pre-COVID): kurs RENDAH (13.732) DAN penumpang TINGGI (9,12 juta).
- **Apr 2020** (lockdown): kurs LEBIH TINGGI (15.867) DAN penumpang COLLAPSE (980 ribu).
- **2023–2024** (recovery): kurs TERUS NAIK (15.000–16.300) tapi penumpang juga TERUS NAIK (8 juta/bulan).

Di scatter, titik-titik recovery (warna hijau) ada di pojok kanan atas (kurs tinggi & pax tinggi). Titik-titik lockdown (merah) di pojok kanan bawah (kurs tinggi & pax rendah). Trend line linear melewati keduanya → slope jadi positif karena recovery dominan jumlah datanya (24 bulan vs lockdown 19 bulan).

### Ini adalah ***spurious correlation*** klasik

Penyebab sebenarnya = "waktu" / "fase COVID". Karena kebetulan kurs cenderung naik bersamaan dengan periode recovery (lewat banyak alasan independen: kebijakan moneter global, geopolitik, dll), dan penumpang juga naik di periode yang sama (karena reopening), keduanya **tampak berkorelasi positif** padahal tidak ada hubungan kausal langsung dalam arah itu.

**Implikasi:** angka R²=0,35 dan slope positif di scatter naive **tidak boleh disimpulkan sebagai "kurs meningkatkan demand"**. Kita harus mengontrol COVID phase → ini job Bab 4.

## Output
- `plot.png` — scatter dengan warna covid_phase
- `metrics.txt` — slope/r²/p-value

## Target Tableau — Step by Step

### Langkah Pembuatan Sheet
1. **Buat worksheet baru**, beri nama `Bab2_WS1_ScatterTotal`.
2. **Drag `avg_kurs_tengah` ke Columns**. Pil harus hijau dan bertuliskan `AVG(avg_kurs_tengah)`. Kalau masih SUM, klik kanan pil → Measure → Average.
3. **Drag `jumlah_penumpang` ke Rows**. Pil hijau `SUM(jumlah_penumpang)`. Tetap SUM (additive).
4. **Pecah titik per bulan**:
   - Drag `waktu_id` ke kotak **Detail** di Marks card.
   - Klik kanan pil `waktu_id` yang baru muncul di Marks card → pilih **Dimension** (jangan Measure/SUM). Pil berubah jadi biru.
   - Layar akan langsung menyebar dari 1 titik jadi **60 titik** (1 per bulan).
5. **Pilih Marks Card → Circle** (dropdown atas).
6. **Drag `covid_phase` ke Color** di Marks card. Tableau akan otomatis assign 4 warna untuk 4 fase.
7. **Tambah Trend Line**:
   - Buka tab **Analytics** (kiri atas, sebelah Data).
   - Drag **Trend Line** ke chart, lepaskan di opsi **Linear**.
   - Tableau akan menggambar garis tren linear.
8. **Lihat R² dan slope**: hover mouse ke garis Trend Line → tooltip akan muncul:
   - **R-Squared: 0.347**
   - **p-value: < 0.0001**
   - Formula: `jumlah_penumpang = 2294.47 * avg_kurs_tengah + -28983655`
9. **Annotation manual** (untuk presentasi): klik kanan area kosong di chart → Annotate → Area → ketik "R² = 0,347 | Slope = +2.294 pax/IDR | p < 10⁻⁶".

### Cross-check ke Python
File `metrics.txt` di folder ini:
- slope = **2.294,47** ✓
- R-squared = **0,3471** ✓
- p-value = **0,000001** ✓

Kalau angka di Tableau berbeda jauh, kemungkinan:
- `avg_kurs_tengah` masih SUM (bukan AVG) → cek Step 2.
- `waktu_id` masih Measure (bukan Dimension) → cek Step 4. Hanya akan ada 1 titik kalau Measure.
- Join data source rusak → cek Tableau Data Source page.

### Catatan untuk Paper
Slope **POSITIF** (+2.294) di chart ini adalah finding *counter-intuitive* yang nanti dijelaskan di Bab 4 sebagai *spurious correlation* karena COVID. Saat presentasi, JANGAN langsung klaim "kurs naik → pax naik" — ini titik *intellectual hook* yang akan di-resolve di Bab 4.
