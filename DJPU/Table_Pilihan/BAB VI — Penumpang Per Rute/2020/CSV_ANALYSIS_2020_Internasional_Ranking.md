# CSV Analysis: Statistik Per Rute — Internasional Ranking 2020

## 📊 Informasi Umum

| Properti | Nilai |
|----------|-------|
| **Nama File** | `STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI TAHUN 2020 BERDASARKAN URUTAN JUMLAH PENUMPANG.csv` |
| **Sumber** | Extract dari PDF (Kemenhub/DJPU) |
| **Periode** | Tahun 2020 (ranking berdasarkan jumlah penumpang) |
| **Jumlah Baris** | 161 (1 header + 157 rute + 1 Total + 1 footer + 1 empty row) |
| **Jumlah Kolom** | 8 |
| **Tipe Data Utama** | Float (ada desimal `.0`) & String (persentase dengan koma) |
| **Missing Value** | Sel kosong (untuk beberapa rute tidak beroperasi) |

---

## 🗂️ Struktur Tabel

### Skema Saat Ini

```
NO (int)
RUTE (string)
JUMLAH PENERBANGAN (int/float)
JUMLAH PENUMPANG (float)
KAPASITAS SEAT (float)
JUMLAH BARANG (float)
JUMLAH POS (float)
L/F (string - percentage dengan koma)
```

### Detail Per Kolom

| No | Nama Kolom | Deskripsi | Tipe Data Saat Ini | Tipe Data Rekomendasi | Nullable | Contoh Nilai |
|----|-----------|-----------|-------------------|----------------------|----------|--------------|
| 1 | `NO` | Nomor urut ranking | Integer | `INT` | ❌ No | `1`, `2`, ..., `157` (ada skip) |
| 2 | `RUTE` | Rute internasional (Asal-Tujuan) | String | `VARCHAR(150)` | ❌ No | `Jakarta (CGK)-SINGAPURA (SIN)` |
| 3 | `JUMLAH PENERBANGAN` | Total penerbangan di 2020 | Integer/Float | `INT` | ✅ Yes | `8032` |
| 4 | `JUMLAH PENUMPANG` | Total penumpang di 2020 | Float | `DECIMAL(15,2)` | ✅ Yes | `618117.0` |
| 5 | `KAPASITAS SEAT` | Total kapasitas kursi tersedia | Float | `DECIMAL(15,2)` | ✅ Yes | `1266002.0` |
| 6 | `JUMLAH BARANG` | Total berat barang/kargo | Float | `DECIMAL(15,2)` | ✅ Yes | `58849280.0` |
| 7 | `JUMLAH POS` | Total berat pos | Float | `DECIMAL(15,2)` | ✅ Yes | `200832.0` |
| 8 | `L/F` | Load Factor (persentase okupansi) | String (format: `"XX,X%"`) | `DECIMAL(5,2)` | ✅ Yes | `"48,8%"`, `"0,0%"` |

**Catatan:** Berbeda dengan Domestik Ranking yang pakai integer, file ini punya **suffix `.0`** di banyak nilai numerik.

---

## 🔍 Analisis Nilai Unik & Distribusi

### Kolom Kategorikal

#### 1. `NO`
- **Nilai Unik:** ~147 (ada skip nomor dan out-of-order: 140, 141, ..., 155, 154, 153, 156, 157)
- **Catatan:** **Nomor tidak urut** — sama seperti file Internasional Bulanan, indikasi ada baris yang dihapus/difilter di sumber asli.

#### 2. `RUTE`
- **Nilai Unik:** ~147 rute internasional
- **Format:** Sama seperti file Internasional Bulanan — variasi format
  - `Jakarta (CGK)-SINGAPURA (SIN)` (normal)
  - `Kuala Lumpur (KUL)-Denpasar (DPS)` (normal)
  - `"Manado (MDC)-Catitipan, Barangay Buhangin (D"` (ada truncation/cut off)
  - `SINGAPURA (SIN)-Denpasar (DPS)` (kota asal di awal)
- **Catatan:** 
  - Sama seperti file bulanan — ada variasi format penulisan
  - Beberapa rute punya nama kota yang aneh/truncated

#### 3. `JUMLAH PENERBANGAN`
- **Tipe:** Integer/Float (ada suffix `.0`)
- **Range:** 0 hingga 8,032
- **Top 3 Rute Terbanyak:**
  1. Jakarta (CGK)-SINGAPURA (SIN): 8,032 penerbangan
  2. Jakarta (CGK)-Kuala Lumpur (KUL): 4,794 penerbangan
  3. SINGAPURA (SIN)-Denpasar (DPS): 2,853 penerbangan

#### 4. `JUMLAH PENUMPANG`
- **Tipe:** Float dengan suffix `.0`
- **Range:** 0 hingga 618,117
- **Top 3 Rute Teramai:**
  1. Jakarta (CGK)-SINGAPURA (SIN): 618,117 penumpang
  2. Jakarta (CGK)-Kuala Lumpur (KUL): 510,306 penumpang
  3. SINGAPURA (SIN)-Denpasar (DPS): 430,904 penumpang

#### 5. `KAPASITAS SEAT`
- **Tipe:** Float dengan suffix `.0`
- **Range:** 0 hingga 1,266,002
- **Insight:** Kapasitas > penumpang → Load Factor < 100% (normal)

#### 6. `JUMLAH BARANG`
- **Tipe:** Float dengan suffix `.0`
- **Range:** 0 hingga 58,849,280
- **Insight:** Rute CGK-SIN juga bawa barang terbanyak (58.8M kg)

#### 7. `JUMLAH POS`
- **Tipe:** Float dengan suffix `.0`
- **Range:** 0 hingga 618,100
- **Insight:** Secara umum lebih rendah dari domestik

#### 8. `L/F` (Load Factor)
- **Tipe:** String dengan koma desimal & simbol `%`
- **Format:** `"XX,X%"` (contoh: `"48,8%"`)
- **Range:** `"0,0%"` (rute tidak aktif) hingga `"81,5%"`
- **Top 3 Load Factor Tertinggi:**
  1. Sydney (SYD)-Denpasar (DPS): 76.4%
  2. Denpasar (DPS)-Doha (DOH): 75.6%
  3. Perth (PER)-Denpasar (DPS): 71.8%
- **Rute dengan LF 0%:** Beberapa rute di akhir list (tidak beroperasi di 2020)

**Visualisasi Data Sample:**
```
┌─────┬──────────────────────────┬──────────┬─────────────┬───────────┬────────────┬─────────┬────────┐
│ NO  │ RUTE                     │ Flights  │ Passengers  │  Seats    │ Cargo      │   Pos   │  L/F   │
├─────┼──────────────────────────┼──────────┼─────────────┼───────────┼────────────┼─────────┼────────┤
│ 1   │ CGK-SIN (Jakarta-Sing)   │   8032   │  618,117.0  │1,266,002.0│58,849,280.0│200,832.0│ 48.8%  │
│ 2   │ CGK-KUL (Jakarta-KL)     │   4794   │  510,306.0  │  930,797.0│ 9,005,311.0│202,286.0│ 54.8%  │
│ 3   │ SIN-DPS (Singapura-Bali) │   2853   │  430,904.0  │  660,601.0│ 1,964,399.0│ 35,412.0│ 65.2%  │
│ ... │ ...                      │    ...   │     ...     │    ...    │     ...    │    ...  │ ...    │
│ 150 │ KUL-Majalengka (KJT)     │      0   │        0.0  │        0.0│         0.0│      0.0│  0.0%  │
└─────┴──────────────────────────┴──────────┴─────────────┴───────────┴────────────┴─────────┴────────┘
```

#### 9. Baris Total (Akhir File)
- **JUMLAH PENERBANGAN:** 60,825
- **JUMLAH PENUMPANG:** 7,187,439
- **KAPASITAS SEAT:** 12,660,624
- **JUMLAH BARANG:** 317,385,786
- **JUMLAH POS:** 6,181,001
- **L/F Rata-rata:** 56.8%

#### 10. Footer Metadata
- Baris terakhir: `* Rute Codeshare Niaga Berjadwal Luar Negeri` (bukan data rute)

---

## ⚠️ Potensi Masalah & Saran Pre-Processing

### 1. Format Load Factor dengan Koma Desimal

| Properti | Detail |
|----------|--------|
| **Masalah** | Load Factor menggunakan koma sebagai desimal (`"48,8%"`) bukan titik (`48.8`) |
| **Dampak** | Database/ETL tools akan gagal parse langsung ke `DECIMAL` |
| **Saran** | Lakukan 3 langkah cleaning: (1) Hapus simbol `%`, (2) Ganti koma `,` menjadi titik `.`, (3) Konversi ke numerik (DECIMAL) |

**Visualisasi Transformasi:**
```
SEBELUM:  "48,8%"  →  SESUDAH:  48.8
SEBELUM:  "0,0%"   →  SESUDAH:  0.0
SEBELUM:  "76,4%"  →  SESUDAH:  76.4
```

---

### 2. Nilai Numerik dengan Suffix `.0`

| Properti | Detail |
|----------|--------|
| **Masalah** | Banyak nilai numerik punya suffix `.0` (contoh: `618117.0`, `1266002.0`) karena parsing sebagai float |
| **Dampak** | • Tidak efisien untuk storage (float vs int)<br>• Tampil kurang rapi (ada `.0` yang tidak perlu) |
| **Saran** | **Convert ke integer** untuk kolom yang seharusnya whole number: `JUMLAH PENERBANGAN`, `JUMLAH PENUMPANG`, `KAPASITAS SEAT`, `JUMLAH BARANG`, `JUMLAH POS` |

**Visualisasi Transformasi:**
```
SEBELUM:  618117.0  →  SESUDAH:  618117
SEBELUM:  1266002.0 →  SESUDAH:  1266002
SEBELUM:  58849280.0→  SESUDAH:  58849280
```

---

### 3. Rute dengan Load Factor 0% (Tidak Beroperasi)

| Properti | Detail |
|----------|--------|
| **Masalah** | Beberapa rute di akhir list punya LF `"0,0%"` dan semua metrik 0/kosong |
| **Dampak** | • Data tidak informatif<br>• Bisa skew average LF |
| **Saran** | **Beri flag:** Tambahkan kolom `is_active = FALSE` untuk rute dengan LF = 0% |

**Contoh Rute Tidak Aktif:**
```
┌─────┬──────────────────────────┬──────────┬─────────────┬────────┐
│ NO  │ RUTE                     │ Flights  │ Passengers  │  L/F   │
├─────┼──────────────────────────┼──────────┼─────────────┼────────┤
│ 150 │ KUL-Majalengka           │    0     │      0.0    │  0.0%  │
│ 151 │ KUL-Balikpapan           │    0     │      0.0    │  0.0%  │
│ 152 │ Semarang-Haikou          │    0     │      0.0    │  0.0%  │
│ ... │ ...                      │   ...    │      ...    │  ...   │
│ 157 │ Jakarta-Findel (LUX)     │    0     │      0.0    │  0.0%  │
└─────┴──────────────────────────┴──────────┴─────────────┴────────┘
```

---

### 4. Missing Value di Beberapa Metrik

| Properti | Detail |
|----------|--------|
| **Masalah** | Beberapa rute punya data tidak lengkap (misal: ada penumpang, tapi kosong di pos) |
| **Dampak** | ETL bisa gagal jika kolom di-set `NOT NULL` |
| **Saran** | **Set kolom opsional sebagai `NULL`:** `JUMLAH POS`, `JUMLAH BARANG` boleh NULL. `JUMLAH PENUMPANG` harus ada. |

---

### 5. Nama Kolom Panjang & Ber-spasi

| Properti | Detail |
|----------|--------|
| **Masalah** | Nama kolom panjang dan pakai spasi: `JUMLAH BARANG`, `JUMLAH POS`, `L/F` |
| **Dampak** | Query SQL harus quote |
| **Saran** | **Rename ke snake_case yang lebih pendek:** |

**Visualisasi Rename:**
```
SEBELUM:  NO, RUTE, JUMLAH PENERBANGAN, JUMLAH PENUMPANG, 
          KAPASITAS SEAT, JUMLAH BARANG, JUMLAH POS, L/F

SESUDAH:  route_rank, route_pp, total_flights, total_passengers, 
          total_seats, cargo_kg, postal_kg, load_factor_pct
```

---

### 6. Baris Total & Footer Metadata

| Properti | Detail |
|----------|--------|
| **Masalah** | Baris terakhir `Total,,60825,7187439.0,...` dan footer `* Rute Codeshare...` adalah metadata |
| **Dampak** | Jika dimuat ke database, akan jadi noise/data kotor |
| **Saran** | **Hapus atau pisahkan:** Baris Total → flag `is_total_row = TRUE`. Footer → simpan sebagai metadata terpisah. |

**Visualisasi:**
```
┌─────┬──────────┬──────────┬─────────────┬─────────────┐
│ NO  │ RUTE     │ Flights  │ Passengers  │    L/F      │
├─────┼──────────┼──────────┼─────────────┼─────────────┤
│ 1   │ CGK-SIN  │  8032    │  618,117.0  │   48.8%     │
│ ... │ ...      │   ...    │     ...     │    ...      │
│ -   │ **Total**│**60,825**│**7,187,439**│ **56.8%**   │ ⚠️
│ *   │ **Rute Codeshare Niaga Berjadwal Luar Negeri**  │ ⚠️
└─────┴──────────┴──────────┴─────────────┴─────────────┘
```

---

### 7. Nomor Urut Tidak Konsisten (Ada Skip & Out of Order)

| Properti | Detail |
|----------|--------|
| **Masalah** | Nomor urut tidak sequential: 140, 141, ..., 155, 154, 153, 156, 157 |
| **Dampak** | Tidak bisa pakai `NO` sebagai primary key reliable |
| **Saran** | **Generate surrogate key** (auto-increment ID) saat load ke database |

---

### 8. Format Rute dengan Variasi Naming (Sama seperti File Bulanan)

| Properti | Detail |
|----------|--------|
| **Masalah** | Format rute tidak konsisten — ada yang uppercase, title case, ada yang truncated |
| **Dampak** | Sulit join dengan tabel referensi bandara |
| **Saran** | **Standardisasi + parse** menjadi kolom terpisah: `asal_kota`, `asal_iata`, `tujuan_kota`, `tujuan_iata` |

**Contoh Inkonsistensi:**
```
┌──────────────────────────────────────────────────────┐
│ VARIASI FORMAT RUTE                                  │
├──────────────────────────────────────────────────────┤
│ "Jakarta (CGK)-SINGAPURA (SIN)"   ← SIN uppercase    │
│ "Kuala Lumpur (KUL)-Denpasar (DPS)" ← Title case     │
│ "Manado (MDC)-Catitipan, Barangay Buhangin (D" ← Truncated! │
└──────────────────────────────────────────────────────┘
```

---

### 9. Data COVID-19 Impact (Anomali 2020)

| Properti | Detail |
|----------|--------|
| **Observasi** | Total penumpang 2020 (`7.2M`) turun drastis dari estimasi 2019 (mungkin 50M+) → **↓85%+** |
| **Dampak** | • Data 2020 sangat tidak representatif<br>• Load Factor rata-rata juga turun (56.8%) |
| **Saran** | **Beri konteks metadata:** Tambahkan flag `is_pandemic_year = TRUE` |

---

## 📐 Rekomendasi Skema Database (Gambaran)

### Opsi A: Wide Format (Seperti CSV Asli)

**Konsep:** Satu tabel dengan semua metrik per rute

**Struktur Logis:**
```
┌──────┬──────────────┬─────────┬────────────┬───────────┬────────────┬────────┬────────┐
│ ID   │ Rute         │ Flights │ Passengers │   Seats   │  Cargo_Kg  │  Pos   │   LF   │
├──────┼──────────────┼─────────┼────────────┼───────────┼────────────┼────────┼────────┤
│ 1    │ CGK-SIN      │  8032   │  618117    │ 1266002   │ 58849280   │ 200832 │  48.8  │
│ 2    │ CGK-KUL      │  4794   │  510306    │  930797   │  9005311   │ 202286 │  54.8  │
└──────┴──────────────┴─────────┴────────────┴───────────┴────────────┴────────┴────────┘
```

**Kolom yang Dibutuhkan:**
- **Primary Key** (auto-generated ID)
- **Route Rank** (INT)
- **Rute** (VARCHAR)
- **Total Flights** (INT)
- **Total Passengers** (DECIMAL)
- **Total Seats** (DECIMAL)
- **Cargo Kg** (DECIMAL)
- **Postal Kg** (DECIMAL)
- **Load Factor %** (DECIMAL)
- **Is Active** (BOOLEAN): LF > 0
- **Is Total Row** (BOOLEAN)

**Kelebihan:** 
- ✅ Simple, sesuai format sumber
- ✅ Semua metrik langsung tersedia

**Kekurangan:**
- ❌ Hanya 1 tahun (2020)
- ❌ Nilai `.0` perlu cleaning

**Kapan Pakai Opsi Ini?**
→ Jika hanya untuk **reporting ranking 2020**

---

### Opsi B: Long Format (Recommended)

**Konsep:** Satu tabel vertikal dengan satu baris = satu rute + satu tahun

**Tabel: Faktastatistik_rute_internasional (Fact Table)**
```
┌──────────┬──────────────┬──────┬─────────┬────────────┬───────────┬────────────┬────────┬─────────┐
│ ID (PK)  │ Rute         │ Tahun│ Flights │ Passengers │   Seats   │ Cargo_Kg   │  Pos   │   LF    │
├──────────┼──────────────┼──────┼─────────┼────────────┼───────────┼────────────┼────────┼─────────┤
│ 1        │ CGK-SIN      │ 2020 │  8032   │  618117    │ 1266002   │ 58849280   │ 200832 │  48.80  │
│ 2        │ CGK-KUL      │ 2020 │  4794   │  510306    │  930797   │  9005311   │ 202286 │  54.80  │
└──────────┴──────────────┴──────┴─────────┴────────────┴───────────┴────────────┴────────┴─────────┘
```

**Struktur Logis:**
- **Primary Key** (ID unik per record)
- **Rute** (VARCHAR): atau Foreign Key ke tabel master rute
- **Tahun** (INT): 2020
- **Total Flights** (INT)
- **Total Passengers** (DECIMAL)
- **Total Seats** (DECIMAL)
- **Cargo Kg** (DECIMAL)
- **Postal Kg** (DECIMAL)
- **Load Factor %** (DECIMAL)
- **Is Active** (BOOLEAN): LF > 0
- **Kategori Rute** (VARCHAR): "Internasional"

**Kelebihan:**
- ✅ Mudah bandingkan tahun (jika nanti ada data 2021, 2022)
- ✅ Konsisten dengan file lain jika pakai long format
- ✅ Scalable untuk historis data

**Kekurangan:**
- ❌ Baris lebih banyak (147 rute × N tahun)
- ❌ File CSV asli hanya punya 2020

**Kapan Pakai Opsi Ini?**
→ Jika data akan **dibandingkan dengan tahun lain** atau ada rencana koleksi data multi-tahun

---

### 📊 Perbandingan Kedua Opsi

| Aspek | Wide Format | Long Format |
|-------|-------------|-------------|
| **Jumlah Tabel** | 1 | 1 (atau 2 jika ada master rute) |
| **Jumlah Baris** | ~147 | 147 × N tahun |
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
  ✅ Konsisten dengan file lain (jika keduanya long format)
  ✅ Mudah bandingkan ranking antar tahun
  ✅ Skalabel untuk data historis
  ✅ Optimal untuk dashboard & international route analysis
```

**Alur ETL Sederhana:**
```
CSV Mentah → Pre-Processing → Load ke Staging → Transform → Load ke Production
     ↓            ↓              ↓              ↓            ↓
  (Parsing    (Clean LF,     (Tabel       (Add Tahun,  (Tabel final
   CSV)        Remove .0,     Sementara)   Parse Rute,  siap pakai)
               Rename, Flag                  Flag Total)
               Active)
```

---

## 🎯 Kesimpulan & Next Steps

### Masalah Kritikal (Harus Ditangani)
1. ✅ Load Factor format (`"48,8%"` → `48.8`)
2. ✅ Suffix `.0` pada nilai numerik (remove)
3. ✅ Kolom nama perlu rename (snake_case)
4. ✅ Baris Total & footer metadata perlu isolasi
5. ✅ Rute tidak aktif (LF = 0%) perlu flag

### Masalah Struktural (Pertimbangkan Transformasi)
1. ⚠️ Wide → Long format (jika mau bandingkan tahun)
2. ⚠️ Parse rute menjadi asal/tujuan + IATA code
3. ⚠️ Context metadata (COVID-19 impact ekstrem di 2020)

### Next Steps untuk File Ini
- [ ] Tentukan format target (wide vs long)
- [ ] Buat script pre-processing (cleaning LF + remove .0 + rename)
- [ ] Validasi hasil cleaning
- [ ] Bandingkan dengan file Domestik Ranking (struktur kolom sama?)

---

## 📝 Metadata Tambahan

| Properti | Nilai |
|----------|-------|
| **Analysis Date** | 2026-04-10 |
| **Analyzed By** | Data Engineer (AI Assistant) |
| **Jumlah Rute Unik** | ~147 (perlu verifikasi) |
| **Total Penumpang 2020** | 7,187,439 |
| **Total Penerbangan** | 60,825 |
| **Average Load Factor** | 56.8% |
| **Rute Tidak Aktif (LF=0%)** | ~8 rute di akhir list |
| **Encoding** | UTF-8 (asumsi) |
| **Delimiter** | `,` (comma) |
| **Missing Value** | Sel kosong (bukan `-` atau `NULL`) |

---

> **Catatan:** Dokumen ini hanya fokus pada file Internasional Ranking 2020. Untuk analisis file lain dalam BAB VI, lihat file markdown terpisah.
