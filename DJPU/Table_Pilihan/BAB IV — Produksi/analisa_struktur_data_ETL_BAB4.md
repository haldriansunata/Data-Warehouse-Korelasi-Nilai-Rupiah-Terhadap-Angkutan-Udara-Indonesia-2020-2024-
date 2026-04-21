# Analisis Struktur Data BAB IV - Produksi Angkutan Udara (2020-2024)

Dokumen ini mendokumentasikan hasil _Schema Profiling_ dan klasifikasi _Dimensional Modeling_ terhadap seluruh dataset ekstraksi performa produktivitas maskapai pada **BAB IV**. Data terbagi menjadi 3 matriks utama: Prod. Dalam Negeri (Dasar), Prod. Luar Negeri (Nasional), dan Prod. Luar Negeri (Asing). 

Total file observasi: **96 File CSV**

## 1. Analisis Struktur dan Skema (*Data Profiling*)

Analisis otomatis menggunakan script Python terhadap ke-96 CSV yang dihasilkan merepresentasikan tingkat kebersihan data (_Data Quality_) yang luar biasa sempurna dan identik secara skema.

### 1.1 Konsistensi Skema (Zero Schema Drift)
*   Sebanyak **96 dari 96 file** (100%) memiliki arsitektur kolom yang persis sama. Tidak ditemukan adanya pergeseran nama kolom antar tahun maupun antar file/maskapai (_`inconsistent_schemas_found: false`_).
*   **Struktur Header Standar (8 Kolom):**
    `[NO, DESCRIPTION, Unit, 2020, 2021, 2022, 2023, 2024]`
*   **Missing Values:** Bebas dari missing values (*`has_nulls: false`*).

### 1.2 Konsistensi Metrik (*Value Metriks Baku*)
Setiap entitas maskapai secara mutlak berisi **14 baris indikator** yang seragam tanpa kurang/lebih. Standarisasi metrik performa udara mencakup operasional teknis & pax:
  * _Aircraft Departure_, _Aircraft Hours_, _Aircraft KM_
  * _Available Seat KM_, _Available Ton KM_
  * _Freight Carried_, _Passenger Carried_
  * _Passenger KM_, _Passenger L/F_, _Weight L/F_
  * _Ton KM Performed_ (ter-breakdown ke Freight, Mail, Passenger, & Total)

## 2. Data Warehouse Modeling (Target Arsitektur ETL)

Bertolak belakang dengan dataset BAB II atau BAB III yang merupakan konvensi master tabel list (Dimension Tables), isi data dari **BAB IV adalah Murni Tabel Fakta (`Fact Table`) target akhir _Data Warehouse_**.

Dataset BAB IV menyimpan pengukuran observasi (Metrics/Measures) kuantitatif numerik (tonase, km, durasi) yang terus teragregasi.

### 2.1 Klasifikasi: Fact Table (`fact_produktivitas` atau `fact_airlines_metrics`)
Sebagai tabel fakta yang mencatat apa saja "Transaksional Bulanan/Tahunan" yang terjadi di tubuh industri aviasi.

### 2.2 Granularitas (Grain)
*   **Current Grain (Sumber CSV):** Satu baris per `Metrik Performa`, dilebarkan ke kanan (Pivot) per kolom tahun `[2020.. 2024]` untuk satu Maskapai.
*   **Target Data Warehouse Grain:** Satu baris mencatat **satu Nilai Metrik Performa per Tahun untuk Entitas Maskapai di sebuah Jalur Wilayah Udara (Luar/Dalam Negeri).**

### 2.3 Tantangan Unpivot (Wide-to-Long Transformation / Melt)
Bentuk CSV raw saat ini adalah _Wide Format_ atau Pivot Tabel. OLAP Data Warehouse seperti sistem dibelakang Tableau tidak menyenangi tabel pivot tahun sebagai Header Kolom (`2020`, `2021`, ...).
Anda **DIWAJIBKAN** untuk melakukan operasi `UNPIVOT` (di Python: `pd.melt()`) pada tahap Transformasi ETL agar tahun-tahun tersebut bergeser turun membentuk kolom **`Tahun`** sebagai sumbu waktu (Dim Time) dan value nya mengisi kolom **`Metric_Value`**.

### 2.4 Canonical Target Schema (Struktur Skema Final DW)
Rancangan skema relasional tabel Fakta agar _Tableau Engine_ bekerja ringan dan gampang dibedah (*slice-and-dice*):
1.  `sk_produksi_id` (Primary Key, Surrogate UUID/Bigint)
2.  `sk_airline_id` (Foreign Key -> _nge-link ke `dim_badan_usaha` dr. BAB II_)
3.  `tahun_observasi` (Contoh: `2021` - Integer) -> _Hasil Melting Header_
4.  `nama_metrik` (Contoh: `Passenger Carried` - Varchar)
5.  `unit_metrik` (Contoh: `number` atau `ton` - Enum/Varchar)
6.  `nilai_performa` (Decimal/Float) -> _Harus melalui Cleansing kutip desimal eropa misalnya "55,73"_
7.  `cakupan_operasi` (Label Enum: `Dalam Negeri` vs `Luar Negeri`) -> _Diperoleh dari ekstrak Metadata Nama File/Folder induk_

**Catatan Khusus ETL Value:** Nilai numerik Anda dibungkus `"..."` dan menggunakan koma `,` sebagai angka desimal pecahan. ETL Anda WAJIB mengganti karakter `,` menjadi `.` bertipe FLOAT _casting_, serta menghapus karakter strip `-` menjadi Nullable (`NaN` atau `0`) untuk metrik *Mail* yang bolong.
