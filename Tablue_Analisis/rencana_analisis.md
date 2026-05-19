# Rencana Analisis Komprehensif

**Topik:** Korelasi Nilai Rupiah (IDR/USD) Terhadap Angkutan Udara Indonesia
**Periode:** Januari 2020 – Desember 2024 (60 bulan)
**Grain analisis:** Bulanan × Rute
**Anggota:** 5 orang × 1 bab per anggota
**Sumber data:** `output/BULANAN/` (sudah di-physical-join di Tableau, pusat = `fact_penumpang_rute`)

---

## 1. Penilaian Rencana Lama (Bab 1–5 di `tutorial.md`, core only)

Rencana lama **bukan cacat fatal** untuk topik ini — alur (konteks → hipotesis → mekanisme → robustness → heterogenitas) sehat dan sudah menyentuh kurs, penumpang, covid_phase, Lebaran/Natal. Tapi karena kamu cuma menjalankan *core* (skip semua "extension opsional"), ada **empat gap material** yang bikin analisis belum maksimal mengingat tabel `fact_makro_bulanan` kamu sebenarnya kaya:

| # | Gap | Konsekuensi |
|---|---|---|
| 1 | `bi_rate`, `inflasi_yoy`, `inflasi_mtm` hanya jadi overlay di Bab 1, tidak pernah diuji sebagai variabel analisis | Channel monetary/income (selain cost-push avtur) tidak teruji. Padahal jalur **kurs → BI rate → daya beli → demand** sama validnya secara teori dengan jalur cost-push. |
| 2 | Volatilitas kurs (`max_kurs_tengah - min_kurs_tengah`) tidak dianalisis | Bulan-bulan stress pasar (Mar 2020, Feb 2022, Okt 2024) ditangkap hanya lewat level, bukan regime stress. Konsumen sering tunda perjalanan saat *uncertainty* tinggi, bukan saat kurs *tinggi*. |
| 3 | Analisis per-negara destinasi cuma extension Bab 5 | Hipotesis "kurs USD/IDR menekan demand internasional" paling tajam ketika dibreakdown by negara. Rute ke US/JP/EU/AU lebih ter-dolarized daripada ASEAN — ini headline finding yang hilang. |
| 4 | `jumlah_hari_libur` & `is_peak_season` tidak dipakai | Kontrol musiman terbatas pada flag Lebaran/Natal saja, granularity tidak optimal. |

**Verdict:** rencana lama cukup untuk *menghantar* topik, tapi belum memaksimalkan data. Rencana di bawah dirancang dari nol untuk menyentuh **semua kolom yang bernilai analitik** dalam batas 5 bab × 3–5 worksheet per bab.

---

## 2. Inventaris & Pemetaan Kolom

### 2.1 Kolom yang **WAJIB** dipakai

| Tabel | Kolom | Peran analitik | Dipakai di Bab |
|---|---|---|---|
| `fact_penumpang_rute` | `jumlah_penumpang` | **Outcome utama** (additive, SUM) | 1, 2, 3, 4, 5 |
| `fact_makro_bulanan` | `avg_kurs_tengah` | **Variabel X utama** (level kurs) | 1, 2, 3, 4, 5 |
| `fact_makro_bulanan` | `min_kurs_tengah`, `max_kurs_tengah` | Volatilitas (spread = max − min) | 1, 4 |
| `fact_makro_bulanan` | `brent_usd_bbl` | Proxy biaya avtur (channel cost-push) | 1, 3 |
| `fact_makro_bulanan` | `bi_rate` | Channel kebijakan moneter | 1, 3 |
| `fact_makro_bulanan` | `inflasi_yoy`, `inflasi_mtm` | Channel daya beli | 1, 3 |
| `fact_makro_bulanan` | `tarif_tiket_ihk` | Outcome antara (channel pricing) | 3 |
| `dim_waktu_bulanan` | `tahun`, `bulan`, `nama_bulan` | Sumbu waktu, label seasonal | 1, 2, 3, 4, 5 |
| `dim_waktu_bulanan` | `covid_phase` | Confounder struktural (4 fase) | 1, 2, 3, 4, 5 |
| `dim_waktu_bulanan` | `has_lebaran`, `has_natal`, `is_peak_season` | Seasonal control (binary) | 1, 4 |
| `dim_waktu_bulanan` | `jumlah_hari_libur` | Seasonal control (kontinyu) | 4 |
| `dim_rute` | `kategori` (DOM/INT) | Segmentasi inti | 2, 4, 5 |
| `dim_rute` | `kode_rute` | Level rute (heterogenitas) | 5 |
| `dim_bandara` (origin & destination) | `iata`, `negara`, `provinsi` | OD matrix, geografi | 5 |

### 2.2 Kolom yang **boleh diabaikan** (pertimbangan: low signal, redundan, atau hanya untuk label)

| Tabel | Kolom | Alasan |
|---|---|---|
| `fact_makro_bulanan` | `avg_kurs_jual`, `avg_kurs_beli` | Redundan dengan `avg_kurs_tengah` (selisih tipis, korelasi >0.99). Pilih satu. |
| `fact_makro_bulanan` | `jumlah_hari_trading` | Hanya 16–23 per bulan, variasi kecil, low analytical value. |
| `fact_makro_bulanan` | `brent_high`, `brent_low` | Hanya berguna kalau mau bandingkan volatilitas Brent paralel dengan volatilitas kurs — opsional, bukan core. |
| `dim_waktu_bulanan` | `kuartal`, `semester` | Redundan untuk data bulanan. Pakai kalau perlu agregasi kuartal saja. |
| `dim_bandara` | `nama_bandara` | Pakai sebagai *tooltip/label* saja, bukan dimensi analisis (gunakan `iata` atau `kota`). |
| `dim_bandara` | `bandara_id`, `rute_id`, `waktu_id` | Surrogate key, dipakai Tableau internal lewat join. Bukan dimensi analisis. |

Kalau presentasi mepet waktu, **semua kolom di tabel 2.2 boleh tidak disebut** sama sekali tanpa mengurangi kualitas argumen.

---

## 3. Alur Naratif 5 Bab

```
Bab 1: KONTEKS         → "Apa yang terjadi 2020–2024?"
Bab 2: HIPOTESIS UTAMA → "Apakah kurs ↑ membuat penumpang ↓?"
Bab 3: MEKANISME       → "Lewat jalur apa kurs sampai ke penumpang?"
                          (3 channel paralel: cost-push, moneter, daya beli)
Bab 4: ROBUSTNESS      → "Apakah korelasi bertahan setelah dikontrol?"
                          (COVID, musim, volatilitas)
Bab 5: HETEROGENITAS   → "Siapa yang paling kena? Rute/negara/provinsi mana?"
```

Setiap bab membangun di atas bab sebelumnya. Pembagian anggota tetap 1-bab-per-orang (Anggota 1 = Bab 1, dst).

---

## Bab 1 — Lanskap Makro × Demand (Anggota 1)

### Pertanyaan Riset
Bagaimana kurs IDR/USD dan demand angkutan udara Indonesia berkembang 2020–2024, dan event eksternal apa yang membentuknya?

### Variabel
- **fact_makro:** `avg_kurs_tengah`, `min_kurs_tengah`, `max_kurs_tengah`, `brent_usd_bbl`, `bi_rate`, `inflasi_yoy`, `inflasi_mtm`
- **fact_penumpang:** `jumlah_penumpang`
- **dim_waktu:** `tahun`, `bulan`, `nama_bulan`, `covid_phase`

### Worksheet

**WS1 — Multi-panel time series (4 panel sejajar ke bawah)**
- *Columns:* `Tanggal Analisis` (calculated: `DATEPARSE('yyyyMM', STR([waktu_id]))`, continuous month).
- *Rows (4 pil terpisah):* `SUM(jumlah_penumpang)`, `AVG(avg_kurs_tengah)`, `AVG(brent_usd_bbl)`, `AVG(bi_rate)`.
- *Marks:* Line.
- *Annotations (Reference Lines):* 01-Mar-2020 (PSBB), 01-Jul-2021 (PPKM Darurat), 01-Feb-2022 (Russia–Ukraine), 01-May-2022 (VOA dibuka), 01-Jan-2023 (PPKM dicabut), 01-Apr-2024 (rupiah tembus Rp 16.000), 01-Oct-2024 (eskalasi Timur Tengah).
- **Tujuan:** audience melihat pergerakan 4 indikator inti dalam satu *narrative timeline* sebelum bicara korelasi.

**WS2 — Kurs band (level + volatility band)**
- *Columns:* `Tanggal Analisis` (continuous).
- *Rows:* `AVG(avg_kurs_tengah)` (line), lalu tambah `AVG(min_kurs_tengah)` dan `AVG(max_kurs_tengah)` sebagai dual axis → buat band (area chart) di belakang line.
- **Tujuan:** menampilkan kurs bukan sebagai angka tunggal tapi rentang per bulan — visualnya kuat untuk menyoroti stres pasar (Mar 2020, Okt 2024).

**WS3 — Inflasi YoY & MtM dengan COVID phase background**
- *Columns:* `Tanggal Analisis` (continuous).
- *Rows:* `AVG(inflasi_yoy)` di axis kiri, `AVG(inflasi_mtm)` di axis kanan (dual axis, jangan synchronize karena beda skala).
- *Pane background color:* `covid_phase` (drag ke Color, atur transparan ~30%).
- **Tujuan:** memperlihatkan bagaimana fase COVID overlap dengan rezim inflasi yang berbeda — setup untuk Bab 4.

**WS4 — Seasonal heatmap penumpang (tahun × bulan)**
- *Columns:* `nama_bulan` (discrete, sort manual Jan–Des).
- *Rows:* `tahun` (discrete).
- *Marks:* Square.
- *Color:* `SUM(jumlah_penumpang)` (sequential palette, mis. orange).
- **Tujuan:** pattern musiman + COVID dip terlihat dalam satu visual.

### Pesan utama Bab 1
Periode 2020–2024 terdiri dari **empat rezim** (`pre_pandemic`, `lockdown`, `transisi`, `recovery`) dengan kurs naik 17% (~13.700 → ~16.100) dan demand pulih asimetris. Belum bicara korelasi, baru *setting the stage*.

---

## Bab 2 — Hipotesis Utama: Kurs ↑ → Demand ↓ ? (Anggota 2)

### Pertanyaan Riset
Apakah ada hubungan signifikan antara level kurs IDR/USD dan jumlah penumpang? Apakah arah dan kekuatan hubungan berbeda antara **domestik** dan **internasional**? Apakah efek bersifat *contemporaneous* atau *lagged*?

### Variabel
- **fact_makro:** `avg_kurs_tengah`
- **fact_penumpang:** `jumlah_penumpang`
- **dim_rute:** `kategori` (DOM/INT)
- **dim_waktu:** `covid_phase`, `waktu_id`

### Worksheet

**WS1 — Scatter kurs × total penumpang**
- *Columns:* `AVG(avg_kurs_tengah)`. *Rows:* `SUM(jumlah_penumpang)`.
- *Detail:* `waktu_id` (Dimension/discrete) → 60 titik.
- *Color:* `covid_phase`. *Trend Line:* Linear.
- **Catat:** R² dan slope dari tooltip trend line.

**WS2 — Scatter kurs × penumpang INTERNASIONAL**
- Duplicate WS1. *Filter:* `kategori` = INTERNASIONAL.
- Biasanya R² lebih tinggi dan slope negatif lebih curam → hipotesis teoritis terkonfirmasi.

**WS3 — Scatter kurs × penumpang DOMESTIK**
- Duplicate WS1. *Filter:* `kategori` = DOMESTIK.
- Slope biasanya lebih landai atau ambigu (cost di-pass-through sebagian saja).

**WS4 — Lag scatter (kurs t−1 → penumpang t)**
- Buat calculated field: `Kurs Lag 1 = LOOKUP(AVG([avg_kurs_tengah]), -1)`.
- Scatter: *Columns* `Kurs Lag 1`, *Rows* `SUM(jumlah_penumpang)`, *Detail* `waktu_id`, *Color* `covid_phase`, trend linear.
- Ulangi untuk Lag 2 dan Lag 3 → bandingkan R². Booking biasanya dilakukan 1–3 bulan sebelumnya, jadi puncak korelasi sering di lag 1–2.

**WS5 — Dashboard ringkasan**
- Gabung WS1–WS3 berdampingan + tabel kecil ringkasan R² & slope dari WS4.

### Pesan utama Bab 2
Slope kurs–penumpang **negatif** dan signifikan, dengan magnitudo lebih besar di INT daripada DOM, dan puncak korelasi pada lag 1–2 bulan (jika ditemukan). Ini *headline finding* paper kalian.

---

## Bab 3 — Mekanisme Transmisi (Anggota 3)

### Pertanyaan Riset
Jika kurs benar-benar mempengaruhi demand, **lewat jalur apa**? Tiga channel paralel diuji:

1. **Cost-push channel:** kurs → Brent dalam IDR → tarif tiket → penumpang.
2. **Monetary channel:** kurs → BI rate (respon kebijakan) → biaya kapital/kredit konsumtif → penumpang.
3. **Purchasing-power channel:** kurs → inflasi → daya beli riil → penumpang.

### Variabel
- **fact_makro:** `avg_kurs_tengah`, `brent_usd_bbl`, `tarif_tiket_ihk`, `bi_rate`, `inflasi_yoy`
- **fact_penumpang:** `jumlah_penumpang`
- **dim_waktu:** `covid_phase`, `waktu_id`

### Worksheet

**WS1 — Channel 1 Step A: Kurs × Brent (in IDR)**
- Buat calculated field: `Brent IDR per Bbl = AVG([brent_usd_bbl]) * AVG([avg_kurs_tengah])`.
- *Columns:* `AVG(avg_kurs_tengah)`. *Rows:* `Brent IDR per Bbl`. *Detail:* `waktu_id`. *Color:* `covid_phase`. Trend linear.
- **Tujuan:** menunjukkan bahwa biaya avtur dalam IDR naik dua kali lipat — sekali karena Brent naik, sekali karena kurs.

**WS2 — Channel 1 Step B: Brent IDR × Tarif tiket IHK**
- *Columns:* `Brent IDR per Bbl`. *Rows:* `AVG(tarif_tiket_ihk)`. *Detail:* `waktu_id`. *Color:* `covid_phase`. Trend linear.

**WS3 — Channel 1 Step C: Tarif tiket × Penumpang**
- *Columns:* `AVG(tarif_tiket_ihk)`. *Rows:* `SUM(jumlah_penumpang)`. *Detail:* `waktu_id`. *Color:* `covid_phase`. Trend linear.

**WS4 — Channel 2: Kurs × BI rate**
- *Columns:* `AVG(avg_kurs_tengah)`. *Rows:* `AVG(bi_rate)`. *Detail:* `waktu_id`. *Color:* `covid_phase`. Trend linear.
- **Catatan:** harapkan slope positif — BI menaikkan suku bunga sebagai respons depresiasi.

**WS5 — Channel 3: Kurs × Inflasi YoY**
- *Columns:* `AVG(avg_kurs_tengah)`. *Rows:* `AVG(inflasi_yoy)`. *Detail:* `waktu_id`. *Color:* `covid_phase`. Trend linear.
- **Catatan:** pas-through kurs ke harga umum (bukan cuma tiket).

**WS6 — Dashboard "Tiga Channel"**
- Layout 3 kolom × 2 baris:
  - Baris atas (Channel 1 cost-push): WS1, WS2, WS3.
  - Baris bawah (Channel 2 & 3): WS4, WS5, kosongan/teks ringkasan.
- Annotation R² manual di setiap panel.

### Pesan utama Bab 3
Kurs mempengaruhi demand lewat **lebih dari satu jalur**. Channel cost-push (avtur → tarif) biasanya yang paling kuat, tapi channel moneter (BI rate) dan daya beli (inflasi) ikut menyumbang. Ini yang membuat paper kalian *bukan* analisis korelasi naif.

---

## Bab 4 — Robustness: Confounder + Volatility (Anggota 4)

### Pertanyaan Riset
Apakah korelasi kurs–penumpang **bertahan** setelah dikontrol untuk (a) fase COVID, (b) musim libur, (c) jumlah hari libur, (d) volatilitas kurs (bukan cuma level)?

### Variabel
- **fact_makro:** `avg_kurs_tengah`, `min_kurs_tengah`, `max_kurs_tengah`
- **fact_penumpang:** `jumlah_penumpang`
- **dim_waktu:** `covid_phase`, `has_lebaran`, `has_natal`, `is_peak_season`, `jumlah_hari_libur`
- **dim_rute:** `kategori`

### Worksheet

**WS1 — Faceted scatter per `covid_phase`**
- *Columns:* `covid_phase` (discrete) lalu `AVG(avg_kurs_tengah)`.
- *Rows:* `SUM(jumlah_penumpang)`. *Detail:* `waktu_id`. *Color:* `covid_phase`. *Trend Line:* Linear per pane.
- **Tujuan:** kalau slope tetap negatif di `recovery` (atau bahkan `pre_pandemic`), maka hubungan **bukan** artefak COVID.

**WS2 — Volatilitas kurs × penumpang**
- Calculated field: `Spread Kurs = AVG([max_kurs_tengah]) - AVG([min_kurs_tengah])`.
- *Columns:* `Spread Kurs`. *Rows:* `SUM(jumlah_penumpang)`. *Detail:* `waktu_id`. *Color:* `covid_phase`. Trend linear.
- **Tujuan:** menjawab "apakah *uncertainty* (spread besar) menekan demand independen dari level?".

**WS3 — Efek Lebaran (DOM)**
- *Filter:* `kategori` = DOMESTIK.
- *Columns:* `has_lebaran` (discrete: 0/1).
- *Rows:* `MEDIAN(jumlah_penumpang)` per rute (Detail = `kode_rute`).
- *Marks:* Bar (atau box plot via Show Me).
- **Tujuan:** kuantifikasi boost mudik.

**WS4 — Efek Natal**
- Duplicate WS3, ganti ke `has_natal`. Tidak perlu filter DOMESTIK karena Natal berlaku di kedua segmen.

**WS5 — Hubungan kontinyu: hari libur × penumpang**
- *Columns:* `jumlah_hari_libur` (continuous).
- *Rows:* `SUM(jumlah_penumpang)`. *Detail:* `waktu_id`. *Color:* `covid_phase`. Trend linear.
- **Tujuan:** menggunakan granularity kontinyu, bukan flag binary, untuk mengontrol *opportunity to travel*.

**WS6 — Interaksi `is_peak_season` × kurs**
- *Columns:* `AVG(avg_kurs_tengah)`. *Rows:* `SUM(jumlah_penumpang)`. *Detail:* `waktu_id`. *Color:* `is_peak_season` (akan ada 2 warna). *Trend Line:* Linear per color.
- **Tujuan:** apakah peak season (Lebaran, libur sekolah, Natal) lebih *resilient* terhadap pelemahan kurs?

### Pesan utama Bab 4
Korelasi kurs–penumpang tetap signifikan di 2–3 fase COVID (terutama `recovery`), volatilitas kurs sendiri ikut menekan demand, dan bulan peak-season menunjukkan sensitivitas berbeda terhadap kurs. Ini meningkatkan kredibilitas finding Bab 2.

---

## Bab 5 — Heterogenitas Geografis (Anggota 5)

### Pertanyaan Riset
Siapa yang paling kena pelemahan rupiah? Apakah ada **konsentrasi geografis** — rute, bandara, provinsi, atau negara tujuan tertentu — yang paling sensitif? Implikasi praktis untuk regulator dan maskapai.

### Variabel
- **fact_penumpang:** `jumlah_penumpang`
- **fact_makro:** `avg_kurs_tengah`
- **dim_rute:** `kategori`, `kode_rute`
- **dim_bandara (origin & destination):** `iata`, `kota`, `provinsi`, `negara`

### Worksheet

**WS1 — Top 15 rute by penumpang total**
- *Rows:* `kode_rute`. *Columns:* `SUM(jumlah_penumpang)`. Sort descending.
- *Filter:* Top 15 by SUM(jumlah_penumpang). *Color:* `kategori`.
- **Tujuan:** konteks "rute mana yang penting" sebelum bicara sensitivitas.

**WS2 — Sensitivitas per rute INTERNASIONAL**
- *Filter:* `kategori` = INTERNASIONAL. *Filter tambahan:* Top 10 rute INT by total penumpang (agar chart tidak terlalu ramai).
- *Columns:* `AVG(avg_kurs_tengah)`. *Rows:* `SUM(jumlah_penumpang)`. *Detail:* `waktu_id`. *Color:* `kode_rute`.
- *Trend Line:* Linear **per color** (centang "Linear per color").
- **Tujuan:** rute dengan slope paling curam negatif = paling sensitif terhadap kurs.

**WS3 — Sensitivitas per NEGARA destinasi**
- Pakai instance `dim_bandara_destination` (yang join via `bandara_2_id`).
- *Filter:* `kategori` = INTERNASIONAL.
- *Columns:* `AVG(avg_kurs_tengah)`. *Rows:* `SUM(jumlah_penumpang)`. *Detail:* `waktu_id`. *Color:* `[dim_bandara_destination].negara`.
- *Trend Line:* Linear per color.
- **Tujuan:** hipotesis teoritis — negara dengan mata uang yang berkorelasi kuat dengan USD (US, JP, AU, EU, KSA, UAE) lebih sensitif daripada ASEAN (yang juga mengalami depresiasi paralel).

**WS4 — OD Matrix (Top 10 origin × Top 10 destination)**
- *Rows:* `[dim_bandara_origin].iata`. *Columns:* `[dim_bandara_destination].iata`.
- *Marks:* Square. *Color:* `SUM(jumlah_penumpang)`. *Filter:* Top 10 di kedua axis.
- **Tujuan:** flow asimetris klasik — hub vs spoke, dominasi rute Java–Bali.

**WS5 — Peta provinsi origin**
- *Marks:* Map (Tableau auto-detect provinsi).
- Drag `[dim_bandara_origin].provinsi` ke worksheet.
- *Size:* `SUM(jumlah_penumpang)`. *Color:* slope sensitivitas (calculated field; alternatif: total penumpang dengan filter `tahun` = 2024).
- **Tujuan:** distribusi geografis demand domestik dan pengaruhnya.

**WS6 (opsional, kalau waktu cukup) — Hub vs Spoke**
- Calculated field: `Tipe Origin = IF [dim_bandara_origin].iata IN ('CGK','DPS','SUB','KNO','UPG') THEN 'Hub' ELSE 'Spoke' END`.
- Scatter kurs × penumpang dengan *Color* = Tipe Origin, trend line per color.

### Pesan utama Bab 5
Pelemahan rupiah **tidak rata pukulannya**. Rute ke negara dengan ekonomi USD-pegged (Jepang, AS, Australia) lebih sensitif daripada ke ASEAN. Hub utama (CGK, DPS) menunjukkan pola berbeda dari spoke airports. Ini implikasi konkret untuk strategi maskapai dan kebijakan tarif batas atas regulator.

---

## 4. Catatan Aggregasi (KRUSIAL — Jangan Salah!)

Karena `fact_makro_bulanan` di-join ke grain bulanan-per-rute, **setiap baris makro di-replikasi** ke ratusan baris rute di bulan yang sama. Konsekuensinya:

| Measure | Default agg yang BENAR |
|---|---|
| `jumlah_penumpang` | **SUM** (additive) |
| `avg_kurs_jual`, `avg_kurs_beli`, `avg_kurs_tengah` | **AVG** |
| `min_kurs_tengah`, `max_kurs_tengah` | **AVG** |
| `jumlah_hari_trading` | AVG |
| `tarif_tiket_ihk` | AVG |
| `inflasi_yoy`, `inflasi_mtm` | AVG |
| `bi_rate` | AVG |
| `brent_usd_bbl`, `brent_high`, `brent_low` | AVG |
| `jumlah_hari_libur` | AVG |

**Cara setting di Tableau:** klik kanan setiap measure makro di Data pane → **Default Properties → Aggregation → Average**. Lakukan **satu kali** untuk seluruh kolom makro. Setelah itu di mana pun mereka di-drag, default agg sudah AVG.

**Rule sederhana untuk diingat:** *jumlah_penumpang = SUM. Semua makro = AVG.*

---

## 5. Tips Presentasi (50 menit, 10 menit per anggota)

**Urutan:**
1. **Anggota 1 (Bab 1)** — set the stage, audience harus paham 2020–2024 *terjadi apa* dulu sebelum bicara korelasi.
2. **Anggota 2 (Bab 2)** — *headline finding* langsung. Audience masih segar, maksimalkan dampak.
3. **Anggota 3 (Bab 3)** — perdalam dengan *kok bisa*. Channel mana yang dominan.
4. **Anggota 4 (Bab 4)** — *critical thinker*. "Ini bukan kebetulan COVID/seasonal." Bagian yang bikin paper terlihat *rigorous*.
5. **Anggota 5 (Bab 5)** — *zoom in* ke rute & geografi, tutup dengan implikasi praktis.

**Tip Tableau presentasi:**
- Setiap anggota siapkan **1 Dashboard** (bukan banyak worksheet terpisah). Susun 3–5 worksheet per dashboard side-by-side.
- Pakai **Filter Action** antar worksheet di dashboard supaya audience bisa lihat interaksi.
- Beri **annotation R² dan slope** secara manual sebagai teks di atas tiap scatter (jangan andalkan hover saat presentasi).
- Reference Lines di chart waktu untuk event-event (PSBB, PPKM Darurat, Rusia–Ukraina, VOA, PPKM dicabut, Rupiah 16K) — bikin sekali, terapkan ke semua worksheet time series.

---

## 6. Ringkasan: Apa yang Berubah dari Rencana Lama?

| Aspek | Rencana lama (core only) | Rencana baru |
|---|---|---|
| Channel di Bab 3 | 1 channel (cost-push: kurs→Brent→tarif→pax) | **3 channel paralel**: cost-push + moneter (BI rate) + daya beli (inflasi) |
| Volatilitas kurs | Tidak dipakai | **WS terpisah** di Bab 1 (band) + Bab 4 (spread × penumpang) |
| Per-negara destinasi | Extension Bab 5 (skip) | **WS3 inti** di Bab 5 |
| `jumlah_hari_libur` | Tidak dipakai | **WS5 Bab 4** (kontrol kontinyu) |
| `is_peak_season` | Tidak dipakai | **WS6 Bab 4** (interaksi dengan kurs) |
| `min/max_kurs_tengah` | Tidak dipakai | **WS2 Bab 1** + spread di Bab 4 |
| Lag analysis | Extension Bab 2 (skip) | **WS4 inti** di Bab 2 |

**Total worksheet:** ~26 (Bab 1: 4, Bab 2: 5, Bab 3: 6, Bab 4: 6, Bab 5: 5–6). Rata-rata 5 per anggota — masih realistis untuk 1 minggu kerja.

---

## 7. Apa yang Aman Diabaikan

Kalau waktu mepet, **boleh skip** tanpa melemahkan argumen utama:
- `avg_kurs_jual`, `avg_kurs_beli` (redundan dengan `avg_kurs_tengah`)
- `jumlah_hari_trading` (low signal)
- `brent_high`, `brent_low` (hanya kalau mau bahas volatilitas Brent paralel)
- `kuartal`, `semester` (redundan untuk data bulanan)
- `nama_bandara` (label saja)
- WS6 Bab 5 (Hub vs Spoke) — *nice-to-have*, bukan core

Yang **TIDAK boleh** diskip karena akan melemahkan topik:
- Channel moneter (WS4 Bab 3) — jangan hilangkan, sayang sekali kalau `bi_rate` tidak dipakai
- Per-negara destinasi (WS3 Bab 5) — ini *headline* internasional
- Faceted scatter per covid_phase (WS1 Bab 4) — robustness check inti
