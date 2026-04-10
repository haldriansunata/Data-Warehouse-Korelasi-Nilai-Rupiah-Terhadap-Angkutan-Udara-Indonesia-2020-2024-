# BAB VI Summary: Penumpang Per Rute — Tahun 2021

## 📊 Overview

Summary ini merangkum analisis dari **4 file CSV tahun 2021** dalam folder `BAB VI — Penumpang Per Rute/2021/`.

### File yang Dianalisis

| No | File | Kategori | Dimensi | Baris | Kolom | Status `NO` |
|----|------|----------|---------|-------|-------|-------------|
| 1 | `JUMLAH PENUMPANG PER RUTE ... DALAM NEGERI JAN-DES 2021.csv` | Domestik | Bulanan | **381** | 18 | ✅ Konsisten (1-379) |
| 2 | `JUMLAH PENUMPANG PER RUTE ... LUAR NEGERI ... 2021.csv` | Internasional | Bulanan | **148** | 18 | ✅ Konsisten (1-145) |
| 3 | `STATISTIK PER RUTE ... DALAM NEGERI ... 2021.csv` | Domestik | Ranking | **381** | 8 | ✅ Konsisten (1-379) |
| 4 | `STATISTIK PER RUTE ... LUAR NEGERI ... 2021.csv` | Internasional | Ranking | **148** | 8 | ✅ Konsisten (1-145) |

**Total:** 1,058 baris data mentah (termasuk header, total rows, dan footer)

---

## 🔍 Perbandingan Struktur: 2021 vs 2020

### Perbedaan Utama

| Aspek | 2020 | 2021 | Dampak |
|-------|------|------|--------|
| **Jumlah Rute Domestik** | 410 | **379** | ↓ 31 rute (berkurang) |
| **Jumlah Rute Internasional** | ~147 | **~145** | ↓ 2 rute (berkurang sedikit) |
| **Nama Kolom Bulan** | `May-20`, `Aug-20`, `Oct-20`, `Dec-20` | **`Mei-21`, `Agu-21`, `Okt-21`, `Des-21`** | ⚠️ **Bahasa Indonesia vs Inggris** |
| **Kolom Komparasi** | `TOTAL 2019`, `TOTAL 2018` | **`TOTAL 2020`, `TOTAL 2019`** | ⚠️ Bergeser |
| **Tipe Data** | Integer (Domestik), Float (Internasional) | **Float (semua file)** | ⚠️ Tidak konsisten |
| **Format Rute** | `Jakarta (CGK)-Denpasar (DPS)` | **`Jakarta (CGK) - Denpasar (DPS)`** | ⚠️ **Ada spasi tambahan** |
| **Konsistensi `NO`** | Domestik ✅, Internasional ❌ | **Semua ✅ Konsisten** | ✅ **Lebih baik dari 2020** |
| **Nilai "KARGO"** | Ada (Internasional Bulanan) | **Tidak ada** | ✅ Lebih bersih |
| **Footer Codeshare** | Ada (Internasional Ranking) | **Tidak ada** | ✅ Lebih bersih |

---

## ⚠️ Masalah Umum (Cross-Cutting Issues)

### 1. Wide Format (Semua File)
- **Saran:** Transform ke long format

### 2. Missing Value (Sel Kosong)
- **Saran:** Replace dengan `NULL`

### 3. Baris Total di Akhir
- **Saran:** Flag `is_total_row`

### 4. Nama Kolom Tidak Standard
- **Saran:** Rename ke snake_case

### 5. Format Rute dengan Spasi (Semua File 2021)
- **Masalah:** `Jakarta (CGK) - Denpasar (DPS)` vs 2020: `Jakarta (CGK)-Denpasar (DPS)`
- **Dampak:** Sulit join data 2020 vs 2021
- **Saran:** Standardisasi (hapus spasi)

### 6. Nama Kolom Bulan Berbeda vs 2020
- **Masalah:** `Mei-21`, `Agu-21`, `Okt-21`, `Des-21` vs `May-20`, `Aug-20`, `Oct-20`, `Dec-20`
- **Saran:** Standardisasi ke `m01_2021`, `m02_2021`, dll.

### 7. Format Float dengan `.0`
- **Saran:** Convert ke Integer

### 8. Load Factor Koma Desimal (File Ranking)
- **Saran:** Replace `,` → `.`

---

## 📊 Data Summary (2021)

### Volume Data

| Metrik | Domestik | Internasional | Total |
|--------|----------|---------------|-------|
| **Jumlah Rute** | 379 | ~145 | ~524 |
| **Total Penumpang 2021** | 33,336,639 | 1,362,755 (bulanan) / 1,190,882 (ranking) | ~34.7M |
| **Total Penerbangan** | 339,638 | 21,562 | 361,200 |
| **Average Load Factor** | 66.5% | 27.0% | 62.4% (weighted) |

### Recovery dari COVID-19 (2021 vs 2020 vs 2019)

| Metrik | 2019 | 2020 | 2021 | Growth 2021 vs 2020 | Growth 2021 vs 2019 |
|--------|------|------|------|---------------------|---------------------|
| **Penumpang Domestik** | ~100.5M | 35.4M | 33.3M | ↓ -5.8% | ↓ -67.0% |
| **Penumpang Internasional** | ~35.7M | 7.0M | 1.36M | ↓ -80.5% | ↓ -96.2% |

---

## 📐 Rekomendasi Skema Unified

**Sama seperti 2020 — Star Schema dengan:**
- `dim_rute` (master rute)
- `dim_tanggal` (time dimension)
- `fact_penumpang_bulanan` (dari file bulanan)
- `fact_statistik_rute` (dari file ranking)

**Catatan Penting:** Perlu standardisasi format rute & nama kolom agar bisa unify data 2020 & 2021.

---

## 🎯 Rekomendasi Final

### 1. Format Target

| File | Format Source | Format Target |
|------|---------------|---------------|
| **Domestik Bulanan** | Wide (12 bulan) | **Long** |
| **Internasional Bulanan** | Wide (12 bulan) | **Long** |
| **Domestik Ranking** | Wide (6 metrik) | **Long** |
| **Internasional Ranking** | Wide (6 metrik) | **Long** |

### 2. Prioritas Pre-Processing

| Prioritas | Task |
|-----------|------|
| 🔴 **Kritikal** | Standardisasi nama kolom bulan (Mei/Agu/Okt/Des → m05/m08/m10/m12) |
| 🔴 **Kritikal** | Standardisasi format rute (hapus spasi) |
| 🔴 **Kritikal** | Convert Float ke Integer |
| 🟡 **Penting** | Clean Load Factor |
| 🟡 **Penting** | Rename kolom ke snake_case |
| 🟡 **Penting** | Parse rute → asal/tujuan + IATA |
| 🟢 **Nice to Have** | Flag is_pandemic_year |

---

## 📋 Checklist Next Steps

### Untuk Tahun 2021
- [x] Analisis 4 file CSV 2021
- [x] Identifikasi perbedaan vs 2020
- [ ] Buat script pre-processing (handle perbedaan nama kolom & format rute)
- [ ] Test ETL pipeline
- [ ] Validasi vs Total rows

### Untuk Integrasi 2020 + 2021
- [ ] Standardisasi format rute (pilih salah satu)
- [ ] Standardisasi nama kolom bulan
- [ ] Unify dim_rute (mapping rute 2020 vs 2021)
- [ ] Append data ke fact tables

---

## 📝 Metadata Summary

| Properti | Nilai |
|----------|-------|
| **Analysis Date** | 2026-04-10 |
| **Tahun** | 2021 |
| **Jumlah File** | 4 |
| **Jumlah Total Baris** | 1,058 |
| **Jumlah Rute Domestik** | 379 |
| **Jumlah Rute Internasional** | ~145 |
| **Total Penumpang Domestik 2021** | 33,336,639 |
| **Total Penumpang Internasional 2021** | 1,362,755 |
| **Average Load Factor Domestik** | 66.5% |
| **Average Load Factor Internasional** | 27.0% |
| **Perbedaan Signifikan vs 2020** | Nama kolom bulan (Bahasa Indonesia), format rute ada spasi, semua Float, nomor konsisten ✅ |

---

> **Catatan:** Summary ini merangkum 4 file analisis individual 2021.
> - `CSV_ANALYSIS_2021_Domestik_Bulanan.md`
> - `CSV_ANALYSIS_2021_Internasional_Bulanan.md`
> - `CSV_ANALYSIS_2021_Domestik_Ranking.md`
> - `CSV_ANALYSIS_2021_Internasional_Ranking.md`
>
> **Penting:** File 2021 punya beberapa perbedaan struktur vs 2020 yang perlu di-handle saat ETL (nama kolom bulan, format rute dengan spasi, tipe data Float).
