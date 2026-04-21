# Analisis Struktur Data BAB VII - Lalu Lintas Bandara

Dokumen ini membedah analisis _Data Engineering_ untuk file CSV berukuran komprehensif pada kelompok BAB VII, yaitu: **`DATA LALU LINTAS ANGKUTAN UDARA DI BANDAR UDARA TAHUN 2020 - 2024.csv`**. Laporan ini memetakan kondisi fisik struktur CSV tersebut ke dalam pemodelan _Data Warehouse_ DW target.

## 1. Analisis Skema (*Structure Profiling*)

Tidak ada _Schema Drift_ di sini karena *resource* data ini dihimpun secara komprehensif di dalam **satu _single file_ vertikal**. Keseluruhan data dari tahun 2020 hingga 2024 (1281 baris) sudah dibaut secara _Long-Format_ secara natural dari sumbernya.

### 1.1 Profil Tipe Kolom & Fisik
*   **Total Kolom**: 22 Kolom (Sangat Lebar / _Wide-Metrics_).
*   **Header Kolom**: `propinsi_code`, `propinsi_name`, `airport_code`, `airport_name`, `year`, `pesawat_dtg`, `pesawat_brk`, `pesawat_total`, `penumpang_dtg`, `penumpang_brk`, `penumpang_total`, `penumpang_tra`, `bagasi_dtg`, `bagasi_brk`, `bagasi_total`, `barang_dtg`, `barang_brk`, `barang_total`, `pos_dtg`, `pos_brk`, `pos_total`, `keterangan`.
*   **Nilai Nulls**: Terdeteksi (*`has_nulls: true`*). Terutama pada maskapai kecil atau bandara perintis yang tidak mencatat metrik pergerakan khusus (seperti muatan pos/kargo logistik).

### 1.2 Anomali & Value Profiling (Tipe Data)
Analisis mendeteksi sebuah _Data Type Anomaly_ berskala besar:
Seluruh kolom yang berhubungan dengan lalu lintas komersial (`penumpang_dtg` sampai `pos_total`) dibaca oleh sistem sebagai **String / Teks**, bukan Numerik (*Float/Integer*).

**Penyebab (*Root Cause Criteria*):**
Angka yang disajikan menggunakan format _ribuan/desimal lokal Indonesia_ (contoh: pemisah ribuan berupa titik `1.000.000` dan desimal berupa koma `,`). Ada juga indikasi nilai kosong diisi dengan *dash* string (`"-"`), yang otomatis memaksa interpreter Python pandas membaca seluruh kolom sebagai rentetan huruf/string.

**Anomali Value Dimensi Tambahan (`keterangan`):**
Kolom keterangan mencatat periode bulan aktif perekaman. Valuenya memiliki format tipografi yang tidak konsisten: `Data 12 Bln`, `Data 12 Bulan`, `Data 12 bln`, `Data 5 bln`, `Data 10 Bln`.

---

## 2. Data Warehouse Modeling (Target Arsitektur ETL)

Berbeda dengan dataset bab lainnya, master data CSV pada BAB 7 ini sangat canggih dan bisa diikutsertakan ke dua elemen DW sekaligus (_Bridge_).

### 2.1 Klasifikasi 1: Pipeline untuk membuahkan `Dim_Bandara` (Dimension Table)
Tabel asli CSV ini mengandung empat variabel Master Referensi: `propinsi_code`, `propinsi_name`, `airport_code`, dan `airport_name`.

**CATATAN KRUSIAL ANOMALI (`airport_code`)**: Berdasarkan spesifikasi data internal, kolom `airport_code` ternyata **BUKAN** merujuk pada identitas unik kode bandara standar penerbangan IATA/ICAO (seperti CGK atau WIII), melainkan difungsikan sebatas sistem *index alphabet sequence* pengurutan (A, B, C...) yang berlaku per provinsi. 
Implikasinya: Kolom ini nilainya akan *reset*/berulang jika berganti provinsi. Oleh karena itu, nilai *airport_code* mentah dari tabel ini **TIDAK BISA** dan **TIDAK BOLEH** dijadikan *Primary Key* atau digunakan sebagai patokan untuk integrasi silang (Join) dengan dimensi rute di BAB lainnya.

Pada pipa ETL di Python Anda, proses pembentukan master `dim_bandara` disarankan hanya merekam gabungan `propinsi_name` dan `airport_name` untuk menentukan _uniqueness_.
*   _Target Canonical List:_ `[sk_bandara_id, nama_bandara, kode_propinsi, nama_propinsi]` *(Catatan: 'airport_code' sebatas index urutan A/B/C ini dapat Anda buang/Drop secara aman di fase Staging karena tidak membawa nilai semantik metadata yang berguna).*

### 2.2 Klasifikasi 2: Pipeline untuk menghasilkan `Fact_Lalu_Lintas_Bandara` (Fact Table)
Dataset utamanya diplot secara murni sebagai **Tabel Fakta Trafik Tahunan**.

*   **Granularitas (Grain):** Satu baris mencatat kumulatif performa kedatangan/keberangkatan (metrik penerbangan, metrik penumpang, bagasi, kargo, pos) **Per SATU bandara di SATU Tahun spesifik per SATU Kategori (Domestik/Internasional).**
*   **Target Canonical Fact Schema:**
    1.  `sk_lalu_lintas_id` (PK, Surrogate Key Integer)
    2.  `sk_dim_bandara_id` (FK -> menghubungkan ke `dim_bandara`)
    3.  `tahun_observasi` (Diambil langsung dari kolom `year`)
    4.  **`kategori`** (Text: 'DOMESTIK' atau 'INTERNASIONAL')
    *_Metrik Total:_
    5.  `total_flight_datang`, `total_flight_berangkat`, `komulatif_flight`
    6.  `total_pax_datang`, `total_pax_berangkat`, `komulatif_pax`, `pax_transit`
    7.  `bagasi_datang_kg`, `bagasi_berangkat_kg`, `komulatif_bagasi_kg`
    8.  `cargo_datang_kg`, `cargo_berangkat_kg`, `komulatif_cargo_kg`
    9.  `pos_datang_kg`, `pos_berangkat_kg`, `komulatif_pos_kg`
    *_Keterangan Tambahan:_
    10. `bulan_aktif_beroperasi` (Integer, cth: 12, 5, 10. Nilainya di ekstrak (_regex text digit_) dari kolom `keterangan`).

### 2.3 Transformasi Wajib pada Pipeline Parameter (Action-Plan)
1.  **Drop Reference Columns:** Setelah Dimensi Bandara (`dim_bandara`) berhasil diisolasi, hapus nama propinsi dan nama bandara dari Tabel Fakta ini. Cukup simpan _Foreign Key_ ID-nya saja untuk efisiensi kapastias DW.
2.  **Number Formatting Sanitization**: Operasikan kode `.str.replace('.', '')` pada seluruh metrik volume untuk menghapus titik desimal ribuan. Setelahnya, *replace* tanda `" - "` menjadi `0.0`. Terakhir, casting (_ubah tipe data_) kolom-kolom string tersebut menjadi _Integer_ atau _Float_ numerik murni.
3.  **Regex Extractor for Status Kolom**: Gunakan teknik _Regex_ (`\d+`) pada kolom `keterangan` untuk hanya mengekstrak nilai angkanya saja secara _pure_ independen (Sehingga `Data 12 Bln` / `Data 12 Bulan` lebur menunggal menjadi metrik baku integer `12`).
4.  **Ekstraksi Kategori (Resolusi Keputusan DWH K3): JAWABAN (A) Terdapat Split!** Pada file mentah, kelompok domestik dan internasional tersaji sebagai *baris terpisah*. Identifier kategorinya ditanam *(embedded)* pada akhiran teks nama bandara, misal: `"SULTAN ISKANDAR MUDA - BANDA ACEH (DOM)"` atau `"...(INT)"`. Anda WAJIB membuat parser di skrip Python:
    * Lakukan Regex untuk menarik teks dalam kurung di akhir karakter.
    * Lakukan mapping: `(DOM)`, `(DOMESTIK)`, atau String/Bandara tanpa Tagging diubah menjadi `'DOMESTIK'`.
    * Tag `(INT)`, `(INTERNASIONAL)` diubah menjadi `'INTERNASIONAL'`.
    * Kolom Kategori turunan mandiri ini selanjutnya ditetapkan ke *Fact Table*.
