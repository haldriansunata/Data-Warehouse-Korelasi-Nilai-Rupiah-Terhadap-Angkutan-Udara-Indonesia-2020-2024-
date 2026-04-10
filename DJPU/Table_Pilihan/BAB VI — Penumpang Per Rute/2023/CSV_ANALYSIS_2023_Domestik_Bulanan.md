# CSV Analysis: Jumlah Penumpang Per Rute — Domestik Bulanan 2023

## 📊 Informasi Umum

| Properti | Nilai |
|----------|-------|
| **Nama File** | `JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI JAN-DES 2023.csv` |
| **Jumlah Baris** | 306 (1 header + 303 rute + 1 Total + 1 empty) |
| **Jumlah Kolom** | 15 |
| **Format Rute** | Hanya IATA code (`CGK-DPS`) |
| **Format Angka** | Float dengan `.0` suffix (contoh: `392247.0`) |
| **Missing Value** | Sel kosong |

---

## ⚠️ PERBEDAAN vs 2020-2022

### 1. Format Angka Kembali ke Float Biasa (BUKAN Titik sebagai Ribuan!)

| Tahun | Format Angka | Contoh |
|-------|--------------|--------|
| **2020** | Integer | `231865` |
| **2021** | Float dengan `.0` | `107991.0` |
| **2022** | **Float dengan titik = ribuan** | `324.111` (= 324,111) |
| **2023** | **Float dengan `.0`** (kembali normal!) | `392247.0` |

**Ini perubahan PENTING!** 2023 kembali ke format float biasa, bukan titik sebagai pemisah ribuan seperti 2022.

### 2. Nama Kolom Bulan

| Tahun | Format |
|-------|--------|
| **2020** | `Jan-20`, `May-20`, `Aug-20`, `Oct-20`, `Dec-20` (Inggris) |
| **2021** | `Jan-21`, `Mei-21`, `Agu-21`, `Okt-21`, `Des-21` (Indonesia) |
| **2022** | `Jan-22`, `May-22`, `Aug-22`, `Oct-22`, `Dec-22` (Inggris) |
| **2023** | `Jan-23`, `Mei-23`, `Jun-23`, `Jul-23`, ... **(Indonesia kembali!)** |

### 3. Format Rute

| Tahun | Format | Contoh |
|-------|--------|--------|
| **2020** | Nama kota + IATA | `Jakarta (CGK)-Denpasar (DPS)` |
| **2021** | Nama kota + IATA + spasi | `Jakarta (CGK) - Denpasar (DPS)` |
| **2022-2023** | **Hanya IATA code** | `CGK-DPS` |

### 4. Jumlah Rute

| Tahun | Jumlah Rute Domestik |
|-------|---------------------|
| **2020** | 410 |
| **2021** | 379 |
| **2022** | 374 |
| **2023** | **303** (berkurang signifikan!) |

### 5. Kolom Komparasi

| Tahun | Kolom Komparasi |
|-------|-----------------|
| **2020** | `TOTAL 2020`, `TOTAL 2019`, `TOTAL 2018` |
| **2021** | `TOTAL 2021`, `TOTAL 2020`, `TOTAL 2019` |
| **2022-2023** | **Hanya `TOTAL 2023`** (tidak ada komparasi) |

---

## 🗂️ Struktur Tabel 2023

### Skema Saat Ini

```
NO (int)
RUTE (string - hanya IATA code)
Jan-23 (float)
Feb-23 (float)
Mar-23 (float)
Apr-23 (float)
Mei-23 (float) - Bahasa Indonesia
Jun-23 (float)
Jul-23 (float)
Agu-23 (float) - Bahasa Indonesia
Sep-23 (float)
Okt-23 (float) - Bahasa Indonesia
Nov-23 (float)
Des-23 (float) - Bahasa Indonesia
TOTAL 2023 (float)
```

### Detail Per Kolom

| No | Nama Kolom | Deskripsi | Tipe Data Saat Ini | Tipe Data Rekomendasi | Nullable | Contoh Nilai |
|----|-----------|-----------|-------------------|----------------------|----------|--------------|
| 1 | `NO` | Nomor urut rute | Integer | `INT` | ❌ No | `1`, `2`, ..., `303` |
| 2 | `RUTE` | Rute (hanya IATA code) | String | `VARCHAR(20)` | ❌ No | `CGK-DPS` |
| 3-14 | `Jan-23` s/d `Des-23` | Jumlah penumpang per bulan | Float | `INT` | ✅ Yes | `392247.0` |
| 15 | `TOTAL 2023` | Total akumulasi 2023 | Float | `DECIMAL(15,2)` | ✅ Yes | `4961724.0` |

**Catatan:** 
- Format angka 2023 **kembali normal** (float dengan `.0`, bukan titik sebagai ribuan seperti 2022)
- Nama bulan **kembali ke Bahasa Indonesia** (`Mei`, `Agu`, `Okt`, `Des`)

---

## 🔍 Analisis Nilai Unik & Distribusi

### Kolom Kategorikal

#### 1. `NO`
- **Nilai Unik:** 303 (1-303)
- **Catatan:** ✅ **KONSISTEN** sequential tanpa skip

#### 2. `RUTE`
- **Nilai Unik:** 303 rute domestik
- **Format:** Hanya IATA code
- **Contoh:**
  - `CGK-DPS` (Jakarta-Denpasar)
  - `CGK-KNO` (Jakarta-Medan)
  - `SUB-HLP` (Surabaya-Jakarta Halim)
- **Catatan:** ⚠️ Tetap hanya IATA code seperti 2022

#### 3. Kolom Bulanan
- **Tipe:** Float dengan suffix `.0`
- **Range:** 0 hingga 501,516 (`Jul-23` untuk CGK-DPS)
- **Missing Value:** Sel kosong

#### 4. Kolom Total
- **Baris Total:** `65,925,924` (TOTAL 2023)
- **Insight:** Growth dari 2022 (`56.4M`) → 2023 (`65.9M`) = ↑ +16.9%

---

## ⚠️ Potensi Masalah & Saran Pre-Processing

### 1. Format Angka Kembali Normal (Float dengan .0)

| Properti | Detail |
|----------|--------|
| **Observasi** | 2023: `392247.0` (float biasa) vs 2022: `324.111` (titik = ribuan) |
| **Dampak** | • Parser 2022 tidak bisa dipakai untuk 2023<br>• Perlu logic berbeda per tahun |
| **Saran** | **Cek format per tahun:**<br>- 2020: Convert integer<br>- 2021: Remove `.0`<br>- 2022: Hapus titik (pemisah ribuan)<br>- 2023: Remove `.0` |

**Visualisasi Transformasi:**
```
2023:  "392247.0"  →  Remove .0: "392247"  →  SESUDAH:  392247
2022:  "324.111"   →  Remove titik: "324111" →  SESUDAH:  324111
```

### 2. Format Rute Hanya IATA Code

| Properti | Detail |
|----------|--------|
| **Masalah** | `CGK-DPS` vs 2020-2021: nama kota lengkap |
| **Saran** | **Mapping table** IATA code ↔ nama kota |

### 3. Nama Kolom Bulan Bahasa Indonesia (vs 2022 Inggris)

| Properti | Detail |
|----------|--------|
| **Masalah** | 2023: `Mei-23`, `Agu-23`, `Okt-23`, `Des-23` vs 2022: `May-22`, `Aug-22`, `Oct-22`, `Dec-22` |
| **Saran** | **Standardisasi:** `m01_2023`, `m02_2023`, ..., `m12_2023` |

### 4. Jumlah Rute Berkurang Signifikan

| Properti | Detail |
|----------|--------|
| **Observasi** | 2022: 374 rute → 2023: **303 rute** (↓ 71 rute!) |
| **Insight** | Ada konsolidasi atau penutupan rute yang tidak profitable |
| **Saran** | **Track route lifecycle:** flag `is_active` per tahun |

### 5. Tidak Ada Kolom Komparasi

| Properti | Detail |
|----------|--------|
| **Masalah** | Hanya ada `TOTAL 2023`, tidak ada `TOTAL 2022` atau `TOTAL 2021` |
| **Saran** | **Join di database** setelah load ke fact table |

### 6. Baris Total dengan Label

| Properti | Detail |
|----------|--------|
| **Format** | `Total,,517490.0,65925924.0,...` |
| **Saran** | Flag `is_total_row = TRUE` |

---

## 📐 Rekomendasi Skema Database

**Sama seperti tahun sebelumnya — Long Format recommended.**

---

## 🎯 Kesimpulan & Next Steps

### Masalah Kritikal (Harus Ditangani)
1. ✅ Format angka float dengan `.0` (remove `.0`)
2. ✅ Format rute hanya IATA code (perlu mapping)
3. ✅ Nama kolom bulan Bahasa Indonesia (standardisasi)
4. ✅ Jumlah rute berkurang (track lifecycle)
5. ✅ Tidak ada kolom komparasi
6. ✅ Missing value (sel kosong → `NULL`)
7. ✅ Baris Total perlu flag

### Next Steps untuk File Ini
- [ ] Remove `.0` dari nilai float
- [ ] Buat mapping table IATA code → nama kota
- [ ] Standardisasi nama kolom bulan
- [ ] Unpivot ke long format

---

## 📝 Metadata Tambahan

| Properti | Nilai |
|----------|-------|
| **Analysis Date** | 2026-04-10 |
| **Analyzed By** | Data Engineer (AI Assistant) |
| **Jumlah Rute Unik** | 303 |
| **Total Penumpang 2023** | 65,925,924 |
| **Growth 2023 vs 2022** | ↑ +16.9% |
| **Growth 2023 vs 2019** | ↓ -34.4% |
| **Format Angka** | Float dengan `.0` (kembali normal setelah 2022 pakai titik sebagai ribuan) |
| **Format Rute** | Hanya IATA code |
| **Nama Bulan** | Bahasa Indonesia (`Mei`, `Agu`, `Okt`, `Des`) |

**Perbandingan Format Antar Tahun:**
| Aspek | 2020 | 2021 | 2022 | **2023** |
|-------|------|------|------|----------|
| **Jumlah Rute** | 410 | 379 | 374 | **303** |
| **Format Rute** | Nama + IATA | Nama + IATA | IATA only | **IATA only** |
| **Format Angka** | Integer | Float (.0) | Titik = ribuan | **Float (.0)** |
| **Nama Bulan** | Inggris | Indonesia | Inggris | **Indonesia** |
| **Kolom Komparasi** | 2019, 2018 | 2020, 2019 | Tidak ada | **Tidak ada** |
| **Jumlah Kolom** | 18 | 18 | 15 | **15** |

---

> **Catatan:** Dokumen ini hanya fokus pada file Domestik Bulanan 2023. Format angka 2023 kembali normal (float dengan `.0`) setelah 2022 menggunakan titik sebagai pemisah ribuan.
