# Korelasi Nilai Tukar Rupiah Terhadap Permintaan Angkutan Udara Indonesia: Analisis Data Warehouse Bulanan 2020–2024

**Penyusun:** Kelompok Data Warehouse (5 anggota)
**Periode Data:** Januari 2020 – Desember 2024 (60 bulan)
**Mata Kuliah / Tema:** Data Warehouse — Analisis Korelasi Makroekonomi terhadap Sektor Transportasi Udara

---

## Abstrak

Penelitian ini menguji hubungan antara nilai tukar Rupiah terhadap Dolar AS (IDR/USD) dan permintaan angkutan udara di Indonesia selama periode 2020–2024, menggunakan data warehouse bulanan yang menggabungkan data Direktorat Jenderal Perhubungan Udara (DJPU), Bank Indonesia, Badan Pusat Statistik (BPS), dan Brent crude oil. Data warehouse dibangun dengan skema star (1 tabel fakta utama × 4 dimensi), dengan grain bulanan-per-rute (17.118 baris fakta dari 60 bulan × 553 rute). Analisis dilakukan dalam lima bab: (1) deskripsi konteks makro, (2) korelasi naive kurs–penumpang, (3) mekanisme transmisi multi-channel (cost-push, moneter, daya beli), (4) kontrol confounder (fase COVID dan musiman), serta (5) heterogenitas geografis per rute, negara, dan provinsi.

Temuan utama menunjukkan bahwa korelasi naive kurs–penumpang **bertanda positif dan signifikan** (slope +2.294 penumpang per 1 IDR pelemahan, R² = 0,347, p < 10⁻⁶), arah yang berlawanan dengan prediksi teori ekonomi. Setelah kontrol fase COVID, slope ini terbukti merupakan **artefak structural break pandemi**, bukan hubungan kausal. Di antara tiga channel transmisi yang diuji, channel **moneter (kurs → BI Rate)** menunjukkan korelasi paling kuat (R² = 0,645) dengan arah sesuai teori, sementara channel daya beli (kurs → inflasi umum) tidak signifikan (R² = 0,074). Analisis heterogenitas mengungkap bahwa rute internasional ke ASEAN didorong oleh volume dan responsif terhadap dinamika makro, sementara rute ke Arab Saudi (R² = 0,25) dan Jepang (R² = 0,33) lebih dipengaruhi faktor non-kurs (kuota haji, kebijakan visa). Penelitian merekomendasikan agar stabilisasi rupiah via kebijakan moneter dijadikan prioritas dibanding intervensi cost-push, dengan pendekatan kebijakan yang dibedakan per koridor geografis.

**Kata Kunci:** nilai tukar, permintaan angkutan udara, data warehouse, channel transmisi, COVID-19, spurious correlation, Indonesia.

---

## 1. Pendahuluan

### 1.1 Latar Belakang

Periode 2020–2024 merupakan periode yang ekstrem secara struktural bagi sektor transportasi udara Indonesia. Pandemi COVID-19 menyebabkan kontraksi historis pada permintaan penerbangan (BPS, 2024), sementara nilai tukar Rupiah terhadap Dolar AS terdepresiasi sekitar 19% dari Rp 13.732 (rata-rata Januari 2020) ke Rp 16.329 (rata-rata Desember 2024). Secara bersamaan, harga minyak mentah dunia mengalami dua guncangan besar: anjlok ke USD 26 per barel pada April 2020 akibat kolaps permintaan global, lalu melonjak ke USD 116 per barel pada Juni 2022 pasca-invasi Rusia ke Ukraina (Investing.com, 2024).

Bagi industri penerbangan, ketiga dinamika ini saling terkait. Avtur (jet fuel) — yang secara global di-denominasi dalam USD — menyumbang sekitar 40% biaya operasi maskapai (INACA, 2024). Ketika rupiah melemah dan harga minyak mentah naik, biaya operasi maskapai dalam Rupiah mengalami *double-shock*. Direktur Utama Garuda Indonesia pada 2024 mengakui bahwa tarif batas atas yang ditetapkan tahun 2019 — saat asumsi harga avtur Rp 9.000 per liter dan kurs Rp 14.200/USD — sudah tidak relevan dengan kondisi 2024 (Rakyat Merdeka, 2024). Sementara itu, Bank Indonesia merespon depresiasi rupiah dengan menaikkan suku bunga acuan (BI Rate) dari 3,5% pada periode pandemi menjadi 6,25% pada akhir 2024.

Pertanyaan kritis yang muncul: **bagaimana sebenarnya pengaruh pelemahan rupiah terhadap permintaan angkutan udara di Indonesia?** Apakah pelemahan kurs menekan demand (sesuai prediksi teori ekonomi), dan jika ya, lewat jalur transmisi apa? Penelitian ini menjawab pertanyaan tersebut menggunakan data warehouse bulanan yang menggabungkan data operasional penerbangan dan indikator makroekonomi.

### 1.2 Rumusan Masalah

1. Apakah terdapat hubungan signifikan antara level kurs IDR/USD dan jumlah penumpang angkutan udara Indonesia pada periode 2020–2024?
2. Lewat jalur transmisi (channel) apa pengaruh kurs sampai ke permintaan penumpang? Apakah didominasi oleh channel *cost-push* (kenaikan biaya bahan bakar), channel moneter (respons BI Rate), atau channel daya beli (inflasi)?
3. Apakah korelasi yang ditemukan tetap robust setelah dikontrol untuk confounder utama yaitu fase pandemi COVID-19 dan pola musiman (Lebaran, Natal, hari libur)?
4. Apakah terdapat heterogenitas geografis dalam respons permintaan terhadap kurs — antara segmen domestik dan internasional, antar rute, antar negara destinasi, dan antar provinsi origin?

### 1.3 Tujuan Penelitian

Penelitian ini bertujuan untuk:
1. Menguji secara statistik hubungan antara nilai tukar rupiah dan permintaan angkutan udara Indonesia.
2. Mengidentifikasi channel transmisi dominan dari kurs ke permintaan.
3. Memverifikasi robustness korelasi setelah kontrol fase COVID dan pola musiman.
4. Memetakan heterogenitas geografis untuk memberikan implikasi kebijakan yang berbeda per segmen.

### 1.4 Manfaat

**Akademik:** Menambah literatur empiris tentang transmisi makroekonomi ke sektor transportasi udara Indonesia, dengan fokus pada periode COVID-19 yang belum banyak dianalisis dalam framework data warehouse.

**Praktis:** Memberikan rekomendasi berbasis bukti bagi regulator (Kemenhub, BI) dan operator maskapai mengenai kebijakan tarif, hedging bahan bakar, dan strategi koridor.

---

## 2. Tinjauan Pustaka

### 2.1 Teori Exchange Rate Pass-through

*Exchange rate pass-through* (ERPT) adalah proses transmisi perubahan nilai tukar ke harga domestik (Goldberg & Knetter, 1997). Untuk barang impor atau barang dengan komponen impor tinggi, depresiasi mata uang lokal akan menaikkan harga dalam mata uang lokal. Untuk Indonesia, pass-through kurs ke inflasi umum secara historis lemah hingga moderat (10–20% dalam jangka panjang), karena banyak harga diatur (BBM bersubsidi, listrik, beras).

Namun untuk sektor yang sangat ter-dolarisasi seperti aviasi (bahan bakar, leasing pesawat, perawatan), pass-through diperkirakan lebih tinggi.

### 2.2 Elastisitas Demand Transportasi Udara

Literatur internasional umumnya menemukan elastisitas pendapatan permintaan angkutan udara sebesar 1,5–2,0 (IATA, 2023), artinya kenaikan pendapatan 1% mendorong demand 1,5–2,0%. Elastisitas harga (tiket) berkisar −0,5 hingga −1,5 tergantung segmen: leisure lebih elastis (−1,0 sampai −1,5), business kurang elastis (−0,3 sampai −0,5).

### 2.3 Channel Transmisi Makro ke Demand Transport

Tiga channel teoritis menghubungkan kurs ke permintaan transportasi udara:

1. **Channel Cost-push (Biaya Bahan Bakar):** Pelemahan kurs → biaya bahan bakar penerbangan dalam IDR naik → harga tiket naik → demand turun. Bahan bakar penerbangan (avtur) di Indonesia secara struktural mengikuti harga minyak mentah dunia (Brent crude oil), dan diperdagangkan dalam USD.

2. **Channel Moneter (Suku Bunga):** Pelemahan kurs → BI menaikkan suku bunga acuan untuk *defend* rupiah → biaya kapital naik, kredit konsumtif lebih mahal → daya beli diskresioner (termasuk travel) tertekan.

3. **Channel Daya Beli (Inflasi):** Pelemahan kurs → inflasi umum naik (lewat barang impor) → real income turun → konsumsi diskresioner termasuk travel turun.

### 2.4 COVID-19 dan Sektor Penerbangan Indonesia

ICAO (2022) mencatat bahwa COVID-19 menyebabkan kontraksi terbesar dalam sejarah aviasi global. Di Indonesia, periode 2020–2022 ditandai oleh tiga rezim kebijakan: PSBB (April 2020), PPKM bertingkat (2021), dan PPKM Darurat (Juli–September 2021) akibat varian Delta. Pencabutan resmi PPKM dilakukan pada Januari 2023.

BPS (2024) melaporkan recovery asimetris: penumpang domestik 2024 mencapai 63,69 juta (sekitar 80% baseline 2019 yang 79,5 juta), sementara penumpang internasional tumbuh 21,46% menjadi 19 juta dari 15,64 juta pada 2023, masih dalam fase recovery agresif.

### 2.5 Spurious Correlation dan Confounder

Granger & Newbold (1974) memperingatkan bahaya *spurious correlation* dalam analisis time-series ketika dua variabel sama-sama mengikuti tren yang sama (misalnya tren waktu atau struktural break). Untuk periode 2020–2024 di Indonesia, COVID-19 adalah *structural break* yang berpotensi menghasilkan korelasi semu antara variabel makro dan demand transportasi. Kontrol fase COVID melalui faceted regression menjadi kebutuhan metodologis penelitian ini.

---

## 3. Data dan Metodologi

### 3.1 Sumber Data

| Sumber | Data | Periode |
|---|---|---|
| DJPU (Direktorat Jenderal Perhubungan Udara) | Jumlah penumpang per rute bulanan (BAB VI); daftar rute dan bandara (BAB III) | 2020–2024 |
| Bank Indonesia | Kurs Transaksi Rupiah (harian, di-agregat bulanan); Data Inflasi YoY (xlsx) | 2020–2024 |
| BPS (Badan Pusat Statistik) | BI Rate bulanan; Inflasi MtM nasional; Survei Harga Konsumen (indeks tarif tiket) | 2020–2024 |
| Investing.com | Brent Crude Oil futures (close, high, low bulanan) | 2020–2024 |

### 3.2 ETL Pipeline

Pipeline ETL ditulis dalam Python (folder `output/BULANAN/etl_bulanan/`) dengan urutan:

```
01_dim_waktu.py            → _tmp/dim_waktu_bulanan.csv (basic 60 baris)
05_fact_kurs.py            → _tmp/fact_kurs_bulanan.csv (agregasi harian → bulanan)
03_dim_bandara.py          → BULANAN/dim_bandara.csv (232 IATA, dengan CITY_OVERRIDES manual)
04_dim_rute.py             → BULANAN/dim_rute.csv (553 rute dengan FK ke dim_bandara)
06_fact_penumpang_rute.py  → BULANAN/fact_penumpang_rute.csv (17.118 baris)
build_makro_warehouse.py   → BULANAN/fact_makro_bulanan.csv + enrich dim_waktu (covid_phase, has_lebaran, dll)
```

### 3.3 Skema Data Warehouse

Skema *star* dengan satu tabel fakta utama dan empat dimensi:

```
                       dim_waktu_bulanan
                            │ (waktu_id)
                            ▼
dim_bandara ◄── dim_rute ◄── fact_penumpang_rute ──► fact_makro_bulanan
   (bandara_id)  (rute_id)   (grain: waktu_id × rute_id)   (grain: waktu_id)
```

**Tabel utama:**
- `fact_penumpang_rute` (17.118 baris): variabel utama `jumlah_penumpang`.
- `fact_makro_bulanan` (60 baris): variabel makro per bulan (kurs, Brent, BI rate, inflasi, tarif tiket IHK).
- `dim_waktu_bulanan` (60 baris): atribut waktu termasuk `covid_phase`, `has_lebaran`, `has_natal`, `is_peak_season`, `jumlah_hari_libur`.
- `dim_rute` (553 baris): pasangan IATA dan `kategori` (DOMESTIK/INTERNASIONAL).
- `dim_bandara` (232 baris): nama, IATA, kota, provinsi, negara.

### 3.4 Variabel dan Catatan Proxy

| Variabel | Satuan | Catatan |
|---|---|---|
| `jumlah_penumpang` | Orang | Outcome utama; additive (SUM) |
| `avg_kurs_tengah` | IDR per 1 USD | Variabel X utama |
| `min_kurs_tengah`, `max_kurs_tengah` | IDR | Untuk hitung spread (volatilitas) |
| `brent_usd_bbl` | **USD** per barrel | **Proxy *upstream* biaya bahan bakar penerbangan**. Penelitian ini *tidak memiliki* data harga avtur (jet fuel/Jet A-1) langsung. Avtur disuling dari crude oil sehingga harga avtur berkorelasi ~80–90% dengan Brent dengan lag 1–2 bulan. Sesuai literatur transportasi udara, Brent × FX dipakai sebagai proxy upstream ketika data avtur langsung tidak tersedia. |
| `tarif_tiket_ihk` | Indeks (base 100) | Indeks Harga Konsumen tarif pesawat dari BPS |
| `bi_rate` | % per tahun | Suku bunga acuan BI |
| `inflasi_yoy` | % per tahun | Inflasi umum tahun-ke-tahun (Data BI) |
| `inflasi_mtm` | % per bulan | Inflasi month-to-month (BPS) |
| `covid_phase` | Kategori | 4 fase: pre_pandemic (Jan–Feb 2020), lockdown (Mar 2020–Sep 2021), transisi (Okt 2021–Des 2022), recovery (Jan 2023–Des 2024) |

**Catatan limitasi data avtur:** Channel cost-push diuji sebagai `kurs → Brent IDR → tarif tiket IHK → penumpang`. Step intermediate "harga avtur Indonesia" tidak diuji langsung karena tidak ada data dalam dataset. Brent dipakai sebagai proxy upstream, bukan sebagai substitusi avtur Indonesia.

### 3.5 Metode Analisis

1. **Regresi linear OLS** (Ordinary Least Squares): `y = a + bx + ε`, dihitung dengan `scipy.stats.linregress`. Output: slope (b), intercept (a), Pearson r, R², p-value.
2. **Pearson correlation** untuk menilai kekuatan dan arah asosiasi.
3. **Mann-Whitney U test** (non-parametric) untuk membandingkan distribusi penumpang antara kelompok binary (Lebaran vs non-Lebaran, Natal vs non-Natal).
4. **Lag analysis**: regresi `penumpang(t) ~ kurs(t-k)` untuk k = 0, 1, …, 6 bulan, untuk mengidentifikasi lag dominan.
5. **Faceted regression**: regresi terpisah per `covid_phase` untuk mengontrol structural break.
6. **Heterogeneity analysis**: regresi terpisah per rute internasional dan per negara destinasi.

Semua analisis dijalankan di Python (pandas, numpy, scipy) dan divisualisasikan di Tableau setelah cross-check numerik. Output Python tersedia di `output/BULANAN/analisis/`.

---

## 4. Hasil dan Pembahasan

### 4.1 Konteks Makro × Demand 2020–2024

#### 4.1.1 Indikator Makro

Tabel 4.1 menyajikan range nilai indikator inti selama 60 bulan analisis.

**Tabel 4.1. Range Indikator Makro 2020–2024**

| Indikator | Min | Max | Bulan Min | Bulan Max |
|---|---:|---:|---|---|
| Kurs Tengah (IDR/USD) | 13.732 | 16.329 | Jan 2020 | Des 2024 |
| Spread Kurs (IDR) | ~50 | **2.440** | Bulan tenang | **Mar 2020** |
| Brent (USD/bbl) | 26,35 | 115,60 | Apr 2020 (oil crash) | Jun 2022 (Russia–Ukraine) |
| BI Rate (%) | 3,50 | 6,25 | Era PPKM 2021 | Akhir 2024 |
| Inflasi YoY (%) | 1,32 | 5,95 | 2021 | 2022 transisi |

Kurs mengalami pelemahan struktural 19% (13.732 → 16.329) selama 5 tahun. Spread kurs (max−min harian dalam satu bulan) sebagai proksi volatilitas mencapai puncak 2.440 IDR pada Maret 2020 — bulan kepanikan pasar awal pandemi. Brent crude oil mengalami dua guncangan ekstrem: anjlok 53% (Jan→Apr 2020) lalu melonjak 339% (Apr 2020 → Jun 2022). BI Rate mengalami siklus *easing* (5% → 3,5% pada periode lockdown sebagai stimulus) lalu *tightening* agresif (3,5% → 6,25% pada periode recovery untuk *defend* rupiah).

#### 4.1.2 Demand Penumpang

Total penumpang bulanan menunjukkan struktur tiga rezim yang ekstrem (Tabel 4.2):

**Tabel 4.2. Total Penumpang Bulanan (juta) per Tahun**

| | Jan | Feb | Mar | Apr | Mei | Jun | Jul | Agu | Sep | Okt | Nov | Des |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **2020** | **9,12** | 7,76 | 5,51 | 0,98 | **0,10** | 0,75 | 1,71 | 2,34 | 2,11 | 2,48 | 3,24 | 3,72 |
| **2021** | 2,60 | 2,14 | 2,91 | 3,19 | 2,76 | 3,94 | **1,18** | 1,32 | 2,14 | 3,26 | 3,97 | 4,49 |
| **2022** | 3,70 | 3,08 | 3,96 | 4,24 | 6,02 | 5,39 | 5,72 | 4,94 | 4,58 | 5,51 | 5,32 | 6,51 |
| **2023** | 6,83 | 6,28 | 6,87 | 7,11 | 8,09 | 7,89 | 8,69 | 7,89 | 7,58 | 7,96 | 7,67 | 8,26 |
| **2024** | 7,56 | 7,06 | 7,01 | 8,58 | 8,01 | 8,23 | **9,03** | 8,65 | 8,48 | 8,29 | 7,71 | **8,98** |

Demand kolaps dari **9,12 juta** (Jan 2020, pre-pandemi) ke **96.452** orang (Mei 2020, lockdown puncak) — penurunan 98,9% dalam empat bulan. Recovery terjadi bertahap, mencapai *near-baseline* (8–9 juta/bulan) pada 2024. Tabel ini juga memvalidasi pola musiman yang konsisten: spike di bulan Lebaran (Mei 2020–2022, April 2023–2024) dan Desember (Natal + Tahun Baru).

### 4.2 Hipotesis Utama: Korelasi Naive Kurs–Penumpang

#### 4.2.1 Regresi Linear Naive

Untuk menguji hipotesis utama bahwa pelemahan kurs menekan permintaan penumpang, kami menjalankan regresi `jumlah_penumpang ~ avg_kurs_tengah` untuk total penumpang, segmen internasional, dan segmen domestik (Tabel 4.3).

**Tabel 4.3. Regresi Linear Naive Kurs × Penumpang per Segmen (n = 60 bulan)**

| Segmen | Slope (pax / 1 IDR) | Pearson r | R² | p-value |
|---|---:|---:|---:|---:|
| Total | **+2.294** | +0,589 | 0,347 | < 10⁻⁶ |
| Internasional | +1.176 | +0,697 | **0,486** | < 10⁻⁹ |
| Domestik | +1.119 | +0,475 | 0,226 | < 10⁻³ |

#### 4.2.2 Temuan Mengejutkan: Slope Bertanda Positif

Hasil regresi menunjukkan **slope positif yang signifikan**: setiap pelemahan kurs sebesar 1 IDR diasosiasikan dengan kenaikan 2.294 penumpang per bulan secara nasional. Arah ini **berlawanan dengan prediksi teori ekonomi**, yang memprediksi slope negatif (kurs naik → harga tiket naik → demand turun).

Ranking kekuatan korelasi (R²) sesuai teori: **Internasional (0,486) > Total (0,347) > Domestik (0,226)** — segmen internasional yang lebih ter-dolarisasi memang menunjukkan korelasi lebih kuat. Tapi arah slope yang positif menunjukkan adanya *confounder*.

#### 4.2.3 Lag Analysis

Untuk memeriksa apakah efek kurs *delayed*, kami menjalankan regresi `penumpang(t) ~ kurs(t-k)` untuk k = 0 sampai 6 bulan (Tabel 4.4).

**Tabel 4.4. R² Regresi Lag Kurs (t-k) → Penumpang (t)**

| Lag (bulan) | Total | Internasional | Domestik |
|---:|---:|---:|---:|
| 0 | 0,347 | 0,486 | 0,226 |
| 1 | 0,351 | 0,554 | 0,198 |
| 2 | 0,444 | 0,624 | 0,286 |
| **3** | **0,512** | **0,637** | 0,373 |
| 4 | 0,514 | 0,621 | 0,382 |
| 5 | 0,509 | 0,602 | 0,385 |
| 6 | 0,509 | 0,578 | **0,401** |

R² mencapai puncak di lag 3–4 bulan untuk segmen total dan internasional, konsisten dengan literatur travel demand yang menyebut booking horizon umumnya 1–3 bulan sebelum keberangkatan.

Namun seluruh slope di setiap lag masih bertanda positif — masalah arah slope belum terselesaikan.

#### 4.2.4 Interpretasi Sementara

Slope positif pada korelasi naive **bukan konfirmasi hipotesis "kurs melemah → demand naik"**. Hipotesis sementara: korelasi positif adalah artefak *structural break* COVID-19. Bulan-bulan dengan kurs rendah (Januari 2020, pre-COVID) memiliki demand tinggi (9,12 juta), sementara bulan-bulan dengan kurs tinggi (2023–2024) juga memiliki demand tinggi (8–9 juta) karena recovery pasca-pandemi. Trend line linear yang menghubungkan kedua titik cluster ini akan memiliki slope positif meskipun tidak ada hubungan kausal langsung. Pengujian formal dilakukan di Bab 4.4.

### 4.3 Mekanisme Transmisi Multi-Channel

Untuk mengidentifikasi *bagaimana* kurs mempengaruhi demand, kami menguji tiga channel transmisi paralel.

#### 4.3.1 Channel 1: Cost-push (Kurs → Brent IDR → Tarif → Penumpang)

Channel ini diuji dalam tiga langkah berurutan (Tabel 4.5).

**Tabel 4.5. Channel Cost-push: Tiga Langkah**

| Step | Variabel Penjelas (X) | Outcome (Y) | R² | Slope | p |
|---|---|---|---:|---:|---:|
| A | Kurs | Brent IDR per bbl | 0,12 | +160 IDR/IDR | <0,01 |
| B | Brent IDR per bbl | Tarif Tiket IHK | **0,35** | +0,000277 IHK/IDR | <0,01 |
| C | Tarif Tiket IHK | Penumpang | 0,71* | +15.193 pax/IHK | <10⁻⁹ |

*Step C bertanda positif spurious (didominasi efek COVID, lihat Bab 4.4)

**Catatan proxy:** Channel ini menggunakan Brent crude oil × kurs sebagai proxy *upstream* biaya bahan bakar penerbangan. Data harga avtur Indonesia langsung tidak tersedia dalam dataset.

Step A menunjukkan bahwa kontribusi parsial kurs terhadap variasi `brent_idr` relatif kecil (R² = 0,12), karena Brent USD sendiri berfluktuasi besar secara independen dari kurs (oil shock Russia–Ukraine, oil crash COVID). Namun secara absolut, biaya BBM dalam IDR mengalami *double-shock*: range Brent IDR di periode analisis berlipat 4× (Rp 400.000 → Rp 1.689.000 per barel).

Step B menunjukkan pass-through Brent IDR ke tarif tiket pesawat IHK (R² = 0,35). Setiap kenaikan Brent IDR Rp 1.000.000 per barel diasosiasikan dengan kenaikan indeks tarif 277 poin. Pass-through terbatas, antara lain karena regulasi tarif batas atas yang membatasi maskapai menaikkan harga.

Step C menunjukkan korelasi sangat kuat antara tarif dan penumpang (R² = 0,71), tetapi **bertanda positif spurious** karena kedua variabel digerakkan oleh fase COVID yang sama (tarif rendah & penumpang rendah saat lockdown 2020; tarif tinggi & penumpang tinggi saat recovery 2024). Validasi channel ini memerlukan kontrol COVID, lihat Bab 4.4.

#### 4.3.2 Channel 2: Moneter (Kurs → BI Rate)

**Tabel 4.6. Regresi Kurs → BI Rate**

| Metrik | Nilai | Interpretasi |
|---|---:|---|
| Slope | +0,00132 % per IDR | +1,32% BI rate per 1.000 IDR pelemahan |
| R² | **0,645** | 65% variasi BI rate dijelaskan oleh kurs |
| p-value | <10⁻⁹ | Sangat signifikan |

**Channel ini menunjukkan korelasi paling kuat dari ketiga channel** (R² = 0,645) dengan slope positif sesuai prediksi teori: BI menaikkan suku bunga sebagai respons terhadap pelemahan rupiah untuk menarik kembali capital flow dan menjaga stabilitas. Implementasi historis: BI Rate diturunkan ke 3,5% pada periode lockdown sebagai stimulus, lalu dinaikkan agresif ke 6,25% pada 2023–2024 untuk *defend* rupiah.

Mekanisme transmisi BI rate → demand penumpang adalah tidak langsung: kenaikan BI rate → biaya kapital naik, KPR naik, kredit konsumtif lebih mahal → daya beli diskresioner (termasuk travel) tertekan.

#### 4.3.3 Channel 3: Daya Beli (Kurs → Inflasi Umum)

**Tabel 4.7. Regresi Kurs → Inflasi YoY**

| Metrik | Nilai |
|---|---:|
| Slope | +0,00054 % per IDR |
| R² | **0,074** |
| p-value | marginal |

Channel daya beli **lemah** di data Indonesia 2020–2024. R² hanya 7,4%, artinya kurs sangat sedikit menjelaskan variasi inflasi umum. Pass-through kurs ke inflasi Indonesia secara historis memang rendah karena banyak harga diatur (BBM bersubsidi, listrik). Periode COVID juga menekan inflasi (demand collapse) meskipun kurs melemah.

#### 4.3.4 Sintesis Bab 4.3

**Tabel 4.8. Ranking Channel Transmisi**

| Channel | R² puncak | Status |
|---|---:|---|
| 1: Cost-push (Brent IDR → Tarif) | 0,35 | Moderate, valid; pass-through terbatas oleh regulasi |
| **2: Moneter (Kurs → BI Rate)** | **0,645** | **Terkuat; slope sesuai teori** |
| 3: Daya beli (Kurs → Inflasi YoY) | 0,074 | Lemah; tidak relevan |

Channel **moneter** menjadi channel transmisi paling dominan secara statistik, meskipun literatur Indonesia sering memfokuskan diri pada channel cost-push.

### 4.4 Robustness: Kontrol Confounder

#### 4.4.1 Faceted Regression per Fase COVID

Sebagai uji robustness utama, kami menjalankan regresi `penumpang ~ kurs` **secara terpisah** di setiap fase COVID (Tabel 4.9).

**Tabel 4.9. Slope Kurs → Penumpang per Fase COVID**

| Fase | n bulan | Slope | R² | p-value |
|---|---:|---:|---:|---:|
| pre_pandemic | 2 | — (n terlalu kecil) | — | — |
| **lockdown** | 19 | **−318** | 0,012 | 0,652 |
| transisi | 15 | +1.555 | 0,578 | 0,001 |
| recovery | 24 | +706 | 0,176 | 0,041 |

**Temuan kritis:** Pada fase **lockdown**, slope berbalik menjadi **negatif** (−318) — sesuai teori. Namun signifikansi statistik tidak tercapai (p = 0,652), karena pada fase lockdown variasi demand didominasi oleh kebijakan pembatasan (PSBB, PPKM) yang bersifat administratif, bukan oleh kurs.

Pada fase transisi dan recovery, slope tetap positif dan spurious. **Tidak ada satu pun fase yang menunjukkan slope negatif signifikan**, artinya pada data 2020–2024 ini, *kurs bukan driver utama* permintaan penumpang setelah dikontrol COVID.

**Implikasi:** Korelasi naive positif yang signifikan di Bab 4.2 **adalah artefak structural break COVID**, bukan hubungan kausal. Ini *honest finding* yang harus disampaikan dengan jelas.

#### 4.4.2 Volatilitas Kurs

Kami menguji apakah *volatilitas* kurs (spread max − min dalam satu bulan) punya korelasi independen dengan demand.

**Tabel 4.10. Regresi Spread Kurs → Penumpang**

| Metrik | Nilai |
|---|---:|
| Slope | +175 |
| R² | **0,0006** |
| p-value | tidak signifikan |

Hipotesis ditolak — volatilitas kurs **tidak** punya korelasi independen dengan demand pada data ini. Bulan paling volatil (Maret 2020 dengan spread 2.440 IDR) bertepatan dengan PSBB, sehingga sinyal volatilitas tertelan oleh sinyal lockdown.

#### 4.4.3 Efek Musiman: Lebaran, Natal, Peak Season

**Tabel 4.11. Efek Lebaran dan Natal (Uji Mann–Whitney)**

| Group | n baris rute-bulan | Median penumpang | Boost ratio | p-value |
|---|---:|---:|---:|---:|
| has_lebaran=0 (DOM) | 12.534 | 5.338 | — | — |
| has_lebaran=1 (DOM) | 985 | 5.621 | 1,05× | 0,697 |
| has_natal=0 | 15.647 | 5.839 | — | — |
| has_natal=1 | 1.471 | **7.704** | **1,32×** | <0,001 |

Efek Lebaran tidak signifikan (boost hanya 1,05×, p = 0,70), bukan karena Lebaran tidak nyata, melainkan karena 3 dari 5 bulan Lebaran dalam dataset (Mei 2020, 2021, 2022) jatuh di periode COVID yang menekan demand.

Efek Natal signifikan dengan boost median 32%, karena Natal tidak overlap dengan lockdown.

**Interaksi `is_peak_season` × kurs:**

**Tabel 4.12. Regresi Kurs → Penumpang per Segmen Peak**

| Segmen | n | Slope | R² |
|---|---:|---:|---:|
| Non-peak | 40 | +1.841 | 0,244 |
| **Peak season** | 20 | **+3.087** | **0,547** |

Sensitivitas demand terhadap kurs (diukur lewat R²) **2,2× lebih tinggi** di peak season dibandingkan non-peak. Temuan ini konsisten dengan literatur travel demand: segmen leisure (yang dominan di peak season seperti Lebaran, libur sekolah, Natal) lebih elastis terhadap harga dibanding segmen bisnis.

#### 4.4.4 Sintesis Bab 4.4

Korelasi naive Bab 4.2 **tidak robust** terhadap kontrol fase COVID. Tidak ada satu pun fase yang menunjukkan slope negatif signifikan, menegaskan bahwa hubungan yang ditemukan di Bab 4.2 adalah *artefak structural break*, bukan kausal. Namun, beberapa temuan turunan tetap bermakna: (1) efek Natal signifikan dan kuantitatif (boost 32%), (2) peak season menunjukkan sensitivitas 2,2× lebih tinggi ke kurs.

### 4.5 Heterogenitas Geografis

#### 4.5.1 Top 15 Rute Nasional

**Tabel 4.13. Top 15 Rute by Total Penumpang 2020–2024**

| Rank | Rute | Kategori | Total Pax (juta) |
|---:|---|---|---:|
| 1 | CGK-DPS | DOMESTIK | 16,82 |
| 2 | CGK-KNO | DOMESTIK | 12,35 |
| 3 | CGK-SUB | DOMESTIK | 11,51 |
| 4 | CGK-UPG | DOMESTIK | 10,96 |
| 5 | CGK-SIN | INTERNASIONAL | 8,49 |
| 6 | DPS-SIN | INTERNASIONAL | 6,89 |
| 7 | CGK-PNK | DOMESTIK | 6,21 |
| 8 | CGK-KUL | INTERNASIONAL | 5,91 |
| 9 | CGK-PLM | DOMESTIK | 5,83 |
| 10 | BPN-CGK | DOMESTIK | 5,80 |

**14 dari 15 rute top melibatkan CGK (Soekarno-Hatta)** sebagai salah satu endpoint, menegaskan dominasi CGK sebagai hub absolut sistem penerbangan Indonesia.

#### 4.5.2 Sensitivitas per Negara Destinasi

Untuk rute internasional, kami menjalankan regresi `penumpang ~ kurs` terpisah per negara destinasi (Tabel 4.14, n = 14 negara dengan total pax > 500.000).

**Tabel 4.14. Sensitivitas Kurs → Penumpang per Negara Destinasi (Sorted by R²)**

| Negara | R² | Slope (pax/IDR) | Total Pax (juta) |
|---|---:|---:|---:|
| **FILIPINA** | **0,532** | +20,7 | 1,2 |
| THAILAND | 0,509 | +25,4 | 1,5 |
| QATAR | 0,507 | +50,3 | 3,8 |
| MALAYSIA | 0,501 | +342,1 | 20,5 |
| CHINA | 0,481 | +72,1 | 3,4 |
| AUSTRALIA | 0,481 | +123,4 | 7,9 |
| UNI EMIRAT ARAB | 0,470 | +39,1 | 3,2 |
| SINGAPURA | 0,463 | +277,6 | 18,9 |
| KOREA SELATAN | 0,446 | +30,5 | 2,2 |
| TURKI | 0,410 | +13,5 | 1,3 |
| TAIWAN | 0,401 | +26,6 | 1,9 |
| HONG KONG | 0,398 | +41,7 | 2,5 |
| JEPANG | 0,332 | +24,3 | 2,2 |
| **ARAB SAUDI** | **0,246** | +44,6 | 3,9 |

Slope absolute didominasi oleh volume (Malaysia +342, Singapura +278), sementara **R² lebih informatif untuk membandingkan sensitivitas relatif**:

- **R² tinggi (≥0,50):** Filipina, Thailand, Qatar, Malaysia — rute-rute dengan demand yang variasinya banyak dijelaskan oleh dinamika kurs/COVID.
- **R² rendah (<0,35):** Arab Saudi dan Jepang — dua negara dengan demand yang relatif **independen dari kurs**, didorong oleh faktor lain:
  - Arab Saudi: kuota haji/umroh yang ditetapkan pemerintah Saudi.
  - Jepang: kebijakan visa (e.g., visa-free pasca-pandemi) dan pariwisata kultural yang kurang elastis ke harga.

#### 4.5.3 Distribusi Provinsi Origin

**Tabel 4.15. Top 10 Provinsi Origin (Domestik)**

| Rank | Provinsi | Total Pax (juta) |
|---:|---|---:|
| 1 | Jakarta + DKI Jakarta* | 124,78 |
| 2 | Kalimantan Timur* | 20,96 |
| 3 | Kepulauan Riau | 14,63 |
| 4 | Bali | 13,17 |
| 5 | Kalimantan Selatan | 10,70 |
| 6 | Papua | 6,97 |
| 7 | Jawa Timur | 5,88 |
| 8 | NTT | 3,74 |
| 9 | Papua Barat | 3,43 |
| 10 | Maluku | 3,33 |

*Konsolidasi dari duplikat penamaan provinsi di `dim_bandara` (lihat Limitasi 7.1).

Jakarta mendominasi dengan ~125 juta penumpang, mewakili sekitar 50% total demand domestik. Kalimantan (Timur + Selatan + Tengah) total ~31 juta — terkait flow tenaga kerja ke industri tambang dan sawit. Kepulauan Riau (Batam) berperan sebagai gerbang Singapura. Indonesia Timur (Papua, NTT, Maluku) ~13 juta — penting untuk konektivitas region, biasanya rute "thin" yang bergantung subsidi.

#### 4.5.4 OD Matrix

Heatmap OD matrix (Top 10 IATA × Top 10 IATA) menegaskan struktur hub-and-spoke: hampir seluruh flow signifikan melibatkan CGK sebagai salah satu endpoint. Pasangan non-CGK yang menonjol hanya: SUB-UPG (Surabaya-Makassar, 5,43 juta), KNO-KUL (Medan-Kuala Lumpur, 2,2 juta), dan BTH-CGK (Batam-Jakarta, 5,37 juta).

---

## 5. Diskusi

### 5.1 Sintesis Temuan

Tabel 5.1 merangkum tujuh temuan utama penelitian.

**Tabel 5.1. Ringkasan Temuan Utama**

| # | Temuan | R² / Effect Size | Signifikansi |
|---|---|---:|---|
| 1 | Korelasi naive kurs–penumpang POSITIF | R² = 0,347 | p < 10⁻⁶ |
| 2 | Korelasi naive adalah artefak COVID; setelah kontrol, slope hanya negatif di lockdown (tidak signifikan) | R² = 0,012 (lockdown) | p = 0,65 |
| 3 | Channel moneter (Kurs → BI Rate) paling kuat | R² = 0,645 | p < 10⁻⁹ |
| 4 | Channel cost-push (Brent IDR → Tarif IHK) moderate | R² = 0,35 | p < 0,01 |
| 5 | Channel daya beli lemah/tidak relevan | R² = 0,074 | marginal |
| 6 | Efek Natal signifikan (boost median 32%), Lebaran tidak (terkontaminasi COVID) | 1,32× boost | p < 0,001 |
| 7 | Heterogenitas per negara: ASEAN volume-driven, Saudi/Jepang non-kurs | R² range 0,25–0,53 | semua signifikan |

### 5.2 Mengapa Slope Naive Bertanda Positif?

Penyebab teknis: distribusi titik di scatter plot tidak linear melainkan berbentuk *L terbalik*:
- Pre-pandemic (Jan–Feb 2020): kurs rendah (~13.700), penumpang tinggi (~8 juta).
- Lockdown (Mar 2020–Sep 2021): kurs naik volatile (~15.000), penumpang sangat rendah (0,1–4 juta).
- Recovery (2023–2024): kurs terus naik (~15.500–16.300), penumpang juga terus naik (7–9 juta) karena reopening dan pent-up demand.

Trend line linear yang menghubungkan ketiga cluster ini secara matematis memiliki slope positif, **meskipun tidak ada hubungan kausal langsung**. Inilah contoh klasik *spurious correlation* akibat *structural break*.

### 5.3 Mengapa Channel Moneter Dominan?

Tiga alasan teoretis:
1. **Respons BI sangat cepat dan terukur** terhadap depresiasi rupiah, sebagaimana tercermin dalam pernyataan rutin BI mengenai upaya menjaga stabilitas (Bank Indonesia, 2024).
2. **Kebijakan moneter punya scope sektoral luas**: kenaikan suku bunga mempengaruhi *seluruh* sektor konsumsi diskresioner (KPR, kredit kendaraan, kartu kredit, kredit travel), bukan hanya transportasi.
3. **Pass-through kurs ke avtur dan tarif tiket dibatasi oleh regulasi tarif batas atas**, yang membuat channel cost-push lebih *muted*. INACA (2024) melaporkan bahwa tarif batas atas yang ditetapkan 2019 sudah tidak relevan dengan kondisi 2024, menunjukkan *binding constraint* yang menghambat pass-through penuh.

### 5.4 Heterogenitas Geografis: Implikasi Teori dan Kebijakan

Temuan R² rendah pada Arab Saudi (0,246) dan Jepang (0,332) konsisten dengan teori bahwa **rute dengan demand "non-tradable" (haji, kuota visa) kurang elastis terhadap kondisi makro**. Sebaliknya, rute ASEAN (Malaysia, Singapura, Filipina, Thailand) yang dominan untuk leisure dan business travel, sensitivitasnya lebih tinggi.

Implikasi kebijakan yang berbeda per koridor:
- **Koridor ASEAN:** kebijakan tarif kompetitif, stabilisasi makro, dan promosi pariwisata efektif.
- **Koridor Timur Tengah (Saudi, UAE, Qatar):** kebijakan kuota haji, kerjasama bilateral, dan koordinasi dengan Kementerian Agama.
- **Koridor Jepang/Korea:** kebijakan visa dan promosi pariwisata kultural.

### 5.5 Implikasi Operasional untuk Maskapai

1. **Hedging avtur** tetap penting meski pass-through dibatasi regulasi, karena maskapai menanggung *spread* antara kenaikan biaya dan tarif batas atas.
2. **Konsentrasi pada hub CGK** (14 dari 15 rute top) menjadikan bandara ini *single point of failure*. Diversifikasi via Kertajati (KJT) atau Yogyakarta (YIA) menjadi strategis.
3. **Peak season strategy:** karena demand peak 2,2× lebih sensitif kurs, maskapai dapat melakukan *dynamic pricing* lebih agresif di periode ini.

---

## 6. Kesimpulan

Penelitian ini menyajikan analisis empiris dari hubungan kurs IDR/USD dan permintaan angkutan udara Indonesia 2020–2024 menggunakan data warehouse bulanan. Temuan kunci adalah:

1. **Korelasi naive kurs–penumpang bertanda POSITIF dan signifikan** (slope +2.294 pax/IDR, R² = 0,347, p < 10⁻⁶), arah yang **berlawanan** dengan prediksi teori standar.

2. **Korelasi positif ini adalah artefak structural break COVID-19**, bukan hubungan kausal. Setelah faceted regression per fase COVID, tidak ada fase yang menunjukkan slope negatif signifikan (slope lockdown −318, p = 0,652).

3. **Channel transmisi paling kuat** dari kurs ke sektor angkutan udara adalah **channel moneter** (Kurs → BI Rate, R² = 0,645, slope sesuai teori), bukan channel cost-push (R² Brent IDR → tarif tiket = 0,35) sebagaimana sering diasumsikan literatur Indonesia.

4. **Channel daya beli (kurs → inflasi umum) tidak signifikan** (R² = 0,074), konsisten dengan literatur bahwa pass-through kurs ke inflasi Indonesia rendah karena banyak harga diatur.

5. **Heterogenitas geografis bermakna**: sensitivitas demand terhadap kurs paling tinggi di koridor ASEAN dan Timur Tengah komersial, paling rendah di koridor Arab Saudi (haji) dan Jepang (visa).

6. **Efek musiman**: Natal memberi boost demand 32% (signifikan), Lebaran terkontaminasi COVID (tidak signifikan dalam dataset ini), peak season menunjukkan sensitivitas 2,2× lebih tinggi terhadap kurs.

**Implikasi kebijakan utama:** Stabilisasi rupiah via kebijakan moneter BI seharusnya menjadi prioritas dibanding intervensi sektoral cost-push (misalnya subsidi BBM atau intervensi tarif batas atas), karena channel moneter terbukti menjadi jalur transmisi dominan dalam periode analisis. Kebijakan operasional dan promosi pariwisata sebaiknya didiferensiasikan per koridor geografis sesuai sensitivitas masing-masing.

---

## 7. Limitasi dan Saran

### 7.1 Limitasi Data

1. **Periode singkat (60 bulan)** dengan dominasi structural break COVID. Hanya 2 bulan masuk kategori pre-pandemic, terlalu sedikit untuk regresi terpisah yang valid.
2. **Tidak tersedianya data harga avtur Indonesia langsung**. Channel cost-push diuji menggunakan Brent crude oil × kurs sebagai *proxy upstream*. Avtur memang disuling dari crude oil dan korelasinya ~80–90% (lag 1–2 bulan), namun proxy bukan substitusi.
3. **Single FX (IDR/USD only)**. Rute internasional ke negara dengan mata uang berbeda (JPY, AUD, MYR, SGD) idealnya dianalisis dengan kurs bilateral masing-masing.
4. **Indeks tarif tiket BPS bukan harga maskapai langsung** — tidak dapat memisahkan efek antar maskapai atau antar kelas tarif.
5. **Granularity bulanan, bukan booking level** — tidak dapat menangkap dinamika lead-time atau price elasticity instan.
6. **Tidak ada data supply** (jumlah seat tersedia, frekuensi penerbangan, load factor). Penurunan penumpang bisa karena demand turun atau supply dipotong (sebagaimana dilaporkan Sandiaga Uno pada Juni 2024 untuk rute Bali).
7. **Inkonsistensi penamaan provinsi di dim_bandara** (sebagian dalam Bahasa Indonesia, sebagian dalam Bahasa Inggris dari `airportsdata` library) yang membutuhkan konsolidasi manual saat analisis.

### 7.2 Saran untuk Riset Lanjutan

1. **Dataset avtur Pertamina** untuk pengujian langsung channel cost-push tanpa proxy.
2. **Multi-currency FX** untuk rute internasional spesifik (kurs IDR/JPY untuk rute Indonesia–Jepang, dst).
3. **Diff-in-difference** dengan event seperti Visa-on-Arrival (Mei 2022) atau pencabutan PPKM (Januari 2023) sebagai treatment.
4. **Disaggregate per maskapai** untuk menganalisis strategi pricing dan rute yang berbeda.
5. **Vector Error Correction Model (VECM)** untuk menangkap dinamika ko-integrasi dan kausalitas dua-arah antara kurs, BI rate, dan demand.
6. **Inkorporasi data supply** (jumlah seat, frekuensi) untuk dekomposisi demand vs supply.

### 7.3 Limitasi Metodologis

1. **OLS regresi linear** sederhana tidak menangkap non-linearitas atau threshold effects. Model panel atau model state-space dapat memperkaya analisis.
2. **Faceted regression per covid_phase** mengkontrol level tapi tidak interaksi penuh. Regresi multivariate dengan interaksi (`kurs × covid_phase`) dapat menggantikan.
3. **Tidak ada uji stasioneritas** (ADF/KPSS) eksplisit pada deret kurs dan penumpang sebelum regresi, meskipun untuk periode 60 bulan dengan structural break, asumsi stationaritas memang sulit dipenuhi.

---

## 8. Daftar Pustaka

Badan Pusat Statistik (BPS). (2024). *Statistik Transportasi 2024: Kenaikan Jumlah Penumpang Semua Moda Transportasi*. Jakarta: BPS RI.

Bank Indonesia. (2024). *Statistik Ekonomi dan Keuangan Indonesia (SEKI): Kurs Transaksi Bank Indonesia*. Diakses dari https://www.bi.go.id

Goldberg, P. K., & Knetter, M. M. (1997). Goods prices and exchange rates: What have we learned? *Journal of Economic Literature*, 35(3), 1243–1272.

Granger, C. W. J., & Newbold, P. (1974). Spurious regressions in econometrics. *Journal of Econometrics*, 2(2), 111–120.

ICAO. (2022). *Effects of Novel Coronavirus (COVID-19) on Civil Aviation: Economic Impact Analysis*. Montreal: International Civil Aviation Organization.

IATA. (2023). *Industry Statistics Fact Sheet*. International Air Transport Association.

INACA. (2024). *Pernyataan INACA tentang Penyebab Tiket Pesawat Mahal*. Tempo.co, 21 Juli 2024.

Investing.com. (2024). *Brent Oil Futures Historical Data 2020–2024*. Diakses dari https://www.investing.com

Kementerian Perhubungan. (2023). *Kaleidoskop 2023: Naik-Turun Industri Penerbangan Indonesia*. Kompas, 31 Desember 2023.

Rakyat Merdeka. (2024). *Harga Avtur dan Nilai Kurs Sudah Naik, Garuda Minta Tarif Pesawat Dievaluasi*. Diakses Mei 2024.

Direktorat Jenderal Perhubungan Udara (DJPU), Kementerian Perhubungan. (2024). *Buku Statistik Angkutan Udara 2020–2024, BAB III dan BAB VI*. Jakarta: DJPU.

---

## Lampiran A — Skema Data Warehouse

```
dim_waktu_bulanan (60 baris)
├── waktu_id, tahun, bulan, nama_bulan, kuartal, semester
├── covid_phase, has_lebaran, has_natal, is_peak_season
└── jumlah_hari_libur

dim_rute (553 baris)
├── rute_id, kode_rute, kategori (DOM/INT)
└── bandara_1_id, bandara_2_id (FK ke dim_bandara)

dim_bandara (232 baris)
└── bandara_id, nama_bandara, iata, kota, provinsi, negara

fact_makro_bulanan (60 baris)
├── waktu_id (FK ke dim_waktu)
├── avg_kurs_jual, avg_kurs_beli, avg_kurs_tengah
├── min_kurs_tengah, max_kurs_tengah, jumlah_hari_trading
├── tarif_tiket_ihk, inflasi_yoy, inflasi_mtm, bi_rate
└── brent_usd_bbl, brent_high, brent_low

fact_penumpang_rute (17.118 baris)
├── waktu_id (FK), rute_id (FK)
└── jumlah_penumpang
```

## Lampiran B — Reproducibility

Seluruh analisis dapat direproduksi dengan:

```bash
# 1. Re-generate data warehouse
python output/BULANAN/etl_bulanan/run_all_bulanan.py

# 2. Re-run semua analisis (24 worksheet Python)
for f in output/BULANAN/analisis/bab_*/ws*/analysis.py; do
    PYTHONIOENCODING=utf-8 python "$f"
done
```

Output Python tersimpan di setiap folder WS sebagai `metrics.txt`, `*.csv`, dan `plot.png`. Penjelasan setiap WS tersedia di `penjelasan.md` di folder yang sama. Cross-check angka R² dan slope antara Tableau dan Python harus persis match — mismatch menandakan masalah pada default aggregation di Tableau (semua makro = AVG, jumlah_penumpang = SUM).

---

*Paper ini ditulis berdasarkan analisis Python di `output/BULANAN/analisis/` dengan 24 worksheet yang dapat diverifikasi independen. Angka R², slope, dan p-value yang dikutip di paper ini dapat dicek di `metrics.txt` setiap folder worksheet yang relevan.*
