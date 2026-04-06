
---

## Fase 2: Analisis Tabel & Konversi CSV (SEDANG BERLANGSUNG 🔄)

### Tujuan

Menganalisis struktur tabel dan data dari PDF hasil ekstraksi di folder *Table_Pilihan/*, kemudian mengonversinya ke format CSV.

### Kebutuhan Analisis

Sebelum membuat file CSV, lakukan analisis menyeluruh yang mencakup:

1. **Deteksi Judul Tabel**: Mengidentifikasi semua judul/header tabel yang ada di setiap PDF
2. **Analisis Struktur**:

   * Mendeteksi tabel yang berdampingan (satu judul tetapi dua tabel kiri-kanan)
   * Mengidentifikasi tabel dengan judul sama yang harus digabung/dilanjutkan
   * Mendeteksi tabel multi-halaman yang berlanjut antar halaman
3. **Analisis Kolom**:

   * Mengidentifikasi semua kolom di setiap tabel
   * Menangani format CSV/database yang tidak standar (data pemerintah bisa memiliki struktur tidak beraturan)
   * Mencatat sel yang digabung, header bertingkat, atau kolom hierarkis
4. **Analisis Tambahan**:

   * Tipe data di setiap kolom (string, angka, persentase, tanggal, dll.)
   * Penanganan sel kosong atau data yang hilang (kalau kosong biarkan kosong, dan biarkan apa adanya misal '-','0','0.0','0.0%', dan kemungkinan lainnya)
   * Identifikasi baris footer/total
   * Catatan atau anotasi dalam tabel

### Output yang Diharapkan

* **File CSV**: Satu file CSV untuk setiap tabel yang ditemukan dalam setiap PDF

  * Nama file CSV harus sesuai dengan judul tabel yang ditemukan saat analisis
  * Contoh: Jika PDF berisi *"DAFTAR BADAN USAHA ANGKUTAN UDARA NIAGA BERJADWAL TAHUN 2024"*, maka nama CSV harus **DAFTAR BADAN USAHA ANGKUTAN UDARA NIAGA BERJADWAL TAHUN 2024.csv**
  * Jika terdapat beberapa tabel dalam satu PDF, maka akan dihasilkan beberapa file CSV sesuai dengan judul tabel masing-masing
  * Karakter khusus dalam judul akan disesuaikan agar kompatibel dengan sistem file (misalnya: /, , : diganti dengan _)
* **Laporan analisis**: Mendokumentasikan struktur tabel, nama kolom, dan penanganan khusus yang diperlukan(seperti metode yang digunakan sesuai analisis)
* **Struktur folder terorganisir**: Mengikuti struktur BAB untuk memudahkan navigasi

### Konvensi Penamaan CSV

* Format: `{judul_tabel}.csv`
* Judul diambil langsung dari header/judul tabel dalam PDF
* Aturan penyesuaian:

  * Ganti karakter /, , :, *, ?, ", <, >, | dengan _
  * Hilangkan spasi berlebih
  * Pertahankan judul sedekat mungkin dengan aslinya agar tetap mudah dibaca

### Hal-hal Penting yang Perlu Diperhatikan

* **Konten campuran dalam PDF**: PDF tidak hanya berisi tabel. Bisa juga mencakup:

  * Paragraf penjelasan atau teks deskriptif
  * Header bagian yang bukan judul tabel
  * Catatan kaki, sumber data, atau anotasi
  * Grafik, diagram, atau pie chart (elemen visual, bukan data tabel)
  * Nomor halaman, header, atau footer
  * Analisis harus mampu membedakan antara data tabel dan konten non-tabel
  * PDF pemerintah mungkin memiliki format tabel yang tidak standar
  * Beberapa tabel bisa memiliki tata letak kompleks (sel gabungan, header bertingkat, tabel berdampingan)
  * Perlu memastikan integritas data dan pemetaan kolom yang tepat agar bisa dimasukkan ke database dengan benar

sehingga kemampuan script python + LLM kamu diperlukan disini jika ada anomali dengan script saja tidak cukup.
tolong bertindak seperti layaknya data engineer profesional. 