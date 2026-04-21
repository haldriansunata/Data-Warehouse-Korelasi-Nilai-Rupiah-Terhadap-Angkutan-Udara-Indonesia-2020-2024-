# Analisis Struktur Data BAB III - Rute Angkutan Udara (2020-2024)

Dokumen ini merangkum hasil analisis profil data (*Data Profiling*) untuk target file CSV pada BAB III. Analisis ini difokuskan pada tabel master **Rute Angkutan Udara Niaga Berjadwal Dalam Negeri** dan **Luar Negeri** untuk periode 2020 hingga 2024. Dokumen ini bertujuan untuk memberikan pedoman dan *action items* bagi proses ETL.

## 1. Analisis Evolusi Skema Data (Schema Drift)

Terdapat perubahan mendasar pada struktur fisik kolom seiring berjalannya tahun, di mana desain skema bergeser dari format rute terpisah (Asal dan Tujuan) menjadi format rute tergabung. Perlakuan ini mutlak ada baik di kelompok wilayah Domestik maupun Internasional.

### 1.1 Pola Kolom Tiap Tahun
*   **Tahun 2020 & 2021 (Format Terpisah)**: 3 Kolom (`NO`, `RUTE (ASAL)`, `RUTE (TUJUAN)`)
*   **Tahun 2022 (Format Transisi)**: 2 Kolom (`NO`, `RUTE (ASAL - TUJUAN)`) 
*   **Tahun 2023 & 2024 (Format Gabungan)**: 2 Kolom (`NO`, `RUTE (PP)`)

*Implikasi ETL (Penyatuan Tabel):* Normalisasi Schema mutlak dibutuhkan (memecah gabungan menjadi `rute_asal` dan `rute_tujuan` kembali).

---

## 2. Analisis Karakteristik Nilai & Anomali Rute (*Value Profiling*)

*   **Pola Tahun Terpisah (2020-2021):** Terdapat SPASI sebelum kode IATA. Contoh: `Jakarta (CGK)`
*   **Pola Tahun Gabungan (2022-2024):** TIDAK ADA SPASI sebelum kurung, separator utamanya baku `" - "`. Contoh: `Dhoho(DHX) - Balikpapan(BPN)`

*Implikasi ETL:* Perlu Regex Replace Standardisasi: `text.replace("(", " (")` ke seluruh string untuk menyinkronkan Dimensi Location antara tahun format lama dan baru.

---

## 3. Data Warehouse Modeling (Target Arsitektur ETL)

Pada fase *Dimensional Modeling*, informasi di BAB III ini murni berisikan rujukan entitas (bukan tabel metrik observasi harian/bulanan). Oleh karena itu, skema final pada DW akan ditempatkan sebagai **Dimension Table**. 

### 3.1 Klasifikasi: Dimension Table (`dim_rute` atau `dim_route`)
Karena data isinya hanya berupa "kamus" jalur penerbangan yang dilalui per tahunnya (tanpa jumlah muatan, penumpang, payload, dll), ini adalah *Dimension Table* murni.

### 3.2 Granularitas (Grain)
*   **Target Grain:** Satu baris data untuk satu **Pasangan Origin-Destination (O&D) unik** pada rute yang dilayani maskapai.
*   Karena datanya bersifat PP (Pulang-Pergi), pada implementasi DW yang canggih, `Rute(PP)` seringkali di-flatten menjadi dua baris rute 1 arah (`Directional`) e.g., Jakarta -> Bali dan Bali -> Jakarta. Hal ini mempermudah analisa trafik dari satu node bandara asal.

### 3.3 Draft Target Canonical Schema (Struktur Skema Final DW)
Setelah proses Cleansing & Splitting string, format tabel ini akan disatukan menjadi list referensi Rute DW Master:
*   `sk_rute_id` (Surrogate Key, mis. BIGINT)
*   `bandara_asal` (String/Label: misal "Jakarta (CGK)")
*   `kode_iata_asal` (Terekstrak dari dalam kurung e.g., "CGK" - Highly Recommended untuk integrasi Mapbox/Geospasial Tableau)
*   `bandara_tujuan` (String/Label: misal "Balikpapan (BPN)")
*   `kode_iata_tujuan` (Terekstrak: "BPN")
*   `tipe_rute` (Label: 'Dalam Negeri' atau 'Luar Negeri')
