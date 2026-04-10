# CSV Analysis: Statistik Per Rute — Domestik Ranking 2020

## 📊 Informasi Umum

| Properti | Nilai |
|----------|-------|
| **Nama File** | `STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2020 BERDASARKAN URUTAN JUMLAH PENUMPANG.csv` |
| **Sumber** | Extract dari PDF (Kemenhub/DJPU) |
| **Periode** | Tahun 2020 (ranking berdasarkan jumlah penumpang) |
| **Jumlah Baris** | 412 (1 header + 410 rute + 1 footer total) |
| **Jumlah Kolom** | 8 |
| **Tipe Data Utama** | Integer (angka) & String (persentase dengan koma) |
| **Missing Value** | Sel kosong (untuk beberapa rute baru/tidak beroperasi) |

---

## 🗂️ Struktur Tabel

### Skema Saat Ini

```
NO (int)
RUTE (PP) (string)
JUMLAH PENERBANGAN (int)
JUMLAH PENUMPANG (int)
KAPASITAS SEAT (int)
JUMLAH BARANG (Kg) (int)
JUMLAH POS (int)
L/F (string - percentage dengan koma)
```

### Detail Per Kolom

| No | Nama Kolom | Deskripsi | Tipe Data Saat Ini | Tipe Data Rekomendasi | Nullable | Contoh Nilai |
|----|-----------|-----------|-------------------|----------------------|----------|--------------|
| 1 | `NO` | Nomor urut ranking | Integer | `INT` | ❌ No | `1`, `2`, ..., `410` |
| 2 | `RUTE (PP)` | Rute pulang-pergi (Asal-Tujuan) | String | `VARCHAR(150)` | ❌ No | `Jakarta (CGK)-Makassar (UPG)` |
| 3 | `JUMLAH PENERBANGAN` | Total penerbangan PP di 2020 | Integer | `INT` | ❌ No | `15065` |
| 4 | `JUMLAH PENUMPANG` | Total penumpang di 2020 | Integer | `INT` | ❌ No | `1579052` |
| 5 | `KAPASITAS SEAT` | Total kapasitas kursi tersedia | Integer | `INT` | ✅ Yes | `2660708` |
| 6 | `JUMLAH BARANG (Kg)` | Total berat barang/kargo (kilogram) | Integer | `INT` | ✅ Yes | `28494003` |
| 7 | `JUMLAH POS` | Total berat pos (kilogram) | Integer | `INT` | ✅ Yes | `1140884` |
| 8 | `L/F` | Load Factor (persentase okupansi) | String (format: `"XX,X%"`) | `DECIMAL(5,2)` | ✅ Yes | `"59,3%"`, `"0,0%"` |

**Catatan:** Berbeda dengan file Bulanan, file Ranking ini punya **metrik operasional** (penerbangan, kapasitas, barang, pos, load factor), bukan hanya penumpang.

---

## 🔍 Analisis Nilai Unik & Distribusi

### Kolom Kategorikal

#### 1. `NO`
- **Nilai Unik:** 410 (1-410)
- **Range:** 1 sampai 410
- **Catatan:** ✅ **Sekarang KONSISTEN** — file punya 412 baris (header + 410 rute + footer total), nomor urut 1-410 sequential tanpa skip

#### 2. `RUTE (PP)`
- **Nilai Unik:** 410 rute domestik
- **Format:** `Kota Asal (KODE_IATA)-Kota Tujuan (KODE_IATA)`
- **Contoh:**
  - `Jakarta (CGK)-Makassar (UPG)`
  - `"Praya, Lombok (LOP)-Majalengka (KJT)"` (ada koma dalam nama)
  - `Manado (MDC)-Galela (GLX)`
- **Catatan:** 
  - Semua rute **pulang-pergi (PP)**
  - Ranking berdasarkan `JUMLAH PENUMPANG` (descending)

#### 3. `JUMLAH PENERBANGAN`
- **Tipe:** Integer murni
- **Range:** 0 hingga 15,065
- **Top 3 Rute Terbanyak:**
  1. Jakarta (CGK)-Denpasar (DPS): 15,111 penerbangan
  2. Jakarta (CGK)-Makassar (UPG): 15,065 penerbangan
  3. Jakarta (CGK)-Surabaya (SUB): 14,844 penerbangan

#### 4. `JUMLAH PENUMPANG`
- **Tipe:** Integer murni
- **Range:** 0 hingga 1,579,052
- **Top 3 Rute Teramai:**
  1. Jakarta (CGK)-Makassar (UPG): 1,579,052 penumpang
  2. Jakarta (CGK)-Denpasar (DPS): 1,549,163 penumpang
  3. Jakarta (CGK)-Surabaya (SUB): 1,547,687 penumpang

#### 5. `KAPASITAS SEAT`
- **Tipe:** Integer murni
- **Range:** 0 hingga 2,907,008
- **Insight:** Kapasitas > penumpang → Load Factor < 100% (normal)

#### 6. `JUMLAH BARANG (Kg)`
- **Tipe:** Integer murni
- **Range:** 0 hingga 28,494,003 kg
- **Insight:** Rute tersibuk juga membawa barang terbanyak (CGK-UPG: 28.5M kg)

#### 7. `JUMLAH POS`
- **Tipe:** Integer murni
- **Range:** 0 hingga 1,167,519 kg
- **Insight:** Rute CGK-BTM (Batam) punya pos tertinggi (1.17M kg) — mungkin e-commerce

#### 8. `L/F` (Load Factor)
- **Tipe:** String dengan koma desimal & simbol `%`
- **Format:** `"XX,X%"` (contoh: `"59,3%"`)
- **Range:** `"0,0%"` (rute tidak aktif) hingga `"69,5%"`
- **Top 3 Load Factor Tertinggi:**
  1. Makassar (UPG)-Kendari (KDI): 69.5%
  2. Jakarta (CGK)-Yogyakarta (JOG): 69.2%
  3. Surabaya (SUB)-Samarinda (AAP): 69.5%
- **Rute dengan LF 0%:** Rute di akhir list (395-410) — tidak beroperasi di 2020

**Visualisasi Data Sample:**
```
┌─────┬──────────────────────────┬──────────┬─────────────┬───────────┬────────────┬─────────┬────────┐
│ NO  │ RUTE                     │ Flights  │ Passengers  │  Seats    │ Cargo (Kg) │   Pos   │  L/F   │
├─────┼──────────────────────────┼──────────┼─────────────┼───────────┼────────────┼─────────┼────────┤
│ 1   │ CGK-UPG (Jakarta-Mksr)   │   15065  │  1,579,052  │ 2,660,708 │ 28,494,003 │ 1,140,884│ 59.3%  │
│ 2   │ CGK-DPS (Jakarta-Bali)   │   15111  │  1,549,163  │ 2,907,008 │ 20,444,625 │   605,309│ 53.3%  │
│ 3   │ CGK-SUB (Jakarta-Sby)    │   14844  │  1,547,687  │ 2,635,164 │ 15,753,425 │   388,367│ 58.7%  │
│ ... │ ...                      │    ...   │     ...     │    ...    │     ...    │    ...  │ ...    │
│ 410 │ TNJ-LMU (Tj.Pinang-Anmb) │      0   │          0  │         0 │          0 │       0 │  0.0%  │
└─────┴──────────────────────────┴──────────┴─────────────┴───────────┴────────────┴─────────┴────────┘
```

#### 9. Footer Total (Akhir File)
- **Format:** `,,402447,35393966,60269598,430559992,8605576,"58,7%"` (tanpa label "Total")
- **JUMLAH PENERBANGAN:** 402,447
- **JUMLAH PENUMPANG:** 35,393,966
- **KAPASITAS SEAT:** 60,269,598
- **JUMLAH BARANG:** 430,559,992 kg
- **JUMLAH POS:** 8,605,576 kg
- **L/F Rata-rata:** 58.7%

---

## ⚠️ Potensi Masalah & Saran Pre-Processing

### 1. Format Load Factor dengan Koma Desimal

| Properti | Detail |
|----------|--------|
| **Masalah** | Load Factor menggunakan koma sebagai desimal (`"59,3%"`) bukan titik (`59.3`) |
| **Dampak** | Database/ETL tools akan gagal parse langsung ke `DECIMAL` |
| **Saran** | Lakukan 3 langkah cleaning: (1) Hapus simbol `%`, (2) Ganti koma `,` menjadi titik `.`, (3) Konversi ke numerik (DECIMAL) |

**Visualisasi Transformasi:**
```
SEBELUM:  "59,3%"  →  SESUDAH:  59.3
SEBELUM:  "0,0%"   →  SESUDAH:  0.0
SEBELUM:  "69,5%"  →  SESUDAH:  69.5
```

---

### 2. Rute dengan Load Factor 0% (Tidak Beroperasi)

| Properti | Detail |
|----------|--------|
| **Masalah** | Beberapa rute di akhir list (395-410) punya LF `"0,0%"` dan semua metrik kosong/0 |
| **Dampak** | • Data tidak informatif untuk analisis<br>• Bisa skew average LF jika tidak di-filter |
| **Saran** | **Beri flag:** Tambahkan kolom `is_active = FALSE` untuk rute dengan LF = 0%. Bisa di-exclude dari kalkulasi rata-rata. |

**Contoh Rute Tidak Aktif:**
```
┌─────┬──────────────────────────┬──────────┬─────────────┬────────┐
│ NO  │ RUTE                     │ Flights  │ Passengers  │  L/F   │
├─────┼──────────────────────────┼──────────┼─────────────┼────────┤
│ 395 │ PDG-BPN (Padang-Balik)   │    0     │      0      │  0.0%  │
│ 396 │ SOC-AAP (Solo-Samarinda) │    0     │      0      │  0.0%  │
│ ... │ ...                      │   ...    │     ...     │  ...   │
│ 410 │ TNJ-LMU (Tj.Pinang-Anmb) │    0     │      0      │  0.0%  │
└─────┴──────────────────────────┴──────────┴─────────────┴────────┘
```

---

### 3. Missing Value di Beberapa Metrik

| Properti | Detail |
|----------|--------|
| **Masalah** | Beberapa rute punya data tidak lengkap (misal: ada penerbangan & penumpang, tapi kosong di barang/pos) |
| **Dampak** | ETL bisa gagal jika kolom di-set `NOT NULL` |
| **Saran** | **Set kolom opsional sebagai `NULL`:** `KAPASITAS SEAT`, `JUMLAH BARANG`, `JUMLAH POS` boleh NULL. `JUMLAH PENERBANGAN` dan `JUMLAH PENUMPANG` harus ada (not null). |

---

### 4. Nama Kolom Panjang & Ber-spasi

| Properti | Detail |
|----------|--------|
| **Masalah** | Nama kolom panjang dan pakai spasi: `JUMLAH BARANG (Kg)`, `JUMLAH POS`, `L/F` |
| **Dampak** | • Query SQL harus quote: `"JUMLAH BARANG (Kg)"`<br>• Tidak mengikuti naming convention database (snake_case) |
| **Saran** | **Rename ke snake_case yang lebih pendek:** |

**Visualisasi Rename:**
```
SEBELUM:  NO, RUTE (PP), JUMLAH PENERBANGAN, JUMLAH PENUMPANG, 
          KAPASITAS SEAT, JUMLAH BARANG (Kg), JUMLAH POS, L/F

SESUDAH:  route_rank, route_pp, total_flights, total_passengers, 
          total_seats, cargo_kg, postal_kg, load_factor_pct
```

---

### 5. Footer Total Tanpa Label

| Properti | Detail |
|----------|--------|
| **Masalah** | Baris terakhir `,,402447,35393966,...` adalah agregasi sum semua rute tapi **tidak punya label "Total"** (hanya kolom kosong di awal) |
| **Dampak** | Jika dimuat ke database, bisa menyebabkan double-counting |
| **Saran** | **Beri flag:** Tambahkan kolom `is_total_row = TRUE` (detect dari kolom NO yang kosong), atau hapus dari data utama |

**Visualisasi:**
```
┌─────┬──────────┬──────────┬─────────────┬─────────────┐
│ NO  │ RUTE     │ Flights  │ Passengers  │    L/F      │
├─────┼──────────┼──────────┼─────────────┼─────────────┤
│ 1   │ CGK-UPG  │  15065   │  1,579,052  │   59.3%     │
│ 2   │ CGK-DPS  │  15111   │  1,549,163  │   53.3%     │
│ ... │ ...      │   ...    │     ...     │    ...      │
│     │          │**402,447**│**35,393,966**│ **58.7%** │ ⚠️ (footer total)
└─────┴──────────┴──────────┴─────────────┴─────────────┘
```

---

### 6. Kolom Rute Sama dengan File Bulanan

| Properti | Detail |
|----------|--------|
| **Observasi** | Kolom `RUTE (PP)` memiliki format yang sama persis dengan file Domestik Bulanan |
| **Dampak** | ✅ Bagus — bisa di-join menggunakan kolom rute sebagai key |
| **Saran** | **Standardisasi format rute** di semua file agar konsisten (parse asal/tujuan + IATA code) |

---

### 7. Load Factor sebagai Metrik Calculated

| Properti | Detail |
|----------|--------|
| **Observasi** | Load Factor (L/F) sebenarnya bisa dihitung: `LF = JUMLAH PENUMPANG / KAPASITAS SEAT × 100%` |
| **Dampak** | • Jika simpan L/F di database, ada redundancy<br>• Tapi: simpan L/F dari sumber lebih akurat (karena mungkin ada adjustment) |
| **Saran** | **Simpan keduanya:** L/F dari sumber (sebagai fakta) + bisa recalculate di view/query untuk verifikasi. Jika beda > threshold, flag untuk QA. |

**Formula Verifikasi:**
```
L/F Calculated = (JUMLAH PENUMPANG ÷ KAPASITAS SEAT) × 100

Contoh: CGK-UPG
  L/F Source     = 59.3%
  L/F Calculated = (1,579,052 ÷ 2,660,708) × 100 = 59.35%
  Difference     = 0.05% ✅ OK (rounding difference)
```

---

## 📐 Rekomendasi Skema Database (Gambaran)

### Opsi A: Wide Format (Seperti CSV Asli)

**Konsep:** Satu tabel dengan semua metrik per rute

**Struktur Logis:**
```
┌──────┬──────────────┬─────────┬────────────┬───────────┬───────────┬────────┬────────┐
│ ID   │ Rute         │ Flights │ Passengers │   Seats   │ Cargo_Kg  │  Pos   │   LF   │
├──────┼──────────────┼─────────┼────────────┼───────────┼───────────┼────────┼────────┤
│ 1    │ CGK-UPG      │  15065  │  1,579,052 │ 2,660,708 │28,494,003 │1,140,884│ 59.3%  │
│ 2    │ CGK-DPS      │  15111  │  1,549,163 │ 2,907,008 │20,444,625 │  605,309│ 53.3%  │
└──────┴──────────────┴─────────┴────────────┴───────────┴───────────┴────────┴────────┘
```

**Kolom yang Dibutuhkan:**
- **Primary Key** (auto-generated ID)
- **Route Rank** (INT): ranking dari sumber
- **Rute** (VARCHAR): format "Asal (IATA)-Tujuan (IATA)"
- **Total Flights** (INT): jumlah penerbangan
- **Total Passengers** (INT): jumlah penumpang
- **Total Seats** (INT): kapasitas kursi
- **Cargo Kg** (INT): berat barang
- **Postal Kg** (INT): berat pos
- **Load Factor %** (DECIMAL): okupansi
- **Is Active** (BOOLEAN): flag LF > 0
- **Is Total Row** (BOOLEAN): untuk exclude agregasi

**Kelebihan:** 
- ✅ Simple, sesuai format sumber
- ✅ Semua metrik langsung tersedia
- ✅ Cocok untuk reporting ranking

**Kekurangan:**
- ❌ Hanya 1 tahun (2020) — sulit bandingkan dengan tahun lain
- ❌ Ada redundancy (LF bisa calculated)

**Kapan Pakai Opsi Ini?**
→ Jika hanya untuk **reporting ranking 2020** dan tidak perlu historis

---

### Opsi B: Long Format (Recommended)

**Konsep:** Satu tabel vertikal dengan satu baris = satu rute + satu tahun

**Tabel: Faktastatistik_rute (Fact Table)**
```
┌──────────┬──────────────┬──────┬─────────┬────────────┬───────────┬───────────┬────────┬─────────┐
│ ID (PK)  │ Rute         │ Tahun│ Flights │ Passengers │   Seats   │ Cargo_Kg  │  Pos   │   LF    │
├──────────┼──────────────┼──────┼─────────┼────────────┼───────────┼───────────┼────────┼─────────┤
│ 1        │ CGK-UPG      │ 2020 │  15065  │  1,579,052 │ 2,660,708 │28,494,003 │1,140,884│  59.30  │
│ 2        │ CGK-UPG      │ 2019 │   ?     │  3,607,498 │     ?     │    ?      │   ?     │    ?    │
│ 3        │ CGK-DPS      │ 2020 │  15111  │  1,549,163 │ 2,907,008 │20,444,625 │  605,309│  53.30  │
└──────────┴──────────────┴──────┴─────────┴────────────┴───────────┴───────────┴────────┴─────────┘
```

**Struktur Logis:**
- **Primary Key** (ID unik per record)
- **Rute** (VARCHAR): atau Foreign Key ke tabel master rute
- **Tahun** (INT): 2020
- **Total Flights** (INT)
- **Total Passengers** (INT)
- **Total Seats** (INT)
- **Cargo Kg** (INT)
- **Postal Kg** (INT)
- **Load Factor %** (DECIMAL)
- **Is Active** (BOOLEAN): LF > 0
- **Kategori Rute** (VARCHAR): "Domestik"

**Kelebihan:**
- ✅ Mudah bandingkan tahun (jika nanti ada data 2021, 2022)
- ✅ Scalable untuk historis data
- ✅ Optimal untuk analytics dashboard

**Kekurangan:**
- ❌ Baris lebih banyak (410 rute × N tahun)
- ❌ File CSV asli hanya punya 2020 — kolom TOTAL 2018/2019 tidak ada

**Kapan Pakai Opsi Ini?**
→ Jika data akan **dibandingkan dengan tahun lain** atau ada rencana koleksi data multi-tahun

---

### 📊 Perbandingan Kedua Opsi

| Aspek | Wide Format | Long Format |
|-------|-------------|-------------|
| **Jumlah Tabel** | 1 | 1 (atau 2 jika ada master rute) |
| **Jumlah Baris** | 410 | 410 × N tahun |
| **Jumlah Kolom** | 10-11 | 10-11 |
| **Query Ranking** | Langsung (ORDER BY passengers) | Sama (tapi perlu filter tahun) |
| **Query Multi-Tahun** | Tidak bisa (hanya 2020) | Mudah (GROUP BY tahun) |
| **Cocok untuk** | Reporting statis | Analytics & historis |
| **Kompleksitas** | Rendah | Rendah-Medium |

---

### 🎯 Rekomendasi Final

**Untuk Use Case Data Warehouse:**

```
Pakai LONG FORMAT (Opsi B) karena:
  ✅ Konsisten dengan file bulanan (jika keduanya long format)
  ✅ Mudah bandingkan ranking antar tahun
  ✅ Skalabel untuk data historis
  ✅ Optimal untuk dashboard & route performance analysis
```

**Alur ETL Sederhana:**
```
CSV Mentah → Pre-Processing → Load ke Staging → Transform → Load ke Production
     ↓            ↓              ↓              ↓            ↓
  (Parsing    (Clean LF,     (Tabel       (Add Tahun,  (Tabel final
   CSV)        Rename, Flag   Sementara)   Parse Rute,  siap pakai)
               Active)                      Flag Total)
```

---

## 🎯 Kesimpulan & Next Steps

### Masalah Kritikal (Harus Ditangani)
1. ✅ Load Factor format (`"59,3%"` → `59.3`)
2. ✅ Kolom nama perlu rename (snake_case)
3. ✅ Footer total perlu flag/isolasi
4. ✅ Rute tidak aktif (LF = 0%) perlu flag

### Masalah Struktural (Pertimbangkan Transformasi)
1. ⚠️ Wide → Long format (jika mau bandingkan tahun)
2. ⚠️ Parse rute menjadi asal/tujuan + IATA code
3. ⚠️ LF calculated vs source — perlu verifikasi QA

### Next Steps untuk File Ini
- [ ] Tentukan format target (wide vs long)
- [ ] Buat script pre-processing (cleaning LF + rename)
- [ ] Validasi LF calculated vs source
- [ ] Bandingkan dengan file Internasional Ranking (struktur sama?)

---

## 📝 Metadata Tambahan

| Properti | Nilai |
|----------|-------|
| **Analysis Date** | 2026-04-10 |
| **Analysis Revision** | 2 (Updated after CSV correction) |
| **Analyzed By** | Data Engineer (AI Assistant) |
| **Jumlah Rute Unik** | 410 |
| **Total Penumpang 2020** | 35,393,966 |
| **Total Penerbangan** | 402,447 |
| **Average Load Factor** | 58.7% |
| **Rute Tidak Aktif (LF=0%)** | 16 rute (395-410) |
| **Encoding** | UTF-8 (asumsi) |
| **Delimiter** | `,` (comma) |
| **Missing Value** | Sel kosong (bukan `-` atau `NULL`) |

---

> **Catatan:** Dokumen ini hanya fokus pada file Domestik Ranking 2020. Untuk analisis file lain dalam BAB VI, lihat file markdown terpisah.
>
> **Revisi:** Analisis ini diperbarui setelah CSV sumber diperbaiki (dari 467 baris → 412 baris dengan struktur yang lebih konsisten, footer total tanpa label "Total").
