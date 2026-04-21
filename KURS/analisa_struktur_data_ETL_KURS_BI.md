# Analisis Struktur Data - Referensi KURS BI (USD to IDR)

Dokumen ini membedah data penunjang referensial di dalam folder `KURS`, spesifiknya pada data riwayat nilai tukar Bank Indonesia bernama: **`BI.csv`**. Dataset ini diintegrasikan ke _Data Warehouse_ sebagai instrumen analitik untuk mendeteksi korelasi antara fluktuasi nilai Rupiah terhadap volume penerbangan di Indonesia pada tahun amatan 2020-2024.

## 1. Analisis Skema (*Structure Profiling*)

Berdasarkan pembacaan _raw file header_ secara murni, format CSV ini dihasilkan dari *export portal/sistem BI* yang mana menyertakan _metadata tittle_ di bagian awal barisnya.

### 1.1 Anomali Header (Metadata Padding Row)
*   **Baris ke-1 & ke-2**: Berisi judul laporan `"Kurs Transaksi USD"` dan _blank space_. 
*   **Implikasi ETL**: Proses pengambilan data (seperti `pd.read_csv`) **wajib menyertakan _argument_ `skiprows=2`** agar pembacaan matriks mesin tidak hancur dan langsung mengincar parameter tabel sejatinya.

### 1.2 Profil Tabel Asli Waktu-Runtun (Time Series)
*   **Baris Header Sejati (Baris ke-3)**: `[NO, Nilai, Kurs Jual, Kurs Beli, Tanggal]`
*   **Total Data Point**: ~1.230 Baris. Merepresentasikan _hari kerja aktif (trading days)_ dari akhir 2019/awal 2020 hingga Desember 2024.
*   **Volume Kolom `Nilai`**: Selalu konsisten berisi nominal `1` (yang merepresentasikan unit Basis = "1 USD").

### 1.3 Format Value (Tanggal & Tipe Angka)
*   **Format Numerikal Angka**: Angka desimal KURS sudah sangat *clean* menggunakan standar matematis US (titik sebagai operator pemecah fraksi kepingan), misal: `16081.19`. Tidak diperlukan logic `replace` rumit seperti di BAB sebelumnya.
*   **Format String Tanggal**: Menggunakan gaya Amerika (MM/DD/YYYY) dilengkapi penunjuk waktu AM/PM `[12/31/2024 12:00:00 AM]`.

---

## 2. Data Warehouse Modeling (Target Arsitektur ETL)

Data eksternal KURS seperti ini dalam konsep dimensional DW dapat dikategorikan sebagai **Factless Fact Table** atau **Reference Fact Table (`fact_kurs_harian`)** yang bertugas sebagai pencorong referensi analitik pelengkap.

### 2.1 Granularitas (Grain)
*   **Current & Target DW Grain:** Mutlak 1 Baris per 1 Hari Kalender (*Satu nilai tukar Valas per hari observasi*).

### 2.2 Transformasi Wajib (The ETL Action-Plan)
1.  **Skip Metadata Rows:** Potong dua baris teratas secara dinamis saat melakukan `Data Source Loading`.
2.  **Date Standardizer (Parsing Waktu)**: Parse tipe string waktu `"12/31/2024 12:00:00 AM"` menjadi murni objek _Native Date_ berformat **`YYYY-MM-DD`** (`2024-12-31`). Tanggal yang sudah dinormalisasi ini akan menjadi **Primary Foreign Key** yang sangat vital, yang nantinya akan dijodohkan (`Join`) dengan master _dimensi waktu_ waktu saat di-query bersamaan dengan tabel produktivitas `Fakta Rute` maupun `BAB 12 (OTP)`.
3.  **Kalkulasi Metrik Turunan (Kurs Tengah BI)**: 
    *Secara ilmu moneter/bisnis korelasi*, Analis Data jarang menggunakan pergerakan Kurs Jual atau Kurs Beli secara terpisah untuk korelasi industri. Anda wajib **menambahkan (*Derive*) 1 kolom baru** kalkulasi _Kurs Tengah_ selama tahap ETL, dengan rumus: 
    `=> (Kurs Jual + Kurs Beli) / 2`
    *(Angka Trend Kurs Tengah / Middle Rate inilah yang nantinya akan disuperposisikan bertabrakan di Visualisasi Dashboard Tableau Anda untuk menebak seberapa kuatnya Tren Volume Penumpang vs Naik Turunnya Rupiah).*

### 2.3 Canonical Schema Target (Struktur DW Akhir)
Kerangaka tabel _Schema_ referensi pualam ujungnya di _Cloud / Dashboard Analytical_ Anda:
1.  `sk_kurs_id` (Primary Key Autoincrement)
2.  `tanggal_kurs` (Foreign Key / Date ID - Format Baku ISO `YYYY-MM-DD`)
3.  `mata_uang_asal` (String Statis yang ditambahkan paksa saat ETL: `'USD'`)
4.  `mata_uang_tujuan` (String Statis yang ditambahkan paksa saat ETL: `'IDR'`)
5.  `unit_basis` (Integer: diisi _pass-through_ murni dari kolom `Nilai`, yaitu `1`)
6.  `kurs_jual` (Decimal/Float)
7.  `kurs_beli` (Decimal/Float)
8.  `kurs_tengah_bi` (Decimal/Float kalkulasi turunan / _Derived Column_)
