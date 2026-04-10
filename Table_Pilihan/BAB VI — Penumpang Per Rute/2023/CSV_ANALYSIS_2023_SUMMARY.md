# BAB VI Summary: Penumpang Per Rute — Tahun 2023

## 📊 Overview

Summary ini merangkum analisis dari **4 file CSV tahun 2023** dalam folder `BAB VI — Penumpang Per Rute/2023/`.

### File yang Dianalisis

| No | File | Kategori | Baris | Kolom | Format Rute | Format Angka |
|----|------|----------|-------|-------|-------------|--------------|
| 1 | `JUMLAH PENUMPANG PER RUTE ... DALAM NEGERI JAN-DES 2023.csv` | Domestik Bulanan | **306** | **15** | IATA only | Float (.0) |
| 2 | `JUMLAH PENUMPANG PER RUTE ... LUAR NEGERI ... 2023.csv` | Internasional Bulanan | **128** | **15** | IATA only | Float (.0) |
| 3 | `STATISTIK PER RUTE ... DALAM NEGERI ... 2023.csv` | Domestik Ranking | **306** | 8 | IATA only | Float (.0) |
| 4 | `STATISTIK PER RUTE ... LUAR NEGERI ... 2023.csv` | Internasional Ranking | **128** | 8 | IATA only | Float (.0) |

**Total:** 868 baris data mentah

---

## 🔍 Perbedaan vs 2020-2022

### 1. Format Load Factor di File Ranking BERUBAH Total!

| Tahun | Format Load Factor | Contoh |
|-------|-------------------|--------|
| **2020-2022** | String dengan quotes + koma | `"80,6%"` |
| **2023** | **String TANPA quotes + titik** | `80.6%` |

### 2. Format Angka Kembali Normal

| Tahun | Format Angka | Contoh |
|-------|--------------|--------|
| **2022** | Float dengan titik = ribuan | `324.111` (= 324,111) |
| **2023** | **Float dengan `.0`** (kembali normal) | `392247.0` |

### 3. Nama Kolom Bulan Kembali ke Bahasa Indonesia

| Tahun | Format |
|-------|--------|
| **2022** | `Jan-22`, `May-22`, `Aug-22`, `Oct-22`, `Dec-22` (Inggris) |
| **2023** | `Jan-23`, `Mei-23`, `Agu-23`, `Okt-23`, `Des-23` (Indonesia) |

### 4. Jumlah Rute Berkurang Signifikan

| Tahun | Rute Domestik | Rute Internasional |
|-------|---------------|-------------------|
| **2020** | 410 | ~147 |
| **2021** | 379 | ~145 |
| **2022** | 374 | 133 |
| **2023** | **303** | **125** |

---

## ⚠️ Masalah Umum (Cross-Cutting Issues)

### 1. Format Load Factor Berubah (PALING KRUSIAL!)

**Parser untuk 2020-2022 TIDAK BISA dipakai untuk 2023!**

```
2020-2022:  "80,6%"  →  Hapus quotes, replace koma → 80.6
2023:       80.6%    →  Hapus % saja → 80.6

Parser dinamis:
  if value starts with '"' and contains ',':
    # Format 2020-2022
    return value.strip('"').replace(',', '%').rstrip('%')
  else:
    # Format 2023
    return value.rstrip('%')
```

### 2. Format Rute Hanya IATA Code (2022-2023)
- **Saran:** Mapping table IATA ↔ nama kota

### 3. Jumlah Rute Berkurang Drastis
- 2020: 410 → 2023: 303 (domestik) — ↓ 107 rute!
- 2020: ~147 → 2023: 125 (internasional) — ↓ 22 rute
- **Saran:** Track route lifecycle

### 4. Tidak Ada Kolom Komparasi (2022-2023)
- **Saran:** Join di database

### 5. Wide Format
- **Saran:** Transform ke long format

### 6. Missing Value
- **Saran:** Replace dengan `NULL`

### 7. Baris Total
- **Saran:** Flag `is_total_row`

---

## 📊 Data Summary (2023)

### Volume Data

| Metrik | Domestik | Internasional | Total |
|--------|----------|---------------|-------|
| **Jumlah Rute** | 303 | 125 | 428 |
| **Total Penumpang 2023** | 65,925,924 | 29,054,531 | 94,980,455 |
| **Total Penerbangan** | 517,490 | 176,909 | 694,399 |
| **Average Load Factor** | 80.2% | 77.5% | 79.6% |

### Recovery dari COVID-19

| Metrik | 2019 | 2022 | 2023 | Growth 2023 vs 2022 | Growth 2023 vs 2019 |
|--------|------|------|------|---------------------|---------------------|
| **Penumpang Domestik** | ~100.5M | 56.4M | **65.9M** | ↑ +16.9% | ↓ -34.4% |
| **Penumpang Internasional** | ~35.7M | 12.3M | **29.1M** | ↑ +136.3% | ↓ -18.5% |

**Insight:** 2023 menunjukkan **recovery yang sangat kuat**, terutama internasional!

---

## 📐 Rekomendasi Skema Unified

**Sama seperti tahun sebelumnya — Star Schema dengan:**
- `dim_rute` (perlu mapping IATA ↔ nama kota)
- `dim_tanggal`
- `fact_penumpang_bulanan`
- `fact_statistik_rute`

**Catatan Khusus untuk 2023:**
1. **Parser Load Factor dinamis** untuk handle format 2020-2022 vs 2023
2. **Mapping table** untuk convert IATA code ke nama kota
3. **Track route lifecycle** karena banyak rute yang hilang

---

## 🎯 Rekomendasi Final

### 1. Format Target

| File | Format Target |
|------|---------------|
| Semua file 2023 | **Long Format** |

### 2. Prioritas Pre-Processing

| Prioritas | Task |
|-----------|------|
| 🔴 **KRITIKAL** | Parser Load Factor dinamis (handle 2 format) |
| 🔴 **KRITIKAL** | Mapping table IATA code → nama kota |
| 🟡 **Penting** | Standardisasi nama kolom bulan |
| 🟡 **Penting** | Rename kolom ke snake_case |
| 🟡 **Penting** | Remove `.0` dari float |
| 🟢 **Nice to Have** | Flag is_active per tahun |

---

## 📋 Checklist Next Steps

### Untuk Tahun 2023
- [ ] Buat parser Load Factor dinamis
- [ ] Mapping table IATA code
- [ ] Standardisasi nama kolom
- [ ] Unpivot ke long format
- [ ] Validasi vs Total rows

### Untuk Integrasi 2020-2023
- [ ] Handle 3 variasi format Load Factor (2020-2022 koma+quotes, 2023 titik+tanpa quotes)
- [ ] Handle 2 variasi format angka (2022 titik=ribuan, lainnya float .0)
- [ ] Handle 3 variasi nama bulan (Inggris, Indonesia, Inggris, Indonesia)
- [ ] Handle format rute (nama kota vs IATA only)
- [ ] Standardisasi semua kolom

---

## 📝 Metadata Summary

| Properti | Nilai |
|----------|-------|
| **Analysis Date** | 2026-04-10 |
| **Tahun** | 2023 |
| **Jumlah File** | 4 |
| **Jumlah Total Baris** | 868 |
| **Jumlah Rute Domestik** | 303 |
| **Jumlah Rute Internasional** | 125 |
| **Total Penumpang Domestik 2023** | 65,925,924 |
| **Total Penumpang Internasional 2023** | 29,054,531 |
| **Average Load Factor** | 79.6% |
| **Perbedaan Signifikan** | Load Factor format (titik vs koma, tanpa quotes), angka kembali normal, bulan Indonesia |

---

> **Catatan:** Summary ini merangkum 4 file analisis individual 2023.
> 
> **PENTING:** 2023 punya perubahan format Load Factor yang signifikan vs 2020-2022 dan format angka kembali normal (setelah 2022 pakai titik sebagai ribuan).
