# Analisis Struktur Data BAB VI - Lalu Lintas Rute (Bagian: CSV "Jumlah Penumpang per Bulan")

Dokumen ini membedah analisis _Data Engineering_ untuk paruh pertama kumpulan data pada BAB VI, yaitu spesifik terhadap **File CSV JUMLAH PENUMPANG PER RUTE BULAN JAN-DES (Dalam & Luar Negeri, 2020-2024)**. File ini mencatat volume trafik penumpang secara _time-series_ bulanan.

## 1. Analisis Skema dan Schema Drift (*Structure Profiling*)
Data ini disajikan dalam format _Wide-Table Pivot_ (nama bulan melebar ke kanan sebagai kolom). Terdapat _Schema Drift_ (evolusi kolom) seiring transisi tahun.

*   **Tahun 2020 & 2021 (Format Lama)**
    *   **Jumlah Kolom**: 17
    *   **Struktur Header**: `[NO, RUTE, Jan, Feb, Mar, Apr, Mei, Jun, Jul, Agu, Sep, Okt, Nov, Des, TOTAL <Tahun Ini>, TOTAL <Tahun Lalu>, TOTAL <2 Tahun Lalu>]`
*   **Tahun 2022, 2023 & 2024 (Format Baru)**
    *   **Jumlah Kolom**: 15
    *   **Struktur Header**: `[NO, RUTE, Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec, TOTAL <Tahun Ini>]`

*Tantangan Skema*: 
1. Penamaan bulan berganti bahasa dari Indonesia (Jan, Agu, Okt) di 2020-2021 menjadi format Inggis (Jan, Aug, Oct) di 2022+.
2. Di tahun lama, terdapat dua kolom ekstra (Total tahun-tahun kebelakang) yang dihilangkan pada laporan tahun baru. 
3. *Nulls*: `has_nulls: true` terdeteksi di seluruh file. Ini biasanya disebabkan oleh baris "total/footer" di ujung CSV atau rute yang belum beroperasi penuh setahun penuh sehingga nilainya divisualisasikan kosong (NaN).

---

## 2. Data Warehouse Modeling (Target Faktorial DW)

Data ini menyimpan kuantifikasi transaksional penumpang. Pada DW Dimensional Modeling, data ini diplot mutlak sebagai **Tabel Fakta Historikal (`fact_penumpang_rute_bulanan`)**.

### 2.1 Granularitas (Grain)
*   **Current Grain:** Pivot. Satu baris mendeskripsikan satu pasang rute dengan 12 bulan dilebarkan ke kanan, berlaku untuk satu rentang tahun (_Wide Format_).
*   **Target DW Grain:** *Satu baris menampung total jumlah penumpang pada SATU Rute di SATU Bulan (YYYY-MM).*

### 2.2 Transformasi Wajib (The ETL Action-Plan)
Pipeline ETL Anda harus mengadopsi logika ini agar tabel faktanya "sehat":
1.  **Drop Aggregate Columns**: Hapus kolom-kolom agregat pre-kalkulasi dari CSV seperti `TOTAL 2020`, `TOTAL 2019`, dsb. Tabel fakta di DW hanya butuh raw bulanan; total tahunan biar menjadi tugas *Tableau* untuk menyummary-kannya (`SUM`).
2.  **Unpivot (Melt Time-Series)**: *Melt* ke-12 kolom bulan-bulan itu menjadi satu sumbu panjang (Tarik ke bawah). 
    * Name of Variable = `Bulan`
    * Name of Value = `Jumlah_Penumpang`
3.  **Date Dimension Mapping**: Konversikan data "Jan-20" / "Agu-21" ke format ID Tanggal standar baku e.g., `2020-01-01` untuk di-konek ke `dim_date/dim_waktu`. Perhatikan perubahan format pengetikan bulan Inggris-Indonesia antar tahun (!).

### 2.3 Canonical Schema Target (Struktur DW Akhir)
Setelah Unpivot dan Cleansing, skema ini siap di-_Load_:
*   `sk_fact_rute_bln_id` (PK, Surrogate Key Integer)
*   `sk_rute_id` (FK -> melambangkan Rute (PP) yang terkonek langsung ke referensi Master `dim_rute` BAB III)
*   `sk_date_id` (FK -> menghubungkan ke dimensi Waktu/Bulan)
*   `tipe_penerbangan` (Label: 'Dalam Negeri' atau 'Luar Negeri')
*   `jumlah_penumpang` (Integer: berisi volume pax). Kosong (Null) dikonvert menjadi `0`.
