# BAB VI Summary: Penumpang Per Rute — Tahun 2024

## 📊 Overview

Summary ini merangkum analisis dari **4 file CSV tahun 2024** dalam folder `BAB VI — Penumpang Per Rute/2024/`.

### File yang Dianalisis

| No | File | Kategori | Baris | Kolom | Format Rute | Format Angka |
|----|------|----------|-------|-------|-------------|--------------|
| 1 | `JUMLAH PENUMPANG PER RUTE ... DALAM NEGERI JAN-DES 2024.csv` | Domestik Bulanan | **317** | **15** | IATA only | **Integer** |
| 2 | `JUMLAH PENUMPANG PER RUTE ... LUAR NEGERI ... 2024.csv` | Internasional Bulanan | **137** | **15** | IATA only | Mix Int/Float |
| 3 | `STATISTIK PER RUTE ... DALAM NEGERI ... 2024.csv` | Domestik Ranking | **318** | 8 | IATA only | Integer |
| 4 | `STATISTIK PER RUTE ... LUAR NEGERI ... 2024.csv` | Internasional Ranking | **137** | 8 | IATA only | Integer |

**Total:** 909 baris data mentah

---

## 🔍 Perbedaan SANGAT SIGNIFIKAN vs 2020-2023

### 2024 Adalah Tahun dengan Perubahan Format ANGKA Terbesar!

| Aspek | 2020 | 2021 | 2022 | 2023 | **2024** |
|-------|------|------|------|------|----------|
| **Rute Domestik** | 410 | 379 | 374 | 303 | **314** |
| **Rute Internasional** | ~147 | ~145 | 133 | 125 | **134** |
| **Format Rute** | Nama + IATA | Nama + IATA | IATA only | IATA only | **IATA only** |
| **Format Angka (Bulanan)** | Integer | Float (.0) | Titik = ribuan | Float (.0) | **Integer** ⚠️ |
| **Format LF** | `"XX,X%"` | `"XX,X%"` | `"XX,X%"` | `XX.X%` | **`XX%`** ⚠️ |
| **Nama Kolom LF** | `L/F` | `L/F` | `L/F` | `L/F` | **`LF %`** ⚠️ |
| **Nama Kolom Rute** | `RUTE (PP)` | `RUTE ( PP)` | `RUTE ( PP)` | `RUTE ( PP)` | **`RUTE PP`** ⚠️ |
| **Nama Kolom Barang** | `JUMLAH BARANG (Kg)` | `JUMLAH BARANG` | `JUMLAH BARANG` | `JUMLAH BARANG` | **`JUMLAH BARANG KG`** ⚠️ |
| **Missing Value** | Sel kosong | Sel kosong | Sel kosong | Sel kosong | **`0`** ⚠️ |
| **Error Excel** | Tidak ada | Tidak ada | Tidak ada | Tidak ada | **`#DIV/0!`** ⚠️ |

---

## ⚠️ Masalah Umum (Cross-Cutting Issues)

### 1. Format Load Factor BERUBAH SETIAP TAHUN! (PALING KRUSIAL!)

**Ini adalah perubahan paling kompleks!** Setiap tahun punya format berbeda:

```
2020-2022:  "80,6%"   →  Hapus quotes, replace koma → 80.6
2023:       80.6%     →  Hapus % → 80.6
2024:       87%       →  Hapus % → 87
2024:       #DIV/0!   →  NULL

Parser yang dibutuhkan:
  def parse_load_factor(value, year):
      if value in ['#DIV/0!', '']:
          return None
      if year <= 2022:
          return float(value.strip('"').replace(',', '').replace('%', ''))
      elif year == 2023:
          return float(value.rstrip('%'))
      else:  # 2024
          return float(value.rstrip('%'))
```

### 2. Format Angka Berubah-Ubah

| Tahun | Format | Contoh | Parser |
|-------|--------|--------|--------|
| **2020** | Integer | `231865` | `int(value)` |
| **2021** | Float `.0` | `107991.0` | `int(float(value))` |
| **2022** | Titik = ribuan | `324.111` | `int(value.replace('.', ''))` |
| **2023** | Float `.0` | `392247.0` | `int(float(value))` |
| **2024** | Integer | `380993` | `int(value)` |

### 3. Missing Value Berubah Format

| Tahun | Format Missing |
|-------|---------------|
| **2020-2023** | Sel kosong |
| **2024** | **`0`** (angka nol) |

### 4. Wide Format
- **Saran:** Transform ke long format

### 5. Format Rute Hanya IATA Code (2022-2024)
- **Saran:** Mapping table

### 6. Baris Total
- **Saran:** Flag `is_total_row`

---

## 📊 Data Summary (2024)

### Volume Data

| Metrik | Domestik | Internasional | Total |
|--------|----------|---------------|-------|
| **Jumlah Rute** | 314 | 134 | 448 |
| **Total Penumpang 2024** | 65,795,595 | ~29M | ~94.8M |
| **Total Penerbangan** | 497,831 | ~177K | ~675K |
| **Average Load Factor** | 82% | ~78% | ~81% |

### Recovery dari COVID-19

| Metrik | 2019 | 2023 | 2024 | Growth 2024 vs 2023 | Growth 2024 vs 2019 |
|--------|------|------|------|---------------------|---------------------|
| **Penumpang Domestik** | ~100.5M | 65.9M | **65.8M** | ↓ -0.2% | ↓ -34.5% |
| **Penumpang Internasional** | ~35.7M | 29.1M | **~29M** | ↓ -0.2% | ↓ -18.8% |

**Insight:** 2024 menunjukkan **stabilisasi** setelah recovery besar di 2023.

---

## 📐 Rekomendasi Skema Unified

**Sama seperti tahun sebelumnya — Star Schema dengan:**
- `dim_rute` (perlu mapping IATA ↔ nama kota)
- `dim_tanggal`
- `fact_penumpang_bulanan`
- `fact_statistik_rute`

**Catatan Khusus untuk 2024:**
1. **Parser Load Factor paling kompleks** (handle 4 format berbeda!)
2. **Handle error Excel** `#DIV/0!`
3. **Missing value = `0`** (bukan sel kosong)
4. **Integer murni** untuk data bulanan

---

## 🎯 Rekomendasi Final

### 1. Format Target

| File | Format Target |
|------|---------------|
| Semua file 2024 | **Long Format** |

### 2. Prioritas Pre-Processing

| Prioritas | Task |
|-----------|------|
| 🔴 **KRITIKAL** | Parser Load Factor dinamis (handle 4 format!) |
| 🔴 **KRITIKAL** | Parser angka dinamis (handle 5 format!) |
| 🔴 **KRITIKAL** | Handle `#DIV/0!` → `NULL` |
| 🟡 **Penting** | Mapping table IATA code → nama kota |
| 🟡 **Penting** | Standardisasi nama kolom |
| 🟡 **Penting** | Replace `0` dengan `NULL` untuk missing value |
| 🟢 **Nice to Have** | Flag is_active per tahun |

---

## 📋 Checklist Next Steps

### Untuk Tahun 2024
- [ ] Buat parser Load Factor yang handle 4 format berbeda
- [ ] Buat parser angka yang handle 5 format berbeda
- [ ] Handle `#DIV/0!` error
- [ ] Mapping table IATA code
- [ ] Standardisasi nama kolom
- [ ] Unpivot ke long format
- [ ] Validasi vs Total rows

### Untuk Integrasi 2020-2024
- [ ] Handle 4 variasi format Load Factor
- [ ] Handle 5 variasi format angka
- [ ] Handle 3 variasi nama bulan
- [ ] Handle format rute (nama kota vs IATA only)
- [ ] Handle missing value (sel kosong vs `0`)
- [ ] Standardisasi semua kolom

---

## 📝 Metadata Summary

| Properti | Nilai |
|----------|-------|
| **Analysis Date** | 2026-04-10 |
| **Tahun** | 2024 |
| **Jumlah File** | 4 |
| **Jumlah Total Baris** | 909 |
| **Jumlah Rute Domestik** | 314 |
| **Jumlah Rute Internasional** | 134 |
| **Total Penumpang Domestik 2024** | 65,795,595 |
| **Total Penumpang Internasional 2024** | ~29M |
| **Average Load Factor** | ~81% |
| **Perbedaan Signifikan** | Format angka integer, LF tanpa desimal, ada `#DIV/0!`, missing = `0`, nama kolom berubah |

---

> **Catatan:** Summary ini merangkup 4 file analisis individual 2024.
> 
> **PENTING:** 2024 adalah tahun dengan variasi format TERBANYAK (integer, LF tanpa desimal, `#DIV/0!`, missing = `0`, nama kolom berubah). Parser dinamis sangat dibutuhkan untuk integrasi data multi-tahun.
