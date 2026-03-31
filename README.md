# 📦 Perencanaan Data Warehouse
## Korelasi Nilai Rupiah Terhadap Angkutan Udara Indonesia (2020–2024)

---

## 1. Struktur Folder Data

```
D:\Kuliah\projek_dw\
│
├── KURS\
│   ├── BI.xlsx
│   └── FRED.csv
│
├── DJPU\
│   └── Statistik Angkutan Udara\
│       ├── Statistik_Angkutan_Udara_Tahun_2020.pdf
│       ├── Statistik_Angkutan_Udara_Tahun_2021.pdf
│       ├── Statistik_Angkutan_Udara_Tahun_2022.pdf
│       ├── Statistik_Angkutan_Udara_Tahun_2023.pdf
│       └── Statistik_Angkutan_Udara_Tahun_2024.pdf
│
└── BPS\
    ├── Lalu Lintas Penerbangan Dalam Negeri Indonesia Tahun 2003-2022\
    ├── Lalu Lintas Penerbangan Luar Negeri Indonesia Tahun 2003-2022\
    ├── Jumlah Penumpang Pesawat di Bandara Utama (Orang)\
    ├── Jumlah Penumpang Pada Keberangkatan di Bandara Indonesia (Ribu Orang), 2024\
    ├── Jumlah Penumpang Internasional berdasarkan Moda Transportasi Pesawat Terbang menurut provinsi (Orang)\
    ├── Jumlah Penumpang Domestik berdasarkan Moda Transportasi Pesawat Terbang menurut provinsi (Orang)\
    ├── BongkarMuat Barang Angkutan Udara Dalam Negeri di 5 Bandara Utama (Ton)\
    ├── BongkarMuat Barang Angkutan Udara Luar Negeri di 4 Bandara Utama (Ton)\
    ├── Jumlah Penumpang Pesawat (Angkutan Udara) Domestik di 5 Bandara Utama\
    └── Jumlah Penumpang Pesawat (Angkutan Udara) Internasional di 4 Bandara Utama (Orang)\
```

---

## 2. Inventaris Data

### 2.1 Data Kurs (KURS/)

| File | Sumber | Periode | Format Kolom |
|---|---|---|---|
| BI.xlsx | Bank Indonesia | 1 Jan 2020 – 31 Des 2024 | NO, Nilai, Kurs Jual, Kurs Beli, Tanggal |
| FRED.csv | FRED (St. Louis Fed) | 2020-01 – 2024-12 | observation_date, CCUSMA02IDQ618N |

> **Catatan:** BI.xlsx berisi data harian (kurs jual & beli). FRED.csv berisi rata-rata bulanan IDR/USD. Keduanya bisa digunakan bersama — BI untuk granularitas tinggi, FRED untuk agregasi bulanan.

---

### 2.2 Data BPS (BPS/)

| Nama Dataset | Periode Tersedia | Status | Catatan |
|---|---|---|---|
| Jumlah Penumpang Pesawat Domestik di 5 Bandara Utama | 2017–2026 | ✅ Lengkap | Bulanan |
| Jumlah Penumpang Pesawat Internasional di 4 Bandara Utama | 2017–2026 | ✅ Lengkap | Bulanan |
| BongkarMuat Barang Udara Dalam Negeri di 5 Bandara Utama | 2017–2026 | ✅ Lengkap | Bulanan, dalam Ton |
| BongkarMuat Barang Udara Luar Negeri di 4 Bandara Utama | 2018–2026 | ⚠️ Kurang 2020–2021 | Perlu estimasi atau skip |
| Jumlah Penumpang Domestik per Provinsi (Pesawat) | 2019–2023 | ⚠️ Kurang 2024 | Data tahunan per provinsi |
| Jumlah Penumpang Internasional per Provinsi (Pesawat) | 2019–2020 | ⚠️ Sangat terbatas | Hanya 2 tahun |
| Jumlah Penumpang Pesawat di Bandara Utama | 2006–2024 | ✅ Lengkap | Tahunan, historis panjang |
| Jumlah Penumpang Keberangkatan di Bandara Indonesia | s.d. 2024 | ✅ Lengkap | Tahunan |
| Lalu Lintas Penerbangan Dalam Negeri | 2003–2022 | ✅ 1 file | Tahunan, historis panjang |
| Lalu Lintas Penerbangan Luar Negeri | 2003–2022 | ✅ 1 file | Tahunan, historis panjang |

---

### 2.3 Data DJPU — Statistik Angkutan Udara (PDF, per Tahun)

Struktur bab konsisten di semua tahun (2020–2024):

| Bab | Konten | Relevansi DW | Target Tabel |
|---|---|---|---|
| I | Kerjasama bilateral / Air Service Agreement | ❌ Skip | — |
| II | Daftar maskapai berjadwal, tidak berjadwal, asing | ✅ Tinggi | `dim_maskapai` |
| III | Rute & kota terhubung dalam/luar negeri | ✅ Tinggi | `dim_rute`, `dim_bandara` |
| IV | Produksi per maskapai (penumpang, kargo, pesawat) | ✅ Tinggi | `fact_produksi_maskapai` |
| V | Market share penumpang per maskapai | ✅ Tinggi | `fact_market_share` |
| VI | Penumpang per rute per bulan (domestik & internasional) | ✅ **Utama** | `fact_penumpang_rute` |
| VII | Lalu lintas per bandara (pesawat, penumpang, kargo) | ✅ Tinggi | `fact_lalu_lintas_bandara` |
| VIII | Angkutan perintis | 🟡 Opsional | — |
| IX | Angkutan Lebaran | 🟡 Opsional | `dim_periode_khusus` |
| X | Angkutan Haji | 🟡 Opsional | `dim_periode_khusus` |
| XI | Angkutan Natal & Tahun Baru | 🟡 Opsional | `dim_periode_khusus` |
| XII | On Time Performance (OTP) per maskapai | ✅ Tinggi | `fact_otp` |

> **Catatan:** PDF 2024 (berlabel "Statistik Angkutan Udara 2025") memiliki struktur lebih detail di bab IX–XI (dilengkapi grafik per rute), namun isi inti sama.

---

## 3. Rancangan Tabel Data Warehouse

### Dimension Tables

| Tabel | Sumber Data | Kolom Utama |
|---|---|---|
| `dim_waktu` | Generate manual | tahun, bulan, kuartal, nama_bulan, is_periode_khusus |
| `dim_maskapai` | DJPU Bab II | kode_maskapai, nama_maskapai, tipe (nasional/asing), berjadwal (ya/tidak) |
| `dim_bandara` | DJPU Bab III & VII | kode_iata, nama_bandara, kota, provinsi, pengelola |
| `dim_rute` | DJPU Bab III & VI | origin, destination, jenis (domestik/internasional) |
| `dim_periode_khusus` | DJPU Bab IX–XI | nama_periode, tahun, tanggal_mulai, tanggal_selesai |

### Fact Tables

| Tabel | Sumber Data | Granularitas | Metrik Utama |
|---|---|---|---|
| `fact_kurs_rupiah` | BI.xlsx + FRED.csv | Bulanan | kurs_jual, kurs_beli, kurs_tengah, kurs_rata_usd |
| `fact_penumpang_rute` | DJPU Bab VI | Per rute per bulan | jumlah_penumpang, jenis_rute |
| `fact_lalu_lintas_bandara` | DJPU Bab VII + BPS | Per bandara per bulan | jml_pesawat, jml_penumpang, jml_kargo_ton |
| `fact_produksi_maskapai` | DJPU Bab IV | Per maskapai per tahun | penumpang_diangkut, kargo_ton, penerbangan |
| `fact_market_share` | DJPU Bab V | Per maskapai per tahun | persen_share_domestik, persen_share_internasional |
| `fact_otp` | DJPU Bab XII | Per maskapai per tahun | persen_otp |

---

## 4. Catatan Keterbatasan Data

| Dataset | Masalah | Solusi |
|---|---|---|
| BongkarMuat Luar Negeri (BPS) | Kurang data 2020–2021 | Gunakan data DJPU Bab VII sebagai pengganti |
| Penumpang Domestik per Provinsi | Kurang 2024 | Gunakan data 2019–2023 saja, atau interpolasi |
| Penumpang Internasional per Provinsi | Hanya 2019–2020 | Gunakan sebagai data pendukung saja, bukan fact utama |
| Lalu Lintas Penerbangan BPS | Hanya s.d. 2022 | Gabung dengan DJPU 2023–2024 untuk melengkapi |

---

## 5. Analisis & Kesimpulan

### Kekuatan Dataset Ini

Data yang terkumpul sudah sangat solid untuk menjawab pertanyaan utama proyek. Yang paling bernilai adalah kombinasi antara **data kurs harian dari BI** dan **data penumpang bulanan per rute dari DJPU** — dua dataset ini langsung bisa dikorelasikan setelah di-aggregate ke granularitas bulan. Ini inti dari analisis "korelasi nilai rupiah terhadap angkutan udara."

Data BPS memberikan konteks bulanan yang konsisten (2017–2026), artinya untuk periode 2020–2024 tidak ada gap. Sementara data DJPU dari PDF memberikan kedalaman yang tidak ada di BPS — yaitu breakdown per maskapai, per rute, dan OTP — yang membuat analisis jauh lebih kaya.

### Hal yang Perlu Diputuskan

**Soal dua sumber kurs (BI vs FRED):** Keduanya tidak perlu dipakai bersamaan. Untuk DW ini, **pakai FRED** sebagai sumber utama karena sudah dalam format bulanan dan konsisten. Data BI bisa disimpan sebagai referensi atau digunakan jika perlu granularitas harian.

**Soal data kargo luar negeri yang kurang 2020–2021:** Ini bisa diatasi dengan mengambil angka rekapitulasi dari DJPU Bab VII yang sudah mencakup periode tersebut. Tidak perlu khawatir — data tidak akan kosong.

**Soal penumpang per provinsi yang terbatas:** Dataset ini sebaiknya diposisikan sebagai dimensi pendukung, bukan fact utama. Analisis utama tetap berjalan dari data per bandara dan per rute.

### Risiko yang Perlu Diwaspadai

Satu hal yang belum ada adalah **denominasi harga tiket**. Tanpa data harga, korelasi yang bisa dibangun hanya antara kurs dan *volume* penumpang — bukan kurs dan *biaya terbang*. Ini sebenarnya masih valid secara analitik, tapi perlu dikomunikasikan dengan jelas dalam laporan bahwa fokus analisis adalah pada **permintaan** (demand), bukan keterjangkauan harga.

### Kesimpulan

Dataset yang sudah terkumpul **cukup dan siap** untuk masuk ke tahap desain star schema dan ETL. Tidak ada kebutuhan mencari data tambahan. Langkah selanjutnya yang paling logis adalah melihat sample aktual dari kolom-kolom di setiap file, lalu merancang skema final sebelum mulai proses transformasi data.

## ⚖️ Disclaimer & Data Attribution

Proyek ini dibuat murni untuk tujuan akademis, edukasi, dan portofolio pribadi. Seluruh hak cipta dan kekayaan intelektual dari data mentah yang digunakan dalam repositori ini tetap menjadi milik instansi pencipta data:
* **Badan Pusat Statistik (BPS) Indonesia**
* **Direktorat Jenderal Perhubungan Udara (DJPU) - Kementerian Perhubungan RI**
* **Bank Indonesia (BI)**
* **Federal Reserve Economic Data (FRED)**

Dokumen PDF dan dataset yang diunggah di dalam repositori ini semata-mata digunakan untuk mempermudah reproduksi proses ETL (Extract, Transform, Load) dalam proyek Data Warehouse ini. 

Jika Anda berniat menggunakan data ini untuk keperluan komersial, publikasi resmi, atau pengambilan keputusan nyata, sangat disarankan untuk merujuk dan mengunduh data terbaru langsung dari portal resmi instansi terkait. Penulis tidak bertanggung jawab atas ketidakakuratan data akibat proses ekstraksi dan transformasi.
