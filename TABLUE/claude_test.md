Oke, aku ajarin pelan-pelan dari nol. Baca sampai habis sebelum mulai klik — biar paham dulu "kenapa"-nya, baru eksekusi.

---

# BAGIAN 1: PEMAHAMAN DASAR DULU

## Kenapa harus 2 Data Source (DS1 & DS2)?

Data kamu punya dua "ritme waktu" berbeda:

- **Ritme bulanan** — `fact_penumpang_rute` (data per bulan) dan `fact_kurs_bulanan` (kurs per bulan)
- **Ritme tahunan** — `fact_statistik_rute`, `fact_lalu_lintas_bandara`, `fact_produksi_maskapai`, `fact_otp_maskapai` (semua per tahun) dan `fact_kurs_tahunan` (kurs per tahun)

Kalau dipaksa jadi 1 DS, Tableau akan duplikasi baris (fanout) dan semua angka SUM jadi salah. Makanya dipisah 2.

## Apa itu Physical Join?

Physical join = gabung semua tabel jadi **satu tabel besar** di level data source. Tableau akan bikin satu query SQL raksasa yang join semua tabel sekaligus. Baris menggembung, tapi Tableau tahu kapan harus hitung distinct.

Alternatifnya "Relationship" (garis putus noodle) yang kamu bilang error — itu lain. Kita pakai physical join karena kamu minta fisik.

## Aturan Join yang Harus Dipahami

Di physical join, **urutan tabel penting**. Tabel pertama yang kamu drop ke canvas jadi "pusat" — tabel lain nempel ke tabel ini (atau ke tabel yang sudah nempel).

Kita selalu pilih **fact table sebagai pusat**, bukan dimensi. Kenapa? Karena dimensi bersifat lookup (banyak FK fact nunjuk ke 1 dim), sementara fact adalah data transaksional utama.

---

# BAGIAN 2: BUAT DATA SOURCE 1 (JALUR BULANAN)

## Tujuan DS1

Menggabungkan data **kurs bulanan** dengan **penumpang per rute per bulan**, plus info deskriptif rute dan bandara. Ini adalah data source utama untuk analisis korelasi kurs vs penumpang.

## Tabel yang dipakai di DS1

1. `fact_penumpang_rute` — pusat
2. `fact_kurs_bulanan` — kurs bulanan
3. `dim_waktu_bulanan` — atribut waktu (nama bulan, kuartal, semester)
4. `dim_rute` — info rute
5. `dim_bandara` — info lokasi bandara

## Langkah Klik per Klik

**Step 1 — Buka Tableau Desktop**

Klik **Open** → **More** di panel kiri → Connect → **Text file** → pilih `fact_penumpang_rute.csv` → Open.

Tableau akan buka halaman Data Source (bagian bawah ada canvas kosong, tengah ada preview data).

**Step 2 — Drag tabel pusat ke canvas**

Di kiri ada daftar Files. Drag `fact_penumpang_rute.csv` ke **canvas bagian atas** (area kotak besar yang tulisannya "Drag tables here").

Setelah drag, klik **2 kali** pada kotak `fact_penumpang_rute` di canvas → akan terbuka **area physical layer** (canvas kedua yang lebih kecil, warnanya agak putih). Di sinilah kita physical join.

**⚠️ Penting:** Pastikan kamu di physical layer, bukan logical layer. Ciri physical layer: judul canvas-nya tulisannya "Open" di atas, atau muncul kotak canvas kedua di bawah canvas pertama. Kalau cuma 1 canvas besar dan kotaknya bisa dihubungkan pakai garis noodle, itu logical (relationship).

**Step 3 — Join fact_kurs_bulanan**

Dari panel Files kiri, drag `fact_kurs_bulanan.csv` ke **sebelah kanan** kotak `fact_penumpang_rute` di physical layer.

Popup join akan muncul. Set:
- **Join type:** klik **Left** (ikon diagram lingkaran kiri terisi)
- **Data source:** `fact_penumpang_rute` → pilih field `waktu_id`
- **Second source:** `fact_kurs_bulanan` → pilih field `waktu_id`

Tutup popup dengan klik X di pojok kanan popup.

**Kenapa Left Join?** Karena kita mau semua baris penumpang tetap ada, meskipun kalau ada bulan yang tidak ada kursnya. Dalam kasusmu kurs selalu lengkap, tapi Left Join adalah default aman.

**Step 4 — Join dim_waktu_bulanan**

Drag `dim_waktu_bulanan.csv` ke sebelah kanan. Set:
- Left Join
- `fact_penumpang_rute.waktu_id` = `dim_waktu_bulanan.waktu_id`

**Step 5 — Join dim_rute**

Drag `dim_rute.csv`. Set:
- Left Join
- `fact_penumpang_rute.rute_id` = `dim_rute.rute_id`

**Step 6 — Join dim_bandara (2 kali!)**

Ini bagian tricky. `dim_rute` punya **dua** FK bandara: `bandara_1_id` dan `bandara_2_id`. Jadi kita butuh `dim_bandara` di-join dua kali dengan nama berbeda.

**Join pertama (bandara asal):**
Drag `dim_bandara.csv` ke canvas. Set:
- Left Join
- `dim_rute.bandara_1_id` = `dim_bandara.bandara_id`

Setelah muncul di canvas, **klik kanan** pada kotak `dim_bandara` → **Rename** → ubah jadi `Bandara Asal`.

**Join kedua (bandara tujuan):**
Drag `dim_bandara.csv` **lagi** (file yang sama dari panel Files). Set:
- Left Join
- `dim_rute.bandara_2_id` = `dim_bandara.bandara_id`

Rename kotak kedua ini jadi `Bandara Tujuan`.

**Kenapa 2 kali?** Karena satu rute punya 2 bandara (asal & tujuan), dan kita mau lihat info detail keduanya di Tableau. Tanpa ini kamu cuma bisa tau 1 bandara per rute.

**Step 7 — Rename dan save Data Source**

Di pojok kiri bawah, ada tab nama sheet/data source. Klik kanan nama data source (biasanya "fact_penumpang_rute+") → **Rename** → ketik `DS1 Bulanan`.

**Step 8 — Cek total baris**

Sebelum lanjut, di pojok kanan atas Data Source editor ada tulisan "Update Now" atau angka jumlah row. Klik **Update Now**. Harusnya muncul **±18.610 baris**. Kalau jauh lebih banyak (puluhan ribu lebih), berarti ada fanout — berhenti dan cek ulang join.

---

# BAGIAN 3: BUAT DATA SOURCE 2 (JALUR TAHUNAN)

## Tujuan DS2

Menggabungkan semua fakta tahunan dengan kurs tahunan, sehingga setiap fakta tahunan bisa di-korelasikan dengan kurs.

## Tabel di DS2

1. `fact_kurs_tahunan` — pusat (5 baris, 2020–2024)
2. `fact_statistik_rute` — statistik rute tahunan
3. `fact_lalu_lintas_bandara` — trafik bandara tahunan
4. `fact_produksi_maskapai` — produksi maskapai tahunan
5. `fact_otp_maskapai` — OTP tahunan
6. `dim_rute`, `dim_bandara` (2x), `dim_maskapai` — dimensi pendukung

## Kenapa fact_kurs_tahunan jadi pusat, bukan fact tahunan lain?

Karena `fact_kurs_tahunan` adalah satu-satunya tabel dengan grain pure waktu (5 baris). Kalau pakai misalnya `fact_produksi_maskapai` sebagai pusat, baris-baris di fact lain yang tidak punya maskapai yang sama akan hilang. Dengan kurs sebagai pusat, semua fact tahunan bisa nempel via `waktu_id` yang sama.

## Langkah Klik per Klik

**Step 1 — Tambah Data Source baru**

Di toolbar atas Tableau, klik menu **Data** → **New Data Source** → pilih Text file → `fact_kurs_tahunan.csv`.

**Step 2 — Drag tabel pusat**

Drag `fact_kurs_tahunan.csv` ke canvas atas → klik 2x untuk masuk ke physical layer.

**Step 3 — Join fact tahunan satu per satu (semua ke fact_kurs_tahunan via waktu_id)**

Drag `fact_statistik_rute.csv` → Left Join → `fact_kurs_tahunan.waktu_id = fact_statistik_rute.waktu_id`

Drag `fact_lalu_lintas_bandara.csv` → Left Join → `fact_kurs_tahunan.waktu_id = fact_lalu_lintas_bandara.waktu_id`

Drag `fact_produksi_maskapai.csv` → Left Join → `fact_kurs_tahunan.waktu_id = fact_produksi_maskapai.waktu_id`

Drag `fact_otp_maskapai.csv` → Left Join → `fact_kurs_tahunan.waktu_id = fact_otp_maskapai.waktu_id`

**⚠️ PERINGATAN FANOUT:** Setelah 4 fact di-join, row count di physical layer akan **membengkak drastis**. Ini normal karena setiap tahun punya banyak rute, banyak bandara, banyak maskapai yang semua di-cross-join. Tableau akan handle ini dengan `COUNTD` (count distinct) nanti di sheet, tapi kamu **HARUS** pakai LOD atau distinct aggregation — nanti aku jelaskan di bagian testing.

**Step 4 — Join dimensi**

Drag `dim_rute.csv` → Left Join → `fact_statistik_rute.rute_id = dim_rute.rute_id`

Drag `dim_bandara.csv` → Left Join → `fact_lalu_lintas_bandara.bandara_id = dim_bandara.bandara_id`. Rename jadi `Bandara Lalu Lintas`.

Drag `dim_rute` butuh `dim_bandara` juga untuk info asal/tujuan rute di fact_statistik. Tapi untuk menyederhanakan, **skip dulu** — cuma ambil nama bandara dari satu sisi. Kalau nanti perlu detail bandara asal/tujuan di analisis rute tahunan, baru tambah.

Drag `dim_maskapai.csv` → Left Join → `fact_produksi_maskapai.maskapai_id = dim_maskapai.maskapai_id`

**Step 5 — Rename Data Source**

Klik kanan nama data source → Rename jadi `DS2 Tahunan`.

---

# BAGIAN 4: TESTING DI SHEET — MEMASTIKAN SEMUA BENAR

## Yang perlu kamu pahami sebelum testing

Karena kita pakai physical join (bukan relationship), setiap row di data source sudah "flat" — tapi bisa ada duplikasi. Aturan penting:

1. **SUM untuk ukuran bulanan di DS1** = aman, karena grain `fact_penumpang_rute` adalah bulan × rute, tidak ada duplikasi.
2. **SUM untuk ukuran di DS2** = **HATI-HATI**, karena di DS2 ada cross-join antar fakta tahunan. Kamu harus pakai **MIN** atau **AVG** untuk metrik, **bukan SUM**, saat dicampur dengan fact lain.

Aku akan kasih test yang bisa kamu eksekusi langsung.

---

## TEST DS1 — Semua di data source "DS1 Bulanan"

### Test 1.1 — Validasi dim_waktu_bulanan
**Tujuan:** Memastikan join waktu benar.

- Buka Sheet 1
- Pastikan di kiri atas panel Data, nama data source = `DS1 Bulanan`
- Drag `Nama Bulan` (dari tabel `dim_waktu_bulanan`) → **Columns**
- Drag `Tahun` (dari `dim_waktu_bulanan`) → **Rows**
- Drag `Jumlah Penumpang` (dari `fact_penumpang_rute`) → **Text** di Marks card
- Pastikan `Jumlah Penumpang` aggregation-nya **SUM** (klik pill → Measure → Sum)

**Hasil harusnya:** Tabel 5 baris (2020–2024) × 12 kolom bulan. Isinya angka jutaan. Contoh: 2020 Januari harusnya sekitar 6,8 juta penumpang.

**Kalau salah:** Angka sama persis di semua sel → join waktu_id gagal. Cek ulang format waktu_id (integer 6 digit: 202001).

### Test 1.2 — Validasi kurs bulanan
**Tujuan:** Memastikan kurs ikut ke DS1.

- New worksheet
- Drag `Tahun` (dim_waktu_bulanan) → Columns
- Drag `Nama Bulan` (dim_waktu_bulanan) → Rows
- Drag `Avg Kurs Tengah` (dari `fact_kurs_bulanan`) → Text
- Ubah aggregation jadi **AVG** (klik pill → Measure → Average)

**Hasil harusnya:** Angka antara 13.000–16.500. Tiap sel ada 1 nilai (60 sel total = 5 tahun × 12 bulan).

**Kalau salah:** NULL semua → waktu_id DS1 kurs tidak match dengan dim_waktu_bulanan. Cek tipe data kolom waktu_id, harus Number (whole).

### Test 1.3 — Korelasi kurs vs penumpang (INTI PROYEK)
**Tujuan:** Scatter plot korelasi.

- New worksheet
- Drag `Avg Kurs Tengah` → **Columns** → ubah aggregation ke **AVG**
- Drag `Jumlah Penumpang` → **Rows** → aggregation **SUM**
- Drag `Tahun` dan `Nama Bulan` (keduanya dari dim_waktu_bulanan) → **Detail** di Marks card
- Ubah chart type ke **Circle** (Marks dropdown → Circle)

**Hasil harusnya:** Scatter dengan **60 titik**, tiap titik = 1 bulan. Kamu bisa lihat apakah kurs tinggi ↔ penumpang rendah (korelasi negatif) atau sebaliknya.

**Kalau salah:**
- Muncul 1 titik saja → `Tahun` dan `Nama Bulan` belum di Detail
- Muncul banyak titik aneh (>60) → ada fanout, cek join

### Test 1.4 — Dual axis time series
**Tujuan:** Visualisasi tren bareng.

- New worksheet
- Drag `Tahun` → Columns, lalu drag `Nama Bulan` → Columns (di kanan Tahun)
  - Pastikan `Nama Bulan` jadi **Discrete** (warna biru). Kalau Continuous (hijau), klik pill → Discrete.
  - Urutan bulan harus Januari sampai Desember. Kalau berantakan, klik pill `Nama Bulan` → Sort → Manual → atur urutan.
- Drag `Jumlah Penumpang` → Rows → SUM
- Drag `Avg Kurs Tengah` → Rows (tepat di sebelah kanan pill penumpang, harus muncul grafik kedua di bawah) → AVG
- Klik kanan pill `Avg Kurs Tengah` di Rows → **Dual Axis**
- Klik kanan sumbu kanan (Avg Kurs Tengah) → **Synchronize Axis** (JANGAN di-synchronize karena skala beda jauh, biarkan tidak sinkron)

**Hasil harusnya:** 2 garis tumpang tindih, 1 untuk penumpang (jutaan), 1 untuk kurs (belasan ribu). Lihat pola apakah naik-turunnya berlawanan arah atau sama.

---

## TEST DS2 — Semua di data source "DS2 Tahunan"

### Test 2.1 — Validasi baris fakta tidak duplikat

**Tujuan:** Karena di DS2 ada cross-join, kita cek apakah angka fakta benar dengan aggregation yang tepat.

- New worksheet → ubah data source ke `DS2 Tahunan` (klik nama DS di panel kiri atas)
- Drag `Waktu Id` (dari `fact_kurs_tahunan`) → Columns → ubah jadi **Discrete** (klik pill → Discrete)
- Drag `Otp Percentage` (dari `fact_otp_maskapai`) → Rows → aggregation **AVG**
- Drag `Nama Maskapai` (dari `dim_maskapai`) → Color

**Hasil harusnya:** Garis/bar per maskapai, 2020–2024, nilainya antara 0.0–1.0.

**⚠️ PENTING:** Kalau pakai SUM malah dapat angka >1 (misal 5.2), itu karena fanout. Solusinya: **JANGAN pakai SUM untuk otp_percentage**, pakai **AVG** atau **MIN** (karena semua duplikat barisnya bernilai sama, AVG/MIN menghasilkan nilai asli).

### Test 2.2 — Produksi maskapai per tahun

- New worksheet di DS2
- Drag `Waktu Id` (fact_kurs_tahunan) → Columns, Discrete
- Drag `Nama Maskapai` → Rows
- Drag `Passenger Carried` (fact_produksi_maskapai) → Text

**PERHATIAN:** Coba dulu aggregation **SUM**. Kalau angkanya kelihatan aneh banget (terlalu besar), ganti ke **MIN** atau **AVG**. Alasannya: setiap row maskapai-tahun sudah unik di `fact_produksi_maskapai`, tapi karena di-join dengan tabel lain di DS2, barisnya terduplikasi. MIN/AVG akan kembalikan nilai asli per baris unik.

**Tips universal untuk DS2:** Untuk setiap metrik tahunan di DS2, **gunakan MIN atau AVG**, bukan SUM, kecuali kamu secara sadar ingin menjumlahkan lintas maskapai atau bandara.

### Test 2.3 — Korelasi kurs tahunan vs produksi

- New worksheet di DS2
- Drag `Avg Kurs Tengah` (fact_kurs_tahunan) → Columns → AVG
- Drag `Passenger Carried` (fact_produksi_maskapai) → Rows → **SUM** (dengan asumsi kamu mau total penumpang lintas semua maskapai)

**HATI-HATI:** Karena cross-join di DS2, SUM di sini tidak akurat. Cara benar:

Bikin **Calculated Field** (klik kanan di panel Data → Create Calculated Field):
- Nama: `Total Penumpang Tahunan (Fixed)`
- Formula:
  ```
  { FIXED [Waktu Id (Fact Kurs Tahunan)], [Maskapai Id] : MIN([Passenger Carried]) }
  ```
- Pakai ini di Rows, aggregation SUM.

Ini namanya **LOD (Level of Detail) expression**. Fungsinya: ambil nilai passenger_carried unik per kombinasi tahun-maskapai (MIN karena duplikatnya semua sama), lalu baru SUM lintas maskapai. Ini cara benar handle fanout di DS2.

- Drag `Waktu Id` (fact_kurs_tahunan) → Detail
- Ganti chart type ke Circle

**Hasil:** 5 titik scatter (2020, 2021, 2022, 2023, 2024).

---

## CHEATSHEET AGGREGATION

| Data Source | Tabel | Metrik | Aggregation |
|:---|:---|:---|:---|
| DS1 | fact_penumpang_rute | jumlah_penumpang | **SUM** (aman) |
| DS1 | fact_kurs_bulanan | avg_kurs_* | **AVG** |
| DS1 | fact_kurs_bulanan | min_kurs | **MIN** |
| DS1 | fact_kurs_bulanan | max_kurs | **MAX** |
| DS2 | fact_statistik_rute | jumlah_* | **SUM dengan LOD** atau MIN per grain |
| DS2 | fact_lalu_lintas_bandara | semua metrik | **SUM dengan LOD** atau MIN |
| DS2 | fact_produksi_maskapai | semua metrik | **SUM dengan LOD** atau MIN |
| DS2 | fact_otp_maskapai | otp_percentage | **AVG** (bukan SUM!) |
| DS2 | fact_kurs_tahunan | avg_kurs_* | **AVG** |

---

## Penyelamat kalau Error

| Gejala | Penyebab | Solusi |
|:---|:---|:---|
| Angka NULL semua | waktu_id tipe data salah | Data Source editor → klik ikon tipe data (Abc/#) di atas kolom → ubah ke Number (whole) |
| Total penumpang DS1 > 100 juta per bulan | Fanout | Cek ulang join — harusnya `fact_penumpang_rute` pusat, bukan dim |
| OTP > 1.0 | Duplikasi dari fanout | Ganti SUM → AVG |
| Bulan tidak urut Jan-Des | Default sort alphabetic | Sort manual pill `Nama Bulan` |
| Chart kosong | Data source aktif salah | Cek panel kiri atas, pilih DS yang benar |

Mulai dari Test 1.1 dulu, baru lanjut. Kalau mentok di step tertentu, kasih tau angka yang keluar dan aku bantu debug.