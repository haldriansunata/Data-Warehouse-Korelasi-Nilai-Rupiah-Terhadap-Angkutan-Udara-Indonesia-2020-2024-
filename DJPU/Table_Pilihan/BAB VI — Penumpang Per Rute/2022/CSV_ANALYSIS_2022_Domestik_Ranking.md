# CSV Analysis: Statistik Per Rute — Domestik Ranking 2022

## 📊 Informasi Umum

| Properti | Nilai |
|----------|-------|
| **Nama File** | `STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2022 BERDASARKAN URUTAN JUMLAH PENUMPANG.csv` |
| **Sumber** | Extract dari PDF (Kemenhub/DJPU) |
| **Periode** | Tahun 2022 (ranking berdasarkan jumlah penumpang) |
| **Jumlah Baris** | 377 (1 header + 374 rute + 1 Total + 1 empty) |
| **Jumlah Kolom** | 8 |
| **Tipe Data Utama** | Float (titik = pemisah ribuan untuk beberapa kolom) & String (persentase dengan koma) |
| **Missing Value** | Sel kosong |

---

## ⚠️ PERBEDAAN SANGAT SIGNIFIKAN vs 2020-2021

### 1. Format Rute Hanya IATA Code

| Tahun | Format | Contoh |
|-------|--------|--------|
| **2020-2021** | Nama kota + IATA | `Jakarta (CGK)-Denpasar (DPS)` |
| **2022** | **Hanya IATA code** | `CGK-DPS` |

### 2. Format Angka dengan Titik sebagai Pemisah Ribuan

| Kolom | Format 2022 | Contoh |
|-------|-------------|--------|
| `JUMLAH PENERBANGAN` | Float dengan titik = ribuan | `29.803` (= 29,803) |
| `JUMLAH PENUMPANG` | Float dengan titik = ribuan | `4342921.0` (= 4,342,921) |
| `KAPASITAS SEAT` | Float dengan titik = ribuan | `5586084.0` |
| `JUMLAH BARANG (Kg)` | Float dengan titik = ribuan | `17811490.0` |
| `JUMLAH POS` | Float dengan titik = ribuan | `73.244` (= 73,244) |

### 3. Jumlah Rute

| Tahun | Jumlah Rute |
|-------|-------------|
| **2020** | 410 |
| **2021** | 379 |
| **2022** | **374** |

---

## 🗂️ Struktur Tabel

### Skema Saat Ini

```
NO (float - ada .0)
RUTE ( PP) (string - hanya IATA code)
JUMLAH PENERBANGAN (float - titik = ribuan)
JUMLAH PENUMPANG (float - titik = ribuan)
KAPASITAS SEAT (float - titik = ribuan)
JUMLAH BARANG (Kg) (float - titik = ribuan)
JUMLAH POS (float - titik = ribuan)
L/F (string - percentage dengan koma)
```

### Detail Per Kolom

| No | Nama Kolom | Deskripsi | Tipe Data Saat Ini | Tipe Data Rekomendasi | Nullable | Contoh Nilai |
|----|-----------|-----------|-------------------|----------------------|----------|--------------|
| 1 | `NO` | Nomor urut | Float | `INT` | ❌ No | `1.0`, `2.0`, ... |
| 2 | `RUTE ( PP)` | Rute (IATA only) | String | `VARCHAR(20)` | ❌ No | `CGK-DPS` |
| 3 | `JUMLAH PENERBANGAN` | Total penerbangan 2022 | Float (titik = ribuan) | `INT` | ✅ Yes | `29.803` (= 29,803) |
| 4 | `JUMLAH PENUMPANG` | Total penumpang 2022 | Float (titik = ribuan) | `INT` | ✅ Yes | `4342921.0` |
| 5 | `KAPASITAS SEAT` | Kapasitas kursi | Float (titik = ribuan) | `INT` | ✅ Yes | `5586084.0` |
| 6 | `JUMLAH BARANG (Kg)` | Berat barang | Float (titik = ribuan) | `DECIMAL` | ✅ Yes | `17811490.0` |
| 7 | `JUMLAH POS` | Berat pos | Float (titik = ribuan) | `DECIMAL` | ✅ Yes | `73.244` (= 73,244) |
| 8 | `L/F` | Load Factor | String (`"XX,X%"`) | `DECIMAL(5,2)` | ✅ Yes | `"77,7%"` |

---

## 🔍 Analisis Nilai Unik & Distribusi

### Top Routes 2022

| Rank | Rute | Penumpang | Penerbangan | Load Factor |
|------|------|-----------|-------------|-------------|
| 1 | CGK-DPS | 4,342,921 | 29,803 | 77.7% |
| 2 | CGK-KNO | 3,246,059 | 21,891 | 82.9% |
| 3 | CGK-SUB | 2,594,148 | 17,822 | 84.1% |
| 4 | CGK-UPG | 2,531,093 | 17,450 | 82.0% |
| 5 | CGK-PNK | 1,607,535 | 11,443 | 81.8% |

### Load Factor
- **Range:** `"0,0%"` hingga `"86,4%"`
- **Average:** 78.7% (dari Total row)
- **Top 3 LF:**
  1. CGK-PLM: 86.4%
  2. CGK-TKG: 83.8%
  3. KNO-BTH: 83.5%

### Baris Total
- **JUMLAH PENERBANGAN:** 464,282
- **JUMLAH PENUMPANG:** 56,408,353
- **KAPASITAS SEAT:** 71,706,732
- **JUMLAH BARANG:** 436,587,038 kg
- **JUMLAH POS:** 1,840,319 kg
- **L/F Rata-rata:** 78.7%

---

## ⚠️ Potensi Masalah & Saran Pre-Processing

### 1. Format Angka dengan Titik sebagai Pemisah Ribuan (KRUSIAL!)

| Properti | Detail |
|----------|--------|
| **Masalah** | Angka pakai titik sebagai pemisah ribuan: `29.803` = 29,803 |
| **Saran** | **Parsing khusus:** Baca string → hapus titik → convert ke integer |

**Visualisasi:**
```
SEBELUM:  "29.803"    →  "29803"   →  29803
SEBELUM:  "73.244"    →  "73244"   →  73244
SEBELUM:  "4342921.0" →  "4342921" →  4342921
```

### 2. Format Rute Hanya IATA Code

| Properti | Detail |
|----------|--------|
| **Masalah** | `CGK-DPS` vs 2020-2021: `Jakarta (CGK)-Denpasar (DPS)` |
| **Saran** | **Mapping table** IATA → nama kota |

### 3. Load Factor Koma Desimal

| Properti | Detail |
|----------|--------|
| **Masalah** | `"77,7%"` bukan `77.7` |
| **Saran** | **Replace `,` → `.` dan hapus `%`** |

### 4. Rute dengan LF 0%

- **Jumlah:** ~3 rute (372-374)
- **Saran:** Flag `is_active = FALSE`

### 5. Baris Total Tanpa Label

- **Format:** `,,464282.0,56408353.0,...`
- **Saran:** Flag `is_total_row = TRUE`

---

## 📐 Rekomendasi Skema Database

**Sama seperti tahun sebelumnya — Long Format recommended.**

---

## 🎯 Kesimpulan & Next Steps

### Masalah Kritikal
1. ✅ **Format angka dengan titik sebagai pemisah ribuan**
2. ✅ **Format rute hanya IATA code**
3. ✅ Load Factor koma desimal
4. ✅ Missing value
5. ✅ Baris Total perlu flag

### Next Steps
- [ ] Parser khusus untuk titik sebagai pemisah ribuan
- [ ] Mapping table IATA code
- [ ] Clean Load Factor
- [ ] Unpivot ke long format

---

## 📝 Metadata Tambahan

| Properti | Nilai |
|----------|-------|
| **Analysis Date** | 2026-04-10 |
| **Jumlah Rute** | 374 |
| **Total Penumpang 2022** | 56,408,353 |
| **Total Penerbangan** | 464,282 |
| **Average Load Factor** | 78.7% |
| **Perbedaan Signifikan** | Format rute (IATA only), angka dengan titik sebagai ribuan |

---

> **Catatan:** Dokumen ini hanya fokus pada file Domestik Ranking 2022.
