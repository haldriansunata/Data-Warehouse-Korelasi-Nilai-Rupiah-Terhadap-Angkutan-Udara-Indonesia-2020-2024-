# Solusi Masalah Implementasi Tableau — Master Doc

Dokumen ini menjawab semua isu yang kamu catat di `masalah umum.txt` dan `gabisa.txt`. Disusun berdasarkan **urutan pengerjaan**: yang bisa langsung kamu fiks tanpa bukti → yang butuh upload SS/CSV → yang ditunda.

---

## Klasifikasi Masalah

| # | Isu | Status | Butuh Bukti? |
|---:|---|---|---|
| 1 | Masalah Umum #1 — covid_phase di Color memecah trend line | ✅ **SOLVABLE LANGSUNG** | ❌ |
| 2 | Masalah Umum #2 — Format angka `#,##0,,M` | ✅ **SOLVABLE LANGSUNG** | ❌ |
| 3 | Bab 4 — `has_natal`/`has_lebaran`/`is_peak_season` dimension vs measure | ✅ **SOLVABLE LANGSUNG** | ❌ |
| 4 | Bab 4 WS5 — `jumlah_hari_libur` AVG/SUM? | ✅ **SOLVABLE LANGSUNG** | ❌ |
| 5 | Bab 4 WS2 — `AGG(Spread Kurs)` apakah benar? | ✅ **SOLVABLE LANGSUNG** | ❌ |
| 6 | Bab 5 WS2 — beda bar (Python) vs scatter (Tableau) | ✅ **SOLVABLE LANGSUNG** | ❌ |
| 7 | Bab 5 WS3 — field `negara_asing` tidak ada + Filipina belum muncul | ✅ **RESOLVED** (lihat fix di bawah) | ✅ sudah dicek |
| 8 | Bab 5 WS4 — IATA origin vs destination tidak match | ✅ **RESOLVED** (lihat fix di bawah) | ✅ sudah dicek |
| 9 | Bab 5 WS5 — provinsi (duplikat ID/Inggris) | ✅ **RESOLVED** — Group manual di Tableau | ❌ |

---

## URUTAN PENGERJAAN

### FASE 1 — Fiks Langsung (Tanpa Bukti)
1. Solusi #1 (covid_phase + trend line) — **paling impact**, harus dulu karena memengaruhi Describe Trend Model di banyak WS.
2. Solusi #2 (format angka)
3. Solusi #3, #4, #5 (Bab 4 dimension/measure & agg)
4. Solusi #6 (Bab 5 WS2 — penjelasan saja)

### FASE 2 — Upload Bukti
5. Solusi #7 (Bab 5 WS3) — upload SS Data pane + SS chart sekarang
6. Solusi #8 (Bab 5 WS4) — upload CSV export

### FASE 3 — Cek Angka
Setelah semua di atas selesai, baru bandingkan angka Tableau vs Python.

---

# FASE 1 — SOLUSI LANGSUNG

## Solusi #1 — covid_phase di Color Memecah Trend Line

### Penyebab
Saat `covid_phase` di-drop ke **Color**, Tableau default-nya membuat trend line **per warna** (per fase). Akibat: tampil 4 trend line + Describe Trend Model output 4 persamaan.

### Solusi (yang sesuai keinginanmu: 1 garis + titik tetap warna)
1. Klik **Analytics** pane (kiri atas, sebelah Data).
2. Klik kanan di trend line di chart → **Edit Trend Lines** (atau dari Analytics pane → klik kanan Trend Line yang sudah ada).
3. Di jendela "Trend Lines Options", **uncheck** `[ ] Allow a trend line per color`.
4. Klik OK.

Hasil: **1 trend line** untuk semua 60 titik (lintas fase), tapi **titik tetap berwarna** sesuai covid_phase. Describe Trend Model sekarang akan tampil **1 model tunggal**.

### Mana yang trend line-nya HARUS tetap multi (jangan uncheck)?
Beberapa WS memang sengaja pakai trend line per warna karena itu **bagian analisisnya**:

| WS | Trend Line | Alasan |
|---|---|---|
| Bab 2 WS1, WS2, WS3, WS4 | **1 garis** | Headline correlation; warna cuma untuk konteks COVID |
| Bab 3 WS1, WS2, WS3, WS4, WS5 | **1 garis** | Channel analysis full data |
| **Bab 4 WS1** (Faceted COVID) | **multi (per pane)** | Justru poin analisanya — slope berbeda per fase |
| Bab 4 WS2 (Volatilitas) | **1 garis** | Cek hubungan spread vs pax full data |
| Bab 4 WS5 (Hari Libur) | **1 garis** | Cek korelasi hari libur vs pax full data |
| **Bab 4 WS6** (Peak Interaction) | **multi (per is_peak_season)** | Justru poin analisanya — slope peak vs non-peak |
| **Bab 5 WS2** (Top 10 Rute) | **multi (per kode_rute)** | Justru poin analisanya — slope per rute |
| **Bab 5 WS3** (Per Negara) | **multi (per negara)** | Justru poin analisanya — slope per negara |

### Alternatif jika kamu tidak suka pakai uncheck
Pindahkan `covid_phase` dari **Color** ke **Detail**:
- Trend line otomatis 1 garis ✓
- Tapi titik **tidak berwarna lagi** (semua warna sama) ✗

Solusi uncheck `Allow a trend line per color` lebih cocok untuk kamu.

---

## Solusi #2 — Format Angka `#,##0,,M`

### Penyebab
Format `#,##0,,M` artinya: tampilkan angka dibagi 1.000.000 (dua koma = scale juta), lalu suffix "M".
- 9.122.039 → `9M` (tidak ada desimal)
- 96.452 → `0M` (terlalu kecil)

Format ini terlalu kasar untuk data dengan range lebar (96K – 9M).

### Solusi (pilih salah satu)

**Opsi A — Sederhana, tetap desimal (REKOMENDASI)**
Format custom: `#,##0.0,,"M"` (perhatikan ada `.0` sebelum dua koma).
- 9.122.039 → `9.1M`
- 96.452 → `0.1M`

Caranya:
1. Klik kanan field di Marks/Label/Tooltip → **Format**.
2. Di **Pane** atau **Default Numbers**, pilih **Numbers (Custom)**.
3. Decimal places: `1`.
4. Suffix: ketik `M`.
5. Display Units: pilih **Millions (M)**.

**Opsi B — Pakai K untuk angka kecil, M untuk yang besar**
Format custom: `[>=1000000]#,##0.0,,"M";[>=1000]#,##0,"K";#,##0`
- 9.122.039 → `9.1M`
- 96.452 → `96K`
- 850 → `850`

**Opsi C — Biarkan saja (yang kamu lakukan sekarang)**
Tidak salah, hanya kurang rapi untuk visual presentasi. Untuk angka penuh tampil seperti `9,122,039` — bisa diterima untuk analisis, tapi dashboard mungkin terlalu lebar.

### Catatan untuk kamu
Karena kamu sekarang biarkan default (Opsi C), aku **tidak akan paksa ganti**. Tapi sebelum demo final, pertimbangkan Opsi A untuk dashboard yang lebih rapih.

---

## Solusi #3 — `has_natal` / `has_lebaran` / `is_peak_season` Dimension vs Measure

### Aturan singkat
| Field | Nilai | Convert ke | Alasan |
|---|---|---|---|
| `has_lebaran` | 0/1 | **Dimension** ✓ | Flag biner → kategori |
| `has_natal` | 0/1 | **Dimension** ✓ | Flag biner → kategori |
| `is_peak_season` | 0/1 | **Dimension** ✓ | Flag biner → kategori |
| `jumlah_hari_libur` | 0–5 | **Dimension** kalau pakai untuk grouping; **Measure (AVG)** kalau pakai di axis numerik |

Yang kamu lakukan (convert ke Dimension): **BENAR**.

### Cara convert
Klik kanan field di Data pane → **Convert to Dimension**. Pil yang tadi hijau (continuous measure) jadi biru (discrete dimension).

---

## Solusi #4 — Bab 4 WS5 `jumlah_hari_libur` AVG atau SUM?

### Jawab: **AVG** (lebih konsisten)

### Penjelasan
`jumlah_hari_libur` ada di `dim_waktu_bulanan` — **1 nilai per `waktu_id`**. Saat scatter dengan `waktu_id` di Detail, aggregator (AVG/SUM/MIN/MAX) sama saja hasilnya karena hanya 1 baris per kombinasi.

Tapi **konvensi**:
- Field di `fact_makro` / `dim_waktu` yang sifatnya "1 nilai per bulan" (kurs, BI rate, hari libur) → **AVG**.
- Field di `fact_penumpang_rute` yang menjumlahkan banyak baris → **SUM**.

Set default aggregation `jumlah_hari_libur` ke **Average** (klik kanan di Data pane → Default Properties → Aggregation → Average).

---

## Solusi #5 — Bab 4 WS2 `AGG(Spread Kurs)` Apakah Benar?

### Jawab: **BENAR**, ini perilaku normal Tableau

### Penjelasan
Calculated field-mu:
```
Spread Kurs = AVG([max_kurs_tengah]) - AVG([min_kurs_tengah])
```

Karena formula sudah pakai `AVG(...)` di dalamnya, Tableau menganggap field-nya sudah ter-aggregate (level: aggregate measure). Saat di-drag ke Columns, otomatis dibungkus `AGG(...)`.

`AGG(Spread Kurs)` = `Average(max) - Average(min)` per granularity (di sini per `waktu_id`).

### Yang penting: jangan dobel-aggregate
Jangan buat `AVG([Spread Kurs])` di Tableau — itu akan **error** ("Cannot mix aggregate and non-aggregate"). Field yang sudah ada `AGG(...)` jangan dibungkus lagi.

---

## Solusi #6 — Bab 5 WS2 Beda Bar (Python) vs Scatter (Tableau)

### Penjelasan
- **Python `plot.png`**: horizontal bar chart, X = slope per rute, Y = nama rute. Tujuannya ranking visual.
- **Tableau tutorial**: scatter `kurs vs pax` per rute, 10 trend line. Tujuannya menunjukkan slope individual + spread datanya.

**Keduanya valid** — mereka menjawab pertanyaan yang sama dari sudut berbeda:
- Bar = "Mana rute paling sensitif?" (ranking jelas)
- Scatter+trend = "Seberapa erat hubungan kurs–pax di tiap rute?" (visual goodness-of-fit)

### Kalau mau buat bar versi Tableau (bonus)
Bisa! Pakai calculated field WINDOW_CORR:
```
Slope per Rute = (WINDOW_AVG(SUM([jumlah_penumpang]) * AVG([avg_kurs_tengah])) -
                  WINDOW_AVG(SUM([jumlah_penumpang])) * WINDOW_AVG(AVG([avg_kurs_tengah]))) /
                 (WINDOW_AVG(AVG([avg_kurs_tengah])^2) - WINDOW_AVG(AVG([avg_kurs_tengah]))^2)
```
Lalu bar chart: Y = `kode_rute`, X = `Slope per Rute`. Filter top 10 rute INT.

Tapi ini opsional — yang sekarang sudah cukup baik untuk paper.

---

# FASE 2 — BUTUH BUKTI VISUAL

## Solusi #7 — Bab 5 WS3 Field `negara_asing` Tidak Ada

### Penyebab
Tutorial menyebut `o_negara` dan `d_negara` sebagai field setelah self-join `dim_bandara` 2x. Tapi di Tableau-mu, field yang muncul mungkin namanya:
- `Negara` (dari instance pertama dim_bandara)
- `Negara (Dim Bandara.csv1)` atau `Negara1` (dari instance kedua)

Jadi formula calculated field di tutorial **tidak match**.

### Untuk fiks ini, aku butuh BUKTI dari kamu

Upload ke folder **`output/BULANAN/analisis/masalah/feedback_tableau/bab5_ws3_per_negara/`**:

1. **SS1_data_pane.png** — Screenshot Data pane Tableau yang nge-zoom ke field-field hasil join dim_bandara. Aku perlu lihat **nama exact** field-field `negara`, `iata`, `kota` dari kedua instance.

2. **SS2_data_source_tab.png** — Screenshot tab **Data Source** (kiri bawah Tableau) yang menampilkan join structure-mu. Aku mau verifikasi join key: apakah pakai `bandara_1_id ↔ bandara_id` (origin) dan `bandara_2_id ↔ bandara_id` (destination).

3. **SS3_chart_sekarang.png** — Screenshot worksheet `Bab5_WS3_PerNegara` apa adanya sekarang (sebelum diperbaiki). Termasuk Marks card, Filters, Columns, Rows.

4. **export_negara_visible.csv** — Di worksheet WS3, klik kanan sheet → **View Data → Full Data → Download**. Aku perlu lihat list negara yang muncul dan urutannya.

### Yang aku akan kerjakan setelah file di atas masuk
- Rewrite calculated field `negara_asing` dengan nama field yang benar
- Pastikan filter "Top 14 by SUM(pax)" menghasilkan Filipina (kalau tidak, debug kenapa)
- Update penjelasan WS3 dengan instruksi yang match data structure-mu

---

## Solusi #8 — Bab 5 WS4 IATA Origin vs Destination Tidak Match

### Penyebab (kemungkinan besar)
ETL `dim_rute` di proyek ini menormalisasi pasangan bandara secara **alfabetis**: pair `(A, B)` di mana A < B alfabetis. Jadi:
- Bandara dengan IATA awal alfabet (A, B, C) → sering jadi `bandara_1` (origin di matrix)
- Bandara dengan IATA akhir alfabet (Y, U, S) → sering jadi `bandara_2` (destination di matrix)

Akibat: top 10 origin ≠ top 10 destination — list-nya berbeda. Ini **bukan bug**, tapi konsekuensi data structure.

### Untuk fiks ini, aku butuh BUKTI dari kamu

Upload ke folder **`output/BULANAN/analisis/masalah/feedback_tableau/bab5_ws4_od_matrix/`**:

1. **export_top10_origin.csv** — Di worksheet WS4, klik kanan field `o_iata` di Rows → **Show Filter** → buka filter UI. Atau lebih simpel: buat sheet baru dengan `o_iata` di Rows, `SUM(pax)` di Columns, sort desc, export top 10. Aku mau lihat top 10 IATA dari sisi origin.

2. **export_top10_destination.csv** — Sama tapi untuk `d_iata` di Rows.

3. **SS_od_matrix_sekarang.png** — Screenshot OD matrix-mu sekarang apa adanya.

### Yang aku akan kerjakan setelah file di atas masuk
- Bandingkan list origin vs destination kamu dengan output Python
- Update tutorial WS4 dengan solusi yang sesuai (kemungkinan: pakai **union top 15** = top 10 dari kedua sisi, gabung ke 1 filter)

---

# UPDATE: FASE 2 SUDAH RESOLVED (Sumber: bukti yang kamu upload)

## Solusi #7 — RESOLVED ✅
**Diagnosis**: filter di WS3 pakai `[Negara]` (origin) bukan calculated field `negara_asing`. Akibat Filipina (yang ada di sisi destination MNL) tidak muncul.

**Fix lengkap**: lihat section **"🔧 PERBAIKAN FINAL"** di `bab_5_heterogenitas/ws3_per_negara/penjelasan.md`. Yang harus kamu lakukan:
1. Hapus filter `Negara` lama dari Filters dan Color.
2. Buat calculated field `Negara Asing = IF [Negara] != "INDONESIA" THEN [Negara] ELSE [Negara (Dim Bandara Destination.Csv)] END`.
3. Pakai `Negara Asing` di filter (Top 14 by SUM pax) + Color.

Setelah ini, 14 negara akan muncul **termasuk Filipina** dan match Python.

## Solusi #8 — RESOLVED ✅
**Diagnosis**: Top 10 Tableau (per axis sendiri-sendiri) ≠ Top 10 Python (per gabungan kedua axis), karena dim_rute normalize pasangan alfabetis.

**Fix lengkap**: lihat section **"🔧 PERBAIKAN FINAL"** di `bab_5_heterogenitas/ws4_od_matrix/penjelasan.md`. Yang harus kamu lakukan:
1. Pakai 1 list IATA tunggal yang sama untuk kedua axis: **`CGK, DPS, SUB, UPG, KNO, SIN, BPN, KUL, BTH, YIA`**.
2. Filter `o_iata` IN list + filter `d_iata` IN list (manual select, atau pakai Set).

Setelah ini, OD matrix akan match Python.

---

# UPDATE: Solusi #9 — RESOLVED ✅

## Bab 5 WS5 Provinsi
Pendekatan **Group manual di Tableau Web** (tidak ubah CSV, aman untuk 24 sheet lain).

Field `Provinsi` di `dim_bandara` punya **18 pasangan duplikat** Bahasa Indonesia vs Inggris (mis. JAKARTA vs DKI JAKARTA; EAST KALIMANTAN vs KALIMANTAN TIMUR).

**Fix lengkap**: lihat `bab_5_heterogenitas/ws5_provinsi/penjelasan.md` → section "Target Tableau — Tutorial Step-by-Step":
- Step 1 = Buat Group `Provinsi (Cleaned)` dengan 18 pasangan (tabel mapping lengkap di tutorial).
- Step 2-8 = Bar chart Top 15.
- Step 9 (opsional) = Peta provinsi.

Pendekatan B (fix CSV via Python) dibahas tapi tidak dipilih karena resiko di Tableau Web Authoring (Replace Data Source terbatas) lebih tinggi dari benefit-nya.

---

# RINGKASAN: APA YANG HARUS KAMU LAKUKAN SEKARANG

1. **Baca Solusi #1 sampai #6** — semuanya bisa langsung kamu fiks sendiri di Tableau tanpa bantuan aku lagi.
2. **Setelah selesai dengan #1-#6**, kerjakan upload bukti untuk #7 dan #8 ke folder:
   ```
   output/BULANAN/analisis/masalah/feedback_tableau/
   ├── bab5_ws3_per_negara/
   │     ├── SS1_data_pane.png
   │     ├── SS2_data_source_tab.png
   │     ├── SS3_chart_sekarang.png
   │     └── export_negara_visible.csv
   ├── bab5_ws4_od_matrix/
   │     ├── export_top10_origin.csv
   │     ├── export_top10_destination.csv
   │     └── SS_od_matrix_sekarang.png
   └── _global/                      (kalau ada masalah tambahan)
   ```
3. **Bilang ke aku** kalau folder sudah terisi → aku lanjut analisa dan fiks tutorial WS3/WS4.
4. Setelah #7 dan #8 selesai → baru kita masuk **FASE 3** (WS5 provinsi) + **cek angka Python vs Tableau**.

---

# CATATAN BAB 1 (yang kamu fiks sendiri)

Aku baca `gabisa.txt`. Solusi AI yang kamu pakai untuk WS2 dan WS3 Bab 1 sudah benar:

- **Bab 1 WS2** (Measure Values untuk 3 line min/max/avg) — solusi pakai Measure Values + Measure Names ke Color: ✅ valid.
- **Bab 1 WS3** (Reference Band 4 fase COVID): ✅ valid, tanggal-tanggalnya sesuai dengan ETL covid_phase di `build_makro_warehouse.py`.
- **Bab 2 WS4** (Lag Dynamic Parameter): ✅ valid, instruksi Compute Using = `waktu_id` Ascending sudah benar.
- **Bab 5 WS2** (filter Top 10 by Kode Rute): ✅ valid.

Jadi work yang kamu lakukan sendirian dengan AI lain itu OK semua. Tidak perlu diulang.
