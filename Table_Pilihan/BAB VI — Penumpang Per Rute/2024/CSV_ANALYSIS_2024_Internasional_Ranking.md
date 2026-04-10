# CSV Analysis: Statistik Per Rute — Internasional Ranking 2024

## 📊 Informasi Umum

| Properti | Nilai |
|----------|-------|
| **Nama File** | `STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI TAHUN 2024 BERDASARKAN URUTAN JUMLAH PENUMPANG.csv` |
| **Jumlah Baris** | 137 (1 header + 134 rute + 1 Total + 1 empty) |
| **Jumlah Kolom** | 8 |
| **Format Rute** | Hanya IATA code |
| **Format Angka** | Integer |
| **Load Factor** | String dengan `%` TANPA desimal (contoh: `82%`) |

---

## ⚠️ PERBEDAAN SANGAT SIGNIFIKAN vs 2020-2023

### 1. Format Load Factor

| Tahun | Format Load Factor | Contoh |
|-------|-------------------|--------|
| **2020-2022** | String dengan quotes + koma | `"77,8%"` |
| **2023** | String tanpa quotes + titik desimal | `77.5%` |
| **2024** | **String tanpa quotes + TANPA desimal** | `82%` |

### 2. Nama Kolom Berubah

| Tahun | Nama Kolom LF | Nama Kolom Barang | Nama Kolom Pos |
|-------|--------------|------------------|----------------|
| **2020-2023** | `L/F` | `JUMLAH BARANG` | `JUMLAH POS` |
| **2024** | **`LF %`** | **`JUMLAH BARANG KG`** | **`JUMLAH POS KG`** |

### 3. Jumlah Rute

| Tahun | Jumlah Rute Internasional |
|-------|--------------------------|
| **2020** | ~147 |
| **2021** | ~145 |
| **2022** | 133 |
| **2023** | 125 |
| **2024** | **134** (bertambah 9 dari 2023) |

---

## 🗂️ Struktur Tabel

```
NO (int)
RUTE PP (string - IATA only)
JUMLAH PENERBANGAN (int)
JUMLAH PENUMPANG (int)
KAPASITAS SEAT (int)
JUMLAH BARANG KG (int)
JUMLAH POS KG (int)
LF % (string - integer + %)
```

### Top Routes 2024

| Rank | Rute | Penumpang | Penerbangan | LF |
|------|------|-----------|-------------|-----|
| 1 | CGK-SIN | 3,331,178 | 21,614 | 82% |
| 2 | DPS-SIN | 2,742,281 | 13,125 | 83% |
| 3 | CGK-KUL | 2,703,041 | 19,278 | 79% |
| 4 | DPS-KUL | 1,796,779 | 10,814 | 81% |
| 5 | CGK-JED | 1,143,776 | 3,241 | 83% |

### Total Row
- **JUMLAH PENERBANGAN:** 176,909 (perlu verifikasi)
- **JUMLAH PENUMPANG:** 29,054,531
- **KAPASITAS SEAT:** 37,506,423
- **JUMLAH BARANG KG:** 337,227,183 kg
- **JUMLAH POS KG:** 3,910,788 kg
- **LF Rata-rata:** 77-78% (perlu verifikasi)

---

## ⚠️ Potensi Masalah & Saran

### 1. Format Load Factor BERUBAH Lagi! (KRUSIAL!)
- **2024:** `82%` (tanpa desimal)
- **2023:** `77.5%` (dengan desimal)
- **2020-2022:** `"77,8%"` (koma + quotes)
- **Saran:** Parser dinamis per tahun

### 2. Format Integer Murni
- **Saran:** Langsung baca sebagai integer

### 3. Format Rute Hanya IATA Code
- **Saran:** Mapping table

### 4. Baris Total
- **Saran:** Flag `is_total_row`

---

## 🎯 Kesimpulan

### Masalah Kritikal
1. ✅ **Format Load Factor berubah lagi** (tanpa desimal)
2. ✅ Format integer
3. ✅ Nama kolom berubah
4. ✅ Format rute hanya IATA
5. ✅ Baris Total

### Metadata

| Properti | Nilai |
|----------|-------|
| **Jumlah Rute** | 134 |
| **Total Penumpang** | 29,054,531 |
| **Average LF** | ~78% |
| **Format** | Integer, IATA only, LF tanpa desimal |

---

> **Catatan:** Dokumen ini hanya fokus pada file Internasional Ranking 2024.
