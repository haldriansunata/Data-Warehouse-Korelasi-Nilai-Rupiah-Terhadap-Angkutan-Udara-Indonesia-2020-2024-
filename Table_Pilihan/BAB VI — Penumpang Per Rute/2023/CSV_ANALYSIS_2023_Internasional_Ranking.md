# CSV Analysis: Statistik Per Rute — Internasional Ranking 2023

## 📊 Informasi Umum

| Properti | Nilai |
|----------|-------|
| **Nama File** | `STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI TAHUN 2023 BERDASARKAN URUTAN JUMLAH PENUMPANG.csv` |
| **Jumlah Baris** | 128 (1 header + 125 rute + 1 Total + 1 empty) |
| **Jumlah Kolom** | 8 |
| **Format Rute** | Hanya IATA code |
| **Format Angka** | Float dengan `.0` suffix |
| **Load Factor** | String dengan titik desimal, TANPA quotes |

---

## ⚠️ PERBEDAAN SANGAT PENTING vs 2020-2022

### 1. Format Load Factor TANPA Quotes & Pakai Titik!

| Tahun | Format Load Factor | Contoh |
|-------|-------------------|--------|
| **2020-2022** | String dengan quotes + koma | `"77,8%"` |
| **2023** | **String tanpa quotes + titik** | `77.8%` |

### 2. Format Rute Hanya IATA Code (Sama seperti 2022)

| Tahun | Format | Contoh |
|-------|--------|--------|
| **2020-2021** | Nama kota + IATA | `Jakarta (CGK)-SINGAPURA (SIN)` |
| **2022-2023** | **Hanya IATA code** | `CGK-SIN` |

### 3. Jumlah Rute

| Tahun | Jumlah Rute Internasional |
|-------|--------------------------|
| **2020** | ~147 |
| **2021** | ~145 |
| **2022** | 133 |
| **2023** | **125** |

---

## 🗂️ Struktur Tabel

```
NO (int)
RUTE (string - IATA only)
JUMLAH PENERBANGAN (float)
JUMLAH PENUMPANG (float)
KAPASITAS SEAT (float)
JUMLAH BARANG (float)
JUMLAH POS (float)
L/F (string - titik desimal, TANPA quotes!)
```

### Top Routes 2023

| Rank | Rute | Penumpang | Penerbangan | LF |
|------|------|-----------|-------------|-----|
| 1 | CGK-SIN | 3,005,022 | 20,962 | 77.8% |
| 2 | SIN-DPS | 2,512,167 | 12,621 | 80.9% |
| 3 | CGK-KUL | 1,822,318 | 14,304 | 74.6% |
| 4 | KUL-DPS | 1,430,090 | 9,451 | 74.7% |
| 5 | MEL-DPS | 926,575 | 5,334 | 82.2% |

### Total Row
- **JUMLAH PENERBANGAN:** 176,909
- **JUMLAH PENUMPANG:** 29,054,531
- **KAPASITAS SEAT:** 37,506,423
- **JUMLAH BARANG:** 337,227,183 kg
- **JUMLAH POS:** 3,910,788 kg
- **L/F Rata-rata:** 77.5%

---

## ⚠️ Potensi Masalah & Saran

### 1. Format Load Factor BERUBAH Total! (KRUSIAL!)
- **2023:** `77.8%` (titik, tanpa quotes)
- **2020-2022:** `"77,8%"` (koma, dengan quotes)
- **Saran:** Parser dinamis untuk handle kedua format

### 2. Format Rute Hanya IATA Code
- **Saran:** Mapping table

### 3. Format Float dengan `.0`
- **Saran:** Remove `.0`, convert ke integer

### 4. Rute Kargo (Ada yang kosong di L/F)
- Beberapa rute khusus kargo (contoh: `SIN-HLP`, `CGK-DWC`)
- **Saran:** Flag `is_cargo = TRUE`

### 5. Baris Total
- **Saran:** Flag `is_total_row`

---

## 🎯 Kesimpulan

### Masalah Kritikal
1. ✅ **Format Load Factor berubah** (titik vs koma, tanpa quotes)
2. ✅ Format rute hanya IATA
3. ✅ Format float dengan `.0`
4. ✅ Baris Total

### Metadata

| Properti | Nilai |
|----------|-------|
| **Jumlah Rute** | 125 |
| **Total Penumpang** | 29,054,531 |
| **Average LF** | 77.5% |

---

> **Catatan:** Dokumen ini hanya fokus pada file Internasional Ranking 2023.
