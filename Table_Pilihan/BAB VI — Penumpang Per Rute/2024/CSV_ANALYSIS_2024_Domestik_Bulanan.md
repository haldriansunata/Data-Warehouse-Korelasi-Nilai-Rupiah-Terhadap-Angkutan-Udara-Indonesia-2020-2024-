# CSV Analysis: Jumlah Penumpang Per Rute — Domestik Bulanan 2024

## 📊 Informasi Umum

| Properti | Nilai |
|----------|-------|
| **Nama File** | `JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI JAN-DES 2024.csv` |
| **Jumlah Baris** | 317 (1 header + 314 rute + 1 Total + 1 empty) |
| **Jumlah Kolom** | 15 |
| **Format Rute** | Hanya IATA code (`CGK-DPS`) |
| **Format Angka** | **Integer** (tanpa `.0`!) |
| **Missing Value** | `0` atau sel kosong |
| **Nama Bulan** | Bahasa Indonesia (`Jan-24`, `Mei-24`, `Agu-24`, `Okt-24`, `Des-24`) |

---

## ⚠️ PERBEDAAN SANGAT SIGNIFIKAN vs 2020-2023

### 1. Format Angka Kembali ke Integer Murni (TANPA `.0`!)

| Tahun | Format Angka | Contoh |
|-------|--------------|--------|
| **2020** | Integer | `231865` |
| **2021** | Float dengan `.0` | `107991.0` |
| **2022** | Float dengan titik = ribuan | `324.111` |
| **2023** | Float dengan `.0` | `392247.0` |
| **2024** | **Integer murni** | `380993` |

**Perubahan lagi!** 2024 kembali ke integer murni tanpa `.0`.

### 2. Nama Kolom Rute Berubah!

| Tahun | Nama Kolom | Contoh |
|-------|-----------|--------|
| **2020** | `RUTE (PP)` | `Jakarta (CGK)-Denpasar (DPS)` |
| **2021** | `RUTE ( PP)` | `Jakarta (CGK) - Denpasar (DPS)` |
| **2022-2023** | `RUTE ( PP)` | `CGK-DPS` |
| **2024** | **`RUTE PP`** | `CGK-DPS` |

### 3. Jumlah Rute

| Tahun | Jumlah Rute Domestik |
|-------|---------------------|
| **2020** | 410 |
| **2021** | 379 |
| **2022** | 374 |
| **2023** | 303 |
| **2024** | **314** (bertambah 11 rute dari 2023!) |

### 4. Missing Value Menggunakan `0` (Bukan Sel Kosong!)

| Tahun | Format Missing Value |
|-------|---------------------|
| **2020-2023** | Sel kosong |
| **2024** | **`0`** (angka nol) |

**Contoh:** `MNA-NAH,237,283,322,54,0,202,52,0,0,0,0,0,1150`

---

## 🗂️ Struktur Tabel 2024

### Skema Saat Ini

```
NO (int)
RUTE PP (string - hanya IATA code)
Jan-24 (int)
Feb-24 (int)
Mar-24 (int)
Apr-24 (int)
May-24 (int)
Jun-24 (int)
Jul-24 (int)
Aug-24 (int)
Sep-24 (int)
Oct-24 (int)
Nov-24 (int)
Dec-24 (int)
TOTAL 2024 (int)
```

### Top Routes 2024

| Rank | Rute | Penumpang 2024 |
|------|------|----------------|
| 1 | CGK-DPS | 4,722,720 |
| 2 | CGK-SUB | 2,982,389 |
| 3 | CGK-KNO | 2,962,631 |
| 4 | CGK-UPG | 2,658,549 |
| 5 | BPN-CGK | 1,759,480 |

### Total Row
- **Total Penumpang 2024:** 65,795,595

---

## ⚠️ Potensi Masalah & Saran Pre-Processing

### 1. Format Integer Murni (TIDAK PERLU CONVERT!)
- **Saran:** Langsung baca sebagai integer, tidak perlu parsing khusus

### 2. Missing Value Menggunakan `0`
- **Masalah:** `0` bisa berarti tidak ada data ATAU memang 0 penumpang
- **Saran:** Replace `0` dengan `NULL` jika konteksnya missing

### 3. Format Rute Hanya IATA Code
- **Saran:** Mapping table IATA → nama kota

### 4. Nama Kolom `RUTE PP` (Tanpa Spasi & Kurung)
- **Saran:** Rename ke `route_pp` (snake_case)

### 5. Nama Bulan Bahasa Indonesia
- **Saran:** Standardisasi `m01_2024`, `m02_2024`, ...

### 6. Jumlah Rute Bertambah Lagi
- 2023: 303 → 2024: **314** (↑ 11 rute)
- **Saran:** Track route lifecycle

### 7. Baris Total dengan Label
- **Format:** `TOTAL,,497831,65795595,...`
- **Saran:** Flag `is_total_row`

---

## 📐 Rekomendasi Skema Database

**Sama seperti tahun sebelumnya — Long Format recommended.**

---

## 🎯 Kesimpulan & Next Steps

### Masalah Kritikal
1. ✅ Format integer murni (tidak perlu parsing)
2. ✅ Missing value = `0` (ganti ke `NULL`)
3. ✅ Format rute hanya IATA code
4. ✅ Nama kolom `RUTE PP`
5. ✅ Baris Total perlu flag

### Metadata

| Properti | Nilai |
|----------|-------|
| **Jumlah Rute** | 314 |
| **Total Penumpang 2024** | 65,795,595 |
| **Growth vs 2023** | ↓ -0.2% (stabil) |
| **Format** | Integer, IATA only, bulan Indonesia, missing = `0` |

---

> **Catatan:** Dokumen ini hanya fokus pada file Domestik Bulanan 2024. Format angka kembali ke integer murni setelah 2021-2023 pakai float.
