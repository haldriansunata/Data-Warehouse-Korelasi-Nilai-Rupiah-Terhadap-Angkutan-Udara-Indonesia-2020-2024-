# README - Ekstraksi Data Penumpang Angkutan Udara Niaga Berjadwal 2023

## Deskripsi

Proyek ini melakukan ekstraksi data dari 4 file PDF statistik penumpang angkutan udara niaga berjadwal tahun 2023 ke format CSV yang dapat dibaca dengan Excel.

Data berasal dari laporan resmi yang berisi:
- **Penumpang Domestik** (penerbangan dalam negeri)
- **Penumpang Luar Negeri** (penerbangan internasional)

Setiap kategori memiliki dua jenis tabel:
1. **Bulanan (Jan-Des)** - Data penumpang per bulan Januari sampai Desember
2. **Statistik Tahunan** - Agregat tahunan dengan detail penerbangan, penumpang, kapasitas, barang, pos, dan load factor

---

## File yang Diproses

| No | File PDF | Halaman | Baris Data | Kolom |
|----|----------|---------|------------|-------|
| 1 | JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI JAN-DES 2023.pdf | 12 | 304 | 15 |
| 2 | STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2023 BERDASARKAN URUTAN JUMLAH PENUMPANG.pdf | 6 | 304 | 8 |
| 3 | JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI BULAN JANUARI S.D DESEMBER TAHUN 2023.pdf | 6 | 126 | 15 |
| 4 | STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI TAHUN 2023 BERDASARKAN URUTAN JUMLAH PENUMPANG.pdf | 3 | 126 | 8 |

---

## Struktur Kolom

### File 1 & 3: Data Bulanan (Monthly)

| Kolom | Tipe | Deskripsi |
|-------|------|-----------|
| NO | String | Nomor urut rute |
| RUTE | String | Kode rute (contoh: CGK-DPS) |
| Jan-23 s/d Des-23 | Integer | Jumlah penumpang per bulan |
| TOTAL 2023 | Integer | Total penumpang setahun |

### File 2 & 4: Statistik Tahunan (Statistics)

| Kolom | Tipe | Deskripsi |
|-------|------|-----------|
| NO | String | Nomor urut atau "Total" |
| RUTE | String | Kode rute (contoh: CGK-SIN) |
| JUMLAH PENERBANGAN | Integer | Total penerbangan setahun |
| JUMLAH PENUMPANG | Integer | Total penumpang setahun |
| KAPASITAS SEAT | Integer | Total kapasitas kursi |
| JUMLAH BARANG | Integer | Total berat barang (Kg) |
| JUMLAH POS | Integer | Total berat pos (Kg) |
| L/F | String | Load Factor dalam persentase (contoh: 80,6%) |

---

## Data Cleaning yang Dilakukan

### 1. Number Cleaning
- **Menghapus spasi aneh**: PDF menghasilkan spasi di posisi tidak standar (contoh: `"3 .005.022"` → `3005022`)
- **Menghapus titik pemisah ribuan**: `"1.579.052"` → `1579052`
- **Konversi ke integer**: Semua kolom numerik dikonversi ke integer/float

### 2. Header Normalization
- **Join multi-line headers**: Header yang terpecah 2-3 baris digabung dengan spasi
  - Contoh: `"JUMLAH\nPENERBA\nNGAN"` → `"JUMLAH PENERBANGAN"`
  - Contoh: `"JUMLAH\nBARANG\n(Kg)"` → `"JUMLAH BARANG (Kg)"` → di-map ke `"JUMLAH BARANG"`
- **Standardisasi nama kolom**: Variasi header seperti `"RUTE ( PP)"` dinormalisasi menjadi `"RUTE"`

### 3. Null/Empty Values
- Tanda `"-"` atau sel kosong → dikonversi ke `NaN`
- Baris dengan rute tidak beroperasi → tetap disertakan dengan nilai NaN

### 4. Data Continuity
- **Merge halaman ganjil-genap**: File bulanan memiliki struktur terpisah (Jan-Jun di halaman ganjil, Jul-Des di halaman genap) yang digabung menjadi satu row per rute
- **Nomor urut berlanjut** antar halaman tanpa reset
- **Baris Total** di akhir setiap file tetap di-include

### 5. Encoding
- Semua file CSV menggunakan **UTF-8 with BOM** (`utf-8-sig`) untuk kompatibilitas Excel

---

## Anomali yang Ditemukan & Penanganan

| Anomali | File Terkena | Penanganan |
|---------|--------------|------------|
| Header berulang setiap halaman | Semua | Skip header di halaman selanjutnya, hanya ambil pertama |
| Multi-line headers (2-3 baris) | File 2, 4 | Join dengan spasi, lalu map ke nama standar |
| Spasi dalam angka (PDF artifact) | File 4 | Hapus semua spasi sebelum parse |
| Titik pemisah ribuan | Semua | Hapus titik, konversi ke integer |
| Sel kosong/`-` | Semua | Konversi ke NaN |
| Rute tidak beroperasi | Semua | Pertahankan baris, biarkan NaN |
| Baris Total | Semua | Pertahankan, kolom RUTE = NaN |
| Header tidak konsisten (`RUTE ( PP)` vs `RUTE`) | File 1, 2, 3 | Map ke nama standar |
| Tambahan `(Kg)` di header | File 2 | Di-map ke nama tanpa `(Kg)` |

---

## Output yang Dihasilkan

### File CSV
1. ✅ `JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI JAN-DES 2023.csv`
2. ✅ `STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2023 BERDASARKAN URUTAN JUMLAH PENUMPANG.csv`
3. ✅ `JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI BULAN JANUARI S.D DESEMBER TAHUN 2023.csv`
4. ✅ `STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI TAHUN 2023 BERDASARKAN URUTAN JUMLAH PENUMPANG.csv`

### File Dokumentasi
1. ✅ `ANALISA_STRUKTUR_TABEL.md` - Laporan detail struktur tabel
2. ✅ `README.md` - Dokumentasi ini

### Script Python
1. ✅ `extract_to_csv.py` - Script utama untuk ekstraksi
2. ✅ `analisa_struktur.py` - Script untuk analisa struktur PDF
3. ✅ `debug_statistik_domestik.py` - Script debug (bisa dihapus)
4. ✅ `debug_total_row.py` - Script debug (bisa dihapus)

---

## Cara Menggunakan

### Prasyarat
```bash
pip install pdfplumber pandas
```

### Menjalankan Ekstraksi
```bash
cd "D:\Kuliah\projek_dw\Table_Pilihan\BAB VI — Penumpang Per Rute\2023"
python extract_to_csv.py
```

### Membuka CSV di Excel
File CSV sudah menggunakan encoding UTF-8 BOM, sehingga bisa langsung dibuka di Excel tanpa masalah karakter:
- Klik dua kali file CSV, atau
- Di Excel: Data → From Text/CSV → Pilih file CSV → Load

---

## Ringkasan Statistik

### Domestik (File 1)
- **Total rute:** 303 + 1 baris Total
- **Rute tersibuk:** CGK-DPS (4.961.724 penumpang)
- **Total penumpang domestik 2023:** 65.925.924

### Statistik Domestik (File 2)
- **Total rute:** 303 + 1 baris Total
- **Total penerbangan:** 517.490
- **Load Factor rata-rata:** 80,2%

### Luar Negeri (File 3)
- **Total rute:** 125 + 1 baris Total
- **Rute tersibuk:** CGK-SIN (3.005.022 penumpang)
- **Total penumpang luar negeri 2023:** 29.054.531

### Statistik Luar Negeri (File 4)
- **Total rute:** 125 + 1 baris Total
- **Total penerbangan:** 176.909
- **Load Factor rata-rata:** 77,5%

---

## Catatan Tambahan

- Semua angka sudah dibersihkan dari artifact PDF
- Baris dengan data kosong (rute baru/tidak beroperasi) tetap disertakan untuk kelengkapan data
- File CSV dapat dibuka di Excel, Google Sheets, atau aplikasi spreadsheet lainnya
- Script dapat digunakan kembali untuk file PDF serupa dengan menyesuaikan konfigurasi

---

**Tanggal Ekstraksi:** April 2026
**Tools:** Python 3.x, pdfplumber, pandas
**Encoding:** UTF-8 with BOM
