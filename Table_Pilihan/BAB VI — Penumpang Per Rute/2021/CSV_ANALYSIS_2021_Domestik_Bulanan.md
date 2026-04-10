# CSV Analysis: Jumlah Penumpang Per Rute — Domestik Bulanan 2021

## 📊 Informasi Umum

| Properti | Nilai |
|----------|-------|
| **Nama File** | `JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI JAN-DES 2021.csv` |
| **Sumber** | Extract dari PDF (Kemenhub/DJPU) |
| **Periode** | Januari - Desember 2021 (plus komparasi 2020 & 2019) |
| **Jumlah Baris** | 381 (1 header + 379 rute + 1 Total) |
| **Jumlah Kolom** | 18 |
| **Tipe Data Utama** | Float (semua nilai punya suffix `.0`) |
| **Missing Value** | Sel kosong (tanpa nilai) |

---

## 🗂️ Struktur Tabel

### Skema Saat Ini

```
NO (int)
RUTE ( PP) (string - ada spasi setelah kurung)
Jan-21 (float)
Feb-21 (float)
Mar-21 (float)
Apr-21 (float)
Mei-21 (float) - ⚠️ Nama berbeda dari 2020 (bukan May-21)
Jun-21 (float)
Jul-21 (float)
Agu-21 (float) - ⚠️ Nama berbeda dari 2020 (bukan Aug-21)
Sep-21 (float)
Okt-21 (float) - ⚠️ Nama berbeda dari 2020 (bukan Oct-21)
Nov-21 (float)
Des-21 (float) - ⚠️ Nama berbeda dari 2020 (bukan Dec-21)
TOTAL 2021 (float)
TOTAL 2020 (float) - ⚠️ Kolom baru (di 2020: TOTAL 2019, TOTAL 2018)
TOTAL 2019 (float) - ⚠️ Kolom baru (di 2020: tidak ada)
```

### Detail Per Kolom

| No | Nama Kolom | Deskripsi | Tipe Data Saat Ini | Tipe Data Rekomendasi | Nullable | Contoh Nilai |
|----|-----------|-----------|-------------------|----------------------|----------|--------------|
| 1 | `NO` | Nomor urut rute | Integer | `INT` | ❌ No | `1`, `2`, ..., `379` |
| 2 | `RUTE ( PP)` | Rute pulang-pergi (Asal-Tujuan) | String | `VARCHAR(150)` | ❌ No | `Jakarta (CGK) - Denpasar (DPS)` |
| 3-14 | `Jan-21` s/d `Des-21` | Jumlah penumpang per bulan | Float | `DECIMAL(15,2)` | ✅ Yes | `107991.0`, `(kosong)` |
| 15 | `TOTAL 2021` | Total akumulasi 2021 | Float | `DECIMAL(15,2)` | ✅ Yes | `2002789.0` |
| 16 | `TOTAL 2020` | Total tahun 2020 (komparasi) | Float | `DECIMAL(15,2)` | ✅ Yes | `1549163.0` |
| 17 | `TOTAL 2019` | Total tahun 2019 (komparasi) | Float | `DECIMAL(15,2)` | ✅ Yes | `4384437.0` |

**⚠️ PERBEDAAN PENTING vs 2020:**
1. **Nama kolom bulan:** `Mei-21`, `Agu-21`, `Okt-21`, `Des-21` (bahasa Indonesia) vs `May-20`, `Aug-20`, `Oct-20`, `Dec-20` (bahasa Inggris) di 2020
2. **Kolom komparasi:** `TOTAL 2020`, `TOTAL 2019` vs `TOTAL 2019`, `TOTAL 2018` di 2020
3. **Tipe data:** Float (semua ada `.0`) vs Integer di 2020
4. **Format rute:** Ada spasi setelah dash `Jakarta (CGK) - Denpasar (DPS)` vs `Jakarta (CGK)-Denpasar (DPS)` di 2020

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
  - `Jakarta (CGK) - Denpasar (DPS)` — ⚠️ Spasi tambahan
  - `Makassar (UPG) - Surabaya (SUB)`
  - `"Jakarta (CGK) - Praya, Lombok (LOP)"` (ada koma dalam nama kota)
- **Catatan:** 
  - Semua rute **pulang-pergi (PP)**
  - IATA code dalam kurung: CGK, DPS, SUB, UPG, dll.
  - ⚠️ **Perbedaan dengan 2020:** Spasi di format rute

#### 3. Kolom Bulanan (`Jan-21` s/d `Des-21`)
- **Tipe:** Float dengan suffix `.0` (contoh: `107991.0`)
- **Range:** 0 (kosong/rute belum ada) hingga 484,186
- **Missing Value:** Sel kosong
- **Visualisasi Data Sample:**

```
┌─────┬────────────────────────────────┬─────────┬─────────┬──────────┬─────────┬───────┬──────────┐
│ NO  │ RUTE                           │ Jan-21  │ Feb-21  │ Mar-21   │ Apr-21  │ ...   │ Des-21   │
├─────┼────────────────────────────────┼─────────┼─────────┼──────────┼─────────┼───────┼──────────┤
│ 1   │ CGK - DPS (Jakarta-Bali)       │107991.0 │76081.0  │129566.0  │145001.0 │ ...   │373333.0  │
│ 2   │ CGK - UPG (Jakarta-Makassar)   │132428.0 │117623.0 │158762.0  │156018.0 │ ...   │197107.0  │
│ 3   │ CGK - KNO (Jakarta-Medan)      │167440.0 │110650.0 │138147.0  │140087.0 │ ...   │264694.0  │
│ ... │ ...                            │ ...     │ ...     │ ...      │ ...     │ ...   │ ...      │
│ 379 │ (rute terakhir)                │         │         │          │         │ ...   │          │
└─────┴────────────────────────────────┴─────────┴─────────┴──────────┴─────────┴───────┴──────────┘
```

#### 4. Kolom Total (`TOTAL 2021`, `TOTAL 2020`, `TOTAL 2019`)
- **Format:** Float dengan suffix `.0` (contoh: `2002789.0`)
- **Baris Total (akhir file):** `33336639.0` (2021), `35393966.0` (2020), `100490773.0` (2019) — perlu verifikasi dari footer
- **Insight:** Penurunan 2021 vs 2019 masih signifikan, tapi ada recovery dari 2020

---

## ⚠️ Potensi Masalah & Saran Pre-Processing

### 1. Format Float dengan Suffix `.0`

| Properti | Detail |
|----------|--------|
| **Masalah** | Semua nilai numerik punya suffix `.0` (contoh: `107991.0`) karena parsing sebagai float |
| **Dampak** | • Tidak efisien untuk storage<br>• Tampil kurang rapi |
| **Saran** | **Convert ke integer** untuk kolom bulanan (karena penumpang harus whole number) |

**Visualisasi Transformasi:**
```
SEBELUM:  107991.0  →  SESUDAH:  107991
SEBELUM:  2002789.0 →  SESUDAH:  2002789
```

---

### 2. Nama Kolom Bulan Berbeda vs 2020

| Properti | Detail |
|----------|--------|
| **Masalah** | Nama kolom bulan 2021 pakai bahasa Indonesia: `Mei-21`, `Agu-21`, `Okt-21`, `Des-21` vs 2020 pakai bahasa Inggris: `May-20`, `Aug-20`, `Oct-20`, `Dec-20` |
| **Dampak** | • Script ETL yang hardcode nama kolom dari 2020 akan gagal di 2021<br>• Sulit unify kolom jika gabungkan data multi-tahun |
| **Saran** | **Standardisasi ke format netral:** `m01_2021`, `m02_2021`, `m03_2021`, ..., `m12_2021` untuk semua tahun |

**Perbandingan:**
```
2020: Jan-20, Feb-20, Mar-20, Apr-20, May-20, Jun-20, Jul-20, Aug-20, Sep-20, Oct-20, Nov-20, Dec-20
2021: Jan-21, Feb-21, Mar-21, Apr-21, Mei-21, Jun-21, Jul-21, Agu-21, Sep-21, Okt-21, Nov-21, Des-21

Standard: m01_2020, m02_2020, ..., m12_2020
          m01_2021, m02_2021, ..., m12_2021
```

---

### 3. Format Rute dengan Spasi Tambahan

| Properti | Detail |
|----------|--------|
| **Masalah** | Format rute 2021: `Jakarta (CGK) - Denpasar (DPS)` (ada spasi sebelum & setelah dash) vs 2020: `Jakarta (CGK)-Denpasar (DPS)` (tanpa spasi) |
| **Dampak** | • Sulit join data 2020 vs 2021 berdasarkan nama rute<br>• Akan dianggap rute berbeda padahal sama |
| **Saran** | **Standardisasi format rute** — hapus spasi tambahan atau buat mapping table |

**Visualisasi:**
```
2020: "Jakarta (CGK)-Denpasar (DPS)"     ← Tanpa spasi
2021: "Jakarta (CGK) - Denpasar (DPS)"   ← Dengan spasi

Standard: "Jakarta (CGK)-Denpasar (DPS)" ← Pilih salah satu
```

---

### 4. Missing Value Tidak Seragam (Sel Kosong)

| Properti | Detail |
|----------|--------|
| **Masalah** | Banyak sel kosong tanpa nilai |
| **Dampak** | ETL tools bisa interpretasi beda |
| **Saran** | **Standarisasi:** Replace semua sel kosong dengan `NULL` |

---

### 5. Baris Total di Akhir File

| Properti | Detail |
|----------|--------|
| **Masalah** | Baris terakhir `Total,,339638.0,33336639.0,...` adalah agregasi sum semua rute |
| **Dampak** | Jika dimuat ke database, bisa double-counting |
| **Saran** | **Beri flag atau pisahkan:** Tambahkan kolom `is_total_row` (TRUE/FALSE) |

**Visualisasi:**
```
┌─────┬──────────┬─────────┬───────────┬─────────────┐
│ NO  │ RUTE     │ Jan-21  │ Feb-21    │ TOTAL 2021  │
├─────┼──────────┼─────────┼───────────┼─────────────┤
│ 1   │ CGK-DPS  │107991.0 │76081.0    │2002789.0    │
│ ... │ ...      │ ...     │ ...       │ ...         │
│ -   │ **Total**│339638.0 │73959.0    │**33336639** │ ⚠️
└─────┴──────────┴─────────┴───────────┴─────────────┘
```

---

### 6. Kolom Nama Tidak Standard

| Properti | Detail |
|----------|--------|
| **Masalah** | Nama kolom ada spasi: `RUTE ( PP)`, `JUMLAH BARANG (Kg)` |
| **Dampak** | Query SQL harus quote |
| **Saran** | **Rename ke snake_case:** `route_pp`, `total_flights`, dll |

---

## 📐 Rekomendasi Skema Database (Gambaran)

### Opsi A: Wide Format (Seperti CSV Asli)

**Konsep:** Satu tabel dengan kolom bulan melebar

**Struktur Logis:**
```
┌──────┬──────────────────┬──────────┬──────────┬──────┬──────────┬──────────┬──────────┐
│ ID   │ Rute             │ Jan-21   │ Feb-21   │ ...  │ Des-21   │ TOTAL 21 │ TOTAL 20 │
├──────┼──────────────────┼──────────┼──────────┼──────┼──────────┼──────────┼──────────┤
│ 1    │ CGK - DPS        │107991.0  │76081.0   │ ...  │373333.0  │2002789   │1549163   │
│ 2    │ CGK - UPG        │132428.0  │117623.0  │ ...  │197107.0  │1750282   │1579052   │
└──────┴──────────────────┴──────────┴──────────┴──────┴──────────┴──────────┴──────────┘
```

**Kolom yang Dibutuhkan:**
- **Primary Key** (auto-generated ID)
- **Rute** (VARCHAR): format "Asal (IATA) - Tujuan (IATA)" — perlu standardisasi spasi
- **Kolom per Bulan** (INT): m01_2021, m02_2021, ..., m12_2021
- **Kolom Total Tahun** (DECIMAL): total_2021, total_2020, total_2019
- **Flag Total Row** (BOOLEAN)

**Kelebihan:** 
- ✅ Simple, sesuai format sumber
- ✅ Query langsung tanpa JOIN

**Kekurangan:**
- ❌ Sulit query trend bulanan
- ❌ Row lebar (18 kolom)
- ❌ Tidak scalable untuk data tahun lain

**Kapan Pakai Opsi Ini?**
→ Jika hanya untuk **reporting static 2021**

---

### Opsi B: Long Format (Recommended)

**Konsep:** Satu tabel vertikal dengan satu baris = satu rute + satu bulan

**Tabel: FactPenumpang_bulanan (Fact Table)**
```
┌──────────┬──────────────┬──────┬───────┬────────────┐
│ ID (PK)  │ Rute         │ Tahun│ Bulan │ Penumpang  │
├──────────┼──────────────┼──────┼───────┼────────────┤
│ 1        │ CGK - DPS    │ 2021 │ 01    │ 107991     │
│ 2        │ CGK - DPS    │ 2021 │ 02    │ 76081      │
│ 3        │ CGK - DPS    │ 2021 │ 03    │ 129566     │
│ ...      │ ...          │ ...  │ ...   │ ...        │
└──────────┴──────────────┴──────┴───────┴────────────┘
```

**Struktur Logis:**
- **Primary Key** (ID unik per record)
- **Rute** (VARCHAR): atau Foreign Key ke tabel master rute
- **Tahun** (INT): 2021, 2020, 2019
- **Bulan** (INT): 1-12
- **Penumpang** (INT): jumlah penumpang
- **Flag Total Row** (BOOLEAN)
- **Kategori Rute** (VARCHAR): "Domestik"

**Kelebihan:**
- ✅ Mudah query trend & time-series
- ✅ Mudah agregasi per bulan atau per tahun
- ✅ Scalable jika ada data tahun baru
- ✅ Optimal untuk analytics dashboard

**Kekurangan:**
- ❌ Baris lebih banyak (379 rute × 12 bulan = ~4,548 rows)
- ❌ Kolom TOTAL 2019/2020 perlu handling terpisah

**Kapan Pakai Opsi Ini?**
→ Jika data akan dipakai untuk **trend analysis, forecasting, atau dibandingkan dengan tahun lain**

---

### 📊 Perbandingan Kedua Opsi

| Aspek | Wide Format | Long Format |
|-------|-------------|-------------|
| **Jumlah Tabel** | 1 | 1 (atau 2 jika ada master rute) |
| **Jumlah Baris** | 379 | ~4,548 (379 rute × 12 bulan) |
| **Jumlah Kolom** | 18 | 5-6 |
| **Query Trend Bulanan** | Kompleks (unpivot dulu) | Simple (GROUP BY bulan) |
| **Query Total Tahunan** | Langsung (pakai kolom total) | Perlu agregasi SUM |
| **Cocok untuk** | Reporting statis | Analytics & BI |
| **Kompleksitas** | Rendah | Medium |

---

### 🎯 Rekomendasi Final

**Untuk Use Case Data Warehouse:**

```
Pakai LONG FORMAT (Opsi B) karena:
  ✅ Data warehouse biasanya untuk analytics jangka panjang
  ✅ Mudah bandingkan performa antar bulan/tahun
  ✅ Skalabel jika ada data 2022, 2023, dst
  ✅ Optimal untuk dashboard & visualization
```

**Alur ETL Sederhana:**
```
CSV Mentah → Pre-Processing → Load ke Staging → Transform → Load ke Production
     ↓            ↓              ↓              ↓            ↓
  (Parsing    (Clean NULL,   (Tabel       (Unpivot,    (Tabel final
   CSV)        Remove .0,    Sementara)   Standardize  siap pakai)
               Rename,                    Rute format,
               Flag Total)                Add Tahun)
```

---

## 🎯 Kesimpulan & Next Steps

### Masalah Kritikal (Harus Ditangani)
1. ✅ Suffix `.0` pada semua nilai numerik (convert ke integer)
2. ✅ Nama kolom bulan berbeda vs 2020 (standardisasi)
3. ✅ Format rute dengan spasi tambahan (standardisasi vs 2020)
4. ✅ Missing value (sel kosong → `NULL`)
5. ✅ Baris Total perlu flag/isolasi

### Masalah Struktural (Pertimbangkan Transformasi)
1. ⚠️ Wide → Long format (untuk scalability)
2. ⚠️ Parse rute menjadi asal/tujuan + IATA code
3. ⚠️ Context metadata (COVID-19 recovery 2021)

### Next Steps untuk File Ini
- [ ] Tentukan format target (wide vs long)
- [ ] Buat script pre-processing (cleaning + standardisasi nama kolom & rute)
- [ ] Validasi hasil cleaning (sum vs Total row)
- [ ] Bandingkan dengan file 2020 (pastikan rute yang sama bisa di-join)

---

## 📝 Metadata Tambahan

| Properti | Nilai |
|----------|-------|
| **Analysis Date** | 2026-04-10 |
| **Analyzed By** | Data Engineer (AI Assistant) |
| **Jumlah Rute Unik** | 379 |
| **Total Penumpang 2021** | 33,336,639 (perlu verifikasi dari footer) |
| **Total Penumpang 2020** | 35,393,966 (dari kolom TOTAL 2020) |
| **Total Penumpang 2019** | ~100M (dari kolom TOTAL 2019) |
| **Growth 2021 vs 2020** | ↓ -5.8% (perlu verifikasi) |
| **Growth 2021 vs 2019** | ↓ -66.8% (perlu verifikasi) |
| **Encoding** | UTF-8 (asumsi) |
| **Delimiter** | `,` (comma) |
| **Missing Value** | Sel kosong (bukan `-` atau `NULL`) |

**Perbedaan Penting vs 2020:**
| Aspek | 2020 | 2021 |
|-------|------|------|
| **Jumlah Baris** | 412 | **381** |
| **Jumlah Rute** | 410 | **379** |
| **Nama Kolom Bulan** | May-20, Aug-20, Oct-20, Dec-20 | **Mei-21, Agu-21, Okt-21, Des-21** |
| **Kolom Komparasi** | TOTAL 2019, TOTAL 2018 | **TOTAL 2020, TOTAL 2019** |
| **Tipe Data** | Integer | **Float** |
| **Format Rute** | `Jakarta (CGK)-Denpasar (DPS)` | **`Jakarta (CGK) - Denpasar (DPS)`** (ada spasi) |

---

> **Catatan:** Dokumen ini hanya fokus pada file Domestik Bulanan 2021. Untuk analisis file lain dalam BAB VI, lihat file markdown terpisah.
> 
> **Penting:** File 2021 punya beberapa perbedaan struktur vs 2020 yang perlu di-handle saat ETL.
