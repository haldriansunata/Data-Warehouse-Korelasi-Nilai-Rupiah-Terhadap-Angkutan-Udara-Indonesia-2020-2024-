# CSV Analysis: Jumlah Penumpang Per Rute — Internasional Bulanan 2021

## 📊 Informasi Umum

| Properti | Nilai |
|----------|-------|
| **Nama File** | `JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI BULAN JANUARI S.D DESEMBER TAHUN 2021.csv` |
| **Sumber** | Extract dari PDF (Kemenhub/DJPU) |
| **Periode** | Januari - Desember 2021 (plus komparasi 2020 & 2019) |
| **Jumlah Baris** | 148 (1 header + 145 rute + 1 Total + 1 empty/footer) |
| **Jumlah Kolom** | 18 |
| **Tipe Data Utama** | Float (semua nilai punya suffix `.0`) |
| **Missing Value** | Sel kosong |

---

## 🗂️ Struktur Tabel

### Skema Saat Ini

```
NO (int)
RUTE (string)
Jan-21 (float)
Feb-21 (float)
Mar-21 (float)
Apr-21 (float)
Mei-21 (float) - ⚠️ Bahasa Indonesia
Jun-21 (float)
Jul-21 (float)
Agu-21 (float) - ⚠️ Bahasa Indonesia
Sep-21 (float)
Okt-21 (float) - ⚠️ Bahasa Indonesia
Nov-21 (float)
Des-21 (float) - ⚠️ Bahasa Indonesia
TOTAL 2021 (float)
TOTAL 2020 (float)
TOTAL 2019 (float)
```

### Detail Per Kolom

| No | Nama Kolom | Deskripsi | Tipe Data Saat Ini | Tipe Data Rekomendasi | Nullable | Contoh Nilai |
|----|-----------|-----------|-------------------|----------------------|----------|--------------|
| 1 | `NO` | Nomor urut rute | Integer | `INT` | ⚠️ Ada skip | `1`, `2`, ..., `145` (tapi ada skip: 140,141,142,143,144,145) |
| 2 | `RUTE` | Rute internasional | String | `VARCHAR(150)` | ❌ No | `Jakarta (CGK) - Singapura (SIN)` |
| 3-14 | `Jan-21` s/d `Des-21` | Jumlah penumpang per bulan | Float | `DECIMAL(15,2)` | ✅ Yes | `7734.0`, `(kosong)` |
| 15 | `TOTAL 2021` | Total akumulasi 2021 | Float | `DECIMAL(15,2)` | ✅ Yes | `199358.0` |
| 16 | `TOTAL 2020` | Total tahun 2020 | Float | `DECIMAL(15,2)` | ✅ Yes | `618117.0` |
| 17 | `TOTAL 2019` | Total tahun 2019 | Float | `DECIMAL(15,2)` | ✅ Yes | `4077673.0` |

**⚠️ PERBEDAAN PENTING vs 2020:**
1. **Nama kolom bulan:** `Mei-21`, `Agu-21`, `Okt-21`, `Des-21` (bahasa Indonesia) vs `May-20`, `Aug-20`, `Oct-20`, `Dec-20` (bahasa Inggris)
2. **Jumlah rute:** ~145 vs ~147 di 2020 (berkurang sedikit)
3. **Format rute:** Ada spasi `Jakarta (CGK) - Singapura (SIN)` vs `Jakarta (CGK)-SINGAPURA (SIN)` di 2020
4. **Tidak ada nilai "KARGO"** di 2021 (semua numerik atau kosong)

---

## 🔍 Analisis Nilai Unik & Distribusi

### Kolom Kategorikal

#### 1. `NO`
- **Nilai Unik:** 145 (1-145) — ✅ **KONSISTEN** (tidak ada skip seperti 2020)
- **Catatan:** File 2021 sudah lebih rapi dari 2020

#### 2. `RUTE`
- **Nilai Unik:** ~145 rute internasional
- **Format:** `Kota Asal (KODE_IATA) - Kota Tujuan (KODE_IATA)` — ⚠️ **Ada spasi sebelum & setelah dash**
- **Contoh:**
  - `Jakarta (CGK) - Singapura (SIN)`
  - `Jakarta (CGK) - Doha (DOH)`
  - `"Praya, Lombok (LOP) - Kuala Lumpur (KUL)"` (ada koma)

#### 3. Kolom Bulanan (`Jan-21` s/d `Des-21`)
- **Tipe:** Float dengan suffix `.0`
- **Range:** 0 hingga 484,186
- **Missing Value:** Sel kosong (banyak di akhir tahun untuk beberapa rute)

#### 4. Kolom Total
- **Baris Total:** `93,297` (Jan), `73,959` (Feb), ..., `213,741` (Des) → Total 2021: `1,362,755`
- **Insight:** Recovery dari 2020 (`7,002,158`) masih jauh di bawah 2019 (`35,683,914`)

---

## ⚠️ Potensi Masalah & Saran Pre-Processing

### 1. Nama Kolom Bulan Berbeda vs 2020

| Properti | Detail |
|----------|--------|
| **Masalah** | `Mei-21`, `Agu-21`, `Okt-21`, `Des-21` vs `May-20`, `Aug-20`, `Oct-20`, `Dec-20` |
| **Saran** | **Standardisasi:** `m01_2021`, `m02_2021`, ..., `m12_2021` |

### 2. Format Float dengan Suffix `.0`

| Properti | Detail |
|----------|--------|
| **Masalah** | Semua nilai punya `.0` |
| **Saran** | **Convert ke integer** |

### 3. Format Rute dengan Spasi Tambahan

| Properti | Detail |
|----------|--------|
| **Masalah** | `Jakarta (CGK) - Singapura (SIN)` vs 2020: `Jakarta (CGK)-SINGAPURA (SIN)` |
| **Saran** | **Standardisasi:** hapus spasi, uppercase IATA code |

### 4. Missing Value & Rute Baru/Tidak Aktif

| Properti | Detail |
|----------|--------|
| **Observasi** | Banyak rute yang kosong di beberapa bulan (terutama akhir tahun) |
| **Saran** | Replace dengan `NULL`, flag `is_active` per bulan |

### 5. Baris Total

| Properti | Detail |
|----------|--------|
| **Masalah** | Baris `Total,,93297.0,...` adalah agregasi |
| **Saran** | **Beri flag** `is_total_row = TRUE` |

---

## 📐 Rekomendasi Skema Database

**Sama seperti Domestik — pakai Long Format untuk scalability.**

---

## 🎯 Kesimpulan & Next Steps

### Masalah Kritikal
1. ✅ Nama kolom bulan berbeda vs 2020
2. ✅ Suffix `.0` pada semua nilai
3. ✅ Format rute dengan spasi
4. ✅ Missing value
5. ✅ Baris Total perlu flag

### Next Steps
- [ ] Standardisasi nama kolom
- [ ] Convert Float ke Integer
- [ ] Standardisasi format rute
- [ ] Unpivot ke long format

---

## 📝 Metadata Tambahan

| Properti | Nilai |
|----------|-------|
| **Analysis Date** | 2026-04-10 |
| **Analyzed By** | Data Engineer (AI Assistant) |
| **Jumlah Rute Unik** | ~145 |
| **Total Penumpang 2021** | 1,362,755 |
| **Total Penumpang 2020** | 7,002,158 |
| **Total Penumpang 2019** | 35,683,914 |
| **Growth 2021 vs 2020** | ↓ -80.5% |
| **Growth 2021 vs 2019** | ↓ -96.2% |
| **Perbedaan vs 2020** | Nomor konsisten (tidak ada skip), tidak ada "KARGO", ada spasi di rute |

---

> **Catatan:** Dokumen ini hanya fokus pada file Internasional Bulanan 2021.
