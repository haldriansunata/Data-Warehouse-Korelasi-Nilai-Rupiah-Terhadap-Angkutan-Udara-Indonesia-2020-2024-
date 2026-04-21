# Analisis Struktur Data BAB VI - Lalu Lintas Rute (Bagian: CSV "Statistik Per Rute")

Dokumen ini membedah analisis _Data Engineering_ untuk paruh kedua kumpulan data pada BAB VI, yaitu spesifik terhadap **File CSV STATISTIK PER RUTE BERDASARKAN URUTAN JUMLAH PENUMPANG (Dalam & Luar Negeri, 2020-2024)**. File ini mencatat rekapitulasi ringkasan performa transportasi (Pesawat, Pax, Kapasitas, Barang, Pos, Load Factor) untuk satu rute di tahun yang disurvei penuh.

## 1. Analisis Skema dan Schema Drift (*Structure Profiling*)
Format file-file ini dikodekan menggunakan _Long Format_ yang terkompresi ke per spesifik rute dari keseluruhan 1 tahun performa. Struktur tabel ini terbukti cukup stabil.

*   **Konsistensi Dimensi / Frame**
    Total file "Statistik Per Rute" = **10 File**. Seluruh 10 file tersebut memiliki dimensi lebar persis **8 Kolom**.
*   **Struktur Evolusi Header (Schema Drift)**
    Meski jumlahnya sama yaitu 8, nama pengetikan headernya bergeser.
    *   2020-2023: `[NO, RUTE, JUMLAH PENERBANGAN, JUMLAH PENUMPANG, KAPASITAS SEAT, JUMLAH BARANG / JUMLAH BARANG (Kg), JUMLAH POS, L/F]`
    *   2024: `[NO, RUTE PP, JUMLAH PENERBANGAN, JUMLAH PENUMPANG, KAPASITAS SEAT, JUMLAH BARANG KG, JUMLAH POS KG, LF %]`

*Tantangan Skema*: 
1. Inkonsistensi simbol: Kolom "L/F" dipanggil "LF %" di 2024. Kolom muatan dipanggil "JUMLAH BARANG" lalu menjadi "JUMLAH BARANG KG". 
2. Terdapat missing value (`has_nulls: true`) dikarenakan mungkin ada rute yang tidak merekam trafik pos (hanya logistik kargo biasa) atau merupakan blank row/footer.

---

## 2. Data Warehouse Modeling (Target Faktorial DW)

Karena data ini murni _metric performance driven_ (Fakta muatan / efisiensi), maka dataset ini adalah warga sejati (Citizen) dari **Tabel Fakta (`fact_statistik_tahunan_rute`)**. Bedanya dengan 'CSV Jumlah' sebelumnya, level ringkasan tabel ini jauh lebih tebal/memadat (High-Level Aggregation).

### 2.1 Granularitas (Grain)
*   **Current Grain:** Satu baris memotret total komulatif 6 metrik (Penerbangan, Pax, Limit Seat, Berat Barang, Berat Pos, Rasio LF) dari satu Rute selama periode SATU Tahun yang dipantau.
*   **Target DW Grain:** *Identik dengan raw source-nya.* Satu baris berisi agregat performa murni pada 1 Kombinasi Jalur Rute di tahun ke-X. (Tidak diturunkan bulanan!).

### 2.2 Transformasi Wajib (The ETL Action-Plan)
Pipeline ETL kelompok statistik tahunan menuntut arsitektur yang berfokus perataan Mapping, tidak harus Unpivot Ekstrim:
1.  **Column Renaming (Schema Mapping)**: Ciptakan kamus pengganti (*dictionary mapper*). Semua header file (baik itu 'LF %' atau 'L/F') wajib direname paksa menjadi format Canonical DW. Misal:
    * `JUMLAH PENERBANGAN` -> `flight_freq_total`
    * `KAPASITAS SEAT` -> `capacity_seats_total`
    * `JUMLAH BARANG KG` / `JUMLAH BARANG (Kg)` -> `cargo_weight_kg`
    * `L/F` / `LF %` -> `load_factor_percentage`
2.  **Metadata Injection (Year ID)**: Raw file sama sekali tidak memiliki kolom _Tahun_. Proses ETL Python harus menyuntikkan (Inject) kolom `[tahun = 2024]` secara statis membaca nama direktori/file folder induknya `(../../2024/...)`.
3.  **Data Type Casting & Sanitasi**: Menghapus tanda desimal eropa koma `,` di metrik Load Factor.

### 2.3 Canonical Schema Target (Struktur DW Akhir)
Desain ujung *Target Schema* ke Cloud DW / Tableau Extract:
*   `sk_fact_stat_rute_id` (PK, Surrogate Integer)
*   `sk_rute_id` (FK -> Koneksi ke Tabel Dimensi `dim_rute` hasil cleansing BAB 3)
*   `tahun_observasi` (Integer, cth. 2024. Hasil Injeksi statis)
*   `tipe_rute` (Enum Label: 'Dalam Negeri' | 'Luar Negeri')
*   `total_flight_departure` (Integer / Jumlah Penerbangan)
*   `total_pax_carried` (Integer)
*   `total_seat_capacity` (Integer)
*   `total_cargo_logistics_kg` (Float/Integer)
*   `total_pos_mail_kg` (Float/Integer)
*   `load_factor_pax_percentage` (Float/Decimal) 
