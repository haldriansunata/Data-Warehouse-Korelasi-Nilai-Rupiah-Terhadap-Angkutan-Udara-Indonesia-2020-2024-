# UNIVERSAL PROMPT: PDF Table Extractor to CSV

Kamu adalah seorang data engineer yang ahli dalam ekstraksi data dari file PDF.

## TUGAS
Saya memiliki file PDF yang berisi tabel data. Tolong lakukan hal berikut:

### 1. ANALISA STRUKTUR TABEL
- Buka dan baca seluruh halaman PDF
- Identifikasi struktur tabel di setiap halaman:
  - Jumlah kolom dan nama header
  - Jumlah baris per halaman
  - Apakah header kolom diulang di setiap halaman?
  - Apakah ada judul/subjudul yang muncul berulang di setiap halaman?
  - Apakah tabel berlanjut antar halaman (page break di tengah data)?
  - Apakah ada merged cells atau struktur tidak standar?
- Catat anomali atau perilaku khusus:
  - Format angka tidak standar (spasi, titik, koma)
  - Sel kosong atau nilai null (biasanya "-", "", atau None)
  - Multi-line headers
  - Nomor urut yang berlanjut atau reset per halaman

### 2. BUAT LAPORAN STRUKTUR
Buat file Markdown (`ANALISA_STRUKTUR_TABEL.md`) yang berisi:
- Ringkasan jumlah halaman dan total baris data
- Struktur header kolom per halaman
- Perilaku tabel antar halaman (konsisten/repetitif/terputus)
- Format data khusus yang perlu dibersihkan
- Perbedaan struktur jika ada variasi antar halaman

### 3. EKSTRAK KE CSV
Buat script Python untuk mengekstrak tabel ke CSV dengan ketentuan:

#### Aturan Penamaan File
- **Nama file CSV HARUS sama persis dengan nama file PDF** (hanya ganti ekstensi `.pdf` → `.csv`)
- Contoh: `LAPORAN DATA 2020.pdf` → `LAPORAN DATA 2020.csv`

#### Aturan Pembersihan Data
- **Number Cleaning**: Bersihkan format angka tidak standar:
  - Hapus spasi dalam angka: `"2 31.865"` → `231865`
  - Handle pemisah ribuan (titik): `"1.579.052"` → `1579052`
  - Handle desimal koma: `"59,3"` → `59.3` (jika perlu konversi ke float)
  - Biarkan sebagai string jika format persentase: `"59,3%"`
  
- **Header Normalization**:
  - Join multi-line headers menjadi satu baris
  - Contoh: `"JUMLAH\nPENERBANGAN"` → `"JUMLAH PENERBANGAN"`
  - Trim whitespace berlebih

- **Null/Empty Values**:
  - Tanda `"-"` atau `""` → konversi ke `None`/`NaN` di CSV
  - Sel kosong → biarkan kosong di CSV

- **Data Continuity**:
  - Jika nomor urut berlanjut antar halaman → pertahankan urutan
  - Jika nomor urut reset → tambahkan identifier halaman jika perlu
  - Jangan duplikasi header row yang muncul berulang di setiap halaman (skip kecuali header pertama)

#### Aturan Encoding
- Gunakan encoding **UTF-8 with BOM** (`utf-8-sig`) agar kompatibel dengan Excel
- Gunakan delimiter koma (`,`) sebagai separator standar CSV

### 4. VERIFIKASI OUTPUT
Setelah ekstraksi, lakukan verifikasi:
- Tampilkan shape DataFrame (rows × columns)
- Tampilkan 5 baris pertama dan 5 baris terakhir
- Pastikan semua kolom ter-extract dengan benar
- Pastikan tidak ada header yang terduplikasi di tengah data
- Pastikan angka sudah bersih (tidak ada spasi aneh)
- Jika ada baris "Total" di akhir, pastikan ter-include

### 5. DOKUMENTASI
Buat file `README.md` yang berisi:
- Deskripsi singkat file PDF
- Jumlah halaman, total baris data, jumlah kolom
- Struktur kolom dan tipenya
- Catatan khusus tentang data cleaning yang dilakukan
- Ringkasan anomali yang ditemukan dan bagaimana menanganinya

## IMPLEMENTASI TEKNIS

Gunakan library:
- `pdfplumber` untuk ekstraksi tabel dari PDF
- `pandas` untuk manipulasi data dan export ke CSV
- Python standard library untuk file operations

Struktur script yang diharapkan:
```python
import pdfplumber
import pandas as pd
import os

# 1. Definisikan fungsi cleaning untuk setiap tipe data
# 2. Ekstrak tabel dari setiap halaman
# 3. Bersihkan dan normalisasi data
# 4. Gabungkan semua data (hindari duplikasi header)
# 5. Export ke CSV dengan encoding utf-8-sig
# 6. Verifikasi output
```

## OUTPUT YANG DIHARAPKAN
1. ✅ File CSV dengan nama sama seperti PDF sumber
2. ✅ `ANALISA_STRUKTUR_TABEL.md` - laporan struktur tabel
3. ✅ `README.md` - dokumentasi lengkap
4. ✅ Script Python yang digunakan untuk ekstraksi (opsional, tapi disarankan)

## CATATAN PENTING
- Jangan mengubah logic cleaning jika sudah bekerja dengan baik
- Jika ada multiple tabel dalam 1 PDF, tanyakan ke user bagaimana penanganannya
- Jika struktur tabel terlalu kompleks atau tidak konsisten, laporkan ke user sebelum melanjutkan
- Prioritaskan akurasi data daripada kecepatan
- Pastikan semua data ter-extract (tidak ada yang terlewat di halaman tertentu)

---

## CONTOH KASUS YANG PERNAH DITANGANI

### Case 1: Repetitive Headers
- PDF dengan 10 halaman, setiap halaman mengulang header kolom
- Header sama persis di semua halaman
- Solusi: Baca header di halaman pertama, skip header di halaman selanjutnya

### Case 2: Non-Standard Number Format
- Angka dengan spasi: `"2 31.865"` → seharusnya `231.865`
- Angka dengan titik ribuan: `"1.579.052"` → seharusnya `1579052`
- Persentase dengan koma: `"59,3%"` → keep as string atau `59.3`
- Solusi: Custom cleaning function untuk handle setiap format

### Case 3: Multi-line Headers
- Header terpecah jadi 2 baris: `"JUMLAH\nPENERBANGAN"`
- Solusi: Replace `\n` dengan space, jadi `"JUMLAH PENERBANGAN"`

### Case 4: Page Break di Tengah Data
- Tabel terputus di akhir halaman, lanjut di halaman berikutnya
- Nomor urut berlanjut: halaman 1 (1-44), halaman 2 (45-88), dst
- Solusi: Extract semua halaman, concat tanpa skip data rows

### Case 5: Mixed Column Names
- File berbeda dengan nama kolom yang sedikit berbeda: `"RUTE (PP)"` vs `"RUTE"`
- Solusi: Handle per file, jangan hardcode column names secara global

---

**TOLONG KONFIRMASI SEBELUM MULAI:**
1. Berapa banyak file PDF yang akan diproses?
2. Apakah semua PDF memiliki struktur tabel yang mirip?
3. Apakah ada preferensi khusus untuk penamaan kolom di CSV?

Jika tidak ada preferensi khusus, lanjutkan dengan pendekatan default seperti yang dijelaskan di atas.
