### 📌 Rangkuman Insight Desain Data Warehouse

**1. Penanganan Lokasi dan Rute (Konsep *Role-Playing Dimension*)**
* **Isu:** Data penerbangan melibatkan dua lokasi (Asal dan Tujuan). Apakah perlu membuat `Dim_Provinsi` atau `Dim_Kota` secara terpisah?
* **Solusi:** Tidak perlu memecah lokasi menjadi tabel provinsi atau kota. Cukup buat satu dimensi master, yaitu **`Dim_Bandara`**, yang merangkum hierarki lokasi (Bandara -> Kota -> Provinsi -> Negara). Untuk menghubungkan 2 bandara dalam satu rute penerbangan, gunakan **`Dim_Rute`** yang memiliki dua *Foreign Key* (FK) yang mengarah ke tabel `Dim_Bandara` yang sama (satu sebagai bandara ke-1, satu sebagai bandara ke-2).

**2. Efisiensi dan Penghapusan Redundansi**
* **Isu:** Kolom apa saja yang harus dihapus untuk menghindari redundansi antar tabel?
* **Solusi:** * **Hapus `kota_a` dan `kota_b` dari `Dim_Rute`:** Atribut deskriptif lokasi murni milik `Dim_Bandara`. `Dim_Rute` hanya bertindak sebagai jembatan logika (menyimpan kunci/ID).
    * **Pindahkan `Kategori` (Domestik/Internasional):** Karena status domestik/internasional adalah sifat mutlak dari sebuah rute, letakkan kolom ini di `Dim_Rute`. Hapus kolom `Kategori` dari *Fact Table* agar tabel fakta tetap ramping dan hanya berisi angka (*Measures*) serta kunci (*Foreign Keys*).

**3. Pemilihan Arsitektur: *Star Schema* vs *Snowflake Schema***
* **Isu:** Mengapa kita memilih menumpuk data lokasi di `Dim_Bandara` (Denormalisasi/Star Schema) alih-alih memecahnya menjadi tabel-tabel kecil (Normalisasi/Snowflake Schema)?
* **Solusi:** Untuk kebutuhan analitik (OLAP) dengan *tools* seperti Tableau/Power BI, kecepatan *query* (membaca data) adalah prioritas utama. *Star Schema* meminimalkan operasi *JOIN*, sehingga jauh lebih cepat. *Snowflake Schema* hanya digunakan pada kondisi darurat/khusus, seperti adanya hierarki data yang sangat masif dan sering berubah nilainya, atau saat ada relasi *many-to-many* (membutuhkan tabel *bridge* khusus). Untuk kasusmu, *Star Schema* adalah pilihan paling presisi dan efisien.

**4. Evaluasi Analisamu: `Fact_Penumpang_Rute` & `Dim_Kurs_Bulanan`**
* **Isu:** Apakah analisa menggunakan *Star Schema* untuk `Fact_Penumpang_Rute` dan `Dim_Kurs_Bulanan` sudah benar tanpa perlu dimensi lokasi yang dipecah?
* **Solusi:** Analisamu 100% benar. Jika tabel faktamu nanti hanya akan dihubungkan dengan `Dim_Rute`, `Dim_Waktu`, dan `Dim_Kurs_Bulanan`, maka memecah lokasi menjadi `Dim_Provinsi` adalah tindakan yang sia-sia dan over-engineering. `Dim_Kurs_Bulanan` (misalnya nilai tukar USD ke IDR) hanya peduli pada Waktu (Bulan/Tahun), bukan lokasi. Karena tidak ada dimensi lain yang perlu meminjam/menggunakan tabel referensi "Provinsi" secara mandiri, maka menaruh nama provinsi langsung di dalam `Dim_Bandara` (Star Schema) adalah langkah yang paling brilian dan efisien.

**5. Penanganan Perbedaan Grain (Tingkat Detail Data)**
* **Isu:** Ditemukan dataset baru (lalu lintas bandara tahunan) yang memiliki metrik serupa (jumlah penumpang) tetapi dengan tingkat detail (*grain*) yang berbeda: agregat 1 bandara (tahunan) vs spesifik 1 rute (bulanan). Apakah keduanya harus digabung?
* **Solusi:** Jangan digabungkan ke dalam satu tabel fakta, dan jangan korbankan data bulanan menjadi tahunan. Buatlah **Tabel Fakta Baru** (`Fact_Lalu_Lintas_Bandara`) yang hidup berdampingan dengan `Fact_Penumpang_Rute`. Keduanya dihubungkan secara elegan melalui konsep **Conformed Dimension** (Dimensi yang Disepakati), yaitu menggunakan `Dim_Bandara` yang sama. Ini memungkinkan analis melakukan *Drill-Across* (analisis lintas tabel tanpa merusak detail masing-masing data).

**6. Pemahaman Metrik Aviasi & Penempatan Kategori Terminal**
* **Isu:** Apa definisi operasional dari kolom Pesawat, Bagasi, Barang, dan Pos? Dan bagaimana menangani konflik penempatan status Domestik/Internasional untuk data bandara?
* **Solusi:** 'Pesawat' merujuk pada frekuensi penerbangan/pergerakan (bukan jumlah fisik pesawat), 'Bagasi' adalah koper bawaan penumpang, 'Barang' adalah muatan kargo komersial, dan 'Pos' adalah kiriman pos resmi. Untuk kategori Domestik/Internasional pada data bandara, atribut ini diekstrak dari tag yang tertanam (*embedded*) di akhir teks `airport_name` pada CSV BAB VII (contoh: `KUALANAMU - MEDAN (DOM)` → Domestik, `KUALANAMU - MEDAN (INT)` → Internasional). Bandara tanpa tag otomatis bernilai `DOMESTIK`. Nilai ini disisipkan sebagai kolom `kategori` murni di dalam `Fact_Lalu_Lintas_Bandara`.

**7. Integrasi Data Performa dan Produksi Maskapai (Transformasi Unpivot)**
* **Isu:** Ditemukan data baru terkait performa ketepatan waktu (OTP) dan produksi maskapai yang format aslinya berupa laporan (tahun menyamping sebagai kolom), serta terputus hubungannya dari `Dim_Bandara`. Bagaimana memasukkannya ke DWH?
* **Solusi:** Data tersebut memiliki granularitas di level Maskapai, bukan Bandara. Solusinya adalah membuat **`Dim_Maskapai`** baru. Selain itu, bentuk data *cross-tab* wajib dilakukan proses *Unpivot* (Melt) melalui ETL, mengubah kolom tahun menjadi baris data, agar sesuai dengan kaidah *database analitik*.

**8. Domain Knowledge (Asas Cabotage) dan Pemetaan Kategori**
* **Isu:** Terdapat 3 sumber data produksi terpisah: Dalam Negeri, Luar Negeri Nasional, dan Luar Negeri Asing. Apakah ada tumpang tindih maskapai asing di penerbangan domestik?
* **Solusi:** Berdasarkan aturan aviasi (Asas Cabotage), rute domestik eksklusif dikelola maskapai nasional. Oleh karena itu, kita mendesain parameter `kategori_maskapai` (Nasional/Asing) untuk diletakkan di `Dim_Maskapai`, dan `kategori_rute` (Domestik/Internasional) diletakkan di `Fact_Produksi_Maskapai`.

**9. Penanganan Overlap Data dan Pembuatan Aggregate Fact Table**
* **Isu:** Terdapat file "Statistik Per Rute Tahunan" yang angka total penumpangnya 100% *overlap* (sama persis) dengan hasil penjumlahan file "Penumpang Rute Bulanan". Apakah data redundan ini dibuang?
* **Solusi:** Di dalam DWH, agregasi yang tumpang tindih **bukanlah masalah**, melainkan strategi umum yang disebut **Aggregate Fact Table** untuk mempercepat *query* dasbor analitik. Buat tabel fakta baru **`Fact_Statistik_Rute`** karena file ini memiliki metrik unik yang tidak ada di tempat lain (Kapasitas Seat, Load Factor, Jumlah Barang/Pos per Rute). Untuk kategori (Domestik/Intl), tidak perlu ditambahkan kolom baru di tabel ini karena atribut tersebut sudah terwariskan dengan rapi dari `Dim_Rute` melalui *foreign key*.

**10. Klasifikasi Data Eksternal (Kurs Mata Uang)**
* **Isu:** Data harian nilai tukar USD ke IDR telah di-ETL menjadi agregat bulanan dengan metrik yang kaya (rata-rata, min, max, hari trading). Apakah ini tergolong Tabel Dimensi atau Tabel Fakta?
* **Solusi:** Karena tabel ini kini berisi sekumpulan *Measures* (metrik kuantitatif yang bisa dihitung secara matematis) dengan tingkat detail (*grain*) bulanan, tabel ini harus diklasifikasikan sebagai **Tabel Fakta (`Fact_Kurs_Bulanan`)**. Tabel ini akan terhubung ke `Dim_Waktu_Bulanan` menggunakan `waktu_id`, menjadikannya fondasi yang sempurna untuk analisis silang (*drill-across*) dengan tabel fakta penerbangan dan maskapai.

**11. Pemisahan Dimensi Waktu Berdasarkan Grain (*Split Dim_Waktu*)**
* **Isu:** `Dim_Waktu` harus melayani dua grain berbeda: Bulanan (untuk `Fact_Penumpang_Rute`, `Fact_Kurs_Bulanan`) dan Tahunan (untuk `Fact_Statistik_Rute`, `Fact_Lalu_Lintas_Bandara`, `Fact_Produksi_Maskapai`, `Fact_OTP_Maskapai`). Jika digabung dalam satu tabel, format `waktu_id` tidak konsisten (6 digit vs 4 digit) dan baris tahunan akan penuh NULL.
* **Solusi:** Pisahkan menjadi dua tabel: **`Dim_Waktu_Bulanan`** (60 baris = 12 × 5 tahun) dan **`Dim_Waktu_Tahunan`** (5 baris, 2020–2024). Setiap tabel fakta terhubung ke dimensi waktu yang sesuai dengan grain-nya. Data OTP tahun 2018–2019 dari BAB XII **dibuang** agar konsisten dengan rentang waktu seluruh dataset lainnya (2020–2024). Kolom tambahan seperti `nama_bulan`, `kuartal`, dan `semester` di `Dim_Waktu_Bulanan` memperkaya kemampuan *slicing* analitik.

**12. Pengayaan Dimensi Maskapai (Kolom Tambahan dari BAB II)**
* **Isu:** Data sumber BAB II memiliki informasi `jenis_kegiatan` (Penumpang/Kargo/Penumpang & Kargo) dan `negara_asal` (untuk maskapai asing) yang semula tidak dicantumkan di blueprint `Dim_Maskapai`.
* **Solusi:** Tambahkan kedua kolom tersebut ke `Dim_Maskapai` untuk memperkaya kemampuan analisis. `jenis_kegiatan` memungkinkan filtering maskapai berdasarkan tipe operasi, dan `negara_asal` memungkinkan analisis distribusi negara asal maskapai asing. Untuk maskapai nasional, `negara_asal` diisi `'Indonesia'`.

---

### 🚀 Blueprint Final Data Warehouse (Checkpoint Terkini)

Berikut adalah struktur final skema DWH:

#### A. Tabel Dimensi (Konteks Deskriptif)

**1. `Dim_Bandara`**
*(Satu sumber kebenaran untuk semua lokasi, diratakan/denormalisasi. Bertindak sebagai Conformed Dimension).*
| Nama Kolom | Tipe | Keterangan |
| :--- | :--- | :--- |
| **bandara_id** | Primary Key | *Surrogate Key* (ID Unik) |
| kode_iata | Natural Key | Kode bandara (misal: CGK, DPS) |
| nama_bandara | Text | Nama bandara (misal: Soekarno-Hatta) |
| kota | Text | Kota lokasi bandara |
| provinsi | Text | Provinsi lokasi bandara (NULL untuk Luar Negeri) |
| negara | Text | Negara asal bandara |

**2. `Dim_Rute`**
*(Tabel relasi yang mengikat 2 bandara dan menyimpan atribut rute)*
| Nama Kolom | Tipe | Keterangan |
| :--- | :--- | :--- |
| **rute_id** | Primary Key | *Surrogate Key* (ID Unik) |
| kode_rute | Natural Key | Kode gabungan (misal: AAP-BDJ) |
| bandara_1_id | Foreign Key | Mengarah ke `Dim_Bandara` (bandara asal/ke-1) |
| bandara_2_id | Foreign Key | Mengarah ke `Dim_Bandara` (bandara tujuan/ke-2) |
| kategori | Text | 'DOMESTIK' atau 'INTERNASIONAL' |

**3. `Dim_Waktu_Bulanan`** ✅
*(Dimensi waktu untuk tabel fakta ber-grain bulanan. Sudah selesai dibuat.)*
| Nama Kolom | Tipe | Keterangan |
| :--- | :--- | :--- |
| **waktu_id** | Primary Key | Format YYYYMM (misal: 202001) |
| tahun | Integer | misal: 2020 |
| bulan | Integer | 1 s.d 12 |
| nama_bulan | Text | Nama bulan (misal: Januari) |
| kuartal | Integer | 1 s.d 4 |
| semester | Integer | 1 atau 2 |

**4. `Dim_Waktu_Tahunan`**
*(Dimensi waktu untuk tabel fakta ber-grain tahunan. Range: 2020–2024.)*
| Nama Kolom | Tipe | Keterangan |
| :--- | :--- | :--- |
| **waktu_id** | Primary Key | Format YYYY (misal: 2020) |
| tahun | Integer | misal: 2020 |

**5. `Dim_Maskapai`**
*(Menyimpan data identitas badan usaha angkutan udara, diperkaya dengan jenis kegiatan dan negara asal)*
| Nama Kolom | Tipe | Keterangan |
| :--- | :--- | :--- |
| **maskapai_id** | Primary Key | *Surrogate Key* (ID Unik) |
| nama_maskapai | Text | Nama perusahaan (Standarisasi via ETL, misal: PT GARUDA INDONESIA) |
| kategori_maskapai | Text | 'NASIONAL' atau 'ASING' |
| jenis_kegiatan | Text | 'PENUMPANG', 'KARGO', atau 'PENUMPANG & KARGO' |
| negara_asal | Text | Negara asal maskapai ('Indonesia' untuk Nasional, nama negara untuk Asing) |

#### B. Tabel Fakta (Metrik Kuantitatif)

**1. `Fact_Penumpang_Rute`**
*(Grain: Rute, Bulanan. Sangat ramping, terpusat pada tren musiman rute)*
| Nama Kolom | Tipe | Keterangan |
| :--- | :--- | :--- |
| **waktu_id** | Foreign Key | Mengarah ke `Dim_Waktu_Bulanan` |
| **rute_id** | Foreign Key | Mengarah ke `Dim_Rute` |
| jumlah_penumpang | Numeric | Metrik/Measure (total penumpang PP) |

**2. `Fact_Statistik_Rute`**
*(Grain: Rute, Tahunan. Aggregate Fact Table untuk metrik performa rute tahunan)*
| Nama Kolom | Tipe | Keterangan |
| :--- | :--- | :--- |
| **waktu_id** | Foreign Key | Mengarah ke `Dim_Waktu_Tahunan` |
| **rute_id** | Foreign Key | Mengarah ke `Dim_Rute` |
| jumlah_penerbangan | Numeric | Frekuensi penerbangan per tahun |
| jumlah_penumpang | Numeric | Total penumpang (untuk *fast query*) |
| kapasitas_seat | Numeric | Total kursi tersedia setahun |
| jumlah_barang_kg | Numeric | Total kargo rute tersebut (KG) |
| jumlah_pos_kg | Numeric | Total surat/pos rute tersebut (KG) |
| load_factor_pct | Numeric | Persentase keterisian kursi (Desimal, misal 0.87) |

**3. `Fact_Lalu_Lintas_Bandara`**
*(Grain: 1 Bandara × 1 Tahun × 1 Kategori. Mengakomodasi beban fasilitas bandara)*
| Nama Kolom | Tipe | Keterangan |
| :--- | :--- | :--- |
| **waktu_id** | Foreign Key | Mengarah ke `Dim_Waktu_Tahunan` |
| **bandara_id** | Foreign Key | Mengarah ke `Dim_Bandara` |
| kategori | Text | 'DOMESTIK' atau 'INTERNASIONAL' (Diekstrak via Regex dari tag embedded di `airport_name` BAB VII) |
| pesawat_dtg | Numeric | Jumlah pergerakan pesawat datang |
| pesawat_brk | Numeric | Jumlah pergerakan pesawat berangkat |
| pesawat_total | Numeric | Total pergerakan pesawat |
| penumpang_dtg | Numeric | Jumlah penumpang datang |
| penumpang_brk | Numeric | Jumlah penumpang berangkat |
| penumpang_tra | Numeric | Jumlah penumpang transit |
| penumpang_total | Numeric | Total jumlah penumpang |
| bagasi_dtg | Numeric | Berat bagasi datang |
| bagasi_brk | Numeric | Berat bagasi berangkat |
| bagasi_total | Numeric | Total berat bagasi |
| barang_dtg | Numeric | Berat kargo/barang datang |
| barang_brk | Numeric | Berat kargo/barang berangkat |
| barang_total | Numeric | Total berat kargo/barang |
| pos_dtg | Numeric | Berat kiriman pos datang |
| pos_brk | Numeric | Berat kiriman pos berangkat |
| pos_total | Numeric | Total berat kiriman pos |

**4. `Fact_Produksi_Maskapai`**
*(Grain: Maskapai, Tahunan. Berisi metrik kapasitas dan beban operasional maskapai)*
| Nama Kolom | Tipe | Keterangan |
| :--- | :--- | :--- |
| **waktu_id** | Foreign Key | Mengarah ke `Dim_Waktu_Tahunan` |
| **maskapai_id** | Foreign Key | Mengarah ke `Dim_Maskapai` |
| kategori_rute | Text | 'DOMESTIK' atau 'INTERNASIONAL' (Berdasarkan asal file data) |
| aircraft_km | Numeric | Jarak tempuh pesawat (dalam unit asli setelah dikali 1000) |
| aircraft_departure | Numeric | Jumlah keberangkatan pesawat |
| aircraft_hours | Numeric | Total jam terbang (Desimal, hasil konversi ETL) |
| passenger_carried | Numeric | Total penumpang yang diangkut |
| freight_carried | Numeric | Total barang yang diangkut (Ton) |
| passenger_km | Numeric | Jarak tempuh penumpang |
| available_seat_km | Numeric | Kursi tersedia per KM (Kapasitas) |
| passenger_load_factor | Numeric | Persentase keterisian penumpang (%) |
| ton_km_passenger | Numeric | Tonase KM - Penumpang |
| ton_km_freight | Numeric | Tonase KM - Kargo |
| ton_km_mail | Numeric | Tonase KM - Pos |
| ton_km_total | Numeric | Tonase KM - Total |
| available_ton_km | Numeric | Kapasitas Ton KM yang tersedia |
| weight_load_factor | Numeric | Persentase keterisian beban (%) |

**5. `Fact_OTP_Maskapai`**
*(Grain: Maskapai, Tahunan. Mengukur ketepatan waktu maskapai. Data 2018–2019 dibuang, hanya 2020–2024.)*
| Nama Kolom | Tipe | Keterangan |
| :--- | :--- | :--- |
| **waktu_id** | Foreign Key | Mengarah ke `Dim_Waktu_Tahunan` |
| **maskapai_id** | Foreign Key | Mengarah ke `Dim_Maskapai` |
| otp_percentage | Numeric | Tingkat ketepatan waktu (Format desimal, misal 0.8619 untuk 86.19%) |

**6. `Fact_Kurs_Bulanan`**
*(Grain: Waktu, Bulanan. Merekam volatilitas dan rata-rata nilai tukar)*
| Nama Kolom | Tipe | Keterangan |
| :--- | :--- | :--- |
| **waktu_id** | Foreign Key | Mengarah ke `Dim_Waktu_Bulanan` |
| avg_kurs_jual | Numeric | Rata-rata kurs jual per bulan |
| avg_kurs_beli | Numeric | Rata-rata kurs beli per bulan |
| avg_kurs_tengah | Numeric | Rata-rata kurs tengah per bulan |
| min_kurs_tengah | Numeric | Nilai kurs tengah terendah di bulan tsb |
| max_kurs_tengah | Numeric | Nilai kurs tengah tertinggi di bulan tsb |
| jumlah_hari_trading | Integer | Jumlah hari bursa aktif (validitas metrik) |

---
---

### 🗺️ Peta Strategi ETL: Dari CSV Sumber ke Tabel DWH Target

Urutan eksekusi disusun berdasarkan dependensi — **Dimensi duluan, Fakta belakangan**. Setiap tabel dipetakan: dari mana datanya, apa transformasinya, dan apa risiko/tantangannya.

---

## FASE 1: BANGUN TABEL DIMENSI (Pondasi Referensi)

---

### 1.1 `Dim_Waktu_Bulanan` ✅ SUDAH SELESAI
| Item | Detail |
|:---|:---|
| **Sumber** | Generate manual via Python |
| **Status** | Selesai (60 baris = 12 × 5 tahun, 2020–2024) |

---

### 1.2 `Dim_Waktu_Tahunan` 🔲 BELUM
| Item | Detail |
|:---|:---|
| **Sumber** | Generate manual via Python |
| **Jumlah Baris** | 5 baris (2020–2024). Data OTP 2018–2019 dibuang (Keputusan K1). |
| **Transformasi** | Buat DataFrame sederhana: `waktu_id` (YYYY) dan `tahun`. |

---

### 1.3 `Dim_Maskapai` 🔲 BELUM
| Item | Detail |
|:---|:---|
| **Sumber** | **BAB II** (CSV Badan Usaha Niaga Berjadwal Nasional + CSV Perusahaan Angkutan Udara Asing, 2020–2024) |

**Transformasi:**

| Langkah | Detail |
|:---|:---|
| 1. Union semua file | Gabungkan CSV nasional (2020–2024) dan CSV asing (2020–2024). |
| 2. Mapping nama kolom | `nama angkutan udara asing` (2024) → rename ke `nama_maskapai`. `nama badan usaha` (nasional) → rename ke `nama_maskapai`. |
| 3. Handle missing column | File asing 2020 tidak punya kolom `negara` → inject `NULL`. |
| 4. Cleansing | Strip whitespace, uppercase, koreksi typo (`Penumparig`→`Penumpang`, `Perumpang`→`Penumpang`, `Cargo`→`Kargo`, `Khusus Kargo`→`Kargo`). Standardisasi `jenis_kegiatan` ke ENUM: `PENUMPANG`, `KARGO`, `PENUMPANG & KARGO`. |
| 5. Derive `kategori_maskapai` | File nasional → `'NASIONAL'`, file asing → `'ASING'`. |
| 6. Derive `negara_asal` | Maskapai nasional → `'Indonesia'`. Maskapai asing → ambil dari kolom `negara` CSV sumber. |
| 7. Deduplikasi | Ambil nama maskapai unik lintas semua tahun. |
| 8. Generate surrogate key | Auto-increment `maskapai_id`. |

---

### 1.4 `Dim_Bandara` 🔲 BELUM — ⚡ PALING KOMPLEKS
| Item | Detail |
|:---|:---|
| **Sumber Utama** | **BAB VII** (`DATA LALU LINTAS ANGKUTAN UDARA DI BANDAR UDARA TAHUN 2020-2024.csv`) |
| **Sumber Pelengkap** | **BAB III** (Rute) dan **BAB VI** (string rute di file Jumlah & Statistik) — untuk ekstraksi `kode_iata` |

**Mengapa kompleks?** Tidak ada satu CSV pun yang menyediakan semua kolom `Dim_Bandara` secara lengkap:

| Kolom Target | Dari Mana | Cara Dapat |
|:---|:---|:---|
| `bandara_id` | Generate | Surrogate Key (auto-increment) |
| `kode_iata` | BAB III / BAB VI | Ekstrak dari string rute, misal `"Jakarta (CGK)"` → parse `CGK` |
| `nama_bandara` | BAB VII | Kolom `airport_name` (setelah strip tag DOM/INT) |
| `kota` | BAB III / BAB VI | Nama sebelum kurung IATA di string rute, misal `"Jakarta"` |
| `provinsi` | BAB VII | Kolom `propinsi_name` |
| `negara` | Derive | Sumber BAB VII → `'Indonesia'`. Bandara asing dari rute internasional → perlu di-set manual atau lookup. |

**Strategi Pembangunan (2 Tahap):**

**Tahap A — Fondasi dari BAB VII (Bandara Domestik):**
1. Baca CSV BAB VII.
2. Bersihkan tag kategori dari `airport_name`: strip `(DOM)`, `(INT)`, `(DOMESTIK)`, `(INTERNASIONAL)` via Regex → simpan nama bandara bersih.
3. Ambil kombinasi unik `(nama_bandara_bersih, propinsi_name)`.
4. **Buang** kolom `airport_code` (bukan IATA, hanya index alfabet per provinsi).
5. Set `negara = 'Indonesia'` untuk semua.

**Tahap B — Perkaya dengan Kode IATA dari BAB III/VI:**
1. Dari CSV rute BAB III & BAB VI, parse semua string rute → ekstrak pasangan `(nama_kota, kode_iata)`.
2. **Match** nama bandara BAB VII ke nama kota dari rute → pasangkan `kode_iata`. (Lihat Strategi Matching K4 di bawah).
3. Bandara asing (muncul di rute internasional, tidak ada di BAB VII) → tambahkan sebagai baris baru dengan `provinsi = NULL`, `negara` diisi manual.

#### Strategi Matching Nama Bandara ↔ Kode IATA (K4)

Tantangan utama: nama di BAB VII adalah **nama bandara** (misal `SOEKARNO-HATTA`), sedangkan nama di string rute BAB III/VI adalah **nama kota** (misal `Jakarta`). Keduanya tidak identik. Berikut urutan strategi dari yang paling direkomendasikan secara best-practice:

**🥇 Prioritas 1: Exact Match setelah Standardisasi Agresif**
Langkah pertama yang wajib dicoba. Normalisasi kedua sisi (uppercase, strip whitespace, hapus tanda baca), lalu cocokkan.
* **Keunggulan:** Paling cepat, nol risiko *false positive* (salah cocok). Tidak perlu library tambahan.
* **Kekurangan:** Hanya menangkap bandara yang kebetulan nama kota dan nama bandaranya sama persis (misal `HALIM PERDANAKUSUMA` tidak akan match ke `Jakarta`). Coverage kemungkinan rendah.
* **Kapan gagal:** Hampir pasti banyak yang tidak match, jadi ini lebih berfungsi sebagai *first pass* penyaring awal.

**🥈 Prioritas 2: Manual Mapping Dictionary (Lookup Table Buatan)**
Buat kamus Python (`dict`) yang secara eksplisit memetakan nama bandara BAB VII ke kode IATA. Contoh: `{"SOEKARNO-HATTA - JAKARTA": "CGK", "NGURAH RAI - BALI": "DPS", ...}`.
* **Keunggulan:** Akurasi 100% — setiap mapping diverifikasi manusia. Ini adalah **gold standard** di proyek DWH profesional untuk dataset berskala kecil-menengah. Jumlah bandara Indonesia terbatas (~200–300), sangat feasible untuk dibangun manual.
* **Kekurangan:** Butuh effort awal untuk menyusun kamus. Jika ada bandara baru di masa depan, kamus harus di-update manual.
* **Rekomendasi:** Gunakan hasil *Prioritas 1* (exact match) untuk mengisi sebanyak mungkin, sisanya lengkapi manual.

**🥉 Prioritas 3: Fuzzy Matching dengan Human Review**
Gunakan library seperti `fuzzywuzzy` atau `rapidfuzz` dengan algoritma *token_set_ratio* untuk mencocokkan string yang mirip tapi tidak identik.
* **Keunggulan:** Otomatis, bisa menangkap variasi ejaan dan urutan kata. Berguna untuk *discovery* — menemukan kandidat match yang tidak terpikirkan.
* **Kekurangan:** **Wajib di-review manual hasilnya.** Fuzzy matching bisa menghasilkan *false positive* (misal: `SULTAN HASANUDDIN - MAKASSAR` bisa salah match ke `SULTAN SYARIF KASIM II - PEKANBARU` jika threshold terlalu longgar). Butuh tuning threshold (biasanya 80–90).
* **Rekomendasi:** Gunakan sebagai alat bantu *discovery* untuk mempercepat pembuatan Manual Mapping Dictionary (Prioritas 2), bukan sebagai pengganti.

**Strategi Gabungan yang Direkomendasikan:**
```
1. Exact Match (tangkap yang mudah)
       ↓ sisa yang belum match
2. Fuzzy Match (generate kandidat)
       ↓ review manual hasilnya
3. Manual Mapping Dict (finalisasi & verifikasi semua)
       ↓ hasil akhir
4. Semua bandara punya kode_iata ✅
```

---

### 1.5 `Dim_Rute` 🔲 BELUM
| Item | Detail |
|:---|:---|
| **Sumber** | **BAB III** (Rute Angkutan Udara Niaga Berjadwal, Domestik & Internasional 2020–2024) |
| **Dependensi** | `Dim_Bandara` harus sudah selesai (butuh FK `bandara_1_id` & `bandara_2_id`) |

**Transformasi:**

| Langkah | Detail |
|:---|:---|
| 1. Normalisasi skema | 2020–2021: 2 kolom terpisah (asal, tujuan). 2022+: 1 kolom gabungan. Pecah semua jadi `bandara_asal` dan `bandara_tujuan`. |
| 2. Standardisasi spasi | `"Jakarta(CGK)"` → `"Jakarta (CGK)"` via `text.replace("(", " (")`. |
| 3. Ekstrak kode IATA | Parse `"Jakarta (CGK)"` → `CGK`. Gabung asal-tujuan → `kode_rute` misal `"CGK-DPS"`. |
| 4. Deduplikasi | Ambil rute unik lintas semua tahun. |
| 5. Derive `kategori` | File Dalam Negeri → `'DOMESTIK'`, file Luar Negeri → `'INTERNASIONAL'`. |
| 6. Lookup FK bandara | `kode_iata` asal → cari `bandara_1_id` di `Dim_Bandara`. Kode tujuan → `bandara_2_id`. |

---

## FASE 2: BANGUN TABEL FAKTA (Metrik Kuantitatif)

Semua dimensi sudah tersedia → FK bisa di-lookup.

---

### 2.1 `Fact_Penumpang_Rute`
| Item | Detail |
|:---|:---|
| **Sumber** | **BAB VI — Jumlah Penumpang Per Bulan** (Dalam Negeri & Luar Negeri, 2020–2024) |
| **Grain** | 1 rute × 1 bulan |
| **Dependensi FK** | `Dim_Waktu_Bulanan`, `Dim_Rute` |

**Transformasi:**

| Langkah | Detail |
|:---|:---|
| 1. Standardisasi header bulan | 2020–2021: Indonesia (`Agu`, `Okt`). 2022+: Inggris (`Aug`, `Oct`). Rename semua ke format baku (1–12). |
| 2. Drop kolom agregat | Hapus kolom `TOTAL <Tahun>` (1–3 kolom tergantung tahun). |
| 3. Parse string rute | Pecah kolom `RUTE` → ambil kode IATA asal & tujuan → gabung jadi `kode_rute`. |
| 4. UNPIVOT (Melt) | 12 kolom bulan → 2 kolom: `bulan` (1–12) dan `jumlah_penumpang`. |
| 5. Construct `waktu_id` | Tahun file + nomor bulan → `YYYYMM` (misal `202003`). |
| 6. Lookup FK | `waktu_id` → `Dim_Waktu_Bulanan`. `kode_rute` → `rute_id` di `Dim_Rute`. |
| 7. Handle NULL | `jumlah_penumpang` kosong/NaN → `0`. Buang baris footer/total. |

---

### 2.2 `Fact_Statistik_Rute`
| Item | Detail |
|:---|:---|
| **Sumber** | **BAB VI — Statistik Per Rute** (Dalam Negeri & Luar Negeri, 2020–2024, 10 file) |
| **Grain** | 1 rute × 1 tahun |
| **Dependensi FK** | `Dim_Waktu_Tahunan`, `Dim_Rute` |

**Transformasi:**

| Langkah | Detail |
|:---|:---|
| 1. Schema mapping header | Rename inkonsistensi: `L/F` / `LF %` → `load_factor_pct`. `JUMLAH BARANG` / `JUMLAH BARANG KG` → `jumlah_barang_kg`. Dst. |
| 2. Inject kolom tahun | CSV tidak punya kolom tahun. Ekstrak dari nama folder/file → inject. |
| 3. Parse string rute | Sama seperti Fact_Penumpang_Rute → ambil `kode_rute`. |
| 4. Cleansing numerik | Hapus koma eropa di Load Factor, casting ke float. |
| 5. Construct `waktu_id` | Tahun langsung → misal `2024`. |
| 6. Lookup FK | `waktu_id` → `Dim_Waktu_Tahunan`. `kode_rute` → `rute_id` di `Dim_Rute`. |
| 7. Handle NULL/footer | Buang baris total, isi NULL metrik dengan `0`. |

---

### 2.3 `Fact_Lalu_Lintas_Bandara`
| Item | Detail |
|:---|:---|
| **Sumber** | **BAB VII** (single CSV, ~1281 baris) |
| **Grain** | 1 bandara × 1 tahun × 1 kategori |
| **Dependensi FK** | `Dim_Waktu_Tahunan`, `Dim_Bandara` |

**Transformasi:**

| Langkah | Detail |
|:---|:---|
| 1. Ekstrak `kategori` | Regex parse tag dari `airport_name`: `(DOM)`/`(DOMESTIK)` → `'DOMESTIK'`, `(INT)`/`(INTERNASIONAL)` → `'INTERNASIONAL'`. Tanpa tag → `'DOMESTIK'`. |
| 2. Bersihkan `airport_name` | Strip tag kategori → nama bandara bersih (untuk matching ke `Dim_Bandara`). |
| 3. Sanitasi numerik | Semua kolom metrik = string. Hapus titik ribuan, ganti dash `"-"` → `0`, casting ke integer/float. |
| 4. Construct `waktu_id` | Kolom `year` → langsung jadi `waktu_id` (YYYY). |
| 5. Lookup FK bandara | Match nama bandara bersih → `bandara_id` di `Dim_Bandara`. |
| 6. Drop kolom referensi | Buang `propinsi_code`, `propinsi_name`, `airport_code`, `airport_name`, `keterangan`. |

---

### 2.4 `Fact_Produksi_Maskapai`
| Item | Detail |
|:---|:---|
| **Sumber** | **BAB IV** (96 file CSV, format wide/pivot, 14 metrik per maskapai) |
| **Grain** | 1 maskapai × 1 tahun × 1 kategori_rute |
| **Dependensi FK** | `Dim_Waktu_Tahunan`, `Dim_Maskapai` |

**Transformasi:**

| Langkah | Detail |
|:---|:---|
| 1. UNPIVOT (Melt) kolom tahun | Kolom `2020`–`2024` → turun jadi baris: kolom `tahun` + kolom `nilai`. |
| 2. PIVOT baris metrik | 14 baris metrik (`Aircraft KM`, `Passenger Carried`, dll.) → naik jadi 14 kolom terpisah. Hasil: satu baris per maskapai per tahun. |
| 3. Sanitasi numerik | Ganti koma eropa → titik, hapus tanda kutip, ganti dash → `NULL`/`0`, casting ke float. |
| 4. Derive `kategori_rute` | Dari metadata folder: Dalam Negeri → `'DOMESTIK'`, Luar Negeri → `'INTERNASIONAL'`. |
| 5. Cleansing nama maskapai | Standardisasi agar match `Dim_Maskapai`: uppercase, strip, hapus `PT.` dll. |
| 6. Construct `waktu_id` | Tahun → format YYYY. |
| 7. Lookup FK | Nama maskapai → `maskapai_id`. `waktu_id` → `Dim_Waktu_Tahunan`. |

**Catatan:** Satu maskapai bisa punya 2 baris per tahun (1 domestik + 1 internasional). Ini bukan duplikasi, ini grain-nya.

---

### 2.5 `Fact_OTP_Maskapai`
| Item | Detail |
|:---|:---|
| **Sumber** | **BAB XII** (1 file CSV, 15 maskapai, format wide 2018–2024) |
| **Grain** | 1 maskapai × 1 tahun |
| **Dependensi FK** | `Dim_Waktu_Tahunan`, `Dim_Maskapai` |

**Transformasi:**

| Langkah | Detail |
|:---|:---|
| 1. UNPIVOT (Melt) | Kolom tahun `2018`–`2024` → baris: `tahun` + `otp_value`. |
| 2. Filter tahun | Buang baris 2018 & 2019 (Keputusan K1). Pertahankan hanya 2020–2024. |
| 3. Sanitasi numerik | Hapus `%`, ganti koma → titik, casting ke float. Konversi ke desimal: bagi 100 (misal `86.19` → `0.8619`). |
| 4. Cleansing nama maskapai | `"PT. Garuda Indonesia"` → `"PT GARUDA INDONESIA"`. Hapus titik singkatan, uppercase, strip. |
| 5. Construct `waktu_id` | Tahun → format YYYY. |
| 6. Lookup FK | Nama maskapai → `maskapai_id`. `waktu_id` → `Dim_Waktu_Tahunan`. |

---

### 2.6 `Fact_Kurs_Bulanan`
| Item | Detail |
|:---|:---|
| **Sumber** | **KURS BI** (`BI.csv`, ~1230 baris harian) |
| **Grain** | 1 bulan (agregat dari harian) |
| **Dependensi FK** | `Dim_Waktu_Bulanan` |

**Transformasi:**

| Langkah | Detail |
|:---|:---|
| 1. Skip metadata | `skiprows=2` saat read CSV (baris 1–2 = judul laporan). |
| 2. Parse tanggal | `"12/31/2024 12:00:00 AM"` → datetime → ekstrak `tahun` dan `bulan`. |
| 3. Derive kurs tengah | `kurs_tengah = (kurs_jual + kurs_beli) / 2` per baris harian. |
| 4. Agregasi bulanan | GroupBy `(tahun, bulan)` → `AVG(kurs_jual)`, `AVG(kurs_beli)`, `AVG(kurs_tengah)`, `MIN(kurs_tengah)`, `MAX(kurs_tengah)`, `COUNT(*)` → `jumlah_hari_trading`. |
| 5. Construct `waktu_id` | `YYYYMM` dari tahun + bulan. |
| 6. Filter range | Pertahankan hanya 2020–2024. |

---

## FASE 3: RINGKASAN URUTAN EKSEKUSI

```
GELOMBANG 1 — Dimensi Independen (tanpa dependensi satu sama lain):
  ├── 1. Dim_Waktu_Bulanan    ✅ SELESAI
  ├── 2. Dim_Waktu_Tahunan    (generate, 5 baris)
  └── 3. Dim_Maskapai          (dari BAB II)

GELOMBANG 2 — Dimensi dengan Integrasi Silang:
  ├── 4. Dim_Bandara           (BAB VII + BAB III/VI untuk IATA)
  └── 5. Dim_Rute              (BAB III, butuh Dim_Bandara selesai)

GELOMBANG 3 — Tabel Fakta (butuh semua dimensi selesai):
  ├── 6. Fact_Penumpang_Rute          (BAB VI Jumlah)
  ├── 7. Fact_Statistik_Rute          (BAB VI Statistik)
  ├── 8. Fact_Lalu_Lintas_Bandara     (BAB VII)
  ├── 9. Fact_Produksi_Maskapai       (BAB IV)
  ├── 10. Fact_OTP_Maskapai           (BAB XII)
  └── 11. Fact_Kurs_Bulanan           (KURS BI)
```

---