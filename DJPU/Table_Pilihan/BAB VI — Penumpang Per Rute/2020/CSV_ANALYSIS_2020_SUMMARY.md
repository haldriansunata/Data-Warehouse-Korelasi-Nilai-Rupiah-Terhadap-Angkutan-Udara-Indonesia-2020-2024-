# BAB VI Summary: Penumpang Per Rute — Tahun 2020

## 📊 Overview

Summary ini merangkum analisis dari **4 file CSV tahun 2020** dalam folder `BAB VI — Penumpang Per Rute/2020/`.

### File yang Dianalisis

| No | File | Kategori | Dimensi | Baris | Kolom | Status `NO` |
|----|------|----------|---------|-------|-------|-------------|
| 1 | `JUMLAH PENUMPANG PER RUTE ... DALAM NEGERI JAN-DES 2020.csv` | Domestik | Bulanan | **412** | 18 | ✅ Konsisten (1-410) |
| 2 | `JUMLAH PENUMPANG PER RUTE ... LUAR NEGERI ... 2020.csv` | Internasional | Bulanan | 160 | 18 | ⚠️ Tidak konsisten (ada skip) |
| 3 | `STATISTIK PER RUTE ... DALAM NEGERI ... 2020.csv` | Domestik | Ranking | **412** | 8 | ✅ Konsisten (1-410) |
| 4 | `STATISTIK PER RUTE ... LUAR NEGERI ... 2020.csv` | Internasional | Ranking | 161 | 8 | ⚠️ Tidak konsisten (ada skip) |

**Total:** 1,145 baris data mentah (termasuk header, total rows, dan footer)

**Catatan:** File Domestik sudah diperbaiki (dari 521/467 baris → 412 baris dengan struktur konsisten). File Internasional masih asli.

---

## 🔍 Perbandingan Struktur 4 File

### 1. Format & Dimensi Waktu

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ FILE BULANAN (2 files: Domestik + Internasional)                            │
├─────────────────────────────────────────────────────────────────────────────┤
│ • 1 baris = 1 rute                                                          │
│ • Kolom waktu: Jan-20, Feb-20, ..., Dec-20, TOTAL 2020, TOTAL 2019, 2018   │
│ • Total kolom waktu: 15 (12 bulan + 3 total tahun)                         │
│ • Format: WIDE                                                              │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ FILE RANKING (2 files: Domestik + Internasional)                            │
├─────────────────────────────────────────────────────────────────────────────┤
│ • 1 baris = 1 rute (ranking berdasarkan penumpang)                        │
│ • Kolom metrik: Flights, Passengers, Seats, Cargo, Pos, L/F                │
│ • Total kolom metrik: 6                                                     │
│ • Format: WIDE (tapi bukan waktu, melainkan metrics)                       │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2. Kolom yang Sama vs Berbeda

| Aspek | File Bulanan | File Ranking |
|-------|--------------|--------------|
| **Kolom ID** | `NO` | `NO` |
| **Kolom Rute** | `RUTE (PP)` (Domestik) atau `RUTE` (Internasional) | `RUTE (PP)` (Domestik) atau `RUTE` (Internasional) |
| **Kolom Waktu** | `Jan-20` s/d `Dec-20` + `TOTAL 2020/2019/2018` | ❌ Tidak ada |
| **Kolom Metrik** | ❌ Tidak ada | `JUMLAH PENERBANGAN`, `JUMLAH PENUMPANG`, `KAPASITAS SEAT`, `JUMLAH BARANG`, `JUMLAH POS`, `L/F` |
| **Total Row** | ✅ Ada di akhir (`Total,,...`) | ✅ Ada (Domestik: tanpa label, Internasional: `Total,,...`) |
| **Footer** | ❌ Tidak ada | ✅ Ada (`* Rute Codeshare...` di Internasional) |
| **Konsistensi `NO`** | ✅ Domestik: Konsisten 1-410<br>⚠️ Internasional: Ada skip | ✅ Domestik: Konsisten 1-410<br>⚠️ Internasional: Ada skip |

### 3. Tipe Data

| Properti | File Bulanan | File Ranking |
|----------|--------------|--------------|
| **Nilai Penumpang** | Integer (Domestik), Float dengan `.0` (Internasional) | Integer (Domestik), Float dengan `.0` (Internasional) |
| **Missing Value** | Sel kosong | Sel kosong |
| **Load Factor** | ❌ Tidak ada | String `"XX,X%"` (koma desimal) |
| **Nilai Khusus** | ❌ Tidak ada | String `"KARGO"` (di Internasional Bulanan) |

---

## ⚠️ Masalah Umum (Cross-Cutting Issues)

### 1. Wide Format (Semua File)

| Properti | Detail |
|----------|--------|
| **Masalah** | Semua 4 file menggunakan **wide format** |
| **Dampak** | • Sulit query time-series & trend<br>• Sulit agregasi cross-file<br>• Tidak scalable untuk tahun baru |
| **Saran** | **Transform ke long format** untuk semua file agar konsisten |

---

### 2. Missing Value Tidak Konsisten (Semua File)

| Properti | Detail |
|----------|--------|
| **Masalah** | Missing value direpresentasikan sebagai **sel kosong** (bukan `NULL`, bukan `-`, bukan `0`) |
| **Dampak** | ETL tools bisa interpretasi beda |
| **Saran** | **Standarisasi:** Replace semua sel kosong dengan `NULL` (atau `0` jika konteksnya memang 0) |

---

### 3. Baris Total di Akhir File (Semua File)

| Properti | Detail |
|----------|--------|
| **Masalah** | Semua file punya baris Total di akhir yang merupakan agregasi |
| **Dampak** | Jika dimuat ke database, bisa double-counting |
| **Saran** | **Beri flag `is_total_row`** atau pisahkan ke metadata |
| **Catatan** | ✅ Domestik Ranking: Footer tanpa label `,,402447,...`<br>✅ Domestik Bulanan: Footer dengan label `Total,,...`<br>✅ Internasional Ranking: Footer dengan label `Total,,...` |

---

### 4. Nama Kolom Tidak Standard (Semua File)

| Properti | Detail |
|----------|--------|
| **Masalah** | Nama kolom panjang, ada spasi, ada special chars: `RUTE (PP)`, `JUMLAH BARANG (Kg)`, `L/F`, `Jan-20` |
| **Dampak** | Query SQL harus quote, tidak mengikuti naming convention |
| **Saran** | **Rename ke snake_case:** `route_pp`, `total_flights`, `cargo_kg`, `load_factor_pct`, `m01_2020`, dll |

---

### 5. Format Rute Tidak Konsisten (Semua File)

| Properti | Detail |
|----------|--------|
| **Masalah** | Format rute variasi: `Jakarta (CGK)-SINGAPURA (SIN)`, `Kuala Lumpur (KUL)-Denpasar (DPS)`, ada yang truncated |
| **Dampak** | Sulit join antar file atau dengan tabel referensi |
| **Saran** | **Parse menjadi kolom terpisah:** `asal_kota`, `asal_iata`, `tujuan_kota`, `tujuan_iata` |

---

### 6. Primary Key Tidak Reliable (File Internasional)

| Properti | Detail |
|----------|--------|
| **Masalah** | Kolom `NO` di file Internasional tidak konsisten (ada skip, out-of-order: 147, 149, 150, 151, 152, **155, 154, 153**, 156, 157) |
| **Dampak** | Tidak bisa pakai `NO` sebagai primary key untuk file Internasional |
| **Saran** | **Generate surrogate key** (auto-increment ID). **File Domestik sudah OKE** (1-410 konsisten). |

---

### 7. Data COVID-19 Impact (Terkhusus 2020)

| Properti | Detail |
|----------|--------|
| **Observasi** | Semua file menunjukkan penurunan drastis 2020 vs 2019 (↓64-85%) |
| **Dampak** | Data 2020 tidak representatif untuk trend normal |
| **Saran** | **Beri flag `is_pandemic_year = TRUE`** dan dokumentasi sebagai outlier |

---

### 8. Masalah Khusus per File

| File | Masalah Khusus | Status |
|------|----------------|--------|
| **Internasional Bulanan** | Ada nilai `"KARGO"` di kolom numerik — perlu replace + flag | ⚠️ Masih ada |
| **Internasional Bulanan & Ranking** | Nomor urut tidak konsisten (ada skip & out-of-order) | ⚠️ Masih ada |
| **Domestik Bulanan & Ranking** | ~~Nomor urut tidak konsisten~~ | ✅ **SUDAH DIPERBAIKI** |

---

## 📐 Rekomendasi Skema Unified (Data Warehouse)

### Konsep: Star Schema (Dimension + Fact Tables)

Berdasarkan analisis 4 file, berikut rekomendasi skema unified yang bisa menampung semua data BAB VI:

```
┌─────────────────────────────────────────────────────────────┐
│ DIMENSION TABLES                                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  dim_rute                        dim_tanggal               │
│  ┌─────────────────────┐         ┌──────────────────┐      │
│  │ rute_id (PK)        │         │ tanggal_id (PK)  │      │
│  │ asal_kota           │         │ tahun            │      │
│  │ asal_iata           │         │ bulan            │      │
│  │ tujuan_kota         │         │ is_quarter_end   │      │
│  │ tujuan_iata         │         │ ...              │      │
│  │ kategori (dom/int)  │         └──────────────────┘      │
│  │ is_active           │                                    │
│  └─────────────────────┘                                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ FACT TABLES                                                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  fact_penumpang_bulanan (dari File Bulanan)                │
│  ┌──────────────────────────────────────────────────┐      │
│  │ fact_bulanan_id (PK)                             │      │
│  │ rute_id (FK → dim_rute)                         │      │
│  │ tanggal_id (FK → dim_tanggal)                   │      │
│  │ jumlah_penumpang (INT)                           │      │
│  │ is_estimated (BOOLEAN)                            │      │
│  │ is_pandemic_year (BOOLEAN)                        │      │
│  └──────────────────────────────────────────────────┘      │
│                                                             │
│  fact_statistik_rute (dari File Ranking)                   │
│  ┌──────────────────────────────────────────────────┐      │
│  │ statistik_id (PK)                                │      │
│  │ rute_id (FK → dim_rute)                         │      │
│  │ tahun (INT)                                      │      │
│  │ total_flights (INT)                              │      │
│  │ total_passengers (INT)                           │      │
│  │ total_seats (INT)                                │      │
│  │ cargo_kg (DECIMAL)                               │      │
│  │ postal_kg (DECIMAL)                              │      │
│  │ load_factor_pct (DECIMAL)                        │      │
│  │ is_pandemic_year (BOOLEAN)                        │      │
│  └──────────────────────────────────────────────────┘      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Penjelasan Tabel

#### 1. `dim_rute` (Dimension - Master Rute)

| Kolom | Tipe | Deskripsi |
|-------|------|-----------|
| `rute_id` | INT (PK) | Surrogate key unik per rute |
| `asal_kota` | VARCHAR | Nama kota asal (contoh: "Jakarta") |
| `asal_iata` | VARCHAR(3) | Kode IATA bandara asal (contoh: "CGK") |
| `tujuan_kota` | VARCHAR | Nama kota tujuan |
| `tujuan_iata` | VARCHAR(3) | Kode IATA bandara tujuan |
| `kategori` | VARCHAR | "Domestik" atau "Internasional" |
| `is_active` | BOOLEAN | TRUE jika rute masih beroperasi |

**Jumlah Baris Estimasi:** ~550 rute unik (410 domestik + ~140 internasional)

---

#### 2. `dim_tanggal` (Dimension - Time)

| Kolom | Tipe | Deskripsi |
|-------|------|-----------|
| `tanggal_id` | INT (PK) | Surrogate key (format: YYYYMMDD) |
| `tahun` | INT | Tahun (contoh: 2020) |
| `bulan` | INT | Bulan (1-12) |
| `bulan_nama` | VARCHAR | Nama bulan (contoh: "Januari") |
| `is_quarter_end` | BOOLEAN | TRUE jika akhir quarter |
| `is_pandemic_year` | BOOLEAN | TRUE untuk tahun 2020-2021 |

**Jumlah Baris Estimasi:** ~365 × N tahun

---

#### 3. `fact_penumpang_bulanan` (Fact - dari File Bulanan)

| Kolom | Tipe | Deskripsi |
|-------|------|-----------|
| `fact_bulanan_id` | INT (PK) | Surrogate key |
| `rute_id` | INT (FK) | Reference ke `dim_rute` |
| `tanggal_id` | INT (FK) | Reference ke `dim_tanggal` |
| `jumlah_penumpang` | INT | Jumlah penumpang di bulan tersebut |
| `is_estimated` | BOOLEAN | TRUE jika data estimasi (ada missing value) |
| `is_pandemic_year` | BOOLEAN | TRUE untuk 2020-2021 |

**Jumlah Baris Estimasi:** ~550 rute × 12 bulan = ~6,600 rows per tahun

---

#### 4. `fact_statistik_rute` (Fact - dari File Ranking)

| Kolom | Tipe | Deskripsi |
|-------|------|-----------|
| `statistik_id` | INT (PK) | Surrogate key |
| `rute_id` | INT (FK) | Reference ke `dim_rute` |
| `tahun` | INT | Tahun data (contoh: 2020) |
| `total_flights` | INT | Total penerbangan |
| `total_passengers` | INT | Total penumpang |
| `total_seats` | INT | Total kapasitas kursi |
| `cargo_kg` | DECIMAL | Total berat barang |
| `postal_kg` | DECIMAL | Total berat pos |
| `load_factor_pct` | DECIMAL | Load Factor (%) |
| `is_pandemic_year` | BOOLEAN | TRUE untuk 2020-2021 |

**Jumlah Baris Estimasi:** ~550 rute × 1 tahun = ~550 rows per tahun

---

### 📊 Alur ETL Unified

```
┌─────────────────────────────────────────────────────────────────────┐
│ ETL PIPELINE: BAB VI - Penumpang Per Rute                          │
└─────────────────────────────────────────────────────────────────────┘

1. EXTRACT
   ├── 4 file CSV 2020 (Domestik/Internasional × Bulanan/Ranking)
   └── Parse CSV dengan encoding UTF-8, delimiter comma

2. CLEANING
   ├── Replace sel kosong → NULL
   ├── Replace "KARGO" → NULL + flag is_cargo (Internasional Bulanan)
   ├── Clean Load Factor: "59,3%" → 59.3 (Ranking files)
   ├── Remove .0 suffix dari numerik (Internasional files)
   ├── Rename kolom ke snake_case
   └── Parse rute → asal_kota, asal_iata, tujuan_kota, tujuan_iata

3. TRANSFORM
   ├── Buat dim_rute (master rute unik dari semua file)
   ├── Buat dim_tanggal (tahun 2020 + months)
   ├── Unpivot file Bulanan → fact_penumpang_bulanan (long format)
   ├── Transform file Ranking → fact_statistik_rute
   ├── Add flag is_pandemic_year = TRUE
   └── Add flag is_total_row = FALSE (exclude total rows)

4. LOAD
   ├── Load dim_rute ke dimension table
   ├── Load dim_tanggal ke dimension table
   ├── Load fact_penumpang_bulanan ke fact table
   └── Load fact_statistik_rute ke fact table

5. VALIDATE
   ├── Check sum fact_penumpang_bulanan vs Total row di sumber
   ├── Check sum fact_statistik_rute vs Total row di sumber
   ├── Verify LF calculated vs source (toleransi 0.5%)
   └── Check duplicate routes di dim_rute
```

---

## 🎯 Rekomendasi Final

### 1. Format Target

| File | Format Source | Format Target | Alasan |
|------|---------------|---------------|--------|
| **Domestik Bulanan** | Wide (12 bulan) | **Long** (1 rute × 1 bulan) | Scalable, mudah time-series |
| **Internasional Bulanan** | Wide (12 bulan) | **Long** (1 rute × 1 bulan) | Konsisten dengan domestik |
| **Domestik Ranking** | Wide (6 metrik) | **Long** (1 rute × 1 tahun) | Mudah bandingkan tahun |
| **Internasional Ranking** | Wide (6 metrik) | **Long** (1 rute × 1 tahun) | Konsisten dengan domestik |

### 2. Prioritas Pre-Processing

| Prioritas | Task | Files Affected |
|-----------|------|----------------|
| 🔴 **Kritikal** | Clean missing value (sel kosong → NULL) | Semua 4 file |
| 🔴 **Kritikal** | Clean Load Factor format (`"XX,X%"` → XX.X) | 2 file Ranking |
| 🔴 **Kritikal** | Replace "KARGO" → NULL + flag | Internasional Bulanan |
| 🟡 **Penting** | Rename kolom ke snake_case | Semua 4 file |
| 🟡 **Penting** | Parse rute → asal/tujuan + IATA | Semua 4 file |
| 🟡 **Penting** | Generate surrogate key (terutama Internasional) | Internasional Bulanan & Ranking |
| 🟢 **Nice to Have** | Remove `.0` suffix dari numerik | 2 file Internasional |
| 🟢 **Nice to Have** | Add flag is_pandemic_year | Semua 4 file |

### 3. Scalability untuk Tahun 2021-2024

```
Jika struktur file 2021-2024 konsisten dengan 2020:

✅ dim_rute → Tambah rute baru jika ada
✅ dim_tanggal → Tambah tahun baru (otomatis)
✅ fact_penumpang_bulanan → INSERT data baru per bulan
✅ fact_statistik_rute → INSERT data baru per tahun

ESTIMASI TOTAL ROWS (5 tahun: 2020-2024):
├── dim_rute: ~550-600 routes
├── dim_tanggal: ~1,825 days (5 × 365)
├── fact_penumpang_bulanan: ~550 × 12 × 5 = ~33,000 rows
└── fact_statistik_rute: ~550 × 5 = ~2,750 rows
```

---

## 📋 Checklist Next Steps

### Untuk Tahun 2020 (Sekarang)
- [x] Review & update ke-2 file Domestik (setelah CSV diperbaiki)
- [x] Review ke-2 file Internasional (struktur masih sama)
- [x] Update summary file dengan angka yang benar
- [ ] Buat script pre-processing (Python/pandas)
- [ ] Test ETL pipeline dengan data 2020
- [ ] Validasi hasil vs Total rows di sumber

### Untuk Tahun 2021-2024 (Nanti)
- [ ] Cek konsistensi struktur file vs 2020
- [ ] Cek apakah file Internasional sudah diperbaiki (nomor urut konsisten?)
- [ ] Jika ada perbedaan, update dokumentasi
- [ ] Jalankan ETL pipeline yang sama (jika konsisten)
- [ ] Validasi cross-year data continuity

### Untuk Data Warehouse
- [ ] Setup database schema (dim_rute, dim_tanggal, fact tables)
- [ ] Setup ETL jobs (Airflow, dbt, atau manual)
- [ ] Setup data quality checks
- [ ] Setup dashboard/visualization (BI tools)

---

## 📝 Metadata Summary

| Properti | Nilai |
|----------|-------|
| **Analysis Date** | 2026-04-10 |
| **Last Updated** | 2026-04-10 (Revision 2) |
| **Analyzed By** | Data Engineer (AI Assistant) |
| **Tahun** | 2020 |
| **Jumlah File** | 4 |
| **Jumlah Total Baris** | 1,145 (termasuk header, total, footer) |
| **Jumlah Rute Domestik** | **410** (bulanan), **410** (ranking) — ✅ Konsisten |
| **Jumlah Rute Internasional** | ~147 (bulanan), ~147 (ranking) — ⚠️ Tidak konsisten |
| **Total Penumpang Domestik 2020** | 35,393,966 |
| **Total Penumpang Internasional 2020** | 7,187,439 |
| **Average Load Factor Domestik** | 58.7% |
| **Average Load Factor Internasional** | 56.8% |
| **COVID Impact** | ↓64-85% vs 2019 |
| **Revision Notes** | File Domestik diperbaiki: 521/467 → 412 baris dengan nomor konsisten |

---

> **Catatan:** Summary ini adalah rangkuman dari 4 file analisis individual. Untuk detail per file, lihat:
> - `CSV_ANALYSIS_2020_Domestik_Bulanan.md` ✅ Updated
> - `CSV_ANALYSIS_2020_Internasional_Bulanan.md` (Original)
> - `CSV_ANALYSIS_2020_Domestik_Ranking.md` ✅ Updated
> - `CSV_ANALYSIS_2020_Internasional_Ranking.md` (Original)
>
> **Revisi:** Summary ini diperbarui setelah CSV Domestik diperbaiki (dari 521/467 baris → 412 baris dengan struktur yang lebih konsisten). File Internasional belum diperbaiki dan masih punya inkonsistensi nomor urut.
>
> Untuk tahun lain (2021-2024), akan ada summary file terpisah dengan format serupa.
