# CSV Analysis: Statistik Per Rute — Domestik Ranking 2024

## 📊 Informasi Umum

| Properti | Nilai |
|----------|-------|
| **Nama File** | `STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2024 BERDASARKAN URUTAN JUMLAH PENUMPANG.csv` |
| **Jumlah Baris** | 318 (1 header + 315 rute + 1 Total + 1 empty) |
| **Jumlah Kolom** | 8 |
| **Format Rute** | Hanya IATA code (`CGK-DPS`) |
| **Format Angka** | **Integer** (tanpa `.0`!) |
| **Load Factor** | String dengan `%` TANPA desimal, TANPA quotes (contoh: `87%`) |

---

## ⚠️ PERBEDAAN SANGAT SIGNIFIKAN vs 2020-2023

### 1. Format Load Factor SANGAT BERBEDA!

| Tahun | Format Load Factor | Contoh |
|-------|-------------------|--------|
| **2020-2022** | String dengan quotes + koma | `"80,6%"` |
| **2023** | String tanpa quotes + titik desimal | `80.6%` |
| **2024** | **String tanpa quotes + TANPA desimal + ada `#DIV/0!`** | `87%`, `0%`, `#DIV/0!` |

**Perubahan lagi!** Load Factor 2024:
- Tidak ada desimal (hanya angka bulat)
- Tidak ada quotes
- Ada nilai error `#DIV/0!` (Excel error!)

### 2. Nama Kolom Berubah!

| Tahun | Nama Kolom |
|-------|-----------|
| **2020-2023** | `L/F` |
| **2024** | **`LF %`** |

### 3. Nama Kolom Barang & Pos

| Tahun | Nama Kolom Barang | Nama Kolom Pos |
|-------|------------------|----------------|
| **2020-2023** | `JUMLAH BARANG` atau `JUMLAH BARANG (Kg)` | `JUMLAH POS` |
| **2024** | **`JUMLAH BARANG KG`** | **`JUMLAH POS KG`** |

### 4. Jumlah Rute

| Tahun | Jumlah Rute Domestik |
|-------|---------------------|
| **2020** | 410 |
| **2021** | 379 |
| **2022** | 374 |
| **2023** | 303 |
| **2024** | **315** (bertambah 12 dari 2023) |

---

## 🗂️ Struktur Tabel

### Skema Saat Ini

```
NO (int)
RUTE PP (string - IATA only)
JUMLAH PENERBANGAN (int)
JUMLAH PENUMPANG (int)
KAPASITAS SEAT (int)
JUMLAH BARANG KG (int)
JUMLAH POS KG (int)
LF % (string - integer + %, ada #DIV/0!)
```

### Top Routes 2024

| Rank | Rute | Penumpang | Penerbangan | LF |
|------|------|-----------|-------------|-----|
| 1 | CGK-DPS | 4,722,720 | 29,327 | 87% |
| 2 | CGK-SUB | 2,982,389 | 21,097 | 83% |
| 3 | CGK-KNO | 2,962,631 | 18,194 | 87% |
| 4 | CGK-UPG | 2,658,549 | 17,900 | 83% |
| 5 | BPN-CGK | 1,759,480 | 11,523 | 84% |

### Total Row
- **JUMLAH PENERBANGAN:** 497,831
- **JUMLAH PENUMPANG:** 65,795,595
- **KAPASITAS SEAT:** 79,903,253
- **JUMLAH BARANG KG:** 541,840,343 kg
- **JUMLAH POS KG:** 1,668,076 kg
- **LF Rata-rata:** 82%

---

## ⚠️ Potensi Masalah & Saran Pre-Processing

### 1. Format Load Factor BERUBAH Total + Ada Error! (KRUSIAL!)

| Properti | Detail |
|----------|--------|
| **Masalah** | 2024: `87%`, `0%`, `#DIV/0!` vs 2023: `80.6%` vs 2020-2022: `"80,6%"` |
| **Error Excel** | `#DIV/0!` muncul ketika Capacity = 0 tapi ada penumpang (atau sebaliknya) |
| **Saran** | **Parser dinamis per tahun:**<br>- 2020-2022: Hapus quotes, replace `,` → `.`<br>- 2023: Hapus `%`<br>- 2024: Hapus `%`, handle `#DIV/0!` → `NULL` |

**Visualisasi Transformasi:**
```
2020-2022:  "80,6%"   →  "80.6"   →  80.6
2023:       80.6%     →  "80.6"   →  80.6
2024:       87%       →  "87"     →  87
2024:       #DIV/0!   →  NULL
```

### 2. Format Integer Murni
- **Saran:** Langsung baca sebagai integer

### 3. Missing Value & Error
- **Saran:** Replace `#DIV/0!` dengan `NULL`

### 4. Format Rute Hanya IATA Code
- **Saran:** Mapping table

### 5. Baris Total
- **Saran:** Flag `is_total_row`

---

## 📐 Rekomendasi Skema Database

**Sama seperti tahun sebelumnya — Long Format recommended.**

---

## 🎯 Kesimpulan & Next Steps

### Masalah Kritikal
1. ✅ **Format Load Factor berubah lagi** + ada `#DIV/0!`
2. ✅ Format integer murni
3. ✅ Nama kolom berubah (`LF %`, `JUMLAH BARANG KG`)
4. ✅ Format rute hanya IATA
5. ✅ Baris Total

### Metadata

| Properti | Nilai |
|----------|-------|
| **Jumlah Rute** | 315 |
| **Total Penumpang 2024** | 65,795,595 |
| **Average LF** | 82% |
| **Format** | Integer, IATA only, LF tanpa desimal, ada `#DIV/0!` |

---

> **Catatan:** Dokumen ini hanya fokus pada file Domestik Ranking 2024. Load Factor 2024 punya format paling sederhana (tanpa desimal) tapi ada error Excel `#DIV/0!`.
