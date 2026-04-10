# CSV Analysis: Jumlah Penumpang Per Rute — Internasional Bulanan 2022

## 📊 Informasi Umum

| Properti | Nilai |
|----------|-------|
| **Nama File** | `JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI BULAN JANUARI S.D DESEMBER TAHUN 2022.csv` |
| **Jumlah Baris** | 136 (1 header + 133 rute + 1 Total + 1 empty) |
| **Jumlah Kolom** | 15 |
| **Format Angka** | Float dengan titik sebagai pemisah ribuan |
| **Format Rute** | Hanya IATA code (`CGK-SIN`) |

---

## ⚠️ PERBEDAAN SANGAT SIGNIFIKAN vs 2020-2021

| Aspek | 2020 | 2021 | **2022** |
|-------|------|------|----------|
| **Jumlah Rute** | ~147 | ~145 | **133** |
| **Format Rute** | Nama + IATA | Nama + IATA | **Hanya IATA** ⚠️ |
| **Format Angka** | Float (.0) | Float (.0) | **Titik = ribuan** ⚠️ |
| **Nama Bulan** | Indonesia | Indonesia | **Inggris** |
| **Kolom Komparasi** | 2019, 2018 | 2020, 2019 | **Tidak ada** ⚠️ |
| **Jumlah Kolom** | 18 | 18 | **15** |

---

## 🗂️ Struktur Tabel

```
NO (float)
RUTE ( PP) (string - IATA only)
Jan-22, Feb-22, ..., Dec-22 (float - titik = ribuan)
TOTAL 2022 (float)
```

### Top Routes 2022

| Rank | Rute | Penumpang 2022 |
|------|------|----------------|
| 1 | CGK-SIN | 1,705,435 |
| 2 | SIN-DPS | 1,205,738 |
| 3 | CGK-KUL | 816,674 |
| 4 | CGK-JED | 637,181 |
| 5 | KUL-DPS | 541,398 |

### Total Row
- **Total Penumpang 2022:** 12,298,746

---

## ⚠️ Potensi Masalah & Saran

### 1. Format Angka dengan Titik sebagai Pemisah Ribuan
- **Contoh:** `35.788` = 35,788 (bukan 35.788)
- **Saran:** Parse string → hapus titik → convert ke integer

### 2. Format Rute Hanya IATA Code
- **Contoh:** `CGK-SIN` vs `Jakarta (CGK)-SINGAPURA (SIN)`
- **Saran:** Mapping table

### 3. Nama Kolom Bulan Bahasa Inggris
- **Saran:** Standardisasi `m01_2022`, `m02_2022`, ...

### 4. Tidak Ada Kolom Komparasi
- **Saran:** Join di database

### 5. Missing Value & Rute Baru/Tidak Aktif
- Banyak rute yang kosong di beberapa bulan
- **Saran:** Replace dengan `NULL`

### 6. Baris Total Tanpa Label
- **Saran:** Flag `is_total_row`

---

## 🎯 Kesimpulan

### Masalah Kritikal
1. ✅ Format angka titik = pemisah ribuan
2. ✅ Format rute hanya IATA code
3. ✅ Nama bulan Bahasa Inggris
4. ✅ Tidak ada kolom komparasi
5. ✅ Missing value
6. ✅ Baris Total

### Metadata

| Properti | Nilai |
|----------|-------|
| **Jumlah Rute** | 133 |
| **Total Penumpang 2022** | 12,298,746 |
| **Growth vs 2021** | ↑ +801% (recovery besar) |
| **Format Khusus** | Titik = pemisah ribuan |

---

> **Catatan:** Dokumen ini hanya fokus pada file Internasional Bulanan 2022.
