# CSV Analysis: Statistik Per Rute — Internasional Ranking 2021

## 📊 Informasi Umum

| Properti | Nilai |
|----------|-------|
| **Nama File** | `STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI TAHUN 2021 BERDASARKAN URUTAN JUMLAH PENUMPANG.csv` |
| **Sumber** | Extract dari PDF (Kemenhub/DJPU) |
| **Periode** | Tahun 2021 (ranking berdasarkan jumlah penumpang) |
| **Jumlah Baris** | 148 (1 header + 145 rute + 1 Total + 1 footer) |
| **Jumlah Kolom** | 8 |
| **Tipe Data Utama** | Float (semua nilai punya suffix `.0`) & String (persentase dengan koma) |
| **Missing Value** | Sel kosong |

---

## 🗂️ Struktur Tabel

### Skema Saat Ini

```
NO (int)
RUTE (string)
JUMLAH PENERBANGAN (float)
JUMLAH PENUMPANG (float)
KAPASITAS SEAT (float)
JUMLAH BARANG (float) - ⚠️ Tidak ada "(Kg)" seperti Domestik
JUMLAH POS (float)
L/F (string - percentage dengan koma)
```

### Detail Per Kolom

| No | Nama Kolom | Deskripsi | Tipe Data Saat Ini | Tipe Data Rekomendasi | Nullable | Contoh Nilai |
|----|-----------|-----------|-------------------|----------------------|----------|--------------|
| 1 | `NO` | Nomor urut ranking | Integer | `INT` | ❌ No | `1`, `2`, ..., `145` |
| 2 | `RUTE` | Rute internasional | String | `VARCHAR(150)` | ❌ No | `Jakarta (CGK) - Singapura (SIN)` |
| 3 | `JUMLAH PENERBANGAN` | Total penerbangan di 2021 | Float | `INT` | ✅ Yes | `6190.0` |
| 4 | `JUMLAH PENUMPANG` | Total penumpang di 2021 | Float | `INT` | ✅ Yes | `199358.0` |
| 5 | `KAPASITAS SEAT` | Total kapasitas kursi | Float | `INT` | ✅ Yes | `960938.0` |
| 6 | `JUMLAH BARANG` | Total berat barang | Float | `DECIMAL(15,2)` | ✅ Yes | `77876539.0` |
| 7 | `JUMLAH POS` | Total berat pos | Float | `DECIMAL(15,2)` | ✅ Yes | `118699.0` |
| 8 | `L/F` | Load Factor | String (format: `"XX,X%"`) | `DECIMAL(5,2)` | ✅ Yes | `"20,7%"`, `"0,0%"` |

**⚠️ PERBEDAAN PENTING vs 2020:**
1. **Tipe data:** Float vs Integer di 2020
2. **Format rute:** Ada spasi `Jakarta (CGK) - Singapura (SIN)` vs `Jakarta (CGK)-SINGAPURA (SIN)` di 2020
3. **Jumlah rute:** 145 vs ~147 di 2020
4. **Nomor urut:** ✅ Konsisten 1-145 (tidak ada skip seperti 2020)
5. **Tidak ada footer `* Rute Codeshare...`** di 2021

---

## 🔍 Analisis Nilai Unik & Distribusi

### Kolom Kategorikal

#### 1. `NO`
- **Nilai Unik:** 145 (1-145) — ✅ **KONSISTEN** (tidak ada skip)

#### 2. `RUTE`
- **Nilai Unik:** 145 rute internasional
- **Format:** `Kota Asal (KODE_IATA) - Kota Tujuan (KODE_IATA)` — ⚠️ **Ada spasi**

#### 3. `JUMLAH PENERBANGAN`
- **Tipe:** Float dengan suffix `.0`
- **Range:** 0 hingga 6,190
- **Top 3:**
  1. Jakarta (CGK) - Singapura (SIN): 6,190
  2. Jakarta (CGK) - Doha (DOH): 1,418
  3. Jakarta (CGK) - Dubai (DXB): 999

#### 4. `JUMLAH PENUMPANG`
- **Tipe:** Float dengan suffix `.0`
- **Range:** 0 hingga 199,358
- **Top 3:**
  1. Jakarta (CGK) - Singapura (SIN): 199,358
  2. Jakarta (CGK) - Doha (DOH): 194,624
  3. Jakarta (CGK) - Dubai (DXB): 173,989

#### 5. `L/F` (Load Factor)
- **Tipe:** String dengan koma desimal
- **Format:** `"XX,X%"`
- **Range:** `"0,0%"` hingga `"61,4%"`
- **Top 3:**
  1. Praya, Lombok (LOP) - Kuala Lumpur (KUL): 61.4%
  2. Jakarta (CGK) - Doha (DOH): 50.8%
  3. Jakarta (CGK) - Istanbul (IST): 49.5%
- **Rute dengan LF 0%:** Banyak (125-144) — tidak beroperasi di 2021

#### 6. Baris Total
- **JUMLAH PENERBANGAN:** 21,562
- **JUMLAH PENUMPANG:** 1,190,882
- **KAPASITAS SEAT:** 4,414,309
- **JUMLAH BARANG:** 288,635,951
- **JUMLAH POS:** 1,527,788
- **L/F Rata-rata:** 27.0%

---

## ⚠️ Potensi Masalah & Saran Pre-Processing

### 1. Format Float dengan Suffix `.0`

| Properti | Detail |
|----------|--------|
| **Masalah** | Semua nilai punya `.0` |
| **Saran** | **Convert ke integer** |

### 2. Format Load Factor dengan Koma Desimal

| Properti | Detail |
|----------|--------|
| **Masalah** | `"20,7%"` bukan `20.7` |
| **Saran** | **Replace `,` → `.` dan hapus `%`** |

### 3. Format Rute dengan Spasi

| Properti | Detail |
|----------|--------|
| **Masalah** | `Jakarta (CGK) - Singapura (SIN)` vs 2020: `Jakarta (CGK)-SINGAPURA (SIN)` |
| **Saran** | **Standardisasi:** hapus spasi, uppercase IATA |

### 4. Rute dengan LF 0%

| Properti | Detail |
|----------|--------|
| **Masalah** | ~20 rute di akhir list tidak beroperasi |
| **Saran** | **Flag** `is_active = FALSE` |

### 5. Nama Kolom Tidak Standard

| Properti | Detail |
|----------|--------|
| **Masalah** | `JUMLAH BARANG` (tanpa satuan) |
| **Saran** | **Rename** ke snake_case: `cargo_kg` |

### 6. Baris Total

| Properti | Detail |
|----------|--------|
| **Saran** | **Flag** `is_total_row = TRUE` |

---

## 📐 Rekomendasi Skema Database

**Sama seperti file lain — Long Format recommended.**

---

## 🎯 Kesimpulan & Next Steps

### Masalah Kritikal
1. ✅ Suffix `.0` pada semua nilai
2. ✅ Load Factor format koma desimal
3. ✅ Format rute dengan spasi (perlu standardisasi vs 2020)
4. ✅ Nama kolom tidak standard
5. ✅ Baris Total perlu flag
6. ✅ Rute tidak aktif (LF = 0%) perlu flag

### Next Steps
- [ ] Convert Float ke Integer
- [ ] Clean Load Factor
- [ ] Standardisasi format rute
- [ ] Unpivot ke long format

---

## 📝 Metadata Tambahan

| Properti | Nilai |
|----------|-------|
| **Analysis Date** | 2026-04-10 |
| **Analyzed By** | Data Engineer (AI Assistant) |
| **Jumlah Rute Unik** | 145 |
| **Total Penumpang 2021** | 1,190,882 |
| **Total Penerbangan** | 21,562 |
| **Average Load Factor** | 27.0% |
| **Rute Tidak Aktif (LF=0%)** | ~20 rute (125-144) |
| **Perbedaan vs 2020** | Nomor konsisten, tidak ada "KARGO", tidak ada footer codeshare, ada spasi di rute |

---

> **Catatan:** Dokumen ini hanya fokus pada file Internasional Ranking 2021.
