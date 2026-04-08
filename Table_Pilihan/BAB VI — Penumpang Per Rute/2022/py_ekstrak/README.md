# PDF to CSV Extraction - Penumpang Per Rute Angkutan Udara 2022

## Deskripsi

Direktori ini berisi hasil ekstraksi data dari **4 file PDF** statistik penumpang per rute angkutan udara niaga berjadwal tahun 2022. Data berasal dari laporan resmi yang diterbitkan untuk tahun 2022.

## Sumber Data

Data berasal dari publikasi resmi statistik penerbangan Indonesia tahun 2022, yang mencakup:
- **Penerbangan Domestik** (Dalam Negeri): Rute antar kota di Indonesia
- **Penerbangan Internasional** (Luar Negeri): Rute dari/ke kota di luar negeri

## File yang Diproses

### 1. Penerbangan Domestik - Data Bulanan
- **PDF**: `JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI JAN-DES 2022.pdf`
- **CSV**: `JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI JAN-DES 2022.csv`
- **Deskripsi**: Jumlah penumpang per rute domestik untuk setiap bulan (Januari - Desember 2022)
- **Halaman**: ~9 halaman
- **Total Baris**: 375 rute (termasuk baris Total)
- **Jumlah Kolom**: 15 kolom

### 2. Penerbangan Domestik - Statistik Tahunan
- **PDF**: `STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2022 BERDASARKAN URUTAN JUMLAH PENUMPANG.pdf`
- **CSV**: `STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2022 BERDASARKAN URUTAN JUMLAH PENUMPANG.csv`
- **Deskripsi**: Statistik agregat penerbangan domestik tahun 2022 (penerbangan, penumpang, kapasitas, barang, pos, load factor)
- **Halaman**: ~9 halaman
- **Total Baris**: 375 rute (termasuk baris Total)
- **Jumlah Kolom**: 8 kolom

### 3. Penerbangan Internasional - Data Bulanan
- **PDF**: `JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI BULAN JANUARI S.D DESEMBER TAHUN 2022.pdf`
- **CSV**: `JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI BULAN JANUARI S.D DESEMBER TAHUN 2022.csv`
- **Deskripsi**: Jumlah penumpang per rute internasional untuk setiap bulan (Januari - Desember 2022)
- **Halaman**: ~3 halaman
- **Total Baris**: 134 rute (termasuk baris Total)
- **Jumlah Kolom**: 15 kolom

### 4. Penerbangan Internasional - Statistik Tahunan
- **PDF**: `STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI TAHUN 2022 BERDASARKAN URUTAN JUMLAH PENUMPANG.pdf`
- **CSV**: `STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI TAHUN 2022 BERDASARKAN URUTAN JUMLAH PENUMPANG.csv`
- **Deskripsi**: Statistik agregat penerbangan internasional tahun 2022
- **Halaman**: ~3 halaman
- **Total Baris**: 134 rute (termasuk baris Total)
- **Jumlah Kolom**: 8 kolom

---

## Struktur Kolom

### File Data Bulanan (15 Kolom)
| Kolom | Tipe | Deskripsi |
|-------|------|-----------|
| `NO` | Integer | Nomor urut rute |
| `RUTE ( PP)` | String | Kode rute pergi-pulang (contoh: CGK-DPS) |
| `Jan-22` s/d `Dec-22` | Float | Jumlah penumpang per bulan (dalam satuan penumpang) |
| `TOTAL 2022` | Float | Total penumpang selama tahun 2022 |

### File Statistik Tahunan (8 Kolom)
| Kolom | Tipe | Deskripsi |
|-------|------|-----------|
| `NO` | Integer | Nomor urut rute |
| `RUTE ( PP)` atau `RUTE` | String | Kode rute |
| `JUMLAH PENERBANGAN` | Float | Total jumlah penerbangan selama 2022 |
| `JUMLAH PENUMPANG` | Float | Total jumlah penumpang selama 2022 |
| `KAPASITAS SEAT` | Float | Total kapasitas kursi yang tersedia |
| `JUMLAH BARANG (Kg)` atau `JUMLAH BARANG` | Float | Total berat barang/kargo (dalam Kg) |
| `JUMLAH POS` | Float | Total jumlah pos yang diangkut |
| `L/F` | String | Load Factor dalam persentase (contoh: 77,7%) |

---

## Data Cleaning yang Dilakukan

### 1. Number Cleaning
- **Hapus spasi artifacts PDF**: Angka dengan spasi tidak standar dibersihkan
  - Contoh: `"2 31.865"` → `231865`
  - Contoh: `"4 8.418"` → `48418`
  
- **Konversi pemisah ribuan**: Titik sebagai pemisah ribuan dihapus
  - Contoh: `"1.579.052"` → `1579052`
  
- **Route column tidak di-cleaning**: Kolom rute (kolom ke-2) dibiarkan sebagai string karena berisi kode rute seperti "CGK-DPS"

### 2. Header Normalization
- **Join multi-line headers**: Header yang terpecah di beberapa baris digabung
  - Contoh: `"TOTAL 2022\n"` → `"TOTAL 2022"`
- **Trim whitespace**: Spasi berlebih di header dihapus

### 3. Null/Empty Values
- **Konversi nilai kosong**: `"-"`, `""`, atau sel kosong → `NaN` di CSV
- **Pertahankan baris Total**: Baris agregat "Total" di akhir tetap di-include meskipun kolom rute kosong

### 4. Data Continuity
- **Nomor urut berlanjut**: Urutan nomor dipertahankan antar halaman
- **Skip duplicate headers**: Header yang muncul berulang di setiap halaman tidak masuk ke data rows
- **Include Total row**: Baris agregat "Total" di akhir setiap file ter-include

---

## Anomali dan Penanganan

### ⚠️ Baris Total dengan Kolom Rute Kosong
- **Masalah**: Baris agregat "Total" di akhir setiap file memiliki kolom rute kosong (`NaN`)
- **Penanganan**: **EXPECTED** - Baris Total adalah agregat, bukan rute spesifik, sehingga kolom rute kosong adalah normal
- **Status**: ✅ Dipertahankan di CSV

### ⚠️ Rute Tanpa Data Bulanan
- **Masalah**: Beberapa rute di akhir file tidak memiliki data bulanan (hanya nomor urut dan nama rute)
- **Contoh**: Baris 370-373 di file domestik (HLP-CXP, SIQ-PKU, TSY-PCB, BPN-AAP)
- **Penanganan**: Nilai `NaN` di kolom bulan, tetap di-include sebagai rute yang ada namun tidak beroperasi/tidak ada data
- **Status**: ✅ Dipertahankan di CSV

### ⚠️ Kolom JUMLAH POS Banyak Nilai Kosong
- **Masalah**: Banyak rute tidak memiliki data JUMLAH POS
- **File Domestik**: 267 dari 375 baris (71%) kosong
- **File Internasional**: 97 dari 134 baris (72%) kosong
- **Penanganan**: Nilai `NaN` di CSV, menunjukkan data tidak tersedia atau tidak dilaporkan
- **Status**: ✅ Normal, data memang tidak tersedia

### ⚠️ Load Factor (L/F) Disimpan sebagai String
- **Masalah**: Kolom L/F berisi persentase dengan format `"77,7%"` yang tidak bisa dikonversi langsung ke float
- **Penanganan**: Disimpan sebagai string untuk mempertahankan format asli
- **Status**: ✅ Disengaja, bisa dikonversi nanti jika perlu analisis numerik

### ⚠️ Perbedaan Nama Kolom antar File
- **Masalah**: File statistik internasional menggunakan `"RUTE"` (bukan `"RUTE ( PP)"`) dan `"JUMLAH BARANG"` (bukan `"JUMLAH BARANG (Kg)"`)
- **Penanganan**: Nama kolom sesuai asli dari PDF, tidak dinormalisasi secara global
- **Status**: ✅ Sesuai sumber data

### ⚠️ PDF Artifacts dengan Spasi Tidak Standar
- **Masalah**: PDF menghasilkan spasi di posisi tidak standar dalam angka
  - Contoh: `"7 6.081"`, `"2 .002.789"`, `"4 8.418"`
- **Penanganan**: Hapus **semua** spasi terlebih dahulu, baru hapus titik (pemisah ribuan), lalu konversi ke integer
- **Status**: ✅ Sudah dibersihkan dengan custom cleaning function

---

## Encoding dan Format

- **Encoding**: UTF-8 with BOM (`utf-8-sig`) untuk kompatibilitas dengan Excel
- **Delimiter**: Koma (`,`) sebagai separator standar CSV
- **Line Ending**: Standar Windows (`\r\n`)
- **Null Representation**: Kosong di CSV (akan dibaca sebagai `NaN` oleh pandas)

---

## Tools dan Library

### Python Libraries
- **pdfplumber**: Ekstraksi tabel dari PDF
- **pandas**: Manipulasi data dan export ke CSV
- **Python standard library**: File operations (os, re, json)

### Script
- **File**: `extract_pdf_to_csv.py`
- **Fungsi utama**:
  - `clean_number()`: Membersihkan format angka dari artifacts PDF
  - `normalize_header()`: Normalisasi multi-line headers
  - `extract_tables_from_pdf()`: Ekstraksi tabel dari semua halaman
  - `process_dataframe()`: Cleaning dan konversi tipe data
  - `verify_output()`: Verifikasi hasil ekstraksi

---

## Cara Menggunakan

### Menjalankan Ulang Ekstraksi
```bash
cd "D:\Kuliah\projek_dw\Table_Pilihan\BAB VI — Penumpang Per Rute\2022"
python extract_pdf_to_csv.py
```

### Membaca CSV dengan pandas
```python
import pandas as pd

# Baca file domestik bulanan
df_domestik_bulanan = pd.read_csv(
    "JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI JAN-DES 2022.csv",
    encoding="utf-8-sig"
)

# Baca file statistik domestik
df_domestik_statistik = pd.read_csv(
    "STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2022 BERDASARKAN URUTAN JUMLAH PENUMPANG.csv",
    encoding="utf-8-sig"
)

# Konversi L/F ke float (hilangkan % dan ganti koma)
df_domestik_statistik['L/F_numeric'] = (
    df_domestik_statistik['L/F']
    .str.replace('%', '')
    .str.replace(',', '.')
    .astype(float)
)
```

---

## Dokumentasi Tambahan

- **ANALISA_STRUKTUR_TABEL.md**: Laporan detail struktur tabel untuk setiap file PDF
- **extract_pdf_to_csv.py**: Script Python yang digunakan untuk ekstraksi
- **structure_info.json**: File JSON metadata struktur (auto-generated oleh script)

---

## Tanggal Ekstraksi

**April 8, 2026**

---

## Kontak dan Referensi

Jika ada pertanyaan tentang data atau proses ekstraksi, silakan merujuk ke:
- File PDF sumber untuk verifikasi data asli
- `ANALISA_STRUKTUR_TABEL.md` untuk detail struktur per file
- Script `extract_pdf_to_csv.py` untuk implementasi teknis
