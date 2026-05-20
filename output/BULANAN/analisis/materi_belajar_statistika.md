# Materi Belajar Statistika — Roadmap Memahami Analisis Bab 1–5

> **Tujuan dokumen ini**: kamu (dan tim) bisa menjelaskan *kenapa* setiap angka di analisis itu valid, bukan sekadar membaca tabelnya. Disusun dari **metode tersulit → termudah**, masing-masing dengan:
> - **Apa**: definisi singkat
> - **Dipakai di**: WS mana
> - **Rumus / mekanika**: cara hitungnya
> - **Materi prasyarat**: yang harus kamu pelajari supaya paham
> - **Sumber belajar**: rekomendasi (buku/playlist/topik kata kunci)
>
> **Cara pakai**: belajar **dari bawah ke atas**. Tier 8 (paling dasar) wajib dulu. Tanpa rata-rata & varians, regresi tidak akan masuk akal.

---

## Ringkasan Hirarki (Tersulit → Termudah)

| Tier | Metode | Tingkat Kesulitan | WS yang Pakai |
|---:|---|---|---|
| **1** | Stratified / Faceted Regression + Spurious Correlation | ⚫⚫⚫⚫⚫ Pakar | Bab 4 WS1 |
| **2** | Lagged Regression (Distributed Lag) | ⚫⚫⚫⚫ Lanjut | Bab 2 WS4 |
| **3** | Interaction Effect & Subgroup Regression | ⚫⚫⚫⚫ Lanjut | Bab 4 WS6, Bab 5 WS2–3 |
| **4** | Mann-Whitney U Test (Non-parametric) | ⚫⚫⚫ Menengah-Lanjut | Bab 4 WS3, WS4 |
| **5** | OLS Linear Regression (slope, intercept, R², p-value) | ⚫⚫⚫ Menengah | Bab 2 WS1–3, Bab 3 WS1–5, Bab 5 WS2–3 |
| **6** | Pearson Correlation (r) | ⚫⚫ Dasar+ | Hampir semua WS dgn scatter |
| **7** | Group Comparison & Pivot/Heatmap | ⚫⚫ Dasar+ | Bab 1 WS4, Bab 4 WS3–5, Bab 5 WS4 |
| **8** | Descriptive Statistics (mean, median, SD, percentile, range) | ⚫ Dasar | SEMUA WS |
| **9** | Time-Series Visualization & Aggregation | ⚫ Dasar | Bab 1 WS1–3 |

---

## TIER 1 — Stratified / Faceted Regression + Spurious Correlation

### Apa
Regresi dijalankan **secara terpisah** pada tiap **subgrup** (di sini: 4 fase COVID). Tujuannya: cek apakah hubungan A–B yang muncul di data gabungan benar-benar nyata, atau hanya **artefak** dari variabel ketiga yang mempengaruhi keduanya (confounder).

### Dipakai di
- **Bab 4 WS1** — Faceted Scatter per COVID Phase (4 panel: pre_pandemic, lockdown, transisi, recovery)

### Mengapa ini paling sulit
Bukan rumusnya yang sulit (toh tetap regresi linear biasa). Yang sulit adalah **konsep di baliknya**:
- Slope di data gabungan = **+2.294** (positif), tapi setelah dipisah per fase, slope di lockdown jadi **−318** (negatif, sesuai teori). Yang mana yang "benar"?
- Jawabannya: keduanya benar **secara aritmatika**, tapi yang **kausal** adalah yang stratifikasi. Slope positif di data gabungan adalah **spurious correlation** — terjadi karena `kurs` dan `penumpang` sama-sama mengikuti tren waktu pasca-COVID, bukan karena `kurs → penumpang`.

### Mekanika
```python
for phase in ['pre_pandemic', 'lockdown', 'transisi', 'recovery']:
    subset = df[df['covid_phase'] == phase]
    slope, intercept, r, p = linreg(subset['kurs'], subset['pax'])
    # bandingkan slope antar fase
```

### Materi Prasyarat
1. **OLS Linear Regression** (Tier 5)
2. **Konsep Confounder & Causal Inference**:
   - Definisi confounding variable
   - Simpson's Paradox (contoh klasik: ini adalah versi paradoks Simpson)
   - Backdoor criterion (Judea Pearl)
3. **Spurious Correlation** (Granger & Newbold 1974):
   - Dua time series yang sama-sama tren (non-stationary) sering korelasi tinggi *padahal tidak kausal*
4. **Stationarity** (opsional tapi membantu): kenapa time series perlu di-detrend dulu

### Sumber Belajar
- StatQuest YouTube: **"Confounding Variables Clearly Explained"** (Josh Starmer)
- Buku: *Causal Inference: The Mixtape* by Scott Cunningham — Bab 1–2 free online (mixtape.scunning.com)
- Cari di YouTube: **"Simpson's Paradox"**, **"Spurious Correlation Granger Newbold"**
- Untuk depth: 3Blue1Brown — *"But what is statistical inference"*

---

## TIER 2 — Lagged Regression (Distributed Lag)

### Apa
Variabel X **digeser ke belakang** k bulan, lalu diregres ke Y bulan sekarang. Kalau R² lebih tinggi di lag k>0 daripada lag 0, artinya efek X ke Y **butuh waktu** (delayed).

### Dipakai di
- **Bab 2 WS4** — Lag Analysis Kurs → Penumpang (lag 0–6 bulan)

### Mekanika
```python
for k in range(0, 7):
    df['kurs_lag'] = df['kurs'].shift(k)   # kurs k bulan yang lalu
    res = linreg(df['kurs_lag'], df['pax'])
    print(f"lag={k}: R²={res.r2:.3f}")
```

Di Tableau: pakai `LOOKUP(AVG([kurs]), -k)` sebagai *table calculation*.

### Mengapa sulit
1. **Order matters** — kalau urutan baris bukan kronologis, `shift()` / `LOOKUP` akan salah. Di Tableau wajib set *Compute Using = waktu_id Ascending*.
2. **NaN handling** — saat lag=3, 3 baris pertama jadi NaN dan harus di-drop.
3. **Multiple comparisons** — kalau cek 7 lag (0–6), peluang salah satunya kebetulan signifikan naik. Harus hati-hati interpretasi.
4. **Lag confound dengan tren** — kalau dua variabel sama-sama nge-tren, lag berapapun masih positif. Lag analysis paling jujur dilakukan **setelah** kontrol confounder (kombinasi Tier 1).

### Materi Prasyarat
1. **OLS Linear Regression** (Tier 5)
2. **Time Series Basics**:
   - Konsep lag, lead, autocorrelation
   - ACF (autocorrelation function), PACF
3. **Distributed Lag Model (DLM)**:
   - `Y_t = β₀ + β₁ X_t + β₂ X_{t-1} + β₃ X_{t-2} + ...`
   - Cumulative effect = sum dari semua β
4. **Granger Causality** (opsional, lanjut): apakah X "menyebabkan" Y dalam arti X membantu prediksi Y

### Sumber Belajar
- Buku: *Introduction to Econometrics* by Stock & Watson — **Bab "Time Series Regression"** (DLM dijelaskan jelas)
- YouTube: **"Distributed Lag Model"**, **"Lag Operator in Time Series"** (Ben Lambert, marinstatslectures)
- Untuk Tableau LOOKUP: search **"Tableau LOOKUP table calculation tutorial"**

---

## TIER 3 — Interaction Effect & Subgroup Regression

### Apa
Mirip Tier 1, tapi tujuannya bukan kontrol confounder melainkan **membandingkan apakah sensitivitas X → Y berbeda antar subgrup**. Misal: apakah elastisitas kurs → demand lebih tinggi di peak season vs non-peak?

### Dipakai di
- **Bab 4 WS6** — Peak Season vs Non-Peak: slope kurs → pax (3.087 vs 1.841)
- **Bab 5 WS2** — Sensitivitas Internasional per kategori
- **Bab 5 WS3** — Sensitivitas per Negara Destinasi (14 negara, R² 0,25–0,53)

### Mekanika
```python
# Cara 1: subgroup regression (yang dipakai di analisis ini)
for group in ['peak', 'non_peak']:
    subset = df[df['is_peak_season'] == group]
    res = linreg(subset['kurs'], subset['pax'])

# Cara 2 yang lebih advanced: interaction term di regresi
# Y = β₀ + β₁·X + β₂·D + β₃·(X·D)
# β₃ = beda slope antar grup, langsung dengan p-value
```

### Mengapa sulit
1. **Beda slope ≠ otomatis signifikan** — harus uji apakah perbedaannya statistically significant (interaction term test atau Chow test).
2. **Sample size per grup** — kalau salah satu grup n-nya kecil (misal Bab 4 WS1 pre_pandemic n=2), regresinya **tidak valid**.
3. **Interpretasi elastisitas** — slope dengan unit asli (pax per IDR) sulit dibandingkan; pakai *elasticity* `(% Δ Y) / (% Δ X)` lebih informatif.

### Materi Prasyarat
1. **OLS Linear Regression** (Tier 5)
2. **Dummy Variables**: cara encoding kategori jadi 0/1
3. **Interaction Term** dalam regresi: `X * D` notation
4. **Chow Test**: uji formal apakah dua subset punya slope sama
5. **Elasticity** (opsional, ekonomi): `e = (∂Y/Y) / (∂X/X)`

### Sumber Belajar
- Buku: *Introductory Econometrics* by Wooldridge — **Bab "Multiple Regression with Qualitative Information"**
- YouTube: **"Interaction effects in regression"** (StatQuest, Andrew Ng)
- Cari: **"Chow test explained"**, **"dummy variable regression"**

---

## TIER 4 — Mann-Whitney U Test (Non-parametric Hypothesis Test)

### Apa
Uji apakah dua grup punya distribusi yang berbeda **tanpa asumsi normalitas**. Alternatif non-parametric dari t-test.

### Dipakai di
- **Bab 4 WS3** — Median pax per rute: bulan Lebaran vs non-Lebaran (p = 0,697 → tidak signifikan)
- **Bab 4 WS4** — Sama untuk Natal/Desember

### Mengapa pakai ini, bukan t-test?
Data penumpang per rute *right-skewed* — beberapa rute besar (CGK-DPS, dsb) jauh di atas median. Kalau pakai t-test (yang bergantung mean & asumsi normal), hasilnya terdistorsi rute outlier. Mann-Whitney bergantung **rank**, jadi tahan outlier.

### Mekanika
```python
from scipy.stats import mannwhitneyu
group_0 = pax_rute[has_lebaran == 0]
group_1 = pax_rute[has_lebaran == 1]
u, p = mannwhitneyu(group_1, group_0, alternative='greater')
# H0: distribusi sama
# H1: distribusi group_1 lebih besar
# p < 0.05 → tolak H0
```

Cara hitung manual:
1. Gabung semua data dari kedua grup, rank dari kecil ke besar
2. Jumlahkan rank di grup 1 → R₁
3. U₁ = R₁ − n₁(n₁+1)/2
4. Bandingkan U₁ dengan distribusi U (tabel atau approksimasi normal untuk n besar)

### Materi Prasyarat
1. **Konsep hipotesis statistik**: H₀, H₁, alpha, p-value, tipe error I dan II
2. **Distribusi & Normalitas**: histogram, skewness, kurtosis, uji Shapiro-Wilk
3. **Rank Statistics**: median, percentile, IQR
4. **Why non-parametric?**: kenapa t-test bisa gagal saat data tidak normal

### Sumber Belajar
- StatQuest: **"Mann-Whitney U Test, Clearly Explained"** (paling jelas)
- Buku: *Practical Statistics for Data Scientists* by Bruce & Bruce — Bab uji hipotesis
- Cari: **"non-parametric test when to use"**, **"Wilcoxon rank sum test"** (= Mann-Whitney untuk 2 sampel)

---

## TIER 5 — OLS Linear Regression (Slope, Intercept, R², p-value)

### Apa
Model paling pondasi: cari **garis lurus** `Y = β₀ + β₁·X + ε` yang meminimalkan jumlah kuadrat residual (sum of squared errors, SSE). Output: slope, intercept, R², p-value.

### Dipakai di (HAMPIR SEMUA)
- **Bab 2 WS1, WS2, WS3** — Scatter Kurs → Pax (total, INT, DOM)
- **Bab 3 WS1–5** — Channel cost-push & moneter
- **Bab 4 WS1, WS2, WS6** — Faceted, volatilitas, interaksi
- **Bab 5 WS2, WS3** — Sensitivitas per kategori & negara

### Mekanika
```
β₁ = Cov(X, Y) / Var(X)
β₀ = mean(Y) − β₁·mean(X)
R² = 1 − SSE/SST   (proporsi varians yang dijelaskan)
p   = uji apakah β₁ ≠ 0 (t-test)
```

Di Python:
```python
from scipy.stats import linregress
res = linregress(x, y)
# res.slope, res.intercept, res.rvalue (= r), res.pvalue
# R² = res.rvalue ** 2
```

### Interpretasi tiap output
| Output | Arti | Contoh dari Bab 2 WS1 |
|---|---|---|
| Slope (β₁) | "Setiap kenaikan X 1 unit, Y berubah berapa unit" | +2.294 pax per 1 IDR kurs |
| Intercept (β₀) | Nilai Y saat X=0 (sering tidak bermakna fisik) | — |
| R² | % variasi Y yang dijelaskan X | 0,347 → 35% |
| p-value | Probabilitas observasi slope ini kalau β₁ sebenarnya = 0 | <10⁻⁶ → highly significant |

### Asumsi OLS (penting, sering diabaikan)
1. **Linearitas** — hubungan benar-benar lurus (cek dengan scatter)
2. **Independence** — residu tidak autocorrelated (gagal di time series → butuh Tier 2)
3. **Homoscedasticity** — varians residual konstan
4. **Normalitas residual** (untuk inferensi p-value)
5. **No multicollinearity** (di multiple regression)

Kalau asumsi dilanggar (apalagi #2 untuk time series), **p-value tidak reliable**.

### Materi Prasyarat
1. **Korelasi Pearson** (Tier 6)
2. **Varians, Kovarians, Standar Deviasi** (Tier 8)
3. **Least Squares**: kenapa minimalkan SSE, bukan absolute error
4. **Aljabar Linear basic**: matriks `(X'X)⁻¹ X'y` (opsional, tapi membantu untuk multiple regression)
5. **t-distribution** untuk p-value
6. **R² vs adjusted R²**: kenapa R² selalu naik tiap tambah variabel

### Sumber Belajar (WAJIB ditonton)
- **StatQuest "Linear Regression, Clearly Explained"** — fondasi
- **StatQuest "R-squared, Clearly Explained"**
- **StatQuest "p-values, Clearly Explained"** + **"Hypothesis Testing, Clearly Explained"**
- Buku: *Introduction to Statistical Learning* (ISL) — Bab 3 "Linear Regression" (PDF gratis di statlearning.com)
- 3Blue1Brown: *"Essence of Linear Algebra"* untuk geometric intuition

---

## TIER 6 — Pearson Correlation (r)

### Apa
Mengukur **kekuatan & arah** hubungan linear antara dua variabel. Range: −1 (negatif sempurna) sampai +1 (positif sempurna), 0 = tidak ada hubungan linear.

### Dipakai di
- Implisit di semua scatter (R² = r²)
- Bab 5 WS3 di kalkulasi sensitivitas per negara

### Mekanika
```
r = Cov(X, Y) / (σ_X · σ_Y)
  = Σ(xᵢ − x̄)(yᵢ − ȳ) / √[Σ(xᵢ − x̄)² · Σ(yᵢ − ȳ)²]
```

### Properti penting
1. **r tidak bergantung satuan** — kurs dalam IDR atau ribuan IDR, r sama.
2. **r = 0 ≠ no relationship**, hanya berarti tidak ada hubungan *linear*. Bisa ada hubungan kuadratik atau eksponensial.
3. **r² = R²** untuk regresi simple (1 prediktor).
4. **Correlation ≠ causation** — ini mantra wajib (lihat Tier 1).

### Materi Prasyarat
1. **Mean, Varians, Standar Deviasi** (Tier 8)
2. **Kovarians**: ukuran arah co-movement
3. **Standardization (z-score)**: r adalah covariance dari versi standardized

### Sumber Belajar
- StatQuest: **"Pearson's Correlation, Clearly Explained"**
- Khan Academy: **"Correlation coefficient intuition"**
- Cari: **"covariance vs correlation"**, **"correlation does not imply causation"**

---

## TIER 7 — Group Comparison, Pivot & Heatmap

### Apa
Bandingkan **statistik agregat** (mean/median/sum) antara grup. Visualisasi bisa **heatmap** (2D pivot tahun×bulan) atau **bar chart** (1D).

### Dipakai di
- **Bab 1 WS4** — Heatmap seasonal: pivot tahun×bulan menampilkan total penumpang
- **Bab 4 WS3, WS4, WS5** — Bandingkan median pax di bulan Lebaran/Natal/banyak-hari-libur vs lainnya
- **Bab 5 WS4** — OD matrix (Origin × Destination, top kota)
- **Bab 5 WS5** — Top 15 provinsi by total pax

### Mekanika
```python
# Pivot (heatmap)
pivot = df.pivot_table(values='pax', index='tahun', columns='bulan', aggfunc='sum')

# Group comparison (bar)
agg = df.groupby('has_lebaran')['pax'].agg(['median', 'mean', 'sum'])
```

### Yang sering disalahpahami
1. **Mean vs Median** — kalau distribusi skewed (kebanyakan data ekonomi: pax, harga, gaji), median lebih representatif.
2. **Heatmap warna scale** — sequential (urut: putih → biru tua) untuk magnitudo, diverging (biru–putih–merah) untuk deviasi dari nol/baseline.
3. **Sum bisa misleading** — kalau jumlah anggota grup tidak sama, mean/median lebih adil.

### Materi Prasyarat
1. **Descriptive statistics** (Tier 8)
2. **Pivot table logic**: long format vs wide format (`pd.melt`, `pd.pivot_table`)
3. **Aggregation functions**: sum, count, mean, median, var, percentile

### Sumber Belajar
- *Python for Data Analysis* by Wes McKinney — Bab GroupBy & Pivot
- YouTube: **"pandas groupby tutorial"**, **"Tableau heatmap tutorial"**
- Untuk warna heatmap yang benar: cari **"sequential vs diverging color scale"**

---

## TIER 8 — Descriptive Statistics (Fondasi WAJIB)

### Apa
Ringkasan numerik distribusi data. Ini fondasi semua statistik di atasnya — tanpa paham yang ini, semua tier di atas bakal sekadar "pakai library".

### Dipakai di
- **SEMUA WS** punya angka deskriptif (mean kurs, median pax, range Brent, dll)

### Yang wajib dipahami
| Konsep | Rumus | Pakai untuk |
|---|---|---|
| **Mean** (rata-rata) | `μ = Σxᵢ / n` | Pusat distribusi (kalau simetris) |
| **Median** | nilai tengah saat data diurutkan | Pusat (kalau skewed) |
| **Variance** | `σ² = Σ(xᵢ − μ)² / n` | Penyebaran |
| **Standard Deviation** | `σ = √σ²` | Penyebaran dalam unit asli |
| **Percentile / Quartile** | P25, P50 (=median), P75 | IQR, box plot |
| **Range** | max − min | Cepat tapi sensitif outlier |
| **Min, Max** | nilai ekstrem | Spotting outlier |
| **Skewness** | asimetri distribusi | Pilih mean vs median |
| **Kurtosis** | "ketinggian" puncak | Ekstrem event probability |

### Sumber Belajar
- **Khan Academy: Statistics and Probability** (gratis, lengkap)
- StatQuest: playlist **"Statistics Fundamentals"** (semua video <15 menit, satu konsep per video)
- Buku populer: *Naked Statistics* by Charles Wheelan (bacaan ringan untuk intuisi)

---

## TIER 9 — Time-Series Visualization & Aggregation (Tanpa Statistik)

### Apa
Murni penyajian data mentah dalam **garis waktu**. Tidak ada perhitungan statistik — tapi pondasi visual untuk semua bab.

### Dipakai di
- **Bab 1 WS1** — Multi-panel time series (4 indikator: pax, kurs, Brent, BI rate)
- **Bab 1 WS2** — Kurs band (min–max range tiap bulan)
- **Bab 1 WS3** — Inflasi & COVID phase reference

### Yang harus dipahami
1. **Continuous vs Discrete axis** (Tableau): pil hijau (continuous) vs biru (discrete) — ini sering bikin chart kacau kalau salah.
2. **Aggregation level** — data harian vs mingguan vs bulanan. Di sini semua sudah bulanan (60 titik per indikator).
3. **Reference line / annotation** — garis vertikal untuk event eksternal (PSBB, Russia-Ukraine, dst.) supaya audience bisa link visual ke konteks.

### Materi Prasyarat
- Hanya **dasar visualisasi** (sumbu X/Y, legend, axis label).
- Pemahaman dasar **waktu** sebagai variabel kontinu.

### Sumber Belajar
- Buku: *Fundamentals of Data Visualization* by Claus Wilke (gratis online: clauswilke.com/dataviz)
- YouTube: **"Tableau time series tutorial"**
- Edward Tufte — prinsip data-ink ratio (untuk wawasan estetika)

---

## Roadmap Belajar (Untuk Tim 5 Orang)

### Minggu 1 — Fondasi (Tier 8 + 9)
- Tonton StatQuest *"Statistics Fundamentals"* playlist
- Latihan: hitung manual mean/median/SD untuk 10 angka, lalu cek dengan `df.describe()`
- Buat 1 time-series chart di Tableau dari scratch

### Minggu 2 — Korelasi & Regresi (Tier 6 + 5)
- StatQuest *"Pearson Correlation"* + *"Linear Regression"* + *"R-squared"* + *"p-values"*
- Latihan: replikasi metrik Bab 2 WS1 (slope=+2.294, R²=0,347) di Excel atau scipy
- Pahami **mengapa slope positif itu spurious** (linkkan ke Tier 1)

### Minggu 3 — Group Comparison & Non-parametric (Tier 7 + 4)
- StatQuest *"Mann-Whitney U Test"*
- Latihan: hitung manual median pax has_lebaran=0 vs 1 dari `summary.csv` Bab 4 WS3
- Buat heatmap seasonal di Tableau (replikasi Bab 1 WS4)

### Minggu 4 — Interaction & Lag (Tier 3 + 2)
- Tonton: **"Distributed Lag Model"**, **"Interaction effects in regression"**
- Latihan: implementasi LOOKUP lag di Tableau (Bab 2 WS4)
- Bandingkan slope peak vs non-peak (Bab 4 WS6)

### Minggu 5 — Faceted Regression & Causal Thinking (Tier 1)
- Tonton: **"Simpson's Paradox"**, **"Confounding variables"**
- Baca: *Causal Inference: The Mixtape* — Bab 1 (gratis)
- Latihan: jelaskan ke teman kenapa slope +2.294 jadi −318 di lockdown — itu bukan kebetulan, itu **pesan utama paper**

---

## Daftar Sumber Konsolidasi

### Video (Gratis, Wajib)
- **StatQuest with Josh Starmer** (YouTube) — paling jelas untuk pemula
- **3Blue1Brown** — visual intuition (Probability, Linear Algebra)
- **Ben Lambert** — econometrics serius tapi friendly
- **MarinStatsLectures** — R + statistika dasar

### Buku PDF Gratis Legal
| Buku | Topik | Link |
|---|---|---|
| *Introduction to Statistical Learning* (ISL) | Regression, classification, all-around | statlearning.com |
| *Causal Inference: The Mixtape* | Tier 1 (confounder, DAG, IV) | mixtape.scunning.com |
| *Forecasting: Principles and Practice* | Time series (Tier 2) | otexts.com/fpp3 |
| *Practical Statistics for Data Scientists* | Tier 4–7 | Tersedia di O'Reilly |
| *Fundamentals of Data Visualization* | Tier 9 | clauswilke.com/dataviz |

### Buku Berbayar (Rekomendasi)
- *Naked Statistics* by Charles Wheelan — bacaan santai
- *Introductory Econometrics* by Wooldridge — referensi standar Indonesia/dunia
- *Mostly Harmless Econometrics* by Angrist & Pischke — causal inference lanjut

### Khan Academy (Gratis)
- **Statistics and Probability** — full course, bahasa Inggris tapi banyak subtitle Indonesia

---

## Cara Cek Pemahaman Sebelum Sidang

Tim wajib bisa menjawab 8 pertanyaan ini *tanpa* membuka catatan:

1. **Apa beda korelasi dan regresi?** *(Tier 5–6)*
2. **Apa arti R² = 0,35?** *(Tier 5)*
3. **Kenapa p-value < 0,05 = "signifikan"?** *(Tier 4)*
4. **Kenapa slope kurs–pax di data gabungan +2.294 tapi di lockdown −318?** *(Tier 1)*
5. **Kenapa pakai Mann-Whitney bukan t-test untuk Lebaran?** *(Tier 4)*
6. **Apa beda lag 0 dan lag 3? Mengapa lag 3 R²-nya lebih tinggi?** *(Tier 2)*
7. **Apa beda sensitivitas peak vs non-peak season? Apa interpretasi ekonominya?** *(Tier 3)*
8. **Kenapa Brent IDR berlipat 4× lipat tapi R² kurs→Brent IDR cuma 0,12?** *(Tier 5 + decomposition)*

Kalau **5 orang anggota tim** masing-masing bisa jawab 8 ini dengan bahasa sendiri, kalian siap presentasi.

---

## Catatan Akhir

Statistika di proyek ini sengaja dipilih yang **fundamental tapi powerful**. Tidak ada yang pakai deep learning atau Bayesian advanced — semua bisa dijelaskan dengan kalkulus SMA + intuisi geometri. Yang membedakan analisis kelompok kalian dari analisis "asal regresi" adalah:

- Kalian **sadar spurious correlation** (Bab 4 WS1) dan tidak over-claim.
- Kalian **stratifikasi** dan **kontrol confounder** (Tier 1, 3).
- Kalian **uji robustness** dengan multiple specifications (Bab 4).
- Kalian **transparan tentang asumsi & limitasi** (Mann-Whitney di Bab 4 WS3 tidak signifikan — kalian *lapor*, bukan sembunyi).

Itu lebih bernilai dari pada laporan dengan 20 model fancy tapi tanpa pemahaman.
