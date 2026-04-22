Berdasarkan *screenshot* yang kamu kirimkan, **kamu sudah melakukan eksekusi Physical Join yang sangat sempurna dan lengkap\!** Kamu berhasil menangani *Role-Playing Dimensions* dengan melakukan aliasing (menarik tabel berkali-kali dan me-rename-nya) baik untuk Bandara maupun Maskapai di jalur tahunan.

Mengingat kamu menggunakan **Physical Layer** dengan skema yang sangat lengkap, terjadi **Fan-out (penggandaan baris) yang sangat masif** di DS2. Oleh karena itu, bagian *Testing* harus dirombak total menggunakan teknik **LOD (Level of Detail)**.

Berikut adalah catatan tutorial yang sudah **ditulis ulang, diperbarui, dan disesuaikan** dengan arsitektur terlengkapmu, beserta struktur tabel *blueprint* final di bagian akhir.

-----

### 📘 MASTER GUIDE: TABLEAU PHYSICAL LAYER JOIN

*(Versi 3.2 — Full Physical Join & LOD Handling)*

#### BAGIAN 1: PEMAHAMAN DASAR PADA PHYSICAL LAYER

**Kenapa harus 2 Data Source (DS1 & DS2)?**
Data kamu memiliki dua "ritme" (*grain*):

  * **Ritme Bulanan (DS1):** `fact_penumpang_rute` dan `fact_kurs_bulanan`.
  * **Ritme Tahunan (DS2):** Statistik rute, lalu lintas bandara, produksi maskapai, OTP, dan kurs tahunan.
    Jika digabung jadi satu, perhitungan aggregasi akan sangat kacau. Kita pisah agar Tableau lebih mudah memprosesnya.

**Aturan Emas Physical Join (Kanvas Putih / Venn Diagram):**

1.  **Pusat adalah Fakta Waktu:** Tabel pertama yang ditarik menjadi pusat/akar.
2.  **Duplikasi Terjadi (Fan-out):** Karena kita menggabungkan 4 tabel fakta di DS2, baris data akan dikalikan (*Cross-Join*). 1 baris produksi akan digandakan sebanyak jumlah rute dan jumlah lalu lintas di tahun yang sama.
3.  **Haram Menggunakan SUM() Biasa di DS2:** Karena barisnya mengganda, `SUM()` akan menghasilkan angka triliunan. Kamu **WAJIB** menggunakan `AVG()`, `MIN()`, atau **LOD (`{ FIXED }`)**.

-----

#### BAGIAN 2: BUAT DATA SOURCE 1 (JALUR BULANAN)

**Tujuan:** Menggabungkan penumpang bulanan dengan kurs bulanan.
**Tabel Pusat:** `fact_penumpang_rute.csv`

**Langkah Klik per Klik:**

1.  Buka Tableau → Connect to Text File → pilih `fact_penumpang_rute.csv`.
2.  Klik 2x pada kotak di kanvas untuk masuk ke **Physical Layer**.
3.  **Join Kurs:** Drag `fact_kurs_bulanan.csv` → Left Join (`waktu_id = waktu_id`).
4.  **Join Waktu:** Drag `dim_waktu_bulanan.csv` → Left Join (`waktu_id = waktu_id`).
5.  **Join Rute:** Drag `dim_rute.csv` → Left Join (`rute_id = rute_id`).
6.  **Join Bandara (Aliasing 2x):**
      * Drag `dim_bandara.csv` → Left Join ke `dim_rute` (`bandara_1_id = bandara_id`). Rename kotak jadi **Dim Bandara Asal**.
      * Drag lagi `dim_bandara.csv` → Left Join ke `dim_rute` (`bandara_2_id = bandara_id`). Rename kotak jadi **Dim Bandara Tujuan**.
7.  Rename Data Source di pojok kiri bawah menjadi **DS1 Bulanan**.

-----

#### BAGIAN 3: BUAT DATA SOURCE 2 (JALUR TAHUNAN — VERSI LENGKAP)

**Tujuan:** Menggabungkan 4 fakta tahunan dengan kurs tahunan.
**Tabel Pusat:** `fact_kurs_tahunan.csv` (Karena ini satu-satunya tabel murni berbasis waktu tanpa dimensi lain).

**Langkah Klik per Klik (Sesuai Screenshot-mu):**

1.  New Data Source → pilih `fact_kurs_tahunan.csv`. Klik 2x untuk masuk Physical Layer.
2.  **Join 4 Fakta ke Pusat (Semua Left Join via `waktu_id`):**
      * Drag `fact_lalu_lintas_bandara.csv`
      * Drag `fact_otp_maskapai.csv`
      * Drag `fact_produksi_maskapai.csv`
      * Drag `fact_statistik_rute.csv`
3.  **Join Dimensi ke Fakta Masing-masing (Aliasing):**
      * **Untuk Lalu Lintas:** Drag `dim_bandara` ke `fact_lalu_lintas` (`bandara_id = bandara_id`). Rename: **Dim Bandara (Lalu Lintas)**.
      * **Untuk OTP:** Drag `dim_maskapai` ke `fact_otp` (`maskapai_id = maskapai_id`). Rename: **Dim Maskapai (OTP)**.
      * **Untuk Produksi:** Drag `dim_maskapai` ke `fact_produksi` (`maskapai_id = maskapai_id`). Rename: **Dim Maskapai (Produksi)**.
      * **Untuk Rute & Statistik:**
          * Drag `dim_rute` ke `fact_statistik` (`rute_id = rute_id`).
          * Drag `dim_bandara` ke `dim_rute` (`bandara_1_id = bandara_id`). Rename: **Dim Bandara Asal (Statistik)**.
          * Drag `dim_bandara` ke `dim_rute` (`bandara_2_id = bandara_id`). Rename: **Dim Bandara Tujuan (Statistik)**.
4.  Rename Data Source menjadi **DS2 Tahunan**.

-----

#### BAGIAN 4: TESTING & VALIDASI DI SHEET (PENGGUNAAN LOD)

Karena DS1 aman (tidak ada fan-out antar tabel fakta), kita fokus pada *testing* DS2 yang rawan duplikasi. Di DS2, jika kamu meletakkan *Measure* (hijau) ke dalam kanvas, **JANGAN PERNAH** biarkan agregasinya berbunyi `SUM(...)`.

**Test 2.1 — Menguji OTP Maskapai (Gunakan AVG)**

1.  Pastikan Data Source aktif adalah **DS2 Tahunan**.
2.  Drag `Tahun` (dari Fact Kurs Tahunan) ke Columns (ubah jadi Discrete/Biru).
3.  Drag `Nama Maskapai` (dari Dim Maskapai OTP) ke Rows.
4.  Drag `Otp Percentage` ke area Text.
5.  **Krusial:** Klik kanan pill `SUM(Otp Percentage)` → Measure → ubah jadi **Average**. (Karena nilainya menduplikat di setiap baris, rata-rata dari nilai yang sama adalah nilai aslinya).
6.  *Validasi:* Angkanya harus berada di rentang 0.0 hingga 1.0.

**Test 2.2 — Menguji Produksi Maskapai (Wajib LOD)**
Jika kamu ingin menjumlahkan total *Passenger Carried* dari semua maskapai di tahun 2024, `SUM()` biasa akan salah total karena duplikasi. Kamu harus membuat Kalkulasi LOD.

1.  Create Calculated Field baru, beri nama **[LOD] Passenger Carried Asli**:
    ```tableau
    { FIXED [Waktu Id], [Maskapai Id (Fact Produksi Maskapai)] : MIN([Passenger Carried]) }
    ```
2.  Drag `Tahun` ke Columns.
3.  Drag **[LOD] Passenger Carried Asli** ke Rows. Biarkan agregasinya `SUM()`.
4.  *Validasi:* Angkanya akan mencerminkan total penumpang produksi yang sebenarnya tanpa efek penggandaan dari *Physical Join*.

**Test 2.3 — Menguji Korelasi Kurs vs Lalu Lintas Bandara**

1.  Create Calculated Field, beri nama **[LOD] Pesawat Datang Asli**:
    ```tableau
    { FIXED [Waktu Id], [Bandara Id (Fact Lalu Lintas Bandara)] : MIN([Pesawat Dtg]) }
    ```
2.  Drag `Avg Kurs Tengah` ke Columns → Ubah jadi **AVG**.
3.  Drag **[LOD] Pesawat Datang Asli** ke Rows → Biarkan **SUM**.
4.  Drag `Tahun` ke Detail. (Akan muncul 5 titik scatter plot).

> **💡 CHEATSHEET AGREGASI PHYSICAL LAYER**
>
>   * **Kolom Kurs (Jual/Beli/Tengah):** Gunakan selalu `AVG`.
>   * **Persentase/Rasio (OTP, Load Factor):** Gunakan selalu `AVG`.
>   * **Angka Kuantitatif (Jumlah Penumpang, Kargo, dll):** Buat Calculated Field `{ FIXED [Waktu Id], [ID Tabel Fakta Asalnya] : MIN([Kolom Target]) }`, lalu kamu bebas menggunakan `SUM` pada Calculated Field tersebut di kanvas.

-----

### 🗄️ BLUEPRINT DATA WAREHOUSE FINAL (REVISI)

Berdasarkan *update* dan konfirmasi terakhir, dimensi `Dim_Waktu_Tahunan` dihapus karena informasinya (hanya `waktu_id` dan `tahun`) sudah *built-in* secara implisit di dalam `Fact_Kurs_Tahunan` sebagai pusat DS2.

Berikut adalah skema tabel bersihmu:

#### A. Tabel Dimensi

| Tabel | Kolom Utama | Keterangan |
| :--- | :--- | :--- |
| **`Dim_Bandara`** | **bandara\_id** (PK), kode\_iata, nama\_bandara, kota, provinsi, negara | Sumber kebenaran lokasi (negara kosong u/ asing). Di-alias jadi Asal, Tujuan, dan Lalu Lintas. |
| **`Dim_Rute`** | **rute\_id** (PK), kode\_rute, bandara\_1\_id (FK), bandara\_2\_id (FK), kategori | Atribut rute dan FK lokasi. |
| **`Dim_Maskapai`** | **maskapai\_id** (PK), nama\_maskapai, kategori\_maskapai, jenis\_kegiatan, negara\_asal | Di-alias untuk Produksi dan OTP. |
| **`Dim_Waktu_Bulanan`**| **waktu\_id** (PK), tahun, bulan, nama\_bulan, kuartal, semester | Digunakan khusus di DS1. Format: YYYYMM. |

#### B. Tabel Fakta

| Tabel | Kolom Kunci & Metrik | Grain / Agregasi Tableau di Physical |
| :--- | :--- | :--- |
| **`Fact_Penumpang_Rute`**| **waktu\_id**, **rute\_id** <br> `jumlah_penumpang` | Bulanan (DS1). <br> 👉 Gunakan `SUM()` |
| **`Fact_Kurs_Bulanan`** | **waktu\_id** <br> `avg_kurs_...`, `min_kurs_...`, dll | Bulanan (DS1). <br> 👉 Gunakan `AVG()` |
| **`Fact_Kurs_Tahunan`** | **waktu\_id** (Menjadi Pusat DS2) <br> `avg_kurs_...`, `min_kurs_...`, dll | Tahunan (DS2). <br> 👉 Gunakan `AVG()` |
| **`Fact_Statistik_Rute`**| **waktu\_id**, **rute\_id** <br> `jumlah_penumpang`, `load_factor_pct`, dll | Tahunan (DS2). <br> 👉 Kuantitas: `FIXED [Rute Id]`, Rasio: `AVG()` |
| **`Fact_Lalu_Lintas`** | **waktu\_id**, **bandara\_id**, `kategori` <br> `pesawat_...`, `penumpang_...`, `barang_...` | Tahunan (DS2). <br> 👉 Kuantitas: `FIXED [Bandara Id]` |
| **`Fact_Produksi`** | **waktu\_id**, **maskapai\_id**, `kategori_rute` <br> `passenger_carried`, `freight_...`, dll | Tahunan (DS2). <br> 👉 Kuantitas: `FIXED [Maskapai Id]` |
| **`Fact_OTP_Maskapai`** | **waktu\_id**, **maskapai\_id** <br> `otp_percentage` | Tahunan (DS2). <br> 👉 Gunakan `AVG()` |

-----