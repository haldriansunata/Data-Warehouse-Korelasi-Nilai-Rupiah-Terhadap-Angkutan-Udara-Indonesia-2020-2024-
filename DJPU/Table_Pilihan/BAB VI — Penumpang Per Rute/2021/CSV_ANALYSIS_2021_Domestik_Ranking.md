# CSV Analysis: Statistik Per Rute — Domestik Ranking 2021

## 📊 Informasi Umum

| Properti | Nilai |
|----------|-------|
| **Nama File** | `STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2021 BERDASARKAN URUTAN JUMLAH PENUMPANG.csv` |
| **Sumber** | Extract dari PDF (Kemenhub/DJPU) |
| **Periode** | Tahun 2021 (ranking berdasarkan jumlah penumpang) |
| **Jumlah Baris** | 381 (1 header + 379 rute + 1 Total) |
| **Jumlah Kolom** | 8 |
| **Tipe Data Utama** | Float (semua nilai punya suffix `.0`) & String (persentase dengan koma) |
| **Missing Value** | Sel kosong (untuk beberapa rute baru/tidak beroperasi) |

---

## 🗂️ Struktur Tabel

### Skema Saat Ini

```
NO (int)
RUTE ( PP) (string - ada spasi setelah kurung)
JUMLAH PENERBANGAN (float)
JUMLAH PENUMPANG (float)
KAPASITAS SEAT (float)
JUMLAH BARANG (Kg) (float)
JUMLAH POS (float)
L/F (string - percentage dengan koma)
```

### Detail Per Kolom

| No | Nama Kolom | Deskripsi | Tipe Data Saat Ini | Tipe Data Rekomendasi | Nullable | Contoh Nilai |
|----|-----------|-----------|-------------------|----------------------|----------|--------------|
| 1 | `NO` | Nomor urut ranking | Integer | `INT` | ❌ No | `1`, `2`, ..., `379` |
| 2 | `RUTE ( PP)` | Rute pulang-pergi (Asal-Tujuan) | String | `VARCHAR(150)` | ❌ No | `Jakarta (CGK) - Denpasar (DPS)` |
| 3 | `JUMLAH PENERBANGAN` | Total penerbangan PP di 2021 | Float | `INT` | ✅ Yes | `14974.0` |
| 4 | `JUMLAH PENUMPANG` | Total penumpang di 2021 | Float | `INT` | ✅ Yes | `2002789.0` |
| 5 | `KAPASITAS SEAT` | Total kapasitas kursi tersedia | Float | `INT` | ✅ Yes | `2977867.0` |
| 6 | `JUMLAH BARANG (Kg)` | Total berat barang/kargo (kilogram) | Float | `DECIMAL(15,2)` | ✅ Yes | `21365798.0` |
| 7 | `JUMLAH POS` | Total berat pos (kilogram) | Float | `DECIMAL(15,2)` | ✅ Yes | `196771.0` |
| 8 | `L/F` | Load Factor (persentase okupansi) | String (format: `"XX,X%"`) | `DECIMAL(5,2)` | ✅ Yes | `"67,3%"`, `"0,0%"` |

**⚠️ PERBEDAAN PENTING vs 2020:**
1. **Tipe data:** Float (semua ada `.0`) vs Integer di 2020
2. **Format rute:** Ada spasi setelah dash `Jakarta (CGK) - Denpasar (DPS)` vs `Jakarta (CGK)-Denpasar (DPS)` di 2020
3. **Jumlah rute:** 379 vs 410 di 2020 (berkurang 31 rute)

---

## 🔍 Analisis Nilai Unik & Distribusi

### Kolom Kategorikal

#### 1. `NO`
- **Nilai Unik:** 379 (1-379)
- **Range:** 1 sampai 379
- **Catatan:** ✅ **KONSISTEN** — file punya 381 baris (header + 379 rute + Total), nomor urut 1-379 sequential tanpa skip

#### 2. `RUTE ( PP)`
- **Nilai Unik:** 379 rute domestik
- **Format:** `Kota Asal (KODE_IATA) - Kota Tujuan (KODE_IATA)` — ⚠️ **Ada spasi sebelum & setelah dash**
- **Contoh:**
  - `Jakarta (CGK) - Denpasar (DPS)`
  - `"Jakarta (CGK) - Praya, Lombok (LOP)"` (ada koma dalam nama)
- **Catatan:** 
  - Semua rute **pulang-pergi (PP)**
  - Ranking berdasarkan `JUMLAH PENUMPANG` (descending)

#### 3. `JUMLAH PENERBANGAN`
- **Tipe:** Float dengan suffix `.0`
- **Range:** 0 hingga 15,789
- **Top 3 Rute Terbanyak:**
  1. Jakarta (CGK) - Makassar (UPG): 15,789 penerbangan
  2. Jakarta (CGK) - Denpasar (DPS): 14,974 penerbangan
  3. Jakarta (CGK) - Medan (KNO): 14,397 penerbangan

#### 4. `JUMLAH PENUMPANG`
- **Tipe:** Float dengan suffix `.0`
- **Range:** 0 hingga 2,002,789
- **Top 3 Rute Teramai:**
  1. Jakarta (CGK) - Denpasar (DPS): 2,002,789 penumpang
  2. Jakarta (CGK) - Makassar (UPG): 1,750,282 penumpang
  3. Jakarta (CGK) - Medan (KNO): 1,735,789 penumpang

#### 5. `KAPASITAS SEAT`
- **Tipe:** Float dengan suffix `.0`
- **Range:** 0 hingga 2,977,867
- **Insight:** Kapasitas > penumpang → Load Factor < 100% (normal)

#### 6. `JUMLAH BARANG (Kg)`
- **Tipe:** Float dengan suffix `.0`
- **Range:** 0 hingga 28,754,522 kg
- **Insight:** Rute CGK-UPG juga bawa barang terbanyak (28.75M kg)

#### 7. `JUMLAH POS`
- **Tipe:** Float dengan suffix `.0`
- **Range:** 0 hingga 789,774 kg
- **Insight:** Rute CGK-UPG punya pos tertinggi (789,774 kg)

#### 8. `L/F` (Load Factor)
- **Tipe:** String dengan koma desimal & simbol `%`
- **Format:** `"XX,X%"` (contoh: `"67,3%"`)
- **Range:** `"0,0%"` (rute tidak aktif) hingga `"73,5%"`
- **Top 3 Load Factor Tertinggi:**
  1. Makassar (UPG) - Kendari (KDI): 73.5%
  2. Medan (KNO) - Batam (BTH): 73.5%
  3. Surabaya (SUB) - Praya, Lombok (LOP): 73.3%
- **Rute dengan LF 0%:** Rute di akhir list (350-378) — tidak beroperasi di 2021

**Visualisasi Data Sample:**
```
┌─────┬────────────────────────────────┬───────────┬─────────────┬───────────┬────────────┬─────────┬────────┐
│ NO  │ RUTE                           │ Flights   │ Passengers  │  Seats    │ Cargo (Kg) │   Pos   │  L/F   │
├─────┼────────────────────────────────┼───────────┼─────────────┼───────────┼────────────┼─────────┼────────┤
│ 1   │ CGK - DPS (Jakarta-Bali)       │  14974.0  │  2,002,789  │ 2,977,867 │ 21,365,798 │ 196,771 │ 67.3%  │
│ 2   │ CGK - UPG (Jakarta-Makassar)   │  15789.0  │  1,750,282  │ 2,679,920 │ 28,754,522 │ 789,774 │ 65.3%  │
│ 3   │ CGK - KNO (Jakarta-Medan)      │  14397.0  │  1,735,789  │ 2,540,826 │ 26,521,622 │ 335,986 │ 68.3%  │
│ ... │ ...                            │    ...    │     ...     │    ...    │     ...    │    ...  │ ...    │
│ 379 │ BKS - TKG (Bengkulu-Lampung)   │      0.0  │          0  │         0 │          0 │       0 │  0.0%  │
└─────┴────────────────────────────────┴───────────┴─────────────┴───────────┴────────────┴─────────┴────────┘
```

#### 9. Baris Total (Akhir File)
- **JUMLAH PENERBANGAN:** 339,638
- **JUMLAH PENUMPANG:** 33,336,639
- **KAPASITAS SEAT:** 50,123,416
- **JUMLAH BARANG:** 417,048,368 kg
- **JUMLAH POS:** 5,278,756 kg
- **L/F Rata-rata:** 66.5%

---

## ⚠️ Potensi Masalah & Saran Pre-Processing

### 1. Format Load Factor dengan Koma Desimal

| Properti | Detail |
|----------|--------|
| **Masalah** | Load Factor menggunakan koma sebagai desimal (`"67,3%"`) bukan titik (`67.3`) |
| **Dampak** | Database/ETL tools akan gagal parse langsung ke `DECIMAL` |
| **Saran** | Lakukan 3 langkah cleaning: (1) Hapus simbol `%`, (2) Ganti koma `,` menjadi titik `.`, (3) Konversi ke numerik (DECIMAL) |

**Visualisasi Transformasi:**
```
SEBELUM:  "67,3%"  →  SESUDAH:  67.3
SEBELUM:  "0,0%"   →  SESUDAH:  0.0
```

---

### 2. Format Float dengan Suffix `.0`

| Properti | Detail |
|----------|--------|
| **Masalah** | Semua nilai numerik punya suffix `.0` (contoh: `14974.0`, `2002789.0`) |
| **Dampak** | • Tidak efisien untuk storage<br>• Tampil kurang rapi |
| **Saran** | **Convert ke integer** untuk kolom numerik |

**Visualisasi Transformasi:**
```
SEBELUM:  14974.0     →  SESUDAH:  14974
SEBELUM:  2002789.0   →  SESUDAH:  2002789
SEBELUM:  2977867.0   →  SESUDAH:  2977867
```

---

### 3. Format Rute dengan Spasi Tambahan (Perlu Standardisasi vs 2020)

| Properti | Detail |
|----------|--------|
| **Masalah** | Format rute 2021: `Jakarta (CGK) - Denpasar (DPS)` (ada spasi) vs 2020: `Jakarta (CGK)-Denpasar (DPS)` (tanpa spasi) |
| **Dampak** | • Sulit join data 2020 vs 2021 berdasarkan nama rute |
| **Saran** | **Standardisasi format rute** — hapus spasi tambahan agar konsisten dengan 2020 |

**Visualisasi:**
```
2020: "Jakarta (CGK)-Denpasar (DPS)"     ← Tanpa spasi
2021: "Jakarta (CGK) - Denpasar (DPS)"   ← Dengan spasi

Standard: "Jakarta (CGK)-Denpasar (DPS)" ← Pilih format 2020
```

---

### 4. Rute dengan Load Factor 0% (Tidak Beroperasi)

| Properti | Detail |
|----------|--------|
| **Masalah** | Beberapa rute di akhir list (350-378) punya LF `"0,0%"` dan semua metrik kosong/0 |
| **Dampak** | • Data tidak informatif<br>• Bisa skew average LF |
| **Saran** | **Beri flag:** Tambahkan kolom `is_active = FALSE` untuk rute dengan LF = 0% |

**Contoh Rute Tidak Aktif:** 29 rute (350-378)

---

### 5. Nama Kolom Tidak Standard

| Properti | Detail |
|----------|--------|
| **Masalah** | Nama kolom panjang dan pakai spasi: `RUTE ( PP)`, `JUMLAH BARANG (Kg)` |
| **Dampak** | Query SQL harus quote |
| **Saran** | **Rename ke snake_case:** `route_pp`, `total_flights`, `cargo_kg`, `load_factor_pct` |

---

### 6. Baris Total di Akhir File

| Properti | Detail |
|----------|--------|
| **Masalah** | Baris terakhir `Total,,339638.0,33336639.0,...` adalah agregasi sum semua rute |
| **Dampak** | Jika dimuat ke database, bisa double-counting |
| **Saran** | **Beri flag:** Tambahkan kolom `is_total_row = TRUE` |

---

### 7. Load Factor sebagai Metrik Calculated

| Properti | Detail |
|----------|--------|
| **Observasi** | Load Factor (L/F) sebenarnya bisa dihitung: `LF = JUMLAH PENUMPANG / KAPASITAS SEAT × 100%` |
| **Saran** | **Simpan keduanya:** L/F dari sumber + bisa recalculate untuk verifikasi |

**Formula Verifikasi:**
```
L/F Calculated = (JUMLAH PENUMPANG ÷ KAPASITAS SEAT) × 100

Contoh: CGK - DPS
  L/F Source     = 67.3%
  L/F Calculated = (2,002,789 ÷ 2,977,867) × 100 = 67.26%
  Difference     = 0.04% ✅ OK (rounding difference)
```

---

## 📐 Rekomendasi Skema Database (Gambaran)

### Opsi A: Wide Format (Seperti CSV Asli)

**Konsep:** Satu tabel dengan semua metrik per rute

**Struktur Logis:**
```
┌──────┬──────────────────┬─────────┬────────────┬───────────┬────────────┬────────┬────────┐
│ ID   │ Rute             │ Flights │ Passengers │   Seats   │ Cargo_Kg   │  Pos   │   LF   │
├──────┼──────────────────┼─────────┼────────────┼───────────┼────────────┼────────┼────────┤
│ 1    │ CGK - DPS        │  14974  │  2,002,789 │ 2,977,867 │ 21,365,798 │196,771 │ 67.3%  │
│ 2    │ CGK - UPG        │  15789  │  1,750,282 │ 2,679,920 │ 28,754,522 │789,774 │ 65.3%  │
└──────┴──────────────────┴─────────┴────────────┴───────────┴────────────┴────────┴────────┘
```

**Kelebihan:** 
- ✅ Simple, sesuai format sumber
- ✅ Semua metrik langsung tersedia

**Kekurangan:**
- ❌ Hanya 1 tahun (2021)
- ❌ Ada redundancy (LF bisa calculated)

---

### Opsi B: Long Format (Recommended)

**Konsep:** Satu tabel vertikal dengan satu baris = satu rute + satu tahun

**Struktur Logis:**
- **Primary Key** (ID unik per record)
- **Rute** (VARCHAR)
- **Tahun** (INT): 2021
- **Total Flights** (INT)
- **Total Passengers** (INT)
- **Total Seats** (INT)
- **Cargo Kg** (DECIMAL)
- **Postal Kg** (DECIMAL)
- **Load Factor %** (DECIMAL)
- **Is Active** (BOOLEAN): LF > 0

**Kelebihan:**
- ✅ Mudah bandingkan tahun
- ✅ Scalable untuk historis data

**Kapan Pakai Opsi Ini?**
→ Jika data akan **dibandingkan dengan tahun lain**

---

## 🎯 Kesimpulan & Next Steps

### Masalah Kritikal (Harus Ditangani)
1. ✅ Suffix `.0` pada semua nilai numerik (convert ke integer)
2. ✅ Load Factor format (`"67,3%"` → `67.3`)
3. ✅ Format rute dengan spasi tambahan (standardisasi vs 2020)
4. ✅ Kolom nama perlu rename (snake_case)
5. ✅ Baris Total perlu flag/isolasi
6. ✅ Rute tidak aktif (LF = 0%) perlu flag

### Next Steps untuk File Ini
- [ ] Tentukan format target (wide vs long)
- [ ] Buat script pre-processing
- [ ] Validasi LF calculated vs source
- [ ] Bandingkan dengan file 2020

---

## 📝 Metadata Tambahan

| Properti | Nilai |
|----------|-------|
| **Analysis Date** | 2026-04-10 |
| **Analyzed By** | Data Engineer (AI Assistant) |
| **Jumlah Rute Unik** | 379 |
| **Total Penumpang 2021** | 33,336,639 |
| **Total Penerbangan** | 339,638 |
| **Average Load Factor** | 66.5% |
| **Rute Tidak Aktif (LF=0%)** | 29 rute (350-378) |
| **Perbedaan vs 2020** | Jumlah rute berkurang 31 (410 → 379), format Float, ada spasi di rute |

---

> **Catatan:** Dokumen ini hanya fokus pada file Domestik Ranking 2021. Untuk analisis file lain dalam BAB VI, lihat file markdown terpisah.
