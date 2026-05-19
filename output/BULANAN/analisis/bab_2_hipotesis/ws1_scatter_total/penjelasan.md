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

## Target Tableau
- Columns: `AVG(avg_kurs_tengah)`
- Rows: `SUM(jumlah_penumpang)`
- Detail: `waktu_id` (Dimension)
- Color: `covid_phase`
- Trend Line: Linear (drag dari Analytics pane)

Tableau akan menampilkan R²=0,347 dan p<0,001 di tooltip trend line.

**Cek match dengan Python**: slope di Tableau harus persis 2.294,47 dan R² = 0,347.
