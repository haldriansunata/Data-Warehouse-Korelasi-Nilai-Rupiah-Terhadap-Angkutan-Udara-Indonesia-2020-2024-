# Komparasi Analisis Antar Dataset: BAB VI vs BAB VII
*(Jumlah Penumpang Per Rute vs Statistik Per Rute vs Data Lalu Lintas Bandara)*

Dokumen ini menyajikan analisis komparatif mendalam mengenai struktur, granularitas, dan semantik (makna bisnis) dari tiga entitas dataset logistik transportasi udara utama yang ada di sistem DJPU. Analisis ini sangat vital untuk mencegah kesalahan kalkulasi metrik (*double calculation bias*) pada saat merancang agregasi _Data Warehouse_ / Tableau.

---

## 1. Analisis Perbandingan Granularitas (Grain) & Struktur Kolom

Setiap tabel memiliki level agregasi (_Grain_) dan fokus dimensi yang berbeda, meskipun berbicara di ekosistem yang sama.

| Aspek Analisis | BAB VI: Jumlah Penumpang Per Rute | BAB VI: Statistik Per Rute | BAB VII: Lalu Lintas Bandara |
| :--- | :--- | :--- | :--- |
| **Fokus Observasi** | Koridor Jaringan Rute (*Network Edge/Link*) | Efisiensi Jaringan Rute (*Network Edge/Link*) | Titik Simpul Bandara (*Network Node*) |
| **Granularitas Waktu** | **Bulanan** (Time-Series _Jan-Des_) | **Tahunan** (1 agregat setahun penuh) | **Tahunan** (1 agregat setahun penuh) |
| **Granularitas Logis** | 1 Baris = 1 Rute (PP) per TAHUN | 1 Baris = 1 Rute (PP) per TAHUN | 1 Baris = 1 Bandara Fisik per TAHUN |
| **Bentuk Kolom (Pivot/Melt)** | **Waktu melebar (Pivot)**. (Ex: Kolom `Jan`, `Feb`, `Mar`) | **Metrik melebar**. (Ex: Kolom `Penerbangan`, `Seat`, `Pax`) | **Arah Tipe melebar**. (Ex: Kolom `dtg`, `brk`, `total`) |
| **Representasi Arah** | Agregat Dua Arah Tergabung (`PP`) | Agregat Dua Arah Tergabung (`PP`) | Memecah Arah (`Datang` vs `Berangkat`) |

---

## 2. Makna Bisnis & Perhitungan Numerik (*Business Semantics*)

Mendasarkan pada konteks domain Transportasi Niaga Udara, berikut adalah kaidah baca metriksnya:

### A. Konsep Pengabungan Arah di BAB VI (Format "RUTE PP")
Tabel Jumlah Penumpang dan Statistik Rute (BAB VI) menggunakan format pelaporan **Rute PP (Pulang-Pergi)**. 
*   **Makna:** Sebuah rute tertulis `CGK-DPS` adalah sebuah koridor selang pipa. Angka di tabel tersebut sudah **menggabungkan** (menjumlahkan) pesawat yang terbang dari Jakarta ke Bali (CGK -> DPS) **DITAMBAH** dengan laju yang terbang dari Bali kembali ke Jakarta (DPS -> CGK).
*   **Tujuan Mencegah Duplikasi:** DJPU tidak menuliskan list `CGK-DPS` lalu membuat baris baru `DPS-CGK` di bawahnya. Ini sengaja dirancang agar koridor ini tidak dihitung ganda (_double count_) di laporan nasional.

### B. Konsep "Jumlah Penumpang" (Frekuensi Transaksi vs Orang)
Angka yang tertera di seluruh report ini adalah **Volume Trafik Keterisian Kursi**, BUKAN melambangkan KTP Individu yang terbang.
*   **Perhitungan Bisnis:** Jika _Budi_ berangkat kerja ke Surabaya hari Senin, dan pulang ke Jakarta pada hari Jumat, si Budi akan menambah angka penyebut `JUMLAH PENUMPANG` sebanyak **2 pax**.
*   **Kapasitas Seat & LF% (Statistik Per Rute):** Tabel ini khusus mengukur "_Apakah rute ini jualan kursinya laku?_". `Load Factor (LF %)` lahir dari hitungan murni = `(JUMLAH PENUMPANG / KAPASITAS SEAT) * 100`.

### C. Konsep Simpul Spesifik di BAB VII (Datang & Berangkat)
Tabel Bandara membongkar arsitektur "PP" tadi dan berfokus pada apa yang terjadi secara fisik di tanah (infrastruktur aspal). 
*   **Makna:** Bandara diukur stresnya berdasarkan berapa roda yang **mendarat (_dtg_)** dan berapa yang **lepas landas (_brk_)**.

---

## 3. Sinergi Tabel: Bagaimana Mereka "Saling Melengkapi" di Data Warehouse?

Ketiga dataset ini tidak menindih satu sama lain, melainkan kepingan puzel yang meng-cover "kebutaan/blind-spot" dari dataset lainnya. Di dalam Tableau _Business Intelligence_ Anda nanti, sinergi ini akan tampak sebagai berikut:

*   **Tabel "Jumlah Penumpang (BAB VI)" adalah Pahlawan TIME-SERIES.**
    Hanya tabel inilah satu-satunya tempat Anda bisa membuat grafik **"Seasonality Trend"** (melihat lonjakan mudik Lebaran di bulan April/Mei atau Libur Nataru di Desember). Tabel lain buta terhadap tren waktu di bawah tahun.

*   **Tabel "Statistik Rute (BAB VI)" adalah Pahlawan EFFICIENCY.**
    Saat bisnis maskapai ingin menutup/menambah armada di suatu rute, mereka melihat tabel ini. Ini satu-satunya tabel yang bisa menjawab _"Meskipun penumpangnya banyak, apakah pesawat terbang setengah kosong (LF % rendah)?"_ dan membandingkan _Passenger Revenue_ vs _Cargo Logistics_.

*   **Tabel "Lalu Lintas Bandara (BAB VII)" adalah Pahlawan INFRASTRUCTURE HUB.**
    Tabel ini bertugas mengevaluasi utilitas Terminal Bandara. Anda bisa mendeteksi arah asimetris (_Asymmetric Flow_). 
    *Fakta Penting:* Jika Anda ingin tahu total kedatangan kota CGK, Anda **TIDAK BISA** dan **TIDAK BOLEH** menebak arah dengan membagi 2 (`Di Bagi / 2`) angka kumulatif "PP" dari tabel Rute BAB VI! Mengapa? Karena arus pesawat tidak selalu simetris (terkadang orang pergi dari Jakarta, namun baliknya tidak transit langsung, mengakibatkan _divergence_). Tabel Bandara (BAB VII) lah yang bertugas menjawab presisi jumlah ketimpangan Arus Datang vs Arus Berangkat tersebut murni dari catatan tower menara ATC.

### Kesimpulan Arsitektur (*The DW Blueprint*)
Ketiga tabel di atas pada Data Warehouse akan eksis secara damai dan direpresentasikan sebagai **3 Fact Table Terpisah** yang akan di-_slice_ oleh kesatuan dimensi yang sama (diapit oleh `Dim_Waktu`, `Dim_Bandara`, `Dim_Rute`). Anda tidak boleh memaksakan menggabungkan mereka (join rata mendatar / _flatten_) secara _horizontal_ karena *Granularitas Waktu & Ruang* yang mereka ukur sangat berbeda (Tahunan vs Bulanan, Simpul vs Garis Rute).
