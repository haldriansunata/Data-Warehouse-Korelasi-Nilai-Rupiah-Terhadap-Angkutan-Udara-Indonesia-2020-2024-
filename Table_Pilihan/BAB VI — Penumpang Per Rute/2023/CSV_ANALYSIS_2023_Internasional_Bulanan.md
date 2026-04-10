# CSV Analysis: Jumlah Penumpang Per Rute — Internasional Bulanan 2023

## 📊 Informasi Umum

| Properti | Nilai |
|----------|-------|
| **Nama File** | `JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI BULAN JANUARI S.D DESEMBER TAHUN 2023.csv` |
| **Jumlah Baris** | 128 (1 header + 125 rute + 1 Total + 1 empty) |
| **Jumlah Kolom** | 15 |
| **Format Rute** | Hanya IATA code (`CGK-SIN`) |
| **Format Angka** | Float dengan `.0` suffix |
| **Nama Bulan** | Bahasa Indonesia (`Mei`, `Jun`, `Jul`, `Agu`, `Sep`, `Okt`, `Nov`, `Des`) |

---

## ⚠️ PERBEDAAN vs 2020-2022

| Aspek | 2020 | 2021 | 2022 | **2023** |
|-------|------|------|------|----------|
| **Jumlah Rute** | ~147 | ~145 | 133 | **125** |
| **Format Rute** | Nama + IATA | Nama + IATA | IATA only | **IATA only** |
| **Format Angka** | Float (.0) | Float (.0) | Titik = ribuan | **Float (.0)** |
| **Nama Bulan** | Inggris | Indonesia | Inggris | **Indonesia** |
| **Kolom Komparasi** | 2019, 2018 | 2020, 2019 | Tidak ada | **Tidak ada** |
| **Jumlah Kolom** | 18 | 18 | 15 | **15** |

---

## 🗂️ Struktur Tabel

```
NO (int)
RUTE (string - IATA only)
Jan-23, Feb-23, ..., Des-23 (float)
TOTAL 2023 (float)
```

### Top Routes 2023

| Rank | Rute | Penumpang 2023 |
|------|------|----------------|
| 1 | CGK-SIN | 3,005,022 |
| 2 | SIN-DPS | 2,512,167 |
| 3 | CGK-KUL | 1,822,318 |
| 4 | KUL-DPS | 1,430,090 |
| 5 | MEL-DPS | 926,575 |

### Total Row
- **Total Penumpang 2023:** 29,054,531

---

## ⚠️ Potensi Masalah & Saran

### 1. Format Float dengan `.0`
- **Saran:** Remove `.0`, convert ke integer

### 2. Format Rute Hanya IATA Code
- **Saran:** Mapping table IATA → nama kota

### 3. Nama Kolom Bulan Bahasa Indonesia
- **Saran:** Standardisasi `m01_2023`, `m02_2023`, ...

### 4. Tidak Ada Kolom Komparasi
- **Saran:** Join di database

### 5. Jumlah Rute Berkurang
- 2022: 133 → 2023: **125** (↓ 8 rute)
- **Saran:** Track route lifecycle

### 6. Missing Value
- **Saran:** Replace dengan `NULL`

### 7. Baris Total dengan Label
- **Format:** `TOTAL,,1992455.0,...`
- **Saran:** Flag `is_total_row`

---

## 🎯 Kesimpulan

### Masalah Kritikal
1. ✅ Format float dengan `.0`
2. ✅ Format rute hanya IATA code
3. ✅ Nama bulan Bahasa Indonesia
4. ✅ Tidak ada kolom komparasi
5. ✅ Missing value
6. ✅ Baris Total

### Metadata

| Properti | Nilai |
|----------|-------|
| **Jumlah Rute** | 125 |
| **Total Penumpang 2023** | 29,054,531 |
| **Growth vs 2022** | ↑ +136.3% (recovery besar!) |
| **Format** | Float `.0`, IATA only, bulan Indonesia |

---

> **Catatan:** Dokumen ini hanya fokus pada file Internasional Bulanan 2023.
