# PDF to CSV Extraction - Penumpang Per Rute 2021

## Deskripsi

Proyek ini melakukan ekstraksi data dari 4 file PDF statistik penumpang per rute angkutan udara niaga berjadwal tahun 2021 ke format CSV yang siap dianalisis.

Data berasal dari laporan statistik penerbangan Indonesia tahun 2021, mencakup:
- **Penerbangan Domestik (Dalam Negeri)**: Rute-rute innerhalb Indonesia
- **Penerbangan Internasional (Luar Negeri)**: Rute-rute dari Indonesia ke luar negeri

Setiap kategori memiliki 2 jenis laporan:
1. **Jumlah Penumpang per Bulan**: Breakdown bulanan Januari-Desember 2021, dengan perbandingan total tahun 2019-2020
2. **Statistik Lengkap**: Data agregat tahunan meliputi jumlah penerbangan, penumpang, kapasitas seat, barang, pos, dan load factor

---

## Ringkasan File

### 1. Domestik - Bulanan (Jan-Des 2021)

| Properti | Nilai |
|----------|-------|
| **File PDF** | JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI JAN-DES 2021.pdf |
| **File CSV** | JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI JAN-DES 2021.csv |
| **Halaman** | 7 |
| **Total Baris** | 379 (378 rute + 1 Total) |
| **Jumlah Kolom** | 17 |

**Struktur Kolom:**
| Kolom | Tipe | Keterangan |
|-------|------|------------|
| NO | Integer | Nomor urut (1-378) |
| RUTE ( PP) | String | Rute penerbangan (format: `Kota Asal (KODE) - Kota Tujuan (KODE)`) |
| Jan-21 s/d Des-21 | Integer | Jumlah penumpang per bulan |
| TOTAL 2021 | Integer | Total penumpang tahun 2021 |
| TOTAL 2020 | Integer | Total penumpang tahun 2020 (perbandingan) |
| TOTAL 2019 | Integer | Total penumpang tahun 2019 (pre-pandemi) |

---

### 2. Internasional - Bulanan (Jan-Des 2021)

| Properti | Nilai |
|----------|-------|
| **File PDF** | JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI BULAN JANUARI S.D DESEMBER TAHUN 2021.pdf |
| **File CSV** | JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI BULAN JANUARI S.D DESEMBER TAHUN 2021.csv |
| **Halaman** | 3 |
| **Total Baris** | 146 (145 rute + 1 Total) |
| **Jumlah Kolom** | 17 |

**Struktur Kolom:**
| Kolom | Tipe | Keterangan |
|-------|------|------------|
| NO | Integer | Nomor urut (1-145) |
| RUTE | String | Rute penerbangan (format: `Kota Asal (KODE) - Kota Tujuan (KODE)`) |
| Jan-21 s/d Des-21 | Integer | Jumlah penumpang per bulan |
| TOTAL 2021 | Integer | Total penumpang tahun 2021 |
| TOTAL 2020 | Integer | Total penumpang tahun 2020 |
| TOTAL 2019 | Integer | Total penumpang tahun 2019 |

---

### 3. Domestik - Statistik (Urut Jumlah Penumpang)

| Properti | Nilai |
|----------|-------|
| **File PDF** | STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2021 BERDASARKAN URUTAN JUMLAH PENUMPANG.pdf |
| **File CSV** | STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2021 BERDASARKAN URUTAN JUMLAH PENUMPANG.csv |
| **Halaman** | 9 |
| **Total Baris** | 379 (378 rute + 1 Total) |
| **Jumlah Kolom** | 8 |

**Struktur Kolom:**
| Kolom | Tipe | Keterangan |
|-------|------|------------|
| NO | Integer | Nomor urut (1-378), diurutkan berdasarkan jumlah penumpang |
| RUTE ( PP) | String | Rute penerbangan |
| JUMLAH PENERBANGAN | Integer | Total penerbangan sepanjang 2021 |
| JUMLAH PENUMPANG | Integer | Total penumpang sepanjang 2021 |
| KAPASITAS SEAT | Integer | Total kapasitas tempat duduk |
| JUMLAH BARANG (Kg) | Integer | Total berat barang/kargo (kilogram) |
| JUMLAH POS | Integer | Total berat pos (kilogram) |
| L/F | String | Load Factor dalam persentase (format: `67,3%`) |

---

### 4. Internasional - Statistik (Urut Jumlah Penumpang)

| Properti | Nilai |
|----------|-------|
| **File PDF** | STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI TAHUN 2021 BERDASARKAN URUTAN JUMLAH PENUMPANG.pdf |
| **File CSV** | STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI TAHUN 2021 BERDASARKAN URUTAN JUMLAH PENUMPANG.csv |
| **Halaman** | 3 |
| **Total Baris** | 146 (145 rute + 1 Total) |
| **Jumlah Kolom** | 8 |

**Struktur Kolom:**
| Kolom | Tipe | Keterangan |
|-------|------|------------|
| NO | Integer | Nomor urut (1-145), diurutkan berdasarkan jumlah penumpang |
| RUTE | String | Rute penerbangan |
| JUMLAH PENERBANGAN | Integer | Total penerbangan sepanjang 2021 |
| JUMLAH PENUMPANG | Integer | Total penumpang sepanjang 2021 |
| KAPASITAS SEAT | Integer | Total kapasitas tempat duduk |
| JUMLAH BARANG | Integer | Total berat barang/kargo (satuan tidak disebutkan) |
| JUMLAH POS | Integer | Total berat pos |
| L/F | String | Load Factor dalam persentase (format: `20,7%`) |

---

## Catatan Data Cleaning

### 1. Angka dengan Spasi Errant
**Masalah:** PDF memiliki artifact spasi di tengah angka akibat formatting.
- Contoh: `"7 6.081"` seharusnya `76.081`
- Contoh: `"2 .002.789"` seharusnya `2.002.789`

**Solusi:** 
1. Hapus semua spasi dalam string angka
2. Hapus titik (pemisah ribuan)
3. Konversi ke integer

### 2. Multi-line Headers
**Masalah:** Header di file STATISTIK terpecah menjadi 2 baris dengan newline (`\n`).
- Contoh: `"JUMLAH\nPENERBANGAN"` → `"JUMLAH PENERBANGAN"`

**Solusi:** Replace `\n` dengan space.

### 3. Header Berulang
**Masalah:** Header kolom muncul di setiap halaman PDF.

**Solusi:** Gunakan header dari halaman pertama, skip header row di halaman selanjutnya.

### 4. Nilai Null / Kosong
**Masalah:** Rute yang tidak beroperasi memiliki nilai `"-"` (dash).

**Solusi:** Konversi ke `NaN` (empty cell di CSV).

### 5. Load Factor Format
**Masalah:** Load factor menggunakan koma sebagai desimal (format Indonesia).
- Contoh: `"67,3%"`

**Solusi:** Dibiarkan sebagai string untuk mempertahankan format persentase.

### 6. Baris Total
**Masalah:** Baris agregat "Total" di akhir setiap PDF memiliki kolom rute kosong.

**Solusi:** Pertahankan baris Total, biarkan kolom rute kosong (NaN).

---

## Anomali yang Ditemukan

| No | Anomali | File | Penanganan |
|----|---------|------|------------|
| 1 | **Spasi errant dalam angka** | Semua PDF | ✅ Ditangani: Hapus spasi + titik ribuan |
| 2 | **Multi-line headers** | File STATISTIK (2 file) | ✅ Ditangani: Join dengan space |
| 3 | **Header berulang per halaman** | Semua PDF | ✅ Ditangani: Skip di halaman 2+ |
| 4 | **Rute tidak aktif (semua NaN)** | Semua PDF | ✅ Dipertahankan sebagai data valid |
| 5 | **Baris Total dengan route kosong** | Semua PDF | ✅ Dipertahankan untuk agregasi |
| 6 | **Perbedaan nama kolom rute** | Domestik: `RUTE ( PP)`, Internasional: `RUTE` | ✅ Dinormalisasi sesuai sumber |
| 7 | **JUMLAH BARANG dengan/satuan** | Domestik: `(Kg)`, Internasional: tanpa satuan | ✅ Dipertahankan sesuai sumber |

---

## Library yang Digunakan

- **pdfplumber**: Ekstraksi tabel dari PDF
- **pandas**: Manipulasi data dan export ke CSV
- **Python standard library**: File operations (`os`, `re`)

---

## Cara Menjalankan Ulang

```bash
cd "D:\Kuliah\projek_dw\Table_Pilihan\BAB VI — Penumpang Per Rute\2021"
python extract_pdf_to_csv.py
```

Script akan memproses ke-4 file PDF dan menghasilkan file CSV dengan nama yang sama (hanya ekstensi yang berubah).

---

## Output Files

| No | File CSV | Baris | Kolom | Encoding |
|----|----------|-------|-------|----------|
| 1 | JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI JAN-DES 2021.csv | 379 | 17 | UTF-8 with BOM |
| 2 | JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI BULAN JANUARI S.D DESEMBER TAHUN 2021.csv | 146 | 17 | UTF-8 with BOM |
| 3 | STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2021 BERDASARKAN URUTAN JUMLAH PENUMPANG.csv | 379 | 8 | UTF-8 with BOM |
| 4 | STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI TAHUN 2021 BERDASARKAN URUTAN JUMLAH PENUMPANG.csv | 146 | 8 | UTF-8 with BOM |

**Catatan:** Encoding UTF-8 with BOM (`utf-8-sig`) digunakan agar kompatibel dengan Excel.

---

## Total Data

| Kategori | Jumlah Rute | Periode |
|----------|-------------|---------|
| Domestik (Bulanan) | 378 rute | Jan-Des 2021 |
| Internasional (Bulanan) | 145 rute | Jan-Des 2021 |
| Domestik (Statistik) | 378 rute | Agregat 2021 |
| Internasional (Statistik) | 145 rute | Agregat 2021 |

**Grand Total:** 1.046 baris data rute + 4 baris Total = **1.050 baris**
