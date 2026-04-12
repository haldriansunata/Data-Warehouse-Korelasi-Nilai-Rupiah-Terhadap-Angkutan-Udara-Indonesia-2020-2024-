# CSV Analysis: Data Lalu Lintas Angkutan Udara di Bandar Udara (2020-2024)

## 📊 Informasi Umum

| Properti | Nilai |
|----------|-------|
| **Nama File** | `DATA LALU LINTAS ANGKUTAN UDARA DI BANDAR UDARA TAHUN 2020 - 2024.csv` |
| **Jumlah File** | 1 file (multi-tahun: 2020-2024) |
| **Jumlah Baris** | 1.282 baris (1 header + ~1.281 data) |
| **Jumlah Kolom** | 23 |
| **Tipe Data Utama** | String (nama provinsi/bandara), Integer (angka dengan titik sebagai pemisah ribuan) |
| **Rentang Tahun** | 2020, 2021, 2022, 2023, 2024 |
| **Kategori Bandara** | Domestik (DOM) dan Internasional (INT) |
| **Missing Value** | Angka `0` (nol) |

---

## 🗂️ Struktur Tabel

### Skema Saat Ini

```
propinsi_code (int)
propinsi_name (string)
airport_code (string - huruf tunggal: A, B, C, dst)
airport_name (string - nama bandara + kategori DOM/INT)
year (int)
pesawat_dtg (string - angka dengan titik ribuan)
pesawat_brk (string - angka dengan titik ribuan)
pesawat_total (string - angka dengan titik ribuan)
penumpang_dtg (string - angka dengan titik ribuan)
penumpang_brk (string - angka dengan titik ribuan)
penumpang_total (string - angka dengan titik ribuan)
penumpang_tra (string - angka dengan titik ribuan)
bagasi_dtg (string - angka dengan titik ribuan)
bagasi_brk (string - angka dengan titik ribuan)
bagasi_total (string - angka dengan titik ribuan)
barang_dtg (string - angka dengan titik ribuan)
barang_brk (string - angka dengan titik ribuan)
barang_total (string - angka dengan titik ribuan)
pos_dtg (string - angka dengan titik ribuan)
pos_brk (string - angka dengan titik ribuan)
pos_total (string - angka dengan titik ribuan)
keterangan (string - "Data 12 Bln")
```

### Detail Per Kolom

| No | Nama Kolom | Deskripsi | Tipe Data Saat Ini | Tipe Data Rekomendasi | Nullable | Contoh Nilai |
|----|-----------|-----------|-------------------|----------------------|----------|--------------|
| 1 | `propinsi_code` | Kode unik provinsi | String (angka) | `INT` | ❌ No | `1`, `2`, `3`, ... |
| 2 | `propinsi_name` | Nama provinsi | String | `VARCHAR(100)` | ❌ No | `PROPINSI DAERAH ISTIMEWA ACEH` |
| 3 | `airport_code` | Kode klasifikasi bandara (huruf) | String (huruf tunggal) | `VARCHAR(5)` | ✅ Yes | `A`, `B`, `C`, ..., `L` |
| 4 | `airport_name` | Nama bandara + kategori (DOM/INT) | String | `VARCHAR(150)` | ❌ No | `SULTAN ISKANDAR MUDA - BANDA ACEH (DOM)` |
| 5 | `year` | Tahun data | Int | `INT` | ❌ No | `2020`, `2021`, `2022`, `2023`, `2024` |
| 6 | `pesawat_dtg` | Jumlah pesawat datang | String (titik = ribuan) | `INT` | ✅ Yes | `1.809` = 1,809 |
| 7 | `pesawat_brk` | Jumlah pesawat berangkat | String (titik = ribuan) | `INT` | ✅ Yes | `1.813` = 1,813 |
| 8 | `pesawat_total` | Total pesawat (dtg + brk) | String (titik = ribuan) | `INT` | ✅ Yes | `3.622` = 3,622 |
| 9 | `penumpang_dtg` | Jumlah penumpang datang | String (titik = ribuan) | `INT` | ✅ Yes | `157.995` = 157,995 |
| 10 | `penumpang_brk` | Jumlah penumpang berangkat | String (titik = ribuan) | `INT` | ✅ Yes | `165.534` = 165,534 |
| 11 | `penumpang_total` | Total penumpang (dtg + brk) | String (titik = ribuan) | `INT` | ✅ Yes | `323.529` = 323,529 |
| 12 | `penumpang_tra` | Penumpang transit/transfer | String (titik = ribuan) | `INT` | ✅ Yes | `532` |
| 13 | `bagasi_dtg` | Berat bagasi datang | String (titik = ribuan) | `INT` | ✅ Yes | `904.353` = 904,353 kg |
| 14 | `bagasi_brk` | Berat bagasi berangkat | String (titik = ribuan) | `INT` | ✅ Yes | `832.514` = 832,514 kg |
| 15 | `bagasi_total` | Total berat bagasi | String (titik = ribuan) | `INT` | ✅ Yes | `1.736.867` = 1,736,867 kg |
| 16 | `barang_dtg` | Berat barang/kargo datang | String (titik = ribuan) | `INT` | ✅ Yes | `4.553.460` = 4,553,460 kg |
| 17 | `barang_brk` | Berat barang/kargo berangkat | String (titik = ribuan) | `INT` | ✅ Yes | `778.885` = 778,885 kg |
| 18 | `barang_total` | Total berat barang/kargo | String (titik = ribuan) | `INT` | ✅ Yes | `5.332.345` = 5,332,345 kg |
| 19 | `pos_dtg` | Berat pos datang | String (titik = ribuan) | `INT` | ✅ Yes | `0`, `239` |
| 20 | `pos_brk` | Berat pos berangkat | String (titik = ribuan) | `INT` | ✅ Yes | `134` |
| 21 | `pos_total` | Total berat pos | String (titik = ribuan) | `INT` | ✅ Yes | `134` |
| 22 | `keterangan` | Keterangan data | String | `VARCHAR(50)` | ✅ Yes | `Data 12 Bln` |

**Catatan:**
- **DTG** = Datang
- **BRKT/BRK** = Berangkat
- **TRA** = Transit/Transfer
- **TOTAL** = DTG + BRK (sudah dikalkulasi di sumber)
- Satuan berat: **Kilogram (kg)**

---

## 📖 Penjelasan Kolom Penting

### 1. Kolom `propinsi_code`

| Properti | Detail |
|----------|--------|
| **Arti** | Kode unik provinsi |
| **Fungsi** | Mengidentifikasi provinsi secara numerik |
| **Konsistensi** | ✅ Konsisten (1 provinsi = 1 code) |
| **Contoh** | `1` = Aceh, `2` = Sumatera Utara, `3` = Sumatera Barat |

**Nilai Unik:** Sekitar 34 provinsi (jumlah provinsi di Indonesia)

---

### 2. Kolom `airport_code`

| Properti | Detail |
|----------|--------|
| **Arti** | Kode klasifikasi bandara (bukan IATA code!) |
| **Fungsi** | Mengklasifikasikan bandara berdasarkan kelas/tingkat |
| **Format** | Huruf tunggal: `A`, `B`, `C`, ..., `L` |
| **Konsistensi** | ✅ Konsisten (huruf A-L) |

**Kemungkinan Arti:**
- **A** = Bandara Utama/Internasional
- **B**, **C**, dst = Bandara sekunder/tertier
- **(Kosong)** = Bandara tanpa klasifikasi (untuk kategori INT)

**Observasi:** Bandara yang sama bisa punya code (untuk DOM) atau kosong (untuk INT). Contoh:
- `A` untuk `SULTAN ISKANDAR MUDA - BANDA ACEH (DOM)`
- `(kosong)` untuk `SULTAN ISKANDAR MUDA - BANDA ACEH (INT)`

---

### 3. Kolom `airport_name`

| Properti | Detail |
|----------|--------|
| **Arti** | Nama lengkap bandara + kategori operasi |
| **Fungsi** | Mengidentifikasi bandara dan apakah data domestik atau internasional |
| **Format** | `NAMA BANDARA - LOKASI (KATEGORI)` |
| **Kategori** | `(DOM)`, `(DOMESTIK)`, `(INT)`, `(INTERNASIONAL)` |

**Observasi:** Nama bandara sama bisa muncul 2 kali (DOM dan INT). Contoh:
- `SULTAN ISKANDAR MUDA - BANDA ACEH (DOM)`
- `SULTAN ISKANDAR MUDA - BANDA ACEH (INT)`

---

### 4. Kolom `year`

| Properti | Detail |
|----------|--------|
| **Arti** | Tahun data |
| **Fungsi** | Membedakan data per tahun |
| **Nilai** | `2020`, `2021`, `2022`, `2023`, `2024` |
| **Konsistensi** | ✅ Konsisten (semua tahun ada) |

---

### 5. Kolom Pesawat (`pesawat_dtg/brk/total`)

| Properti | Detail |
|----------|--------|
| **Arti** | Jumlah penerbangan (pesawat) yang datang/berangkat |
| **Fungsi** | Mengukur frekuensi penerbangan di bandara |
| **Satuan** | Unit (jumlah pesawat) |
| **Format** | Titik sebagai pemisah ribuan |

**Contoh:**
- `pesawat_dtg = 1.809` = 1,809 pesawat datang
- `pesawat_brk = 1.813` = 1,813 pesawat berangkat
- `pesawat_total = 3.622` = 3,622 total (1,809 + 1,813)

---

### 6. Kolom Penumpang (`penumpang_dtg/brk/total/tra`)

| Properti | Detail |
|----------|--------|
| **Arti** | Jumlah penumpang yang datang/berangkat + transit |
| **Fungsi** | Mengukur volume penumpang di bandara |
| **Satuan** | Orang |
| **Format** | Titik sebagai pemisah ribuan |

**Khusus `penumpang_tra`:**
- **Arti:** Penumpang transit/transfer
- **Fungsi:** Penumpang yang singgah di bandara untuk melanjutkan perjalanan
- **Observasi:** Nilai bisa 0 atau sangat kecil dibanding `penumpang_total`

---

### 7. Kolom Bagasi (`bagasi_dtg/brk/total`)

| Properti | Detail |
|----------|--------|
| **Arti** | Berat bagasi penumpang yang datang/berangkat |
| **Fungsi** | Mengukur volume bagasi yang ditangani bandara |
| **Satuan** | Kilogram (kg) |
| **Format** | Titik sebagai pemisah ribuan |

---

### 8. Kolom Barang (`barang_dtg/brk/total`)

| Properti | Detail |
|----------|--------|
| **Arti** | Berat barang/kargo yang datang/berangkat |
| **Fungsi** | Mengukur volume kargo yang ditangani bandara |
| **Satuan** | Kilogram (kg) |
| **Format** | Titik sebagai pemisah ribuan |

**Observasi:** Nilai bisa sangat besar (jutaan kg untuk bandara besar)

---

### 9. Kolom Pos (`pos_dtg/brk/total`)

| Properti | Detail |
|----------|--------|
| **Arti** | Berat pos/surat yang datang/berangkat |
| **Fungsi** | Mengukur volume pos yang ditangani bandara |
| **Satuan** | Kilogram (kg) |
| **Format** | Titik sebagai pemisah ribuan |

**Observasi:** Banyak bandara punya nilai 0 (tidak ada layanan pos)

---

### 10. Kolom `keterangan`

| Properti | Detail |
|----------|--------|
| **Arti** | Keterangan periode data |
| **Fungsi** | Menunjukkan apakah data lengkap 12 bulan atau tidak |
| **Nilai** | `Data 12 Bln` (semua baris) |
| **Konsistensi** | ✅ Konsisten (semua baris sama) |

---

## 📊 Analisis Nilai Unik & Distribusi

### 1. Distribusi per Tahun

| Tahun | Estimasi Baris | Estimasi Bandara |
|-------|---------------|------------------|
| **2020** | ~250-260 | ~125-130 bandara (DOM + INT) |
| **2021** | ~250-260 | ~125-130 bandara |
| **2022** | ~250-260 | ~125-130 bandara |
| **2023** | ~250-260 | ~125-130 bandara |
| **2024** | ~250-260 | ~125-130 bandara |

**Catatan:** Setiap tahun punya jumlah bandara yang kurang lebih sama karena formatnya adalah per bandara × per tahun.

---

### 2. Distribusi Kategori (DOM vs INT)

| Kategori | Estimasi Baris per Tahun | Persentase |
|----------|------------------------|------------|
| **Domestik (DOM)** | ~120-125 | ~95% |
| **Internasional (INT)** | ~5-10 | ~5% |

**Observasi:**
- Sebagian besar data adalah Domestik
- Tidak semua bandara punya layanan Internasional
- Hanya bandara besar yang punya 2 baris (DOM + INT)

---

### 3. Distribusi `airport_code`

| Code | Estimasi Jumlah Bandara | Keterangan |
|------|-----------------------|------------|
| **A** | ~34-40 | Bandara utama/utama di setiap provinsi |
| **B** | ~30-40 | Bandara sekunder |
| **C** | ~20-30 | Bandara tertier |
| **D** | ~10-20 | Bandara kecil |
| **E** | ~10-20 | Bandara kecil |
| **F** | ~10-20 | Bandara kecil |
| **G** | ~5-10 | Bandara sangat kecil |
| **H** | ~5-10 | Bandara sangat kecil |
| **I** | ~5-10 | Bandara sangat kecil |
| **J** | ~5-10 | Bandara sangat kecil |
| **K** | ~5-10 | Bandara sangat kecil |
| **L** | ~5-10 | Bandara sangat kecil |
| **(Kosong)** | ~5-10 | Bandara internasional (tidak pakai code) |

**Observasi:** Code kemungkinan menunjukkan kelas/tingkat bandara.

---

### 4. Bandara dengan Nilai 0 (Tidak Aktif)

**Observasi:** Banyak bandara punya semua kolom = 0 (tidak ada aktivitas)

**Contoh:**
```
1,PROPINSI DAERAH ISTIMEWA ACEH,E,TEUKU CUT ALI - TAPAK TUAN,2020,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,Data 12 Bln
```

**Penyebab:**
- Bandara belum beroperasi
- Bandara tutup sementara
- Data tidak tersedia/tidak dilapor

---

## ⚠️ Potensi Masalah & Saran Pre-Processing

### 1. Format Angka dengan Titik sebagai Pemisah Ribuan

| Properti | Detail |
|----------|--------|
| **Masalah** | Angka menggunakan titik sebagai pemisah ribuan: `1.809` = 1,809 |
| **Dampak** | Jika dibaca sebagai float biasa, akan jadi 1.809 (salah!) |
| **Saran** | **Parsing khusus:** Baca sebagai string → hapus titik → convert ke integer |

**Visualisasi Transformasi:**
```
SEBELUM:  "1.809"      →  Hapus titik: "1809"      →  SESUDAH:  1809
SEBELUM:  "1.494.613"  →  Hapus titik: "1494613"   →  SESUDAH:  1494613
```

---

### 2. Data 0 vs Missing Value

| Properti | Detail |
|----------|--------|
| **Observasi** | Missing value menggunakan angka `0` (bukan sel kosong) |
| **Masalah** | `0` bisa berarti tidak ada data ATAU memang 0 aktivitas |
| **Saran** | **Kontekstual treatment:**<br>- Jika semua kolom = 0 → bandara tidak aktif (biarkan 0)<br>- Jika hanya beberapa kolom = 0 → valid value |

---

### 3. Nama Bandara Muncul 2 Kali (DOM & INT)

| Properti | Detail |
|----------|--------|
| **Masalah** | Bandara yang sama muncul 2 kali: `(DOM)` dan `(INT)` |
| **Dampak** | • Sulit agregasi per bandara<br>• Perlu parsing nama untuk gabungkan DOM + INT |
| **Saran** | **Buat kolom `bandara_id`** yang unik per bandara (tanpa kategori), lalu pisahkan kategori ke kolom lain |

**Visualisasi Transformasi:**
```
SEBELUM:
  SULTAN ISKANDAR MUDA - BANDA ACEH (DOM)
  SULTAN ISKANDAR MUDA - BANDA ACEH (INT)

SESUDAH:
  bandara_id: "SULTAN ISKANDAR MUDA - BANDA ACEH"
  kategori: "DOM" atau "INT"
```

---

### 4. Format Nama Bandara Tidak Konsisten

| Properti | Detail |
|----------|--------|
| **Observasi** | Kategori ditulis berbeda-beda:<br>- `(DOM)` vs `(DOMESTIK)`<br>- `(INT)` vs `(INTERNASIONAL)` |
| **Dampak** | Parsing kategori jadi lebih rumit |
| **Saran** | **Standardisasi:** `(DOMESTIK)` → `(DOM)`, `(INTERNASIONAL)` → `(INT)` |

---

### 5. Kolom `airport_code` Kosong untuk INT

| Properti | Detail |
|----------|--------|
| **Observasi** | Bandara kategori INT tidak punya `airport_code` (kosong) |
| **Dampak** | Kolom nullable, perlu handling khusus |
| **Saran** | Isi code dari versi DOM bandara yang sama |

---

### 6. Banyak Bandara dengan 0 Aktivitas

| Properti | Detail |
|----------|--------|
| **Observasi** | Banyak baris dengan semua kolom numerik = 0 |
| **Dampak** | • Inflasi jumlah bandara aktif<br>• Query agregasi jadi bias |
| **Saran** | **Buat flag `is_active`** = TRUE jika ada kolom numerik > 0 |

---

### 7. Redundansi Data Provinsi

| Properti | Detail |
|----------|--------|
| **Observasi** | `propinsi_code` dan `propinsi_name` berulang di setiap baris (bandara × tahun) |
| **Dampak** | Redundansi data (tapi wajar untuk flat file) |
| **Saran** | **Normalisasi:** Buat tabel `dim_provinsi` terpisah |

---

### 8. Kolom Total Sudah Dikalkulasi

| Properti | Detail |
|----------|--------|
| **Observasi** | `*_total` sudah dihitung di sumber (dtg + brk) |
| **Dampak** | Redundansi (tapi memudahkan query) |
| **Saran** | **Simpan saja** (tidak masalah untuk fact table), tapi pastikan konsistensi: `total == dtg + brk` |

---

## 📐 Rekomendasi Skema Database

### Opsi A: Wide Format (Seperti CSV Asli) — Recommended

**Konsep:** Satu tabel dengan semua kolom lengkap

**Struktur Logis:**
```
┌──────────┬───────────────┬──────┬──────┬──────────┬───────────────┬───────────┬───────┐
│ Bandara  │ Provinsi      │ Year │ Code │ Kategori  │ Pesawat Total │ Penumpang │ ...   │
├──────────┼───────────────┼──────┼──────┼───────────┼───────────────┼───────────┼───────┤
│ Iskandar │ Aceh          │ 2020 │ A    │ DOM       │ 3.622         │ 323.529   │ ...   │
│ Iskandar │ Aceh          │ 2020 │ NULL │ INT       │ 582           │ 53.601    │ ...   │
│ Iskandar │ Aceh          │ 2021 │ A    │ DOM       │ 3.906         │ 318.914   │ ...   │
│ ...      │ ...           │ ...  │ ...  │ ...       │ ...           │ ...       │ ...   │
└──────────┴───────────────┴──────┴──────┴───────────┴───────────────┴───────────┴───────┘
```

**Tabel Utama: `fact_lalu_lintas_bandara`**
```
┌──────────────────────────────────────────────────────────────────────┐
│ PRIMARY KEY: (bandara_id, year, kategori)                            │
├──────────────────────────────────────────────────────────────────────┤
│ bandara_id (VARCHAR)        → ID unik bandara (tanpa kategori)      │
│ provinsi_code (INT)         → FK ke dim_provinsi                    │
│ airport_code (VARCHAR)      → Kode klasifikasi bandara              │
│ kategori (VARCHAR)          → 'DOM' atau 'INT'                      │
│ year (INT)                  → Tahun data                            │
│ pesawat_dtg (INT)           → Jumlah pesawat datang                 │
│ pesawat_brk (INT)           → Jumlah pesawat berangkat              │
│ pesawat_total (INT)         → Total pesawat                         │
│ penumpang_dtg (INT)         → Jumlah penumpang datang               │
│ penumpang_brk (INT)         → Jumlah penumpang berangkat            │
│ penumpang_total (INT)       → Total penumpang                       │
│ penumpang_tra (INT)         → Penumpang transit                     │
│ bagasi_dtg (INT)            → Berat bagasi datang                   │
│ bagasi_brk (INT)            → Berat bagasi berangkat                │
│ bagasi_total (INT)          → Total berat bagasi                    │
│ barang_dtg (INT)            → Berat barang datang                   │
│ barang_brk (INT)            → Berat barang berangkat                │
│ barang_total (INT)          → Total berat barang                    │
│ pos_dtg (INT)               → Berat pos datang                      │
│ pos_brk (INT)               → Berat pos berangkat                   │
│ pos_total (INT)             → Total berat pos                       │
│ is_active (BOOLEAN)         → TRUE jika ada aktivitas               │
│ keterangan (VARCHAR)        → Keterangan data                       │
└──────────────────────────────────────────────────────────────────────┘
```

**Tabel Dimensi:**
```
dim_provinsi:
├── provinsi_code (INT, PK)
└── provinsi_name (VARCHAR)

dim_bandara:
├── bandara_id (VARCHAR, PK)
├── nama_bandara (VARCHAR)
├── lokasi (VARCHAR)
├── airport_code (VARCHAR)
└── is_international (BOOLEAN)
```

**Kelebihan:**
- ✅ Simple, sesuai format sumber
- ✅ Mudah dibaca untuk reporting
- ✅ Optimal untuk query per bandara + tahun
- ✅ Semua data dalam 1 tabel

**Kekurangan:**
- ❌ Banyak kolom (23 kolom)
- ❌ Perlu parsing nama bandara untuk buat `bandara_id`

**Kapan Pakai Opsi Ini?**
→ Jika data akan dipakai untuk **reporting per bandara per tahun**

---

### Opsi B: Long Format (Fully Normalized)

**Konsep:** Pecah jadi fact table vertikal dengan satu baris = 1 bandara × 1 tahun × 1 metrik

**Tabel Utama: `fact_lalu_lintas_bandara_long`**
```
┌────────────────────────────────────────────────────────────┐
│ PRIMARY KEY: (bandara_id, year, kategori, metrik)          │
├────────────────────────────────────────────────────────────┤
│ bandara_id (VARCHAR)  → ID unik bandara                   │
│ provinsi_code (INT)   → FK ke dim_provinsi                │
│ year (INT)            → Tahun data                        │
│ kategori (VARCHAR)    → 'DOM' atau 'INT'                  │
│ metrik (VARCHAR)      → 'pesawat', 'penumpang', dll       │
│ dtg (INT)             → Nilai datang                      │
│ brk (INT)             → Nilai berangkat                   │
│ total (INT)           → Nilai total                       │
└────────────────────────────────────────────────────────────┘
```

**Kelebihan:**
- ✅ Lebih sedikit kolom
- ✅ Mudah tambah metrik baru
- ✅ Optimal untuk dynamic reporting

**Kekurangan:**
- ❌ Query lebih rumit (perlu PIVOT untuk reporting wide)
- ❌ Baris lebih banyak (23 kolom → 7-8 baris per bandara × tahun)
- ❌ Kurang intuitif untuk user

**Kapan Pakai Opsi Ini?**
→ Jika data akan dipakai untuk **dynamic dashboard dengan metrik berubah-ubah**

---

### 📊 Perbandingan Kedua Opsi

| Aspek | Wide Format | Long Format |
|-------|-------------|-------------|
| **Jumlah Kolom** | 23 | 7 |
| **Jumlah Baris** | ~1,281 | ~10,000+ |
| **Query Sederhana** | ✅ Mudah | ❌ Perlu PIVOT |
| **Dynamic Metrik** | ❌ Sulit | ✅ Mudah |
| **Human Readable** | ✅ Mudah dibaca | ❌ Kurang intuitif |
| **Kompleksitas** | Rendah | Medium |

---

### 🎯 Rekomendasi Final

**Untuk Use Case Data Warehouse:**

```
Pakai WIDE FORMAT (Opsi A) karena:
  ✅ Sesuai format sumber (tidak perlu transformasi berat)
  ✅ Mudah dibaca untuk reporting
  ✅ Optimal untuk query per bandara + tahun
  ✅ Kolom sudah standar dan fixed
  ✅ Tidak ada kebutuhan dynamic metrik
```

---

## 🎯 Kesimpulan & Next Steps

### Masalah Kritikal (Harus Ditangani)
1. ✅ Format angka dengan titik sebagai pemisah ribuan (hapus titik → integer)
2. ✅ Parsing `airport_name` untuk pisahkan nama bandara dan kategori (DOM/INT)
3. ✅ Buat `bandara_id` unik per bandara (tanpa kategori)
4. ✅ Standardisasi penulisan kategori: `(DOMESTIK)` → `(DOM)`, `(INTERNASIONAL)` → `(INT)`
5. ✅ Handle `airport_code` kosong untuk kategori INT

### Masalah Struktural (Pertimbangkan Transformasi)
1. ⚠️ Buat tabel dimensi untuk `provinsi` dan `bandara` (normalisasi)
2. ⚠️ Tambah flag `is_active` untuk filter bandara tidak aktif
3. ⚠️ Validasi konsistensi: `total == dtg + brk`

### Next Steps untuk File Ini
- [ ] Tentukan format target (wide vs long) — rekomendasi: wide
- [ ] Buat script parsing `airport_name` untuk extract nama & kategori
- [ ] Buat script pre-processing (cleaning + transform)
- [ ] Validasi hasil cleaning (total == dtg + brk?)
- [ ] Buat tabel dimensi (provinsi, bandara)
- [ ] Buat fact table dengan wide format

---

## 📝 Metadata Tambahan

| Properti | Nilai |
|----------|-------|
| **Analysis Date** | 2026-04-10 |
| **Analyzed By** | Data Engineer (AI Assistant) |
| **Jumlah File** | 1 (multi-tahun: 2020-2024) |
| **Jumlah Baris** | ~1,281 (termasuk header) |
| **Jumlah Kolom** | 23 |
| **Rentang Tahun** | 2020-2024 (5 tahun) |
| **Estimasi Bandara** | ~125-130 bandara (DOM + INT) |
| **Tipe Data** | String (titik = ribuan), 0 = valid atau missing |
| **Kategori** | Domestik (DOM) dan Internasional (INT) |
| **Perubahan Signifikan** | Tidak ada (format konsisten antar tahun) |

---

> **Catatan:** Dokumen ini menganalisis 1 file CSV lalu lintas bandara multi-tahun (2020-2024). File ini berbeda dari file komposisi pengelola karena berisi data detail per bandara per tahun, bukan agregasi per pengelola.
