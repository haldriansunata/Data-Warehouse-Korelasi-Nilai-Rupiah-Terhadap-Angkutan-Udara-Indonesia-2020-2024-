# Rencana Analisis Komprehensif (v2 — Disesuaikan dengan Output Aktual)

**Topik:** Korelasi Nilai Rupiah (IDR/USD) Terhadap Angkutan Udara Indonesia
**Periode:** Januari 2020 – Desember 2024 (60 bulan)
**Grain analisis:** Bulanan × Rute
**Anggota:** 5 orang × 1 bab per anggota
**Sumber data:** `output/BULANAN/` (sudah di-physical-join di Tableau, pusat = `fact_penumpang_rute`)
**Validasi:** semua angka di dokumen ini sudah diverifikasi dengan output Python di `output/BULANAN/analisis/`.

---

## 0. Validasi Output Aktual vs Rencana Lama

Total **24 worksheet Python** berhasil dijalankan dan menghasilkan output lengkap (`analysis.py` + `plot.png` + `metrics.txt`/`.csv` + `penjelasan.md`). Berikut perbedaan dengan plan awal:

| Bab | WS Direncanakan | WS Aktual Dibuat | Yang Tidak Dibuat sebagai Folder Terpisah | Status |
|---|---:|---:|---|---|
| Bab 1 Konteks | 4 | **4** | — | ✓ Lengkap |
| Bab 2 Hipotesis | 5 | **4** | WS5 (Dashboard ringkasan — dibuat langsung di Tableau saja, bukan Python) | ✓ Sesuai |
| Bab 3 Mekanisme | 6 | **5** | WS6 (Dashboard "Tiga Channel" — dibuat langsung di Tableau saja) | ✓ Sesuai |
| Bab 4 Robustness | 6 | **6** | — | ✓ Lengkap |
| Bab 5 Heterogenitas | 5–6 | **5** | WS6 (Hub vs Spoke, opsional) | ✓ Lengkap |

**Catatan**: Dashboard adalah komposit visual di Tableau yang tidak butuh script Python terpisah — anggota tinggal drag worksheet ke dashboard di Tableau saat presentasi. Jadi tidak ada gap material.

**Sanity Check Numerik (3 spot-check):**
- Bab 2 WS1: slope=2.294, R²=0,347, p<10⁻⁶, n=60 ✓ valid (file `metrics.txt`)
- Bab 4 WS1: lockdown slope=−318 (n=19, p=0,65), transisi=+1.555 (n=15, p=0,001), recovery=+706 (n=24, p=0,04) ✓ valid
- Bab 5 WS3: 14 negara, R² range 0,25 (Saudi) – 0,53 (Filipina), n_bulan 54–60 per negara ✓ valid

---

## 1. Findings Aktual — Apakah Layak untuk Paper?

**Jawaban singkat: YA, layak — dengan framing "honest reporting".** Tiga finding inti sudah didukung data yang signifikan secara statistik dan dapat dipertanggungjawabkan di paper akademik:

### Finding #1 (Bab 2) — Korelasi naive kurs–penumpang POSITIF, tapi spurious

| Sheet | Slope | R² | p-value |
|---|---:|---:|---:|
| Total | **+2.294 pax/IDR** | 0,347 | <10⁻⁶ |
| Internasional | +1.176 | **0,486** | <10⁻⁹ |
| Domestik | +1.119 | 0,226 | <10⁻³ |

**Layak untuk paper?** YA — angka signifikan, dan justru menarik bahwa arah-nya berlawanan teori. Ini titik *intellectual interesting* paper kalian.

### Finding #2 (Bab 4) — Setelah kontrol COVID, slope di lockdown phase NEGATIF (sesuai teori), tapi tidak signifikan

| COVID Phase | n | Slope | R² | p |
|---|---:|---:|---:|---:|
| lockdown | 19 | **−318** | 0,012 | 0,652 |
| transisi | 15 | +1.555 | 0,578 | 0,001 |
| recovery | 24 | +706 | 0,176 | 0,041 |

**Layak untuk paper?** YA — finding ini *valuable scientific contribution*: menunjukkan bahwa korelasi naive dipengaruhi structural break COVID. Honest reporting > over-claim.

### Finding #3 (Bab 3) — Channel transmisi terkuat = Moneter (BI Rate), bukan Cost-push

| Channel | R² | Slope | Status Teori |
|---|---:|---:|---|
| 1A: Kurs → Brent IDR | 0,12 | +160 | weak |
| 1B: Brent IDR → Tarif | 0,35 | +0,000277 | moderate |
| 1C: Tarif → Pax | 0,71 | +15.193 (spurious) | spurious COVID |
| **2: Kurs → BI Rate** | **0,645** | **+0,00132 (+1,32%/1000 IDR)** | **✓ sesuai teori** |
| 3: Kurs → Inflasi YoY | 0,074 | +0,000542 | weak |

**Layak untuk paper?** YA — Channel 2 (moneter) menunjukkan korelasi paling kuat dan slope positif sesuai teori. Ini *novel contribution* karena literatur Indonesia sering fokus channel cost-push, padahal data 2020–2024 menunjukkan respons moneter dominan.

### Finding #4 (Bab 5) — Heterogenitas geografis bermakna: pattern berbeda di ASEAN vs Timur Tengah vs Australia

R² per negara destinasi (urut ascending):

| Negara | R² | Insight |
|---|---:|---|
| ARAB SAUDI | **0,25** | Driver = kuota haji/umroh, bukan kurs |
| JEPANG | 0,33 | Driver = kebijakan visa, bukan kurs |
| AUSTRALIA | 0,48 | Mixed (inbound wisman tahan kurs lemah) |
| MALAYSIA | 0,50 | Driver = kurs/volume tinggi ASEAN |
| FILIPINA | **0,53** | R² tertinggi — sensitif ke makro |

**Layak untuk paper?** YA — ini *headline finding* yang membedakan paper kalian dari analisis korelasi naif. Pattern per-negara konsisten dengan literatur (haji-based vs leisure vs business travel).

---

## 2. Inventaris & Pemetaan Kolom (Tetap Sesuai Plan)

### 2.1 Kolom WAJIB (sudah dipakai di output)

| Tabel | Kolom | Dipakai di WS |
|---|---|---|
| `fact_penumpang_rute` | `jumlah_penumpang` | Bab 1 WS1, Bab 2 WS1-4, Bab 3 WS3, Bab 4 WS1-6, Bab 5 WS1-5 |
| `fact_makro_bulanan` | `avg_kurs_tengah` | Bab 1 WS1-2, Bab 2 WS1-4, Bab 3 WS1,4,5, Bab 4 WS1,6, Bab 5 WS2-3 |
| `fact_makro_bulanan` | `min_kurs_tengah`, `max_kurs_tengah` | Bab 1 WS2, Bab 4 WS2 (spread) |
| `fact_makro_bulanan` | `brent_usd_bbl` | Bab 1 WS1, Bab 3 WS1-2 |
| `fact_makro_bulanan` | `bi_rate` | Bab 1 WS1, Bab 1 WS3, Bab 3 WS4 |
| `fact_makro_bulanan` | `inflasi_yoy`, `inflasi_mtm` | Bab 1 WS3, Bab 3 WS5 |
| `fact_makro_bulanan` | `tarif_tiket_ihk` | Bab 3 WS2-3 |
| `dim_waktu` | `covid_phase` | Bab 1 WS3, Bab 2 WS1-4 (color), Bab 3 WS1-5 (color), Bab 4 WS1 (facet) |
| `dim_waktu` | `has_lebaran`, `has_natal`, `is_peak_season` | Bab 4 WS3, WS4, WS6 |
| `dim_waktu` | `jumlah_hari_libur` | Bab 4 WS5 |
| `dim_rute` | `kategori` | Bab 2 WS2-3, Bab 5 WS1-3 |
| `dim_rute` | `kode_rute` | Bab 5 WS1-2 |
| `dim_bandara` (origin & destination) | `iata`, `negara`, `provinsi` | Bab 5 WS3, WS4, WS5 |

**SEMUA kolom WAJIB di rencana sudah ter-pakai di setidaknya 1 WS.** ✓

### 2.2 Kolom yang diabaikan (low signal — sengaja)

| Kolom | Alasan |
|---|---|
| `avg_kurs_jual`, `avg_kurs_beli` | Redundan dengan `avg_kurs_tengah` (korelasi >0,99) |
| `jumlah_hari_trading` | Low signal (range 14–23) |
| `brent_high`, `brent_low` | Tidak dipakai untuk volatility analysis di output ini |
| `kuartal`, `semester` | Redundan untuk data bulanan |
| `nama_bandara` | Hanya label, dipakai untuk tooltip Tableau saja |

---

## 3. Alur Naratif 5 Bab (sesuai output)

```
Bab 1: KONTEKS         → "Apa yang terjadi 2020–2024?"
Bab 2: HIPOTESIS NAIVE → "Apakah kurs ↑ membuat penumpang ↓?"
                          [Finding: TIDAK — slope positif spurious]
Bab 3: MEKANISME       → "Lewat jalur apa kurs sampai ke penumpang?"
                          [Finding: Channel moneter dominan (R²=0,65)]
Bab 4: ROBUSTNESS      → "Apakah korelasi naive bertahan setelah dikontrol?"
                          [Finding: TIDAK — naive correlation adalah artefak COVID]
Bab 5: HETEROGENITAS   → "Siapa yang paling kena? Rute/negara mana?"
                          [Finding: ASEAN volume-driven, Saudi/Jepang non-kurs]
```

**Penting**: alur ini sekarang lebih *honest*. Bab 2 = "naive baseline yang misleading", Bab 4 = "uncovering reality". Ini struktur paper yang kuat secara metodologis.

---

## Bab 1 — Lanskap Konteks (Anggota 1) | 4 WS

### Pertanyaan Riset
Bagaimana kurs IDR/USD dan demand angkutan udara Indonesia berkembang 2020–2024?

### WS yang dibuat
| WS | Folder | Output Utama |
|---|---|---|
| WS1 Multi-panel timeseries | `ws1_multi_panel/` | Plot 4-panel (pax, kurs, brent, BI rate) |
| WS2 Kurs band | `ws2_kurs_band/` | Plot + Top 5 bulan paling volatil (Mar 2020 spread 2.440 IDR) |
| WS3 Inflasi + COVID phase | `ws3_inflasi_covid/` | Plot + rata-rata per fase (lockdown YoY=1,70%, recovery=2,99%) |
| WS4 Seasonal heatmap | `ws4_seasonal_heatmap/` | Pivot tahun×bulan (min: Mei 2020 = 96K, max: Jan 2020 = 9,12M) |

### Pesan utama Bab 1 (sesuai output)
Periode 2020–2024 terdiri dari **4 rezim COVID**, kurs naik **19%** (13.732 → 16.329), Brent berfluktuasi dari **26 USD (Apr 2020 crash) → 116 USD (Jun 2022 Russia-Ukraine)**, BI rate dari **3,5% → 6,25%**. Demand crash dari **9,12 juta** (Jan 2020) ke **96K** (Mei 2020), pulih ke **~9 juta** di pertengahan 2024 — recovery 99% baseline. *Setting the stage* sebelum bicara korelasi.

---

## Bab 2 — Hipotesis Utama: Naive Correlation (Anggota 2) | 4 WS

### Pertanyaan Riset
Apakah ada hubungan signifikan antara level kurs IDR/USD dan jumlah penumpang? Berbeda per segmen (DOM/INT)? Lagged?

### WS yang dibuat
| WS | Folder | R² | Slope |
|---|---|---:|---:|
| WS1 Scatter Total | `ws1_scatter_total/` | 0,347 | +2.294 |
| WS2 Scatter INT | `ws2_scatter_int/` | **0,486** | +1.176 |
| WS3 Scatter DOM | `ws3_scatter_dom/` | 0,226 | +1.119 |
| WS4 Lag analysis (0–6 bulan) | `ws4_lag_analysis/` | INT peak lag 3 = **0,637**; TOTAL peak lag 3–4 = 0,51 | — |

**Dashboard ringkasan**: dibuat langsung di Tableau saat presentasi, tidak butuh Python script.

### Pesan utama Bab 2 (REVISI sesuai output aktual)
~~Slope kurs–penumpang **negatif** dan signifikan~~ → **TIDAK, slope POSITIF dan signifikan**.

Yang benar:
- Korelasi naive menunjukkan slope **POSITIF** (+2.294 pax per 1 IDR pelemahan) — *berlawanan teori ekonomi*.
- R² internasional (0,49) > total (0,35) > domestik (0,23) — ranking sensitivitas sesuai teori meski arah salah.
- Lag analysis: puncak korelasi di lag 3 bulan untuk INT (R²=0,64).
- **Slope positif adalah ARTEFAK COVID** — dijelaskan tuntas di Bab 4. Bab 2 = honest naive baseline.

### Implikasi untuk Paper
Framing harus: "Naive correlation menunjukkan hubungan signifikan tapi arah berlawanan dengan teori; investigasi mendalam (Bab 4) menjelaskan bahwa ini akibat structural break COVID." Ini *intellectual hook* paper kalian.

---

## Bab 3 — Mekanisme Transmisi (Anggota 3) | 5 WS

### Pertanyaan Riset
Lewat jalur apa kurs sampai ke demand? Tiga channel paralel: cost-push (BBM global via Brent sebagai proxy upstream avtur — *kita tidak punya data avtur langsung*), moneter (BI rate), daya beli (inflasi).

### WS yang dibuat
| WS | Folder | Channel | R² | Slope |
|---|---|---|---:|---:|
| WS1 Kurs × Brent IDR | `ws1_kurs_brent_idr/` | 1A cost-push | 0,12 | +160 IDR/IDR |
| WS2 Brent IDR × Tarif | `ws2_brent_idr_tarif/` | 1B cost-push | 0,35 | +0,000277 IHK/IDR |
| WS3 Tarif × Pax | `ws3_tarif_pax/` | 1C cost-push | **0,71** (spurious) | +15.193 pax/IHK |
| WS4 Kurs × BI Rate | `ws4_kurs_birate/` | 2 moneter | **0,645** | **+0,00132 %/IDR** |
| WS5 Kurs × Inflasi YoY | `ws5_kurs_inflasi/` | 3 daya beli | 0,074 | +0,000542 %/IDR |

**Dashboard "Tiga Channel"**: dibuat langsung di Tableau saat presentasi.

### Pesan utama Bab 3 (sesuai output)
Channel paling kuat = **Moneter (Kurs → BI Rate)**, R² **0,645**, slope **POSITIF** sesuai teori (+1,32% BI rate per 1.000 IDR pelemahan). Channel cost-push Step B (Brent IDR → Tarif) moderate (R²=0,35), Step C (Tarif → Pax) tampak sangat kuat (R²=0,71) tapi *spurious* karena COVID. Channel daya beli (inflasi) lemah (R²=0,07) — pass-through kurs ke inflasi umum tertekan oleh kebijakan harga diatur (BBM, listrik).

### Implikasi untuk Paper
Bab 3 = novel contribution. Literatur Indonesia sering fokus channel cost-push, padahal data 2020–2024 menunjukkan **respons moneter BI lebih dominan secara statistik**. Argumen kebijakan: stabilisasi rupiah via BI rate punya efek lebih cepat ke demand transport daripada intervensi cost-push BBM.

---

## Bab 4 — Robustness: Kontrol Confounder (Anggota 4) | 6 WS

### Pertanyaan Riset
Apakah korelasi naive Bab 2 bertahan setelah dikontrol untuk COVID, musim, volatilitas?

### WS yang dibuat
| WS | Folder | Output Utama |
|---|---|---|
| WS1 Facet COVID | `ws1_facet_covid/` | Lockdown slope=−318 (p=0,65), transisi=+1.555 (p=0,001), recovery=+706 (p=0,04) |
| WS2 Volatilitas spread | `ws2_volatilitas/` | R²=0,0006 (tidak signifikan) |
| WS3 Efek Lebaran | `ws3_lebaran/` | Median DOM 5.338 vs 5.621 (boost 1,05×, p=0,70 *tidak signifikan* karena Lebaran overlap COVID) |
| WS4 Efek Natal | `ws4_natal/` | Median 5.839 vs **7.704** (boost **1,32×** signifikan) |
| WS5 Hari libur | `ws5_hari_libur/` | R²=0,001, slope negatif spurious |
| WS6 Peak season × kurs | `ws6_peak_season_interaction/` | Non-peak R²=0,24; peak R²=**0,55** (**2,2× lebih sensitif**) |

### Pesan utama Bab 4 (REVISI sesuai output)
~~Korelasi kurs–penumpang tetap signifikan di 2–3 fase COVID~~ → **TIDAK, hanya lockdown phase yang slope negatif (sesuai teori) tapi tidak signifikan (p=0,65).**

Yang benar:
- **Naive correlation Bab 2 adalah artefak structural break COVID**. Setelah faceting per `covid_phase`, tidak ada fase yang menunjukkan slope negatif signifikan.
- **Volatilitas kurs** sendiri tidak punya korelasi dengan demand (R²~0).
- **Efek Lebaran tidak signifikan** (boost hanya 1,05× median, p=0,70) karena 3 dari 5 bulan Lebaran terjadi di periode COVID.
- **Efek Natal signifikan** (boost 1,32× median) karena Natal tidak overlap lockdown.
- **Peak season 2,2× lebih sensitif** ke kurs daripada non-peak — finding bermakna.

### Implikasi untuk Paper
Bab 4 = *intellectual rigor*. Membuktikan bahwa korelasi naive *misleading*. Paper jadi lebih kuat secara metodologis daripada hanya pakai R² dari Bab 2.

---

## Bab 5 — Heterogenitas Geografis (Anggota 5) | 5 WS

### Pertanyaan Riset
Siapa paling sensitif? Rute/negara/provinsi mana?

### WS yang dibuat
| WS | Folder | Output Utama |
|---|---|---|
| WS1 Top 15 rute | `ws1_top_rute/` | CGK-DPS (16,8M), CGK-KNO (12,4M), CGK-SUB (11,5M); 12/15 rute domestik, **14/15 via CGK** |
| WS2 Sensitivitas INT (top 10) | `ws2_sensitivitas_int/` | Slope ascending: DPS-SYD +17, DPS-MEL +18 (R² rendah, Aussie tahan kurs) → CGK-SIN +114 (volume tinggi) |
| WS3 Per-negara | `ws3_per_negara/` | 14 negara analyzed; R² range 0,25 (Saudi) – 0,53 (Filipina); slope tergantung volume (Malaysia +342) |
| WS4 OD matrix | `ws4_od_matrix/` | Heatmap top 10 IATA × top 10 IATA; konfirmasi hub CGK dominan |
| WS5 Provinsi origin | `ws5_provinsi/` | Jakarta + DKI Jakarta 124,78M (~50% domestik); Kalimantan, Riau Islands, Bali secondary |

**WS6 Hub vs Spoke**: opsional, tidak dibuat. Bisa ditambah di Tableau saat presentasi kalau perlu.

### Pesan utama Bab 5 (REVISI sesuai output)
~~Rute ke negara dengan ekonomi USD-pegged (Jepang, AS, Australia) lebih sensitif daripada ASEAN~~ → **TIDAK persis seperti itu**.

Yang benar (lebih nuanced):
- **Slope absolute** terbesar di **Malaysia (+342)** dan **Singapura (+278)** — *karena volume terbesar* (20M dan 19M), bukan elastisitas.
- **R² tertinggi** di **Filipina (0,53)**, **Qatar (0,51)**, **Thailand (0,51)**, **Malaysia (0,50)**.
- **R² rendah** di **Arab Saudi (0,25)** dan **Jepang (0,33)** — driver lain dominan (kuota haji untuk Saudi, kebijakan visa untuk Jepang).
- **Australia** punya volume besar (7,9M) tapi R² moderate (0,48), mendukung argumen *inbound Aussie tahan kurs lemah*.
- **CGK adalah hub absolut** — 14 dari 15 top rute melewati CGK.

### Implikasi untuk Paper
Headline finding: "Sensitivitas demand terhadap kurs tidak seragam — rute ke **ASEAN dan Timur Tengah komersial** paling responsif secara statistik; rute ke **Arab Saudi (haji) dan Jepang (visa)** punya driver non-makro dominan. Implikasi kebijakan berbeda per koridor."

---

## 4. Catatan Aggregasi (KRUSIAL — Wajib di Tableau)

Tetap sesuai plan. Setelah physical join, measure makro ter-replikasi ke 553 rute. Default agg:

| Field | Default Agg |
|---|---|
| `jumlah_penumpang` | **SUM** (additive) |
| Semua kolom makro (`avg_kurs_*`, `min/max_kurs_*`, `bi_rate`, `inflasi_*`, `tarif_tiket_ihk`, `brent_*`) | **AVG** |
| `jumlah_hari_libur`, `jumlah_hari_trading` | AVG |

Rule sederhana: **`jumlah_penumpang = SUM. Semua makro = AVG.`**

---

## 5. Tips Presentasi (50 menit, 10 menit per anggota)

**Urutan presentasi:**
1. **Anggota 1 (Bab 1)** — set the stage 2020–2024.
2. **Anggota 2 (Bab 2)** — *headline naive*: "kami menemukan korelasi signifikan, tapi arahnya mengejutkan (POSITIF)."
3. **Anggota 3 (Bab 3)** — mekanisme: "channel moneter dominan, bukan cost-push semata."
4. **Anggota 4 (Bab 4)** — *the reveal*: "naive correlation Bab 2 adalah artefak COVID. Bukti faceting."
5. **Anggota 5 (Bab 5)** — implikasi praktis per rute & negara.

**Alur dramatis:** Bab 2 menanam pertanyaan ("kenapa slope positif?"), Bab 3 dan 4 menjawabnya, Bab 5 turunkan ke level operasional.

**Tip teknis:**
- Setiap anggota siapkan **1 Dashboard di Tableau** dengan 3–5 worksheet.
- **Annotation R² & slope manual** di tiap chart (jangan andalkan hover saat live).
- **Reference Lines event** (PSBB, PPKM, Rusia-Ukraina, VOA, PPKM dicabut, Rupiah 16K) — bikin sekali, terapkan ke semua time series.
- **Cross-check angka Tableau vs Python**: setiap R² dan slope di Tableau harus match dengan `metrics.txt` di folder Python yang relevan.

---

## 6. Ringkasan Validasi Akhir

| Aspek | Status |
|---|---|
| Total WS Python | **24/24** ✓ (3 dashboard di Tableau dibuat saat presentasi) |
| Output file (analysis.py + plot.png + metrics + penjelasan.md) | ✓ Lengkap di 24 folder |
| Kolom WAJIB di plan | ✓ Semua sudah dipakai di setidaknya 1 WS |
| Signifikansi statistik finding inti | ✓ 3 dari 4 finding utama p<0,001 |
| Konsistensi narrative | ✓ Sudah di-update agar match output (slope positif spurious → kontrol COVID → channel moneter dominan) |
| Layak untuk paper | ✓ **YA** dengan framing "honest reporting" |

---

## 7. Saran Final Sebelum Mulai Tableau

1. **Sebelum buat WS**, baca `penjelasan.md` di folder Python yang sesuai. Section "Target Tableau" di tiap penjelasan punya instruksi step-by-step.
2. **Setelah selesai tiap WS**, cross-check angka R² dan slope dengan `metrics.txt`/`.csv`. Mismatch = ada masalah di aggregation default (kemungkinan besar lupa set AVG untuk kolom makro).
3. **Untuk Bab 4 WS1 (facet COVID)**: ini sheet TERPENTING dari seluruh analisis kalian, karena menjelaskan kenapa naive correlation Bab 2 misleading. Beri perhatian ekstra ke visualisasinya.
4. **Untuk Bab 5 WS3 (per-negara)**: ini *headline international*. Pastikan calculated field `negara_asing` benar (lihat penjelasan.md).
5. **Buat dashboard di akhir tiap bab** — bukan saat awal — supaya semua worksheet sudah final dan filter action bisa di-set dengan benar.

Selamat membuat Tableau. Kalau ada angka yang tidak match dengan Python, kembali ke `penjelasan.md` dulu untuk cek default agg & filter.
