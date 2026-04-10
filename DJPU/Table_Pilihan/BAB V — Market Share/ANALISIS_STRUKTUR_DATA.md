# 📊 Analisis Struktur Data — Market Share Penumpang Angkutan Udara Dalam Negeri

## 📋 Informasi Umum

| Properti | Detail |
|----------|--------|
| **Nama File** | `TABEL MARKET SHARE PENUMPANG ANGKUTAN UDARA DALAM NEGERI BERDASARKAN BADAN USAHA ANGKUTAN UDARA NIAGA NASIONAL TAHUN 2019-2024.csv` |
| **Sumber** | Direktorat Jenderal Perhubungan Udara (DJPU) |
| **Periode Data** | 2019 - 2024 |
| **Jumlah Baris** | 16 (15 operator + 1 total) |
| **Jumlah Kolom** | 13 |
| **Tipe Data** | CSV (Comma-Separated Values) |

---

## 🔍 Struktur Kolom Saat Ini

### 1️⃣ Kolom Identifikasi

| No | Nama Kolom | Tipe Data | Format | Deskripsi | Contoh |
|----|-----------|-----------|--------|-----------|--------|
| 1 | `NO` | String/VARCHAR | Numerik sebagai identifier | Nomor urut operator (1-15), baris TOTAL menggunakan "-" | `"1"`, `"2"`, `"-"` |
| 2 | `OPERATOR` | String/VARCHAR | Teks | Nama resmi badan usaha angkutan udara niaga nasional | `"PT. GARUDA INDONESIA (Persero) Tbk."` |

### 2️⃣ Kolom Data Tahunan (Berulang per Tahun)

**Pola:** Setiap tahun memiliki 2 kolom: `(Penumpang)` dan `(%)`

| Tahun | Kolom Penumpang | Kolom Persentase | Tipe Data | Format | Deskripsi |
|-------|----------------|------------------|-----------|--------|-----------|
| **2019** | `2019 (Penumpang)` | `2019 (%)` | String → NUMERIC | `15.542.662` / `"19,56%"` | Jumlah penumpang & market share |
| **2020** | `2020 (Penumpang)` | `2020 (%)` | String → NUMERIC | `4.619.487` / `"13,05%"` | Jumlah penumpang & market share |
| **2021** | `2021 (Penumpang)` | `2021 (%)` | String → NUMERIC | `3.490.812` / `"10,46%"` | Jumlah penumpang & market share |
| **2022** | `2022 (Penumpang)` | `2022 (%)` | String → NUMERIC | `4.646.651` / `"8,24%"` | Jumlah penumpang & market share |
| **2023** | `2023 (Penumpang)` | `2023 (%)` | String → NUMERIC | `6.314.490` / `"9,57%"` | Jumlah penumpang & market share |
| **2024** | `2024 (Penumpang)` | `2024 (%)` | String → NUMERIC | `8.665.055` / `"13,16%"` | Jumlah penumpang & market share |

---

## ⚠️ Tantangan & Masalah yang Dihadapi

### 🔴 TANTANGAN 1: Format Data Tidak Standar

#### **Masalah:**
- **Tribune Separator (Titik Ribuan):** Angka menggunakan format Indonesia `15.542.662` (titik sebagai pemisah ribuan)
- **Format Persentase:** Menggunakan koma desimal Indonesia `"19,56%"` dengan simbol persen
- **Tipe Data String:** Semua kolom tersimpan sebagai string, bukan numerik

#### **Dampak:**
- Tidak bisa langsung di-import ke kolom NUMERIC/DECIMAL
- Harus melalui proses cleaning & transformation
- Riskan terjadi error parsing jika tidak ditangani

#### **Solusi:**
```
Before: "15.542.662" → Remove "." → Cast to BIGINT → 15542662
Before: "19,56%"     → Remove "%" → Replace "," with "." → Cast to DECIMAL → 19.56
```

---

### 🔴 TANTANGAN 2: Missing Data / Nilai Null

#### **Masalah:**
- Beberapa sel menggunakan karakter `"-"` yang menandakan **tidak ada data** atau **operator belum beroperasi**
- Contoh: `PT. SUPER AIR JET` di 2019-2020 memiliki nilai `"-"`

#### **Dampak:**
- Tidak bisa langsung dikonversi ke numerik
- Perlu diputuskan: apakah diganti dengan `0`, `NULL`, atau tetap sebagai special marker

#### **Solusi:**
```
"-" → NULL (recommended untuk analisis) atau 0 (jika artinya benar-benar nol penumpang)
```

---

### 🔴 TANTANGAN 3: Struktur Wide Format (Tidak Normalized)

#### **Masalah:**
- Data dalam format **WIDE** (kolom bertambah per tahun)
- Jika ada data 2025, harus tambah kolom baru → **tidak scalable**
- Sulit untuk query time-series (misal: trend pertumbuhan per tahun)

#### **Visualisasi Masalah:**

```
┌─────────────────────────────────────────────────────────────────────┐
│  STRUKTUR SAAT INI (WIDE FORMAT)                                    │
├─────────────────────────────────────────────────────────────────────┤
│  Operator  │ 2019_Pax │ 2019_% │ 2020_Pax │ 2020_% │ ...          │
├─────────────────────────────────────────────────────────────────────┤
│  Garuda    │ 15.5M    │ 19.56% │ 4.6M     │ 13.05% │ ...          │
│  Lion      │ 23.7M    │ 29.87% │ 12.5M    │ 35.36% │ ...          │
│  Citilink  │ 11.8M    │ 14.93% │ 5.4M     │ 15.32% │ ...          │
└─────────────────────────────────────────────────────────────────────┘
         ↓
  ❌ Jika ada tahun baru → HARUS ALTER TABLE (tambah kolom)
  ❌ Sulit query: "Berapa rata-rata pertumbuhan per tahun?"
  ❌ Sulit agregasi: "Total market share per tahun"
```

#### **Solusi:**
**Transform ke LONG/NORMALIZED Format** (lihat rekomendasi struktur di bawah)

---

### 🔴 TANTANGAN 4: Baris TOTAL

#### **Masalah:**
- Baris terakhir adalah agregasi (`TOTAL`) yang bercampur dengan data operator
- `NO` kolom menggunakan `"-"` bukan angka
- Jika tidak difilter, akan terhitung double saat agregasi

#### **Solusi:**
- Pisahkan ke tabel terpisah atau beri flag `is_total = TRUE`
- Atau hilangkan dari tabel utama (total bisa dihitung via SQL `SUM()`)

---

### 🔴 TANTANGAN 5: Nama Operator Tidak Konsisten

#### **Masalah:**
- Nama operator bisa berubah dari tahun ke tahun (rebranding, merger, akuisisi)
- Contoh: `PT. TRAVEL EXPRESS AVIATION SERVICES` mungkin sama dengan `PT. CITILINK INDONESIA` (perlu validasi bisnis)

#### **Dampak:**
- Sulit tracking operator yang berganti nama
- Risiko duplikasi entitas

#### **Solusi:**
- Buat **lookup table** untuk operator dengan kode unik
- Tambah kolom `operator_code` sebagai primary key

---

## ✅ Rekomendasi Struktur Database (Normalized)

### 📐 Konsep: Pisahkan jadi 2 Tabel

```
┌──────────────────────┐         ┌──────────────────────────┐
│  dim_airline         │         │  fact_market_share       │
│  (Master Maskapai)   │         │  (Data Tahunan)          │
├──────────────────────┤         ├──────────────────────────┤
│ • airline_id (PK)    │────┐    │ • airline_id (FK)        │
│ • airline_name       │    └───▶│ • year                   │
│ • airline_code       │    1:N  │ • passenger_count        │
│ • is_active          │         │ • market_share_pct       │
└──────────────────────┘         └──────────────────────────┘
```

**Intinya:**
- **Tabel 1** → Simpan daftar maskapai (sekali input, bisa dipakai berulang)
- **Tabel 2** → Simpan data tahunan (1 maskapai = banyak row untuk tiap tahun)

---

### 🎁 Keuntungan Struktur Baru

```
┌──────────────────────────────────────────────────────────────────┐
│  PERBANDINGAN: STRUKTUR LAMA vs BARU                              │
└──────────────────────────────────────────────────────────────────┘

┌─────────────────────────┬────────────────────────────────────────┐
│ ❌ STRUKTUR LAMA         │ ✅ STRUKTUR BARU                       │
├─────────────────────────┼────────────────────────────────────────┤
│ • Wide format (13 kolom)│ • Long format (6 kolom utama)          │
│ • Sulit extend tahun    │ • Mudah tambah tahun (insert row)      │
│ • Tipe data string      │ • Tipe data numerik siap analisis      │
│ • Missing data "-"      │ • NULL handling proper                 │
│ • TOTAL row bercampur   │ • TOTAL bisa di-CALCULATE via SQL      │
│ • Sulit query time-series│• Mudah: GROUP BY year, airline        │
│ • Tidak ada PK          │ • Ada PK, FK, constraints              │
│ • Redundansi data       │ • Normalized (3NF)                     │
└─────────────────────────┴────────────────────────────────────────┘
```

---

## 📈 Transformasi Data: Before → After

### Visualisasi Transformasi Row

```
┌─────────────────────────────────────────────────────────────────┐
│  ROW TRANSFORMATION (1 Row Wide → 6 Rows Long)                   │
└─────────────────────────────────────────────────────────────────┘

BEFORE (1 Row):
┌─────────┬────────────┬────────────┬──────────┬────────────┬──────────┐
│ NO      │ OPERATOR   │ 2019 (Pax) │ 2019 (%) │ 2020 (Pax) │ 2020 (%) │
├─────────┼────────────┼────────────┼──────────┼────────────┼──────────┤
│ 1       │ Garuda     │ 15.542.662 │ 19,56%   │ 4.619.487  │ 13,05%   │
└─────────┴────────────┴────────────┴──────────┴────────────┴──────────┘

AFTER (2 Rows untuk 2 tahun):
┌────────────┬──────┬───────────────┬─────────────────┐
│ airline_id │ year │ passenger_cnt │ market_share_pct│
├────────────┼──────┼───────────────┼─────────────────┤
│ 1          │ 2019 │ 15542662      │ 19.56           │
│ 1          │ 2020 │ 4619487       │ 13.05           │
└────────────┴──────┴───────────────┴─────────────────┘
```

---

## 📝 Kesimpulan

| Aspek | Status Saat Ini | Setelah Transformasi |
|-------|----------------|---------------------|
| **Format** | Wide (13 kolom) | Long (6 kolom) ✅ |
| **Tipe Data** | String | Numeric (BIGINT, DECIMAL) ✅ |
| **Scalability** | Rendah (harus ALTER TABLE) | Tinggi (hanya INSERT) ✅ |
| **Query Complexity** | Tinggi | Rendah ✅ |
| **Data Quality** | Rentan error | Validated & constrained ✅ |
| **Normalization** | Denormalized | 3NF ✅ |

---

*📅 Analisis dibuat: April 2026*  
*👤 Role: Senior Data Engineer*  
*📊 Dataset: Market Share Penumpang Angkutan Udara Dalam Negeri 2019-2024*
