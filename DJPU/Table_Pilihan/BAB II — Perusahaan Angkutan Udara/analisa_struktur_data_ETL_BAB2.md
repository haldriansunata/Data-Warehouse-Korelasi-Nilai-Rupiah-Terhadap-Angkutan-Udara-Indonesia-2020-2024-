# Analisis Struktur Data BAB II - Perusahaan Angkutan Udara (2020-2024)

Dokumen ini merangkum hasil analisis profil data (*Data Profiling*) untuk target file CSV pada BAB II. Target file terdiri dua kelompok utama: DAFTAR BADAN USAHA ANGKUTAN UDARA NIAGA BERJADWAL dan DAFTAR PERUSAHAAN ANGKUTAN UDARA ASING dari tahun 2020 hingga 2024. Analisis ini ditujukan sebagai panduan teknis pada fase Ekstraksi dan Transformasi (ETL) data.

## 1. Analisis Kategori A: Badan Usaha Angkutan Udara Niaga Berjadwal (Nasional)

Kategori ini mencakup badan usaha penerbangan nasional yang beroperasi pada periode bersangkutan.

### A.1. Konsistensi Skema/Kolom
Secara urutan dan jumlah kolom (Struktur Fisik), keseluruhan CSV dari 2020 s.d 2024 memiliki tingkat konsistensi **100%**.

*   **Total Kolom:** 3
*   **Urutan Kolom Baku (Standardized):**
    1.  `no` (Tipe: int64 / numerik)
    2.  `nama badan usaha` (Tipe: string / text)
    3.  `jenis kegiatan` (Tipe: string / text)

*Implikasi ETL:* Tidak diperlukan adanya skenario pemetaan nama kolom atau resolusi kolom ganda (Schema evolution). Data *raw* setiap tahun di file ini dapat secara langsung dilakukan `concat` atau `union` berdasar indeks letak kolom (positional) maupun by-name `nama badan usaha`.

### A.2. Karakteristik Distinct Value & Anomali Kategori (Jenis Kegiatan)
Walaupun strukturnya konsisten identik, value `JENIS KEGIATAN` memiliki penamaan yang berbeda untuk makna yang identik sehingga mengakibatkan inkonsistensi representasi kategori. Berikut variasi nilainya:
*   **Makna Penumpang (Saja):** `Penumpang`, `Penumparig` (*typo scan pdf di tahun 2022*)
*   **Makna Kargo (Saja):** `Kargo`, `Cargo`
*   **Makna Penumpang & Kargo:** `Penumpang dan Kargo`, `Penumpang Dan Kargo` (Casing berbeda)

*Implikasi ETL (Data Cleansing yang harus dilakukan):* 
1. `Trim/Strip` whitespace.
2. Standardisasi alias. Konversi string kotor ke Master Kategori (misalnya: ENUM -> `Penumpang`, `Kargo`, `Penumpang & Kargo`). Termasuk melakukan koreksi typo di string "Penumparig" pada file 2022.

---

## 2. Analisis Kategori B: Perwakilan / Perusahaan Angkutan Udara Asing

Kategori ini berisi daftar dan kegiatan maskapai perwakilan penerbangan asing. Penamaan file mentah variatif:
* 2024 menggunakan "...PERWAKILAN PERUSAHAAN..."
* 2020-2023 menggunakan "...PERUSAHAAN..." 

### B.1. Konsistensi Skema/Kolom
Terdapat evolusi skema (*Schema drift*) pada file rentang tahun 2020, dimana jumlah dan isi kolomnya **BERBEDA** dengan tahun 2021 keatas.

*   **Tahun 2024**
    *   Kolom (4): `no`, `nama angkutan udara asing`, `negara`, `jenis kegiatan`
*   **Tahun 2021, 2022, 2023**
    *   Kolom (4): `no`, `nama perusahaan`, `negara`, `jenis kegiatan`
*   **Tahun 2020**
    *   Kolom (3): `no`, `nama perusahaan`, `jenis kegiatan` 
    *(Tidak terdapat kolom `NEGARA` sama sekali).*

*Implikasi ETL:*
Mekanisme penggabungan (Union) tidak bisa mentah (`strict concat`).
1. **Mapping Nama Kolom:** Di tahap load CSV, rename/petakan indeks kolom ke 2 di CSV 2024 (`NAMA ANGKUTAN UDARA ASING`) menjadi `NAMA PERUSAHAAN`.
2. **Missing Column Handling:** Saat melakukan Union terhadap data tahun 2020, kolom `NEGARA` wajib diinjeksi manual dengan *NULL* list / kosong.

### B.2. Karakteristik Distinct Value & Anomali Kategori (Jenis Kegiatan)
*   **Makna Penumpang:** `Penumpang`, `Perumpang` (typo data 2022), `Penumpang.`
*   **Makna Kargo:** `Kargo`, `Cargo`, `Khusus Kargo`
*   **Makna Penumpang & Kargo:** `Penumpang dan Kargo` (2022-24), `Penumpang & Cargo` (2020-21)

---

## 3. Data Warehouse Modeling (Target Arsitektur ETL)

Pada tingkatan perancangan Data Warehouse & ETL, dataset pada BAB II ini diposisikan sebagai **Dimension Table (Tabel Dimensi)** master data, bukan *Fact Table*. Berikut rumusan klasifikasinya:

### 3.1 Klasifikasi: Dimension Table (`dim_airline` atau `dim_badan_usaha`)
BAB II murni menginformasikan _list/daftar_ referensi entitas perusahaan/badan usaha (Tanpa metrik / _measures_ numerik pengamatan).

### 3.2 Granularitas (Grain)
*   **Target Grain:** Satu baris per Entitas Perusahaan/Maskapai yang unik (_One row per unique Airline_).
*   **Schema Treatment**: Apabila Anda peduli terhadap peruhaan jenis kegiatan/nama mereka dari tahun ke tahun, tabel dimensi ini dapat berfungsi sebagai SCD (Slowly Changing Dimension) Type 2. Jika tidak, data di-Merge/Upsert dedup untuk menghasilkan Lookup list Maskapai.

### 3.3 Draft Target Canonical Schema (Struktur Skema DW Ideal)
*   `sk_airline_id` (Surrogate Key, contoh: BIGINT atau String Hashing)
*   `nama_airline` (Target gabungan nama perusahaan dari Nasional & Asing)
*   `tipe_airline` (Derived Label ENUM: 'Nasional' atau 'Asing')
*   `jenis_kegiatan` (Setelah Mapping Cleansing: 'Penumpang', 'Kargo', 'Penumpang & Kargo')
*   `negara_asal` (Untuk Nasional: "Indonesia". Untuk Asing: Nilai observasinya).
