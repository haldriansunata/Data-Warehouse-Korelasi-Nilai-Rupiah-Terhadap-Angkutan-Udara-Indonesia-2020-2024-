# CSV Analysis: Statistik Per Rute — Domestik Ranking 2023

## 📊 Informasi Umum

| Properti | Nilai |
|----------|-------|
| **Nama File** | `STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2023 BERDASARKAN URUTAN JUMLAH PENUMPANG.csv` |
| **Jumlah Baris** | 306 (1 header + 303 rute + 1 Total + 1 empty) |
| **Jumlah Kolom** | 8 |
| **Format Rute** | Hanya IATA code (`CGK-DPS`) |
| **Format Angka** | Float dengan `.0` suffix |
| **Load Factor** | String dengan koma desimal (tanpa quotes!) |

---

## ⚠️ PERBEDAAN SANGAT PENTING vs 2020-2022

### 1. Format Load Factor TANPA Quotes!

| Tahun | Format Load Factor | Contoh |
|-------|-------------------|--------|
| **2020-2022** | String dengan quotes | `"80,6%"` |
| **2023** | **String TANPA quotes** | `80.6%` |

**Ini perubahan KRUSIAL!** Load Factor 2023 tidak pakai quotes lagi dan pakai titik (bukan koma)!

### 2. Format Rute Hanya IATA Code (Sama seperti 2022)

| Tahun | Format | Contoh |
|-------|--------|--------|
| **2020-2021** | Nama kota + IATA | `Jakarta (CGK)-Denpasar (DPS)` |
| **2022-2023** | **Hanya IATA code** | `CGK-DPS` |

### 3. Jumlah Rute

| Tahun | Jumlah Rute Domestik |
|-------|---------------------|
| **2020** | 410 |
| **2021** | 379 |
| **2022** | 374 |
| **2023** | **303** (berkurang 71 rute dari 2022!) |

---

## 🗂️ Struktur Tabel

### Skema Saat Ini

```
NO (int)
RUTE (string - IATA only)
JUMLAH PENERBANGAN (float)
JUMLAH PENUMPANG (float)
KAPASITAS SEAT (float)
JUMLAH BARANG (float)
JUMLAH POS (float)
L/F (string - TANPA quotes, titik desimal!)
```

### Detail Per Kolom

| No | Nama Kolom | Deskripsi | Tipe Data Saat Ini | Tipe Data Rekomendasi | Nullable | Contoh Nilai |
|----|-----------|-----------|-------------------|----------------------|----------|--------------|
| 1 | `NO` | Nomor urut | Integer | `INT` | ❌ No | `1`, `2`, ..., `303` |
| 2 | `RUTE` | Rute (IATA only) | String | `VARCHAR(20)` | ❌ No | `CGK-DPS` |
| 3 | `JUMLAH PENERBANGAN` | Total penerbangan 2023 | Float | `INT` | ✅ Yes | `33262.0` |
| 4 | `JUMLAH PENUMPANG` | Total penumpang 2023 | Float | `INT` | ✅ Yes | `4961724.0` |
| 5 | `KAPASITAS SEAT` | Kapasitas kursi | Float | `INT` | ✅ Yes | `6154776.0` |
| 6 | `JUMLAH BARANG` | Berat barang | Float | `DECIMAL` | ✅ Yes | `17882030.0` |
| 7 | `JUMLAH POS` | Berat pos | Float | `DECIMAL` | ✅ Yes | `16693.0` |
| 8 | `L/F` | Load Factor | String (titik desimal, tanpa quotes) | `DECIMAL(5,2)` | ✅ Yes | `80.6%` |

**⚠️ PENTING:** Load Factor 2023 pakai **titik** sebagai desimal dan **TANPA quotes**, berbeda dari 2020-2022 yang pakai koma dan quotes!

---

## 🔍 Analisis Nilai Unik & Distribusi

### Top Routes 2023

| Rank | Rute | Penumpang | Penerbangan | Load Factor |
|------|------|-----------|-------------|-------------|
| 1 | CGK-DPS | 4,961,724 | 33,262 | 80.6% |
| 2 | CGK-KNO | 3,414,822 | 22,046 | 84.9% |
| 3 | CGK-SUB | 3,065,045 | 21,360 | 81.7% |
| 4 | CGK-UPG | 2,636,673 | 17,999 | 81.8% |
| 5 | CGK-BPN | 1,628,679 | 11,064 | 82.4% |

### Load Factor
- **Format:** `80.6%` (titik desimal, tanpa quotes)
- **Range:** `0.0%` hingga `89.0%`
- **Average:** 80.2% (dari Total row)
- **Top 3 LF:**
  1. SUB-LOP: 89.0%
  2. CGK-TKG: 86.1%
  3. KNO-BTH: 86.1%

### Baris Total
- **JUMLAH PENERBANGAN:** 517,490
- **JUMLAH PENUMPANG:** 65,925,924
- **KAPASITAS SEAT:** 82,206,402
- **JUMLAH BARANG:** 451,898,766 kg
- **JUMLAH POS:** 861,725 kg
- **L/F Rata-rata:** 80.2%

---

## ⚠️ Potensi Masalah & Saran Pre-Processing

### 1. Format Load Factor BERUBAH Total! (KRUSIAL!)

| Properti | Detail |
|----------|--------|
| **Masalah** | 2023: `80.6%` (titik, tanpa quotes) vs 2020-2022: `"80,6%"` (koma, dengan quotes) |
| **Dampak** | • Parser untuk 2020-2022 akan gagal di 2023<br>• Perlu logic berbeda per tahun |
| **Saran** | **Parser dinamis:**<br>- 2020-2022: Hapus quotes, replace `,` → `.`<br>- 2023: Hapus `%` saja |

**Visualisasi Transformasi:**
```
2020-2022:  "80,6%"  →  "80.6%"  →  80.6
2023:       80.6%    →  "80.6"   →  80.6
```

### 2. Format Rute Hanya IATA Code

| Properti | Detail |
|----------|--------|
| **Masalah** | `CGK-DPS` vs 2020-2021: nama kota lengkap |
| **Saran** | **Mapping table** IATA code ↔ nama kota |

### 3. Format Float dengan `.0`

| Properti | Detail |
|----------|--------|
| **Saran** | Remove `.0` suffix, convert ke integer |

### 4. Jumlah Rute Berkurang Drastis

| Properti | Detail |
|----------|--------|
| **Observasi** | 2022: 374 → 2023: **303** (↓ 71 rute) |
| **Saran** | Track route lifecycle dengan flag `is_active` per tahun |

### 5. Baris Total dengan Label

| Properti | Detail |
|----------|--------|
| **Format** | `Total,,517490.0,65925924.0,...` |
| **Saran** | Flag `is_total_row = TRUE` |

---

## 📐 Rekomendasi Skema Database

**Sama seperti tahun sebelumnya — Long Format recommended.**

---

## 🎯 Kesimpulan & Next Steps

### Masalah Kritikal
1. ✅ **Format Load Factor berubah total** (titik vs koma, tanpa quotes vs dengan quotes)
2. ✅ Format rute hanya IATA code
3. ✅ Format float dengan `.0`
4. ✅ Jumlah rute berkurang drastis
5. ✅ Baris Total perlu flag

### Next Steps
- [ ] Buat parser Load Factor yang handle kedua format (2020-2022 vs 2023)
- [ ] Mapping table IATA code
- [ ] Remove `.0` dari nilai float
- [ ] Unpivot ke long format

---

## 📝 Metadata Tambahan

| Properti | Nilai |
|----------|-------|
| **Analysis Date** | 2026-04-10 |
| **Jumlah Rute** | 303 |
| **Total Penumpang 2023** | 65,925,924 |
| **Total Penerbangan** | 517,490 |
| **Average Load Factor** | 80.2% |
| **Perbedaan Signifikan** | Load Factor format (titik vs koma, tanpa quotes), rute berkurang 71 |

---

> **Catatan:** Dokumen ini hanya fokus pada file Domestik Ranking 2023. Perubahan format Load Factor di 2023 memerlukan penanganan khusus saat ETL.
