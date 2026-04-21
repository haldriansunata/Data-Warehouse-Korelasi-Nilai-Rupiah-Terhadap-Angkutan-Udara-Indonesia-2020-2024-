# Analisis Struktur Data BAB XII - On Time Performance (OTP)

Dokumen ini memparkan hasil profiling dan _Data Engineering Mapping_ terhadap file CSV tunggal penentu kualitas layanan maskapai nasional pada **BAB XII**: `TINGKAT KETEPATAN WAKTU (ON TIME PERFORMANCE) BADAN USAHA ANGKUTAN UDARA NIAGA PENERBANGAN NIAGA BERJADWAL DALAM NEGERI 2024.csv`

## 1. Analisis Skema dan Tipe Data (*Data Profiling*)
Data direkam dalam format yang sangat sederhana (_Pivot Table_ dimensi maskapai vs waktu). Seluruh rekam jejak efisiensi waktu 15 maskapai domestik dibenturkan dari tahun sebelum pandemi (2018) hingga batas laporan (2024) di dalam file ini.

### 1.1 Struktur Fisik Pivot Historikal (Wide-Table)
*   **Total Baris**: 15 Baris (Mewakili 15 Maskapai berjadwal dalam negeri).
*   **Struktur Header (9 Kolom)**: `[NO, BADAN USAHA, 2018, 2019, 2020, 2021, 2022, 2023, 2024]`
*   **Missing Values**: Utuh 100% (*`has_nulls: false`*). Semua sel terisi angka persentase OTP.

### 1.2 Anomali Tipe Data & Tipografi (*Data Type Anomalies*)
Terdeteksi bahwa seluruh nilai OTP terbaca kuat sebagai kolom **String Text** di mata perantara komputasi, alih-alih sebagai kuantitas perbandingan matematis matematis (Numerik Float).

*   **Format Teks**: Berwujud seperti `"61,07%"`, `"90,73%"`.
*   **Root Cause**: Tabel CSV ini mentah-mentah membawa _Suffix Percent_ (`%`) ke setiap sel nya, dan menggunakan sistem pemisah desimal gaya eropa non-standar komputasi berupa koma (`,`). 

---

## 2. Data Warehouse Modeling (Target Faktorial DW)

Ini adalah dataset murni representasi performa. Dalam kamus metodologi DW, data ini didaulat sebagai referensi **Fact Table (`fact_on_time_performance`)**. 

### 2.1 Granularitas Data (Grain)
*   **Current Grain**: Satu baris data menampung total 7 pengukuran tahunan (2018-2024) yang dilebarkan ke kanan untuk Satu Perusahaan Maskapai Pribadi.
*   **Target DW Grain**: Satu baris difokuskan secara mendalam hanya menampung **Satu Pengukuran OTP per Satu Maskapai di Tahun tersebut.**

### 2.2 Tantangan Transformasi Wajib Terbesar (The ETL Action-Plan)
Pada tahap penulisan Script Modul Pipeline (_Transformation Phase_), beberapa operasi wajib Anda sematkan:

**1. Operasi UNPIVOT (Wide-to-Long Melting)**
Sama seperti BAB IV Produksi, DW/Tableau tidak menerima kolom Header berupa Tahun. Lakukan _Melting_: Header Tahun turun menjadi satu array kolom dimensi turunan (_Dimension Time_) bernama `tahun_observasi`, bersama valuenya yang memanjang di kolom `otp_value`.

**2. Sanitisasi Desimal Float Murni**
Ketikkan logic pembersihan teks pada valuenya sebelum didorong masuk _database_:
*   Hapus karakter persentase: `text.replace("%", "")`
*   Konversi pembatas desimal eropa jadi US: `text.replace(",", ".")`
*   Casting paksa hasil akhirnya menjadi data model numerik: `Float/Decimal Type` (sehingga `"88,78%"` _clean_ menjadi `88.78`).

**3. Koreksi Primary Key Mapping (Alias Naming Maskapai)**
*_CRITICAL ACTION!_* Kolom nama maskapai di CSV ini dituliskan dengan singkatan awalan bertitik (Contoh: `PT. Garuda Indonesia`, `PT. Citilink Indonesia`). Sistem join konvensional akan meleset dan gagal ketika menyatukannya dengan Master Identitas Maskapai di BAB II (`dim_badan_usaha`) yang ejaannya tidak pakai titik dan _Uppercase_ (Contoh BAB II: `PT GARUDA INDONESIA`).
_Solusi_: Gunakan Dictionary Mapping sederhana saat proses ETL, hapus tanda singkatan "PT.", jadikan *Uppercase/Lowercase* semua, dan `Strip()` whitespace berlebih agar FK (_Foreign Key_ UUID) _matching_-nya akurat 100%.

### 2.3 Canonical Schema Target (Struktur DW Akhir)
Hasil dari peleburan target dimensional untuk dikonsumsi visualisasi analitik Tableau Anda nanti:
1.  `sk_fact_otp_id` (PK, Nomor UUID pengenal)
2.  `sk_airline_id` (FK, menembak langsung ke ID dimensi list maskapai di BAB II)
3.  `tahun_observasi` (Integer: cth. 2021) 
4.  `otp_percentage` (Float: cth. 75.34. Digunakan oleh Tableau untuk agregasi _Average_ performa maskapai per tahun).
