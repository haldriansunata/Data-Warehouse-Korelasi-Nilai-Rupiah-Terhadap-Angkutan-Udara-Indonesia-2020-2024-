# BAB VI Summary: Penumpang Per Rute — Tahun 2022

## 📊 Overview

Summary ini merangkum analisis dari **4 file CSV tahun 2022** dalam folder `BAB VI — Penumpang Per Rute/2022/`.

### File yang Dianalisis

| No | File | Kategori | Baris | Kolom | Format Rute | Format Angka |
|----|------|----------|-------|-------|-------------|--------------|
| 1 | `JUMLAH PENUMPANG PER RUTE ... DALAM NEGERI JAN-DES 2022.csv` | Domestik Bulanan | **377** | **15** | **IATA only** ⚠️ | **Titik = ribuan** ⚠️ |
| 2 | `JUMLAH PENUMPANG PER RUTE ... LUAR NEGERI ... 2022.csv` | Internasional Bulanan | **136** | **15** | **IATA only** ⚠️ | **Titik = ribuan** ⚠️ |
| 3 | `STATISTIK PER RUTE ... DALAM NEGERI ... 2022.csv` | Domestik Ranking | **377** | 8 | **IATA only** ⚠️ | **Titik = ribuan** ⚠️ |
| 4 | `STATISTIK PER RUTE ... LUAR NEGERI ... 2022.csv` | Internasional Ranking | **136** | 8 | **IATA only** ⚠️ | **Titik = ribuan** ⚠️ |

**Total:** 1,026 baris data mentah

---

## 🔍 Perbedaan SANGAT SIGNIFIKAN vs 2020-2021

### 2022 Adalah Tahun dengan Perubahan Struktur TERBESAR!

| Aspek | 2020 | 2021 | **2022** | Dampak ETL |
|-------|------|------|----------|------------|
| **Rute Domestik** | 410 | 379 | **374** | ↓ 36 rute dari 2020 |
| **Rute Internasional** | ~147 | ~145 | **133** | ↓ 14 rute dari 2020 |
| **Format Rute** | Nama + IATA | Nama + IATA | **Hanya IATA** ⚠️⚠️ | **TIDAK BISA JOIN LANGSUNG** |
| **Format Angka** | Integer/Float | Float (.0) | **Titik = ribuan** ⚠️⚠️ | **PARSER KHUSUS WAJIB** |
| **Nama Bulan** | Inggris/Indonesia | Indonesia | **Inggris** | ⚠️ Handle 3 variasi |
| **Kolom Komparasi** | 2019, 2018 | 2020, 2019 | **Tidak ada** ⚠️ | Harus join manual |
| **Jumlah Kolom (Bulanan)** | 18 | 18 | **15** | ↓ 3 kolom |

---

## ⚠️ Masalah Umum (Cross-Cutting Issues)

### 1. Format Angka dengan Titik sebagai Pemisah Ribuan (PALING KRUSIAL!)

**Ini adalah perubahan paling berbahaya!**

```
2020-2021:  107991.0   → Float biasa (suffix .0)
2022:       324.111    → Titik = PEMISAH RIBUAN (= 324,111)

Jika salah parse:
  ❌ Baca "324.111" sebagai float = 324.111 (SALAH!)
  ✅ Parse "324.111" → hapus titik → 324111 (BENAR)
```

**Saran Parser:**
```python
def parse_angka_2022(value):
    if pd.isna(value) or value == '':
        return None
    str_val = str(value)
    # Hapus titik (pemisah ribuan)
    str_val = str_val.replace('.', '')
    # Hapus .0 jika ada di akhir
    if str_val.endswith('.0'):
        str_val = str_val[:-2]
    return int(str_val)
```

### 2. Format Rute Hanya IATA Code (TIDAK BISA JOIN LANGSUNG!)

```
2020: "Jakarta (CGK)-Denpasar (DPS)"
2021: "Jakarta (CGK) - Denpasar (DPS)"
2022: "CGK-DPS"  ← TIDAK BISA JOIN LANGSUNG!

Solusi:
  Opsi A: Mapping table IATA → nama kota
  Opsi B: Parse IATA dari format 2020-2021, lalu join
```

### 3. Tidak Ada Kolom Komparasi

- 2022 hanya punya `TOTAL 2022`
- Tidak ada `TOTAL 2021` atau `TOTAL 2020`
- **Saran:** Join di database setelah load

### 4. Wide Format
- **Saran:** Transform ke long format

### 5. Missing Value
- **Saran:** Replace dengan `NULL`

### 6. Baris Total Tanpa Label
- **Saran:** Flag `is_total_row`

---

## 📊 Data Summary (2022)

### Volume Data

| Metrik | Domestik | Internasional | Total |
|--------|----------|---------------|-------|
| **Jumlah Rute** | 374 | 133 | 507 |
| **Total Penumpang 2022** | 56,408,353 | 12,298,746 | 68,707,099 |
| **Total Penerbangan** | 464,282 | 74,438 | 538,720 |
| **Average Load Factor** | 78.7% | 77.9% | 78.6% |

### Recovery dari COVID-19

| Metrik | 2020 | 2021 | 2022 | Growth 2022 vs 2021 | Growth 2022 vs 2019 |
|--------|------|------|------|---------------------|---------------------|
| **Penumpang Domestik** | 35.4M | 33.3M | **56.4M** | ↑ +69.2% | ↓ -43.9% |
| **Penumpang Internasional** | 7.0M | 1.36M | **12.3M** | ↑ +801% | ↓ -65.5% |

**Insight:** 2022 adalah tahun **recovery besar** dari COVID-19!

---

## 📐 Rekomendasi Skema Unified

**Sama seperti 2020-2021 — Star Schema dengan:**
- `dim_rute` (perlu mapping IATA ↔ nama kota)
- `dim_tanggal`
- `fact_penumpang_bulanan`
- `fact_statistik_rute`

**Catatan Khusus untuk 2022:**
1. **Parser wajib** untuk handle titik sebagai pemisah ribuan
2. **Mapping table** untuk convert IATA code ke nama kota
3. **Tidak ada kolom komparasi** — harus join manual

---

## 🎯 Rekomendasi Final

### 1. Format Target

| File | Format Target |
|------|---------------|
| Semua file 2022 | **Long Format** |

### 2. Prioritas Pre-Processing

| Prioritas | Task |
|-----------|------|
| 🔴 **KRITIKAL** | Parser titik sebagai pemisah ribuan |
| 🔴 **KRITIKAL** | Mapping table IATA code → nama kota |
| 🟡 **Penting** | Standardisasi nama kolom bulan |
| 🟡 **Penting** | Rename kolom ke snake_case |
| 🟡 **Penting** | Parse rute (walaupun sudah IATA) |
| 🟢 **Nice to Have** | Flag is_active per tahun |

---

## 📋 Checklist Next Steps

### Untuk Tahun 2022
- [ ] **Buat parser khusus** untuk handle titik sebagai pemisah ribuan
- [ ] **Buat mapping table** IATA code ↔ nama kota
- [ ] Standardisasi nama kolom
- [ ] Unpivot ke long format
- [ ] Validasi vs Total rows

### Untuk Integrasi 2020-2022
- [ ] Buat mapping table untuk unify format rute
- [ ] Handle perbedaan format angka
- [ ] Standardisasi nama kolom bulan (3 variasi!)
- [ ] Join data multi-tahun di fact tables

---

## 📝 Metadata Summary

| Properti | Nilai |
|----------|-------|
| **Analysis Date** | 2026-04-10 |
| **Tahun** | 2022 |
| **Jumlah File** | 4 |
| **Jumlah Total Baris** | 1,026 |
| **Jumlah Rute Domestik** | 374 |
| **Jumlah Rute Internasional** | 133 |
| **Total Penumpang Domestik 2022** | 56,408,353 |
| **Total Penumpang Internasional 2022** | 12,298,746 |
| **Average Load Factor** | 78.6% |
| **Perbedaan Signifikan** | Format rute (IATA only), titik = ribuan, tidak ada kolom komparasi |

---

> **Catatan:** Summary ini merangkum 4 file analisis individual 2022.
> 
> **PENTING:** 2022 adalah tahun dengan perubahan struktur TERBESAR vs 2020-2021. Diperuhkan parser khusus dan mapping table untuk integrasi data multi-tahun.
