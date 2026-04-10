# README - PDF to CSV Extraction

## Deskripsi

Dokumen ini berisi hasil ekstraksi data dari 4 file PDF statistik angkutan udara niaga berjadwal tahun 2024 ke format CSV.

**Sumber**: Buku Statistik Angkutan Udara Tahun 2024  
**Bab**: BAB VI — Penumpang Per Rute  
**Tahun Data**: 2024

---

## File yang Diproses

### 1. JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI JAN-DES 2024

| Properti | Nilai |
|----------|-------|
| **PDF Pages** | 6 halaman |
| **Total Rows** | 315 (314 routes + 1 TOTAL) |
| **Kolom** | 15 |
| **Struktur Kolom** | `NO`, `RUTE PP`, `Jan-24` s/d `Dec-24`, `TOTAL 2024` |
| **Tipe Data** | NO: string, RUTE: string, Bulan: int64, TOTAL: int64 |
| **Output CSV** | `JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI JAN-DES 2024.csv` |

**Deskripsi**: Data bulanan jumlah penumpang untuk rute domestik (dalam negeri) dari Januari hingga Desember 2024.

---

### 2. STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2024 BERDASARKAN URUTAN JUMLAH PENUMPANG

| Properti | Nilai |
|----------|-------|
| **PDF Pages** | 6 halaman |
| **Total Rows** | 316 (315 routes + 1 TOTAL) |
| **Kolom** | 8 |
| **Struktur Kolom** | `NO`, `RUTE PP`, `JUMLAH PENERBANGAN`, `JUMLAH PENUMPANG`, `KAPASITAS SEAT`, `JUMLAH BARANG KG`, `JUMLAH POS KG`, `LF %` |
| **Tipe Data** | NO: string, RUTE: string, Numerik: int64, LF %: string |
| **Output CSV** | `STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2024 BERDASARKAN URUTAN JUMLAH PENUMPANG.csv` |

**Deskripsi**: Statistik tahunan rute domestik berdasarkan urutan jumlah penumpang, termasuk data penerbangan, kapasitas, barang, dan Load Factor (LF).

---

### 3. JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI BULAN JANUARI S.D DESEMBER TAHUN 2024

| Properti | Nilai |
|----------|-------|
| **PDF Pages** | 3 halaman |
| **Total Rows** | 135 (134 routes + 1 TOTAL) |
| **Kolom** | 15 |
| **Struktur Kolom** | `NO`, `RUTE PP`, `Jan-24` s/d `Dec-24`, `TOTAL 2024` |
| **Tipe Data** | NO: string, RUTE: string, Bulan: int64/float64, TOTAL: int64 |
| **Output CSV** | `JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI BULAN JANUARI S.D DESEMBER TAHUN 2024.csv` |

**Deskripsi**: Data bulanan jumlah penumpang untuk rute internasional (luar negeri) dari Januari hingga Desember 2024.

**Catatan**: 
- Routes 1-103: Rute utama dengan penumpang signifikan
- Routes 104-134: Rute tambahan dengan banyak nilai 0 (rute tidak aktif atau baru)

---

### 4. STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI TAHUN 2024 BERDASARKAN URUTAN JUMLAH PENUMPANG

| Properti | Nilai |
|----------|-------|
| **PDF Pages** | 3 halaman |
| **Total Rows** | 135 (134 routes + 1 TOTAL) |
| **Kolom** | 8 |
| **Struktur Kolom** | `NO`, `RUTE PP`, `JUMLAH PENERBANGAN`, `JUMLAH PENUMPANG`, `KAPASITAS SEAT`, `JUMLAH BARANG KG`, `JUMLAH POS KG`, `LF %` |
| **Tipe Data** | NO: string, RUTE: string, Numerik: int64, LF %: string |
| **Output CSV** | `STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI TAHUN 2024 BERDASARKAN URUTAN JUMLAH PENUMPANG.csv` |

**Deskripsi**: Statistik tahunan rute internasional berdasarkan urutan jumlah penumpang.

---

## Data Cleaning yang Dilakukan

### 1. Number Cleaning
- **Titik ribuan dihapus**: `"1.579.052"` → `1579052` (integer)
- **Spasi dalam angka**: Tidak ditemukan anomali signifikan
- **Desimal koma**: Tidak ada (format Indonesia menggunakan titik)

### 2. Header Normalization
- **Multi-line headers dijoin**: 
  - `"JUMLAH\nPENERBANGAN"` → `"JUMLAH PENERBANGAN"`
  - `"JUMLAH\nPENUMPANG"` → `"JUMLAH PENUMPANG"`
  - `"KAPASITAS\nSEAT"` → `"KAPASITAS SEAT"`
  - `"JUMLAH\nBARANG KG"` → `"JUMLAH BARANG KG"`
  - `"JUMLAH\nPOS KG"` → `"JUMLAH POS KG"`

### 3. Typo Correction
- **File 3 (Luar Negeri Bulanan)**: `'OTAL'` → `'TOTAL'` di baris TOTAL

### 4. Null/Empty Values
- **Kolom RUTE PP pada baris TOTAL**: `None` → `NaN` (kosong di CSV)
- **Sel kosong**: Dibiarkan kosong atau `0` sesuai data asli

### 5. Percentage Handling
- **Kolom LF %**: Dibiarkan sebagai string dengan `%` (contoh: `"87%"`)
- **Nilai anomali**: `#DIV/0!` dibiarkan sebagaimana aslinya (kalkulasi error di PDF asli)

### 6. Whitespace Trimming
- Semua string values di-trim untuk menghapus whitespace berlebih

---

## Anomali yang Ditemukan dan Penanganan

| No | Anomali | File | Penanganan |
|----|---------|------|------------|
| 1 | Multi-line headers | File 2 & 4 | ✅ Join dengan space |
| 2 | Typo 'OTAL' | File 3 | ✅ Replace ke 'TOTAL' |
| 3 | Backslash di route `'DEL-DPS\\'` | File 4 | ✅ Dibiarkan sebagaimana aslinya |
| 4 | Nilai `#DIV/0!` di LF % | File 2 & 4 | ✅ Keep as string (error dari PDF) |
| 5 | Routes dengan semua nilai 0 | File 3 & 4 | ✅ Include (data valid tapi tidak aktif) |
| 6 | Float64 di beberapa kolom bulan | File 3 | ✅ Accept (ada `.0` karena parsing) |
| 7 | None di RUTE PP baris TOTAL | Semua | ✅ Convert ke NaN/empty |

---

## Struktur Output CSV

- **Encoding**: UTF-8 with BOM (`utf-8-sig`) untuk kompatibilitas Excel
- **Delimiter**: Koma (`,`)
- **Line Terminator**: `\n` (Unix-style)
- **Quote Character**: `"` (default)
- **Null Representation**: Kosong atau `NaN`

---

## Script yang Digunakan

- **File**: `extract_pdf_to_csv.py`
- **Library**:
  - `pdfplumber` (v0.11.9) - Ekstraksi tabel dari PDF
  - `pandas` (v3.0.2) - Manipulasi data dan export CSV
  - Python standard library - File operations

---

## Ringkasan Total Data

| Kategori | Routes | TOTAL Row | Total Rows |
|----------|--------|-----------|------------|
| **Dalam Negeri - Bulanan** | 314 | 1 | 315 |
| **Dalam Negeri - Statistik** | 315 | 1 | 316 |
| **Luar Negeri - Bulanan** | 134 | 1 | 135 |
| **Luar Negeri - Statistik** | 134 | 1 | 135 |
| **TOTAL** | **897** | **4** | **901** |

---

## Verifikasi Output

Semua file CSV telah diverifikasi dengan:
- ✅ Shape sesuai ekspektasi
- ✅ Tidak ada header terduplikasi di tengah data
- ✅ Angka sudah bersih (tidak ada spasi/titik aneh)
- ✅ Baris TOTAL ter-include di setiap file
- ✅ Sample data (first 5 & last 5 rows) terlihat benar
- ✅ Encoding UTF-8-sig untuk kompatibilitas Excel

---

**Tanggal Ekstraksi**: April 8, 2026  
**Status**: ✅ **SELESAI & VERIFIED**
