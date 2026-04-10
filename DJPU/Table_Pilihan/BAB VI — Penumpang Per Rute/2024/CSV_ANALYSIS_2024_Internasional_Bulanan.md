# CSV Analysis: Jumlah Penumpang Per Rute — Internasional Bulanan 2024

## 📊 Informasi Umum

| Properti | Nilai |
|----------|-------|
| **Nama File** | `JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI BULAN JANUARI S.D DESEMBER TAHUN 2024.csv` |
| **Jumlah Baris** | 137 (1 header + 134 rute + 1 Total + 1 empty) |
| **Jumlah Kolom** | 15 |
| **Format Rute** | Hanya IATA code (`CGK-SIN`) |
| **Format Angka** | Mix Integer dan Float `.0` (contoh: `295204`, `285735.0`) |
| **Nama Bulan** | Bahasa Indonesia (`Jan-24`, `Mei-24`, `Agu-24`, `Okt-24`, `Des-24`) |

---

## ⚠️ PERBEDAAN vs 2020-2023

| Aspek | 2020 | 2021 | 2022 | 2023 | **2024** |
|-------|------|------|------|------|----------|
| **Jumlah Rute** | ~147 | ~145 | 133 | 125 | **134** |
| **Format Rute** | Nama + IATA | Nama + IATA | IATA only | IATA only | **IATA only** |
| **Format Angka** | Float (.0) | Float (.0) | Titik = ribuan | Float (.0) | **Mix Integer + Float** |
| **Nama Bulan** | Inggris | Indonesia | Inggris | Indonesia | **Indonesia** |
| **Kolom Komparasi** | 2019, 2018 | 2020, 2019 | Tidak ada | Tidak ada | **Tidak ada** |

---

## 🗂️ Struktur Tabel

```
NO (int)
RUTE PP (string - IATA only)
Jan-24, Feb-24, ..., Des-24 (mix int/float)
TOTAL 2024 (int)
```

### Top Routes 2024

| Rank | Rute | Penumpang 2024 |
|------|------|----------------|
| 1 | CGK-SIN | 3,331,178 |
| 2 | DPS-SIN | 2,742,281 |
| 3 | CGK-KUL | 2,703,041 |
| 4 | DPS-KUL | 1,796,779 |
| 5 | CGK-JED | 1,143,776 |

### Total Row
- **Total Penumpang 2024:** 29,054,531 (dari footer)

---

## ⚠️ Potensi Masalah & Saran

### 1. Format Angka Tidak Konsisten (Mix Integer + Float)
- Beberapa nilai punya `.0` (`285735.0`), beberapa tidak (`295204`)
- **Saran:** Convert semua ke integer

### 2. Format Rute Hanya IATA Code
- **Saran:** Mapping table

### 3. Nama Kolom Bulan Bahasa Indonesia
- **Saran:** Standardisasi `m01_2024`, ...

### 4. Missing Value = `0` atau Sel Kosong
- **Saran:** Replace dengan `NULL`

### 5. Baris Total
- **Format:** `TOTAL,,162.122,...` (ada yang pakai titik sebagai ribuan?)
- **Saran:** Flag `is_total_row`

---

## 🎯 Kesimpulan

### Masalah Kritikal
1. ✅ Format angka tidak konsisten (mix integer + float)
2. ✅ Format rute hanya IATA
3. ✅ Nama bulan Indonesia
4. ✅ Missing value
5. ✅ Baris Total

### Metadata

| Properti | Nilai |
|----------|-------|
| **Jumlah Rute** | 134 |
| **Total Penumpang 2024** | ~29M |
| **Growth vs 2023** | ↓ (perlu verifikasi) |
| **Format** | Mix integer/float, IATA only, bulan Indonesia |

---

> **Catatan:** Dokumen ini hanya fokus pada file Internasional Bulanan 2024.
