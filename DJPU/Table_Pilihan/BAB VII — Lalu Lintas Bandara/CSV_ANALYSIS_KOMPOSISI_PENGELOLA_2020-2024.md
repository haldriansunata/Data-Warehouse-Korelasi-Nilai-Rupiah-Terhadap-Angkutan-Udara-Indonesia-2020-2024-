# CSV Analysis: Komposisi Penumpang Berdasarkan Pengelola Bandar Udara (2020-2024)

## 📊 Informasi Umum

| Properti | Nilai |
|----------|-------|
| **Nama File** | `KOMPOSISI PENUMPANG BERDASARKAN PENGELOLA BANDAR UDARA TAHUN 2020.csv` s/d `2024.csv` |
| **Jumlah File** | 5 file (1 file per tahun: 2020, 2021, 2022, 2023, 2024) |
| **Jumlah Baris per File** | 5 baris (4 pengelola + 1 Total) |
| **Jumlah Kolom** | 7 |
| **Tipe Data Utama** | String (nama pengelola) & Integer (angka dengan titik sebagai pemisah ribuan) |
| **Missing Value** | Tanda `-` (hanya muncul di 2021 & 2024) |

---

## 📖 Penjelasan Pengelola Bandar Udara

Sebelum masuk ke analisis data, penting untuk memahami **siapa saja pengelola bandara** di Indonesia dan apa tugas mereka.

### 1. AP I — PT Angkasa Pura I (Persero)

| Properti | Detail |
|----------|--------|
| **Kepanjangan** | Angkasa Pura I |
| **Status** | Badan Usaha Milik Negara (BUMN) |
| **Tugas Utama** | Mengelola bandara-bandara komersial di **Indonesia Bagian Tengah dan Timur** |
| **Jumlah Bandara** | 13 bandara utama |
| **Contoh Bandara** | Makassar (UPG), Denpasar (DPS), Manado (MDC), Ambon (AMQ), Sorong (SOQ), dll. |
| **Fungsi** | Mengoperasikan, memelihara, dan mengembangkan bandara menjadi hub penerbangan yang profitable dan efisien |

**Wilayah Kerja:** Sulawesi, Bali, Nusa Tenggara, Maluku, Papua, dan sebagian Kalimantan.

---

### 2. AP II — PT Angkasa Pura II (Persero)

| Properti | Detail |
|----------|--------|
| **Kepanjangan** | Angkasa Pura II |
| **Status** | Badan Usaha Milik Negara (BUMN) |
| **Tugas Utama** | Mengelola bandara-bandara komersial di **Indonesia Bagian Barat** |
| **Jumlah Bandara** | 13 bandara utama |
| **Contoh Bandara** | Jakarta Soekarno-Hatta (CGK), Jakarta Halim (HLP), Medan (KNO), Palembang (PLM), Pekanbaru (PKU), dll. |
| **Fungsi** | Sama seperti AP I, tapi untuk wilayah barat Indonesia |

**Wilayah Kerja:** Sumatera, Jawa, Kalimantan bagian barat, dan sekitarnya.

---

### 3. BUBU — Badan Usaha Bandar Udara

| Properti | Detail |
|----------|--------|
| **Kepanjangan** | Badan Usaha Bandar Udara |
| **Status** | Bisa milik negara, daerah, atau swasta (PT) |
| **Tugas Utama** | Mengelola bandara yang **tidak dikelola oleh Angkasa Pura** (biasanya bandara kecil/menengah) |
| **Contoh** | Bandara yang dikelola oleh pemerintah daerah, perusahaan swasta, atau BUMD |
| **Fungsi** | Mengoperasikan bandara untuk pelayanan publik dan komersial di daerah yang belum dijangkau AP I/AP II |

**Karakteristik:**
- Bandara yang dikelola BUBU biasanya berukuran kecil hingga menengah
- Bisa milik pemerintah daerah (Pemda), swasta, atau BUMD
- Fokus pada pelayanan penerbangan perintis dan domestik regional

---

### 4. UPBU — Unit Penyelenggara Bandar Udara

| Properti | Detail |
|----------|--------|
| **Kepanjangan** | Unit Penyelenggara Bandar Udara |
| **Status** | Unit Pelaksana Teknis (UPT) dari **Direktorat Jenderal Perhubungan Udara** (Kemenhub) |
| **Tugas Utama** | Menyelenggarakan jasa kebandarudaraan di bandara yang **belum diserahkan ke BUMN atau swasta** |
| **Contoh Bandara** | Bandara-bandara kecil di daerah terpencil/perbatasan |
| **Fungsi** | Pelayanan jasa kebandarudaraan, keamanan, keselamatan penerbangan, dan pemeliharaan bandara |

**Karakteristik:**
- Langsung di bawah Kementerian Perhubungan (Kemenhub)
- Biasanya bandara kecil di daerah 3T (Tertinggal, Terdepan, Terluar)
- Fokus pada pelayanan publik, bukan profit
- Tahap awal sebelum diserahkan ke BUMN/swasta

---

### 5. UPBU / SATPEL (2024)

| Properti | Detail |
|----------|--------|
| **Kepanjangan** | Unit Penyelenggara Bandar Udara / Satuan Penyelenggara |
| **Status** | Sama seperti UPBU, tapi kemungkinan penamaan/reskoring organisasi |
| **Perbedaan dengan UPBU** | Kemungkinan SATPEL adalah struktur organisasi yang lebih kecil dari UPBU |

**Catatan:** Muncul di 2024 menggantikan kategori UPBU dari tahun-tahun sebelumnya.

---

### 6. UPTD / PEMDA (2024)

| Properti | Detail |
|----------|--------|
| **Kepanjangan** | Unit Pelaksana Teknis Daerah / Pemerintah Daerah |
| **Status** | Bandara yang dikelola oleh Pemerintah Daerah (Pemda) |
| **Tugas Utama** | Mengelola bandara milik daerah untuk pelayanan publik |
| **Fungsi** | Pelayanan penerbangan perintis dan domestik regional |

**Karakteristik:**
- Milik pemerintah daerah (Provinsi/Kabupaten/Kota)
- Fokus pada konektivitas daerah
- Baru muncul di data 2024 (sebelumnya mungkin masuk kategori lain)

---

### 7. BANDARA KHUSUS (2024)

| Properti | Detail |
|----------|--------|
| **Status** | Bandara dengan fungsi khusus (bukan untuk umum) |
| **Contoh** | Bandara militer, bandara VIP, bandara karantina, dll. |
| **Fungsi** | Pelayanan khusus sesuai peruntukan |

**Karakteristik:**
- Tidak untuk penerbangan komersial umum
- Bisa milik TNI, kepolisian, atau instansi pemerintah tertentu
- Baru muncul di data 2024

---

## 📊 Ringkasan Perbandingan Pengelola

| Pengelola | Status | Wilayah | Fokus | Muncul |
|-----------|--------|---------|-------|--------|
| **AP I** | BUMN | Indonesia Tengah & Timur | Komersial & Profit | 2020-2023 |
| **AP II** | BUMN | Indonesia Barat | Komersial & Profit | 2020-2023 |
| **BUBU** | Negara/Daerah/Swasta | Seluruh Indonesia | Pelayanan publik & komersial | 2020-2024 |
| **UPBU** | Kemenhub | Daerah 3T/terpencil | Pelayanan publik | 2020-2023 |
| **UPBU / SATPEL** | Kemenhub | Daerah 3T/terpencil | Pelayanan publik | 2024 |
| **UPTD / PEMDA** | Pemda | Daerah | Konektivitas daerah | 2024 |
| **BANDARA KHUSUS** | Instansi tertentu | Sesuai peruntukan | Fungsi khusus | 2024 |

---

## 🔍 Mengapa AP I dan AP II Hilang di 2024?

**Kemungkinan Penyebab:**

1. **Penggabungan kategori:** AP I dan AP II mungkin digabung ke dalam kategori BUBU atau kategori baru
2. **Perubahan regulasi:** Ada perubahan aturan tentang klasifikasi bandara
3. **Perubahan struktur organisasi:** AP I dan AP II mungkin tidak lagi disebut sebagai "pengelola" tapi sebagai "operator"
4. **Data belum lengkap:** Mungkin data 2024 menggunakan metodologi pengumpulan yang berbeda

**Yang Perlu Diinvestigasi:**
- Cek regulasi terbaru dari Kemenhub tentang klasifikasi bandara
- Cek apakah ada merger atau restrukturisasi AP I/AP II
- Cek apakah data 2024 menggunakan metodologi pengumpulan yang berbeda

---

## 🗂️ Struktur Tabel

### Skema Saat Ini (Konsisten di Semua Tahun)

```
PENGELOLA BANDARA (string)
DALAM NEGERI DTG (string - angka dengan titik ribuan)
DALAM NEGERI BRKT (string - angka dengan titik ribuan)
DALAM NEGERI TOTAL (string - angka dengan titik ribuan)
LUAR NEGERI DTG (string - angka dengan titik ribuan)
LUAR NEGERI BRKT (string - angka dengan titik ribuan)
LUAR NEGERI TOTAL (string - angka dengan titik ribuan)
```

### Detail Per Kolom

| No | Nama Kolom | Deskripsi | Tipe Data Saat Ini | Tipe Data Rekomendasi | Nullable | Contoh Nilai |
|----|-----------|-----------|-------------------|----------------------|----------|--------------|
| 1 | `PENGELOLA BANDARA` | Nama pengelola bandara | String | `VARCHAR(50)` | ❌ No | `AP I`, `AP II`, `BUBU`, `UPBU` |
| 2 | `DALAM NEGERI DTG` | Jumlah penumpang domestik datang | String (titik = ribuan) | `INT` | ✅ Yes | `14.047.059` |
| 3 | `DALAM NEGERI BRKT` | Jumlah penumpang domestik berangkat | String (titik = ribuan) | `INT` | ✅ Yes | `12.004.748` |
| 4 | `DALAM NEGERI TOTAL` | Total penumpang domestik (DTG + BRKT) | String (titik = ribuan) | `INT` | ✅ Yes | `26.051.807` |
| 5 | `LUAR NEGERI DTG` | Jumlah penumpang internasional datang | String (titik = ribuan) | `INT` | ✅ Yes | `1.581.234` |
| 6 | `LUAR NEGERI BRKT` | Jumlah penumpang internasional berangkat | String (titik = ribuan) | `INT` | ✅ Yes | `1.704.300` |
| 7 | `LUAR NEGERI TOTAL` | Total penumpang internasional (DTG + BRKT) | String (titik = ribuan) | `INT` | ✅ Yes | `3.285.534` |

**Catatan:**
- **DTG** = Datang
- **BRKT** = Berangkat
- **TOTAL** = DTG + BRKT (sudah dikalkulasi di sumber)

---

## 🔍 Analisis Nilai Unik & Distribusi

### 1. Kolom `PENGELOLA BANDARA`

#### Nilai Unik per Tahun

| Pengelola | 2020 | 2021 | 2022 | 2023 | 2024 | Keterangan |
|-----------|------|------|------|------|------|------------|
| **AP I** | ✅ | ✅ | ✅ | ✅ | ❌ | Angkasa Pura I |
| **AP II** | ✅ | ✅ | ✅ | ✅ | ❌ | Angkasa Pura II |
| **BUBU** | ✅ | ✅ | ✅ | ✅ | ✅ | Bandar Udara Bukan Utama |
| **UPBU** | ✅ | ✅ | ✅ | ✅ | ❌ | Unit Penyelenggara Bandar Udara |
| **UPBU / SATPEL** | ❌ | ❌ | ❌ | ❌ | ✅ | 2024: nama berubah |
| **UPTD / PEMDA** | ❌ | ❌ | ❌ | ❌ | ✅ | 2024: kategori baru |
| **BANDARA KHUSUS** | ❌ | ❌ | ❌ | ❌ | ✅ | 2024: kategori baru |
| **TOTAL** | ✅ | ✅ | ✅ | ✅ | ✅ | Baris agregasi |

**⚠️ PERUBAHAN PENTING:**
- **2020-2023:** 4 kategori pengelola (AP I, AP II, BUBU, UPBU)
- **2024:** 4 kategori berbeda (BUBU, UPBU / SATPEL, UPTD / PEMDA, BANDARA KHUSUS)
- **AP I dan AP II hilang di 2024** → kemungkinan digabung ke kategori lain

---

### 2. Data per Tahun

#### Tahun 2020

| Pengelola | Domestik DTG | Domestik BRKT | Domestik TOTAL | Internasional DTG | Internasional BRKT | Internasional TOTAL |
|-----------|-------------|---------------|----------------|-------------------|-------------------|---------------------|
| AP I | 14.047.059 | 12.004.748 | 26.051.807 | 1.581.234 | 1.704.300 | 3.285.534 |
| AP II | 15.161.493 | 13.834.355 | 28.995.848 | 2.434.032 | 2.319.093 | 4.753.125 |
| BUBU | 1.340.861 | 1.147.704 | 2.488.565 | 5.548 | 5.597 | 11.145 |
| UPBU | 4.886.811 | 5.051.245 | 9.938.056 | 5.451 | 5.175 | 10.626 |
| **TOTAL** | **35.436.224** | **32.038.052** | **67.474.276** | **4.026.265** | **4.034.165** | **8.060.430** |

---

#### Tahun 2021

| Pengelola | Domestik DTG | Domestik BRKT | Domestik TOTAL | Internasional DTG | Internasional BRKT | Internasional TOTAL |
|-----------|-------------|---------------|----------------|-------------------|-------------------|---------------------|
| AP I | 14.386.530 | 11.849.839 | 26.236.369 | 95.954 | 13.122 | 109.076 |
| AP II | 13.581.876 | 12.990.016 | 26.571.892 | 911.060 | 896.503 | 1.807.563 |
| BUBU | 73.965 | 81.864 | 155.829 | 36 | 341 | 377 |
| UPBU | 5.063.247 | 5.146.541 | 10.209.788 | `-` | `-` | `-` |
| **TOTAL** | **33.105.618** | **30.068.260** | **63.173.878** | **1.007.050** | **909.966** | **1.917.016** |

**Catatan:** UPBU tidak punya data internasional (nilai `-`)

---

#### Tahun 2022

| Pengelola | Domestik DTG | Domestik BRKT | Domestik TOTAL | Internasional DTG | Internasional BRKT | Internasional TOTAL |
|-----------|-------------|---------------|----------------|-------------------|-------------------|---------------------|
| AP I | 22.944.203 | 19.512.802 | 42.457.005 | 2.984.094 | 2.874.374 | 5.858.468 |
| AP II | 26.753.143 | 25.078.233 | 51.831.376 | 3.772.202 | 4.216.428 | 7.988.630 |
| BUBU | 1.780.400 | 1.680.588 | 3.460.988 | 13.979 | 14.126 | 28.105 |
| UPBU | 5.460.679 | 5.384.119 | 10.844.798 | 0 | 0 | 0 |
| **TOTAL** | **56.938.425** | **51.655.742** | **108.594.167** | **6.770.275** | **7.104.928** | **13.875.203** |

**Catatan:** UPBU punya data internasional tapi 0 (bukan `-`)

---

#### Tahun 2023

| Pengelola | Domestik DTG | Domestik BRKT | Domestik TOTAL | Internasional DTG | Internasional BRKT | Internasional TOTAL |
|-----------|-------------|---------------|----------------|-------------------|-------------------|---------------------|
| AP I | 26.468.754 | 22.676.321 | 49.145.075 | 7.278.216 | 7.320.620 | 14.598.836 |
| AP II | 30.859.967 | 28.201.744 | 59.061.711 | 7.904.246 | 8.143.583 | 16.047.829 |
| BUBU | 266.721 | 266.791 | 533.512 | 23.820 | 20.513 | 44.333 |
| UPBU | 7.866.108 | 7.596.991 | 15.463.099 | 69 | 78 | 147 |
| **TOTAL** | **65.461.550** | **58.741.847** | **124.203.397** | **15.206.351** | **15.484.794** | **30.691.145** |

---

#### Tahun 2024

| Pengelola | Domestik DTG | Domestik BRKT | Domestik TOTAL | Internasional DTG | Internasional BRKT | Internasional TOTAL |
|-----------|-------------|---------------|----------------|-------------------|-------------------|---------------------|
| BUBU | 59.501.705 | 60.095.799 | 119.597.504 | 18.759.645 | 18.931.618 | 37.691.263 |
| UPBU / SATPEL | 6.345.876 | 6.341.233 | 12.687.109 | 6.961 | 6.333 | 13.294 |
| UPTD / PEMDA | 279.693 | 286.443 | 566.136 | `-` | `-` | `-` |
| BANDARA KHUSUS | 86.402 | 91.819 | 178.221 | `-` | `-` | `-` |
| **TOTAL** | **66.213.676** | **66.815.294** | **133.028.970** | **18.766.606** | **18.937.951** | **37.704.557** |

**Catatan:**
- ⚠️ **AP I dan AP II tidak ada** di 2024
- ⚠️ **Kategori baru:** UPBU / SATPEL, UPTD / PEMDA, BANDARA KHUSUS
- ⚠️ UPTD / PEMDA dan BANDARA KHUSUS tidak punya data internasional (nilai `-`)

---

## ⚠️ Potensi Masalah & Saran Pre-Processing

### 1. Format Angka dengan Titik sebagai Pemisah Ribuan

| Properti | Detail |
|----------|--------|
| **Masalah** | Angka menggunakan titik sebagai pemisah ribuan: `14.047.059` = 14,047,059 |
| **Dampak** | Jika dibaca sebagai float biasa, akan jadi 14.047059 (salah!) |
| **Saran** | **Parsing khusus:** Baca sebagai string → hapus titik → convert ke integer |

**Visualisasi Transformasi:**
```
SEBELUM:  "14.047.059"  →  Hapus titik: "14047059"  →  SESUDAH:  14047059
SEBELUM:  "1.581.234"   →  Hapus titik: "1581234"   →  SESUDAH:  1581234
```

---

### 2. Missing Value Menggunakan Tanda `-`

| Properti | Detail |
|----------|--------|
| **Masalah** | Missing value ditandai dengan `-` (bukan `0` atau sel kosong) |
| **Dampak** | ETL akan gagal convert `-` ke integer |
| **Saran** | **Replace `-` dengan `NULL`** (atau `0` jika konteksnya memang tidak ada) |

**Visualisasi Transformasi:**
```
SEBELUM:  "-"         →  SESUDAH:  NULL
SEBELUM:  "95.954"    →  SESUDAH:  95954
```

**Data yang Affected:**
| Tahun | Pengelola | Kolom yang Missing |
|-------|-----------|-------------------|
| **2021** | UPBU | LUAR NEGERI DTG, LUAR NEGERI BRKT, LUAR NEGERI TOTAL |
| **2024** | UPTD / PEMDA | LUAR NEGERI DTG, LUAR NEGERI BRKT, LUAR NEGERI TOTAL |
| **2024** | BANDARA KHUSUS | LUAR NEGERI DTG, LUAR NEGERI BRKT, LUAR NEGERI TOTAL |

---

### 3. Perubahan Kategori Pengelola di 2024 (SANGAT PENTING!)

| Properti | Detail |
|----------|--------|
| **Masalah** | 2020-2023 punya 4 kategori (AP I, AP II, BUBU, UPBU), tapi 2024 punya 4 kategori berbeda (BUBU, UPBU / SATPEL, UPTD / PEMDA, BANDARA KHUSUS) |
| **Dampak** | • Tidak bisa langsung bandingkan data 2023 vs 2024<br>• AP I dan AP II "hilang" di 2024 — kemungkinan digabung ke BUBU atau kategori lain<br>• Mapping antar tahun tidak 1-to-1 |
| **Saran** | **Buat mapping table** untuk menyamakan kategori antar tahun. Opsi: |

**Opsi Mapping:**

| Kategori 2020-2023 | Kemungkinan Mapping ke 2024 |
|--------------------|----------------------------|
| AP I | Mungkin masuk ke BUBU atau kategori baru? |
| AP II | Mungkin masuk ke BUBU atau kategori baru? |
| BUBU | BUBU (tetap) |
| UPBU | UPBU / SATPEL |

**Atau:** Pisahkan analisis 2020-2023 dan 2024 karena kategorisasi berbeda.

---

### 4. Nama Kolom dengan Singkatan (DTG, BRKT)

| Properti | Detail |
|----------|--------|
| **Masalah** | Nama kolom pakai singkatan: `DTG` (Datang), `BRKT` (Berangkat) |
| **Dampak** | • Kurang deskriptif untuk user yang tidak familiar<br>• Tapi: sudah standar di industri penerbangan |
| **Saran** | **Bisa tetap pakai singkatan** (karena sudah umum), atau rename ke `datang` / `berangkat` untuk kejelasan |

**Visualisasi Rename (Opsional):**
```
SEBELUM:  DALAM NEGERI DTG, DALAM NEGERI BRKT, DALAM NEGERI TOTAL
SESUDAH:  domestik_datang, domestik_berangkat, domestik_total
```

---

### 5. Baris TOTAL di Akhir File

| Properti | Detail |
|----------|--------|
| **Masalah** | Baris terakhir `TOTAL,...` adalah agregasi sum semua pengelola |
| **Dampak** | Jika dimuat ke database, bisa menyebabkan double-counting saat aggregasi |
| **Saran** | **Beri flag atau pisahkan:** Tambahkan kolom `is_total_row` (TRUE/FALSE), atau hapus dari data utama dan simpan sebagai metadata terpisah |

**Visualisasi:**
```
┌──────────────────┬──────────────┬──────────────┬─────────────┬────────────────┐
│ PENGELOLA        │ DOM DTG      │ DOM BRKT     │ DOM TOTAL   │ INT TOTAL      │
├──────────────────┼──────────────┼──────────────┼─────────────┼────────────────┤
│ AP I             │ 14.047.059   │ 12.004.748   │ 26.051.807  │ 3.285.534      │
│ AP II            │ 15.161.493   │ 13.834.355   │ 28.995.848  │ 4.753.125      │
│ BUBU             │ 1.340.861    │ 1.147.704    │ 2.488.565   │ 11.145         │
│ UPBU             │ 4.886.811    │ 5.051.245    │ 9.938.056   │ 10.626         │
│ **TOTAL**        │**35.436.224**│**32.038.052**│**67.474.276**│**8.060.430**  │ ⚠️
└──────────────────┴──────────────┴──────────────┴─────────────┴────────────────┘
```

---

### 6. Data Nol vs Missing

| Properti | Detail |
|----------|--------|
| **Observasi** | Ada perbedaan antara `0` (nol) dan `-` (missing):<br>- 2022 UPBU: `0` di internasional (artinya ada operasional tapi 0 penumpang)<br>- 2021 UPBU: `-` di internasional (artinya tidak ada data/tidak operasional) |
| **Saran** | **Bedakan treatment:**<br>- `0` → tetap `0` (valid value)<br>- `-` → `NULL` (missing value) |

---

## 📐 Rekomendasi Skema Database (Gambaran)

### Opsi A: Wide Format (Seperti CSV Asli)

**Konsep:** Satu tabel dengan semua kolom pengelola melebar

**Struktur Logis:**
```
┌──────────────┬──────────┬──────────┬───────────┬──────────┬──────────┬───────────┐
│ Pengelola    │ Dom DTG  │ Dom BRKT │ Dom Total │ Int DTG  │ Int BRKT │ Int Total │
├──────────────┼──────────┼──────────┼───────────┼──────────┼──────────┼───────────┤
│ AP I         │ 14047059 │ 12004748 │ 26051807  │ 1581234  │ 1704300  │ 3285534   │
│ AP II        │ 15161493 │ 13834355 │ 28995848  │ 2434032  │ 2319093  │ 4753125   │
│ BUBU         │ 1340861  │ 1147704  │ 2488565   │ 5548     │ 5597     │ 11145     │
│ UPBU         │ 4886811  │ 5051245  │ 9938056   │ 5451     │ 5175     │ 10626     │
└──────────────┴──────────┴──────────┴───────────┴──────────┴──────────┴───────────┘
```

**Kolom yang Dibutuhkan:**
- **Tahun** (INT): 2020, 2021, 2022, 2023, 2024
- **Pengelola** (VARCHAR): Nama pengelola bandara
- **Domestik Datang** (INT)
- **Domestik Berangkat** (INT)
- **Domestik Total** (INT)
- **Internasional Datang** (INT)
- **Internasional Berangkat** (INT)
- **Internasional Total** (INT)
- **Is Total Row** (BOOLEAN): untuk tandai baris agregasi

**Kelebihan:** 
- ✅ Simple, sesuai format sumber
- ✅ Mudah dibaca untuk reporting

**Kekurangan:**
- ❌ Sulit bandingkan antar tahun (karena kategori pengelola berubah)
- ❌ Tidak scalable jika ada kategori pengelola baru

**Kapan Pakai Opsi Ini?**
→ Jika hanya untuk **reporting static per tahun**

---

### Opsi B: Long Format (Recommended)

**Konsep:** Satu tabel vertikal dengan satu baris = satu pengelola + satu tahun

**Tabel: FaktaKomposisiPenumpang (Fact Table)**
```
┌──────────┬──────────────┬──────┬──────────┬───────────┬──────────┐
│ ID (PK)  │ Pengelola    │ Tahun│ Dom DTG  │ Dom BRKT  │ Dom Total│
├──────────┼──────────────┼──────┼──────────┼───────────┼──────────┤
│ 1        │ AP I         │ 2020 │ 14047059 │ 12004748  │ 26051807 │
│ 2        │ AP I         │ 2021 │ 14386530 │ 11849839  │ 26236369 │
│ 3        │ AP I         │ 2022 │ 22944203 │ 19512802  │ 42457005 │
│ 4        │ AP I         │ 2023 │ 26468754 │ 22676321  │ 49145075 │
│ 5        │ AP II        │ 2020 │ 15161493 │ 13834355  │ 28995848 │
│ ...      │ ...          │ ...  │ ...      │ ...       │ ...      │
└──────────┴──────────────┴──────┴──────────┴───────────┴──────────┘
```

**Struktur Logis:**
- **Primary Key** (ID unik per record)
- **Pengelola** (VARCHAR): Nama pengelola bandara
- **Tahun** (INT): 2020, 2021, 2022, 2023, 2024
- **Domestik Datang** (INT)
- **Domestik Berangkat** (INT)
- **Domestik Total** (INT)
- **Internasional Datang** (INT)
- **Internasional Berangkat** (INT)
- **Internasional Total** (INT)
- **Is Total Row** (BOOLEAN): untuk exclude agregasi

**Kelebihan:**
- ✅ Mudah bandingkan antar tahun
- ✅ Scalable jika ada kategori pengelola baru
- ✅ Optimal untuk trend analysis

**Kekurangan:**
- ❌ Perlu mapping table untuk handle perubahan kategori (2020-2023 vs 2024)
- ❌ Baris lebih banyak (4-5 pengelola × 5 tahun = ~20-25 rows)

**Kapan Pakai Opsi Ini?**
→ Jika data akan dipakai untuk **trend analysis atau perbandingan antar tahun**

---

### 📊 Perbandingan Kedua Opsi

| Aspek | Wide Format | Long Format |
|-------|-------------|-------------|
| **Jumlah Tabel** | 1 per tahun (5 tabel) | 1 (semua tahun digabung) |
| **Jumlah Baris** | 4-5 per tabel | ~20-25 total |
| **Jumlah Kolom** | 7 | 9 |
| **Query Perbandingan Tahun** | Sulit (perlu JOIN 5 tabel) | Mudah (GROUP BY tahun) |
| **Handle Perubahan Kategori** | Sulit | Lebih mudah (tambah mapping) |
| **Cocok untuk** | Reporting statis | Analytics & BI |
| **Kompleksitas** | Rendah | Rendah-Medium |

---

### 🎯 Rekomendasi Final

**Untuk Use Case Data Warehouse:**

```
Pakai LONG FORMAT (Opsi B) karena:
  ✅ Mudah bandingkan performa antar tahun
  ✅ Scalable jika ada kategori pengelola baru
  ✅ Optimal untuk trend analysis & dashboard
  ✅ Lebih fleksibel untuk handle perubahan kategori
```

**Tambahan Penting:**
- **Buat mapping table** untuk kategori pengelola:
  ```
  dim_pengelola:
  ├── pengelola_id (PK)
  ├── nama_pengelola (VARCHAR)
  ├── kategori_lama (VARCHAR): AP I, AP II, BUBU, UPBU
  ├── kategori_baru (VARCHAR): BUBU, UPBU / SATPEL, UPTD / PEMDA, BANDARA KHUSUS
  └── is_active (BOOLEAN)
  ```

---

## 🎯 Kesimpulan & Next Steps

### Masalah Kritikal (Harus Ditangani)
1. ✅ Format angka dengan titik sebagai pemisah ribuan (hapus titik → integer)
2. ✅ Missing value `-` → replace dengan `NULL`
3. ✅ Perubahan kategori pengelola di 2024 (buat mapping table)
4. ✅ Baris Total perlu flag/isolasi
5. ✅ Bedakan `0` (valid) vs `-` (missing)

### Masalah Struktural (Pertimbangkan Transformasi)
1. ⚠️ Wide → Long format (untuk perbandingan antar tahun)
2. ⚠️ Mapping table untuk kategori pengelola (2020-2023 vs 2024)
3. ⚠️ Rename kolom (opsional, untuk kejelasan)

### Next Steps untuk File Ini
- [ ] Tentukan format target (wide vs long)
- [ ] Buat mapping table kategori pengelola
- [ ] Buat script pre-processing (cleaning + transform)
- [ ] Validasi hasil cleaning (Dom Total = DTG + BRKT?)
- [ ] Investigasi kenapa AP I & AP II hilang di 2024

---

## 📝 Metadata Tambahan

| Properti | Nilai |
|----------|-------|
| **Analysis Date** | 2026-04-10 |
| **Analyzed By** | Data Engineer (AI Assistant) |
| **Jumlah File** | 5 (1 per tahun: 2020-2024) |
| **Jumlah Baris per File** | 5 (4 pengelola + 1 Total) |
| **Jumlah Kolom** | 7 |
| **Total Baris (Semua Tahun)** | 25 (5 × 5) |
| **Tipe Data** | String (titik = ribuan), `-` = missing |
| **Perubahan Signifikan** | Kategori pengelola berubah di 2024 (AP I & AP II hilang) |

---

> **Catatan:** Dokumen ini menganalisis 5 file CSV komposisi penumpang berdasarkan pengelola bandara (2020-2024). Temuan utama: terjadi perubahan kategorisasi pengelola di 2024 yang memerlukan mapping table untuk perbandingan antar tahun.
