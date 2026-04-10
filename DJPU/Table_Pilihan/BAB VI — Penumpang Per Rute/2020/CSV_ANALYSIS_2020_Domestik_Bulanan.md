# CSV Analysis: Jumlah Penumpang Per Rute — Domestik Bulanan 2020

## 📊 Informasi Umum

| Properti | Nilai |
|----------|-------|
| **Nama File** | `JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI JAN-DES 2020.csv` |
| **Sumber** | Extract dari PDF (Kemenhub/DJPU) |
| **Periode** | Januari - Desember 2020 (plus komparasi 2019 & 2018) |
| **Jumlah Baris** | 412 (1 header + 410 rute + 1 Total) |
| **Jumlah Kolom** | 18 |
| **Tipe Data Utama** | Integer (angka penumpang bulanan) |
| **Missing Value** | Sel kosong (tanpa nilai) |

---

## 🗂️ Struktur Tabel

### Skema Saat Ini

```
NO (int)
RUTE (PP) (string)
Jan-20 (int)
Feb-20 (int)
Mar-20 (int)
Apr-20 (int)
May-20 (int)
Jun-20 (int)
Jul-20 (int)
Aug-20 (int)
Sep-20 (int)
Oct-20 (int)
Nov-20 (int)
Dec-20 (int)
TOTAL 2020 (float)
TOTAL 2019 (float)
TOTAL 2018 (float)
```

### Detail Per Kolom

| No | Nama Kolom | Deskripsi | Tipe Data Saat Ini | Tipe Data Rekomendasi | Nullable | Contoh Nilai |
|----|-----------|-----------|-------------------|----------------------|----------|--------------|
| 1 | `NO` | Nomor urut rute | Integer | `INT` | ❌ No | `1`, `2`, ..., `410` |
| 2 | `RUTE (PP)` | Rute pulang-pergi (Asal-Tujuan) | String | `VARCHAR(150)` | ❌ No | `Jakarta (CGK)-Makassar (UPG)` |
| 3-14 | `Jan-20` s/d `Dec-20` | Jumlah penumpang per bulan | Integer | `INT` | ✅ Yes | `231865`, `(kosong)` |
| 15 | `TOTAL 2020` | Total akumulasi 2020 | Float | `DECIMAL(15,2)` | ✅ Yes | `1579052.0` |
| 16 | `TOTAL 2019` | Total tahun 2019 (komparasi) | Float | `DECIMAL(15,2)` | ✅ Yes | `3607498.0` |
| 17 | `TOTAL 2018` | Total tahun 2018 (komparasi) | Float | `DECIMAL(15,2)` | ✅ Yes | `2886112.0` |

**Catatan:** Kolom `TOTAL 2018`, `TOTAL 2019`, `TOTAL 2020` memiliki suffix `.0` karena parsing CSV membaca sebagai float.

---

## 🔍 Analisis Nilai Unik & Distribusi

### Kolom Kategorikal

#### 1. `NO`
- **Nilai Unik:** 410 (1-410)
- **Range:** 1 sampai 410
- **Catatan:** ✅ **Sekarang KONSISTEN** — file punya 412 baris (header + 410 rute + Total), nomor urut 1-410 sequential tanpa skip

#### 2. `RUTE (PP)`
- **Nilai Unik:** 410 rute domestik
- **Format:** `Kota Asal (KODE_IATA)-Kota Tujuan (KODE_IATA)`
- **Contoh:**
  - `Jakarta (CGK)-Makassar (UPG)`
  - `Surabaya (SUB)-Denpasar (DPS)`
  - `"Praya, Lombok (LOP)-Majalengka (KJT)"` (ada koma dalam nama kota)
- **Catatan:** 
  - Semua rute **pulang-pergi (PP)** — data sudah agregasi PP
  - IATA code dalam kurung: CGK, DPS, SUB, UPG, dll.

#### 3. Kolom Bulanan (`Jan-20` s/d `Dec-20`)
- **Tipe:** Integer murni (tanpa desimal atau simbol)
- **Range:** 0 (kosong/rute belum ada) hingga 363,789
- **Missing Value:** Sel kosong (bukan `0`, bukan `-`)
- **Visualisasi Data Sample:**

```
┌─────┬──────────────────────────┬───────┬───────┬───────┬─────────┬───────┬─────────┐
│ NO  │ RUTE                     │ Jan-20│ Feb-20│ Mar-20│ Apr-20  │ ...   │ Dec-20  │
├─────┼──────────────────────────┼───────┼───────┼───────┼─────────┼───────┼─────────┤
│ 1   │ CGK-UPG (Jakarta-Mksr)   │231865 │237258 │188899 │  31636  │ ...   │ 181917  │
│ 2   │ CGK-DPS (Jakarta-Bali)   │363789 │302423 │190792 │  20611  │ ...   │ 212308  │
│ 3   │ CGK-SUB (Jakarta-Sby)    │317744 │317469 │228231 │  34134  │ ...   │ 158874  │
│ ... │ ...                      │ ...   │ ...   │ ...   │   ...   │ ...   │ ...     │
│ 410 │ TNJ-LMU (Tj.Pinang-Anmb) │       │       │       │         │ ...   │   1670  │
└─────┴──────────────────────────┴───────┴───────┴───────┴─────────┴───────┴─────────┘
```

#### 4. Kolom Total (`TOTAL 2020`, `TOTAL 2019`, `TOTAL 2018`)
- **Format:** Float dengan suffix `.0` (contoh: `1579052.0`)
- **Baris Total (akhir file):** `35393966.0` (2020), `100490773.0` (2019), `78906585.0` (2018)
- **Insight:** Penurunan drastis 2020 vs 2019 → dampak COVID-19 (↓64.7%)

---

## ⚠️ Potensi Masalah & Saran Pre-Processing

### 1. Missing Value Tidak Seragam (Sel Kosong)

| Properti | Detail |
|----------|--------|
| **Masalah** | Banyak sel kosong tanpa nilai (bukan `0`, bukan `NULL`, bukan `-`) |
| **Dampak** | ETL tools bisa interpretasi beda: ada yang baca sebagai `NULL`, ada yang error |
| **Saran** | **Standarisasi missing value:** Replace semua sel kosong dengan `NULL` (jika data memang belum ada) atau `0` (jika rute sudah ada tapi tidak ada penumpang). Berikan komentar/documentation untuk alasan pemilihan. |

**Visualisasi:**
```
SEBELUM:  (sel kosong)  →  SESUDAH:  NULL  (atau 0, tergantung konteks)
SEBELUM:  231865        →  SESUDAH:  231865  (tidak berubah)
```

**Contoh Rute dengan Banyak Missing:**
| Rute | Bulan Kosong | Kemungkinan Penyebab |
|------|--------------|---------------------|
| Baris 396-410 | Semua atau hampir semua bulan | Rute baru/ belum beroperasi di 2020 |

---

### 2. Wide Format (12 Kolom Bulan + 3 Total)

| Properti | Detail |
|----------|--------|
| **Masalah** | Struktur wide: 1 baris = 1 rute, 15 kolom waktu (12 bulan + 3 total tahun) |
| **Dampak** | • Sulit query time-series (trend bulanan)<br>• Sulit agregasi per bulan antar rute<br>• Tidak scalable jika nanti ada data bulanan tahun lain |
| **Saran** | **Pertimbangkan transformasi ke long format** (1 baris = 1 rute + 1 bulan + 1 tahun). Ini opsional tergantung kebutuhan analisis. |

**Perbandingan Format:**

```
┌─────────────────────────────────────────────────────────────┐
│ WIDE FORMAT (Saat Ini)                                      │
├─────────────┬───────┬───────┬───────┬────────┬──────┬──────────┤
│ Rute        │ Jan-20│ Feb-20│ Mar-20│ ...    │TOTAL20│ TOTAL19 │
├─────────────┼───────┼───────┼───────┼────────┼──────┼──────────┤
│ CGK-UPG     │231865 │237258 │188899 │ ...    │1.58M │  3.61M   │
│ CGK-DPS     │363789 │302423 │190792 │ ...    │1.55M │  4.77M   │
└─────────────┴───────┴───────┴───────┴────────┴──────┴──────────┘

┌──────────────────────────────────────────────┐
│ LONG FORMAT (Direkomendasikan untuk ETL)     │
├──────────────┬───────┬──────┬──────────┤
│ Rute         │ Tahun │ Bulan│ Penumpang│
├──────────────┼───────┼──────┼──────────┤
│ CGK-UPG      │ 2020  │ Jan  │ 231865     │
│ CGK-UPG      │ 2020  │ Feb  │ 237258     │
│ CGK-UPG      │ 2020  │ Mar  │ 188899     │
│ CGK-DPS      │ 2020  │ Jan  │ 363789     │
└──────────────┴───────┴──────┴──────────┘
```

---

### 3. Kolom Nama Menggunakan Pattern `Bulan-Tahun`

| Properti | Detail |
|----------|--------|
| **Masalah** | Nama kolom `Jan-20`, `Feb-20`, dll. menggabungkan bulan + tahun dengan dash |
| **Dampak** | • Sulit parse tahun & bulan secara terpisah<br>• Query SQL harus parsing string dulu |
| **Saran** | **Rename dengan format terstruktur**, contoh: `month_01_2020`, `month_02_2020`, atau pisahkan jadi kolom `bulan` dan `tahun` jika transform ke long format |

**Visualisasi Rename:**
```
SEBELUM:  Jan-20, Feb-20, Mar-20, ..., Dec-20
SESUDAH:  m01_2020, m02_2020, m03_2020, ..., m12_2020
```

---

### 4. Baris Total di Akhir File

| Properti | Detail |
|----------|--------|
| **Masalah** | Baris terakhir `Total,,6832548,...` adalah agregasi sum semua rute |
| **Dampak** | Jika dimuat ke database tanpa filter, bisa menyebabkan double-counting saat aggregasi |
| **Saran** | **Beri flag atau pisahkan:** Tambahkan kolom `is_total_row` (TRUE/FALSE), atau hapus dari data utama dan simpan sebagai metadata terpisah |

**Visualisasi:**
```
┌─────┬──────────┬────────┬─────────┬─────────────┐
│ NO  │ RUTE     │ Jan-20 │ Feb-20  │ TOTAL 2020  │
├─────┼──────────┼────────┼─────────┼─────────────┤
│ 1   │ CGK-UPG  │ 231865 │ 237258  │ 1579052.0   │
│ 2   │ CGK-DPS  │ 363789 │ 302423  │ 1549163.0   │
│ ... │ ...      │ ...    │ ...     │ ...         │
│ -   │ **Total**│6832548 │6274742  │**35393966** │ ⚠️
└─────┴──────────┴────────┴─────────┴─────────────┘
```

---

### 5. Format Rute dengan IATA Code

| Properti | Detail |
|----------|--------|
| **Masalah** | Format rute `Kota Asal (KODE)-Kota Tujuan (KODE)` — nama kota dan IATA code digabung |
| **Dampak** | • Sulit join dengan tabel referensi bandara (jika beda format)<br>• Sulit query berdasarkan IATA code saja |
| **Saran** | **Pertimbangkan parse/split** menjadi kolom terpisah: `asal_kota`, `asal_iata`, `tujuan_kota`, `tujuan_iata`. Atau minimal standardisasi format (trim, uppercase IATA). |

**Contoh Parse:**
```
SEBELUM:  "Jakarta (CGK)-Makassar (UPG)"
SESUDAH:  ├─ asal_kota: "Jakarta"
          ├─ asal_iata: "CGK"
          ├─ tujuan_kota: "Makassar"
          └─ tujuan_iata: "UPG"
```

---

### 6. Data COVID-19 Impact (Anomali 2020)

| Properti | Detail |
|----------|--------|
| **Observasi** | Total penumpang 2020 (`35.4M`) turun drastis vs 2019 (`100.5M`) → **↓64.7%** |
| **Dampak** | • Data 2020 tidak representatif untuk trend normal<br>• Jika digunakan untuk forecasting, perlu flag "pandemi"<br>• Beberapa rute mungkin baru mulai/route berubah di 2020 |
| **Saran** | **Beri konteks metadata:** Tambahkan kolom/flag `is_pandemic_year = TRUE` atau dokumentasi bahwa 2020 adalah outlier. Jika ada data 2021-2024, bisa dibandingkan recovery-nya. |

**Visualisasi Perbandingan Tahun:**
```
┌─────────────────────────────────────────────┐
│ TOTAL PENUMPANG PER TAHUN                   │
├──────────┬──────────────┬──────────────────┤
│ Tahun    │ Total        │ Growth vs Prev   │
├──────────┼──────────────┼──────────────────┤
│ 2018     │ 78.9M        │ —                │
│ 2019     │ 100.5M       │ ↑ +27.3%         │
│ 2020     │ 35.4M        │ ↓ -64.7% ⚠️      │
└──────────┴──────────────┴──────────────────┘
```

---

## 📐 Rekomendasi Skema Database (Gambaran)

### Opsi A: Wide Format (Seperti CSV Asli)

**Konsep:** Satu tabel dengan kolom bulan melebar (horizontal)

**Struktur Logis:**
```
┌──────┬──────────────┬────────┬────────┬──────┬────────┬─────────┬─────────┐
│ ID   │ Rute         │Jan-20  │Feb-20  │ ...  │Dec-20  │ TOTAL20 │ TOTAL19 │
├──────┼──────────────┼────────┼────────┼──────┼────────┼─────────┼─────────┤
│ 1    │ CGK-UPG      │ 231865 │ 237258 │ ...  │ 181917 │ 1579052 │ 3607498 │
│ 2    │ CGK-DPS      │ 363789 │ 302423 │ ...  │ 212308 │ 1549163 │ 4770798 │
└──────┴──────────────┴────────┴────────┴──────┴────────┴─────────┴─────────┘
```

**Kolom yang Dibutuhkan:**
- **Primary Key** (auto-generated ID)
- **Rute** (VARCHAR): format "Asal (IATA)-Tujuan (IATA)"
- **Kolom per Bulan** (INT): m01_2020, m02_2020, ..., m12_2020
- **Kolom Total Tahun** (DECIMAL): total_2020, total_2019, total_2018
- **Flag Total Row** (BOOLEAN): untuk tandai baris agregasi
- **Asal/Tujuan Parse** (opsional): asal_kota, asal_iata, tujuan_kota, tujuan_iata

**Kelebihan:** 
- ✅ Simple, sesuai format sumber
- ✅ Query langsung tanpa JOIN
- ✅ Mudah dibaca user non-teknis

**Kekurangan:**
- ❌ Sulit query trend bulanan (harus unpivot)
- ❌ Row lebar (18 kolom)
- ❌ Tidak scalable untuk data tahun lain

**Kapan Pakai Opsi Ini?**
→ Jika hanya untuk **reporting static 2020** dan tidak akan dibandingkan dengan tahun lain

---

### Opsi B: Long Format (Recommended)

**Konsep:** Satu tabel vertikal dengan satu baris = satu rute + satu bulan

**Tabel: Faktapenumpang_bulanan (Fact Table)**
```
┌──────────┬──────────────┬──────┬───────┬────────────┐
│ ID (PK)  │ Rute         │ Tahun│ Bulan │ Penumpang  │
├──────────┼──────────────┼──────┼───────┼────────────┤
│ 1        │ CGK-UPG      │ 2020 │ 01    │ 231865     │
│ 2        │ CGK-UPG      │ 2020 │ 02    │ 237258     │
│ 3        │ CGK-UPG      │ 2020 │ 03    │ 188899     │
│ ...      │ ...          │ ...  │ ...   │ ...        │
│ 14       │ CGK-UPG      │ 2019 │ 12    │ (dari kolom│
│          │              │      │       │  TOTAL 2019│
│          │              │      │       │  dibagi 12)│
└──────────┴──────────────┴──────┴───────┴────────────┘
```

**Struktur Logis:**
- **Primary Key** (ID unik per record)
- **Rute** (VARCHAR): atau Foreign Key ke tabel master rute
- **Tahun** (INT): 2020, 2019, 2018
- **Bulan** (INT): 1-12
- **Penumpang** (INT): jumlah penumpang
- **Flag Total Row** (BOOLEAN): untuk exclude agregasi
- **Kategori Rute** (VARCHAR): "Domestik"

**Kelebihan:**
- ✅ Mudah query trend & time-series
- ✅ Mudah agregasi per bulan atau per tahun
- ✅ Scalable jika ada data tahun baru
- ✅ Optimal untuk analytics dashboard

**Kekurangan:**
- ❌ Baris lebih banyak (410 rute × 12 bulan = ~4,920 rows)
- ❌ Kolom TOTAL 2018/2019 perlu handling terpisah

**Kapan Pakai Opsi Ini?**
→ Jika data akan dipakai untuk **trend analysis, forecasting, atau dibandingkan dengan tahun lain**

---

### 📊 Perbandingan Kedua Opsi

| Aspek | Wide Format | Long Format |
|-------|-------------|-------------|
| **Jumlah Tabel** | 1 | 1 (atau 2 jika ada master rute) |
| **Jumlah Baris** | 410 | ~4,920 (410 rute × 12 bulan) |
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
  ✅ Skalabel jika ada data 2021, 2022, dst
  ✅ Optimal untuk dashboard & visualization
```

**Alur ETL Sederhana:**
```
CSV Mentah → Pre-Processing → Load ke Staging → Transform → Load ke Production
     ↓            ↓              ↓              ↓            ↓
  (Parsing    (Clean NULL,   (Tabel       (Unpivot,    (Tabel final
   CSV)        Parse Rute,   Sementara)   Parse Rute,  siap pakai)
               Flag Total)                 Add Tahun)
```

---

## 🎯 Kesimpulan & Next Steps

### Masalah Kritikal (Harus Ditangani)
1. ✅ Missing value (sel kosong → `NULL` atau `0`)
2. ✅ Baris Total perlu flag/isolasi
3. ✅ Kolom bulan perlu rename (format terstruktur)

### Masalah Struktural (Pertimbangkan Transformasi)
1. ⚠️ Wide → Long format (untuk scalability)
2. ⚠️ Parse rute menjadi asal/tujuan + IATA code
3. ⚠️ Context metadata (COVID-19 impact 2020)

### Next Steps untuk File Ini
- [ ] Tentukan format target (wide vs long)
- [ ] Buat script pre-processing (cleaning + transform)
- [ ] Validasi hasil cleaning (sum vs Total row)
- [ ] Bandingkan dengan file Internasional Bulanan (struktur sama?)

---

## 📝 Metadata Tambahan

| Properti | Nilai |
|----------|-------|
| **Analysis Date** | 2026-04-10 |
| **Analysis Revision** | 2 (Updated after CSV correction) |
| **Analyzed By** | Data Engineer (AI Assistant) |
| **Jumlah Rute Unik** | 410 |
| **Total Penumpang 2020** | 35,393,966 |
| **Total Penumpang 2019** | 100,490,773 |
| **Growth YoY** | ↓ -64.7% (COVID impact) |
| **Encoding** | UTF-8 (asumsi) |
| **Delimiter** | `,` (comma) |
| **Missing Value** | Sel kosong (bukan `-` atau `NULL`) |

---

> **Catatan:** Dokumen ini hanya fokus pada file Domestik Bulanan 2020. Untuk analisis file lain dalam BAB VI, lihat file markdown terpisah.
> 
> **Revisi:** Analisis ini diperbarui setelah CSV sumber diperbaiki (dari 521 baris → 412 baris dengan struktur yang lebih konsisten).
