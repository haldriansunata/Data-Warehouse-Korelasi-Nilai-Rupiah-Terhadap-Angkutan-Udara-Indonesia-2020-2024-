# CSV Analysis: Jumlah Penumpang Per Rute — Internasional Bulanan 2020

## 📊 Informasi Umum

| Properti | Nilai |
|----------|-------|
| **Nama File** | `JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI BULAN JANUARI S.D DESEMBER TAHUN 2020.csv` |
| **Sumber** | Extract dari PDF (Kemenhub/DJPU) |
| **Periode** | Januari - Desember 2020 (plus komparasi 2019 & 2018) |
| **Jumlah Baris** | 160 (1 header + 158 rute + 1 KARGO rows + 1 Total + 1 footer) |
| **Jumlah Kolom** | 18 |
| **Tipe Data Utama** | Float (ada desimal `.0`) & String (ada "KARGO") |
| **Missing Value** | Sel kosong (tanpa nilai) |

---

## 🗂️ Struktur Tabel

### Skema Saat Ini

```
NO (int)
RUTE (string)
Jan-20 (float/string - ada "KARGO")
Feb-20 (float)
Mar-20 (float)
Apr-20 (float)
May-20 (float)
Jun-20 (float)
Jul-20 (float)
Aug-20 (float)
Sep-20 (float)
Oct-20 (float)
Nov-20 (float)
Dec-20 (float)
TOTAL 2020 (float)
TOTAL 2019 (float)
TOTAL 2018 (float)
```

### Detail Per Kolom

| No | Nama Kolom | Deskripsi | Tipe Data Saat Ini | Tipe Data Rekomendasi | Nullable | Contoh Nilai |
|----|-----------|-----------|-------------------|----------------------|----------|--------------|
| 1 | `NO` | Nomor urut rute | Integer | `INT` | ❌ No | `1`, `2`, ..., `157` (ada skip) |
| 2 | `RUTE` | Rute internasional (Asal-Tujuan) | String | `VARCHAR(150)` | ❌ No | `Jakarta (CGK)-SINGAPURA (SIN)` |
| 3-14 | `Jan-20` s/d `Dec-20` | Jumlah penumpang per bulan | Float/String (ada "KARGO") | `DECIMAL(15,2)` | ✅ Yes | `334069`, `KARGO`, `(kosong)` |
| 15 | `TOTAL 2020` | Total akumulasi 2020 | Float | `DECIMAL(15,2)` | ✅ Yes | `618117.0` |
| 16 | `TOTAL 2019` | Total tahun 2019 (komparasi) | Float | `DECIMAL(15,2)` | ✅ Yes | `4194638.0` |
| 17 | `TOTAL 2018` | Total tahun 2018 (komparasi) | Float | `DECIMAL(15,2)` | ✅ Yes | `4077673.0` |

**Catatan:** Berbeda dengan Domestik yang pakai integer, file ini punya **suffix `.0`** di banyak nilai karena parsing sebagai float.

---

## 🔍 Analisis Nilai Unik & Distribusi

### Kolom Kategorikal

#### 1. `NO`
- **Nilai Unik:** ~147 (ada skip nomor: 140, 141, ..., 147, 148, 149, 150, 151, 152, 155, 154, 153, 156, 157)
- **Catatan:** **Nomor tidak urut** — ada yang skip (147 langsung ke 149, lalu 155 sebelum 154). Ini indikasi ada baris yang dihapus/difilter di sumber asli.

#### 2. `RUTE`
- **Nilai Unik:** ~147 rute internasional
- **Format:** Variasi format:
  - `Jakarta (CGK)-SINGAPURA (SIN)` (normal, IATA uppercase)
  - `Kuala Lumpur (KUL)-Denpasar (DPS)` (normal, title case)
  - `"Manado (MDC)-Catitipan, Barangay Buhangin (DVO)"` (ada koma dalam nama)
  - `SINGAPURA (SIN)-Denpasar (DPS)` (kota tujuan di awal?)
- **Catatan:** 
  - Rute internasional lebih kompleks — ada nama kota non-Indonesia
  - Beberapa rute tidak jelas (contoh: "Catitipan, Barangay Buhangin")
  - Footer: `* Rute Codeshare Niaga Berjadwal Luar Negeri` (bukan data)

#### 3. Kolom Bulanan (`Jan-20` s/d `Dec-20`)
- **Tipe:** Float dengan suffix `.0` (contoh: `169342.0`) atau string "KARGO"
- **Range:** 0 (kosong) hingga 334,069
- **Missing Value:** Sel kosong
- **Masalah Khusus:** Ada nilai **"KARGO"** di beberapa sel (bukan angka)
- **Visualisasi Data Sample:**

```
┌─────┬──────────────────────────┬────────┬─────────┬────────┬────────┬──────┬─────────┐
│ NO  │ RUTE                     │ Jan-20 │ Feb-20  │ Mar-20 │ Apr-20 │ ...  │ Dec-20  │
├─────┼──────────────────────────┼────────┼─────────┼────────┼────────┼──────┼─────────┤
│ 1   │ CGK-SIN (Jakarta-Sing)   │ 334069 │ 169342.0│73928.0 │ 2604.0 │ ...  │ 10859.0 │
│ 2   │ CGK-KUL (Jakarta-KL)     │ 229241 │ 166788.0│82853.0 │ 3975.0 │ ...  │ 3984.0  │
│ 3   │ SIN-DPS (Singapura-Bali) │ 196727 │ 154187.0│79990.0 │ (kosong)│...  │ (kosong)│
│ ... │ ...                      │ ...    │ ...     │ ...    │ ...    │ ...  │ ...     │
│ 147 │ CGK-HAN (Jakarta-Hanoi)  │ KARGO  │ (kosong)│ (kosong)│ (kosong)│...  │ (kosong)│
└─────┴──────────────────────────┴────────┴─────────┴────────┴────────┴──────┴─────────┘
```

#### 4. Nilai "KARGO" dalam Kolom Numerik

| Properti | Detail |
|----------|--------|
| **Lokasi** | Beberapa baris di kolom Jan-20 atau bulan lain |
| **Contoh** | `Jakarta (CGK)-Hanoi (HAN)` → Jan-20 = `KARGO` |
| **Jumlah** | ~7 baris berisi "KARGO" |
| **Arti** | Rute tersebut khusus kargo (bukan penumpang) di bulan tersebut |
| **Dampak** | Tidak bisa convert ke numerik langsung — perlu handling khusus |

**List Rute dengan "KARGO":**
```
NO 154: Jakarta (CGK)-Hanoi (HAN) → Jan-20 = KARGO
NO 153: SINGAPURA (SIN)-Jakarta-HLP (HLP) → Jan-20 = KARGO
NO 156: Jakarta (CGK)-Subang (SZB) → Jan-20 = KARGO
NO 148: Kuala Lumpur (KUL)-Balikpapan (BPN) → Jan-20 = KARGO
NO 157: Jakarta (CGK)-Findel (LUX) → Jan-20 = KARGO
```

#### 5. Kolom Total (`TOTAL 2020`, `TOTAL 2019`, `TOTAL 2018`)
- **Baris Total (akhir file):** `7187439.0` (2020), data 2019/2018 tidak tersedia di Total row
- **Insight:** Penurunan drastis 2020 — banyak rute internasional cuma beroperasi Jan-Mar sebelum COVID lockdown

---

## ⚠️ Potensi Masalah & Saran Pre-Processing

### 1. Nilai "KARGO" dalam Kolom Numerik

| Properti | Detail |
|----------|--------|
| **Masalah** | Ada nilai `KARGO` (string) di kolom yang seharusnya numerik (penumpang) |
| **Dampak** | ETL akan gagal convert ke numerik — error type mismatch |
| **Saran** | **Replace "KARGO" dengan `NULL`** (atau buat tabel terpisah untuk rute kargo). Jika ingin tetap track, tambahkan kolom flag `is_cargo = TRUE` di baris tersebut. |

**Visualisasi:**
```
SEBELUM:  "KARGO"       →  SESUDAH:  NULL  (atau flag is_cargo = TRUE)
SEBELUM:  334069        →  SESUDAH:  334069
```

---

### 2. Missing Value Tidak Seragam (Sel Kosong)

| Properti | Detail |
|----------|--------|
| **Masalah** | Banyak sel kosong, terutama Apr-Des 2020 (dampak COVID) |
| **Dampak** | ETL tools bisa interpretasi beda |
| **Saran** | **Standarisasi:** Replace semua sel kosong dengan `NULL`. Berikan konteks bahwa missing di 2020 kemungkinan karena COVID (bukan data error). |

**Pola Missing yang Jelas:**
```
┌──────────────────────────────────────────────────┐
│ POLA MISSING VALUE PER BULAN (2020)             │
├───────┬──────────────────────────────────────────┤
│ Jan   │ ✅ Hampir semua ada data                 │
│ Feb   │ ✅ Hampir semua ada data                 │
│ Mar   │ ⚠️ Mulai ada yang kosong                 │
│ Apr   │ ❌ Banyak sekali yang kosong (lockdown)  │
│ May   │ ❌ Hampir semua kosong                   │
│ Jun   │ ⚠️ Mulai muncul beberapa                 │
│ Jul   │ ⚠️ Mulai muncul beberapa                 │
│ ...   │ ⚠️ Recovery bertahap                     │
└───────┴──────────────────────────────────────────┘
```

---

### 3. Wide Format (12 Kolom Bulan + 3 Total)

| Properti | Detail |
|----------|--------|
| **Masalah** | Struktur wide: 1 baris = 1 rute, 15 kolom waktu |
| **Dampak** | Sama seperti Domestik Bulanan — sulit time-series analysis |
| **Saran** | **Pertimbangkan transformasi ke long format** (1 baris = 1 rute + 1 bulan + 1 tahun) |

**Perbandingan Format:**
```
┌─────────────────────────────────────────────────────────────┐
│ WIDE FORMAT (Saat Ini)                                      │
├─────────────┬────────┬────────┬────────┬──────┬────────────┤
│ Rute        │ Jan-20 │ Feb-20 │ Mar-20 │ ...  │ TOTAL 2020 │
├─────────────┼────────┼────────┼────────┼──────┼────────────┤
│ CGK-SIN     │ 334069 │169342.0│73928.0 │ ...  │  618117.0  │
│ CGK-KUL     │ 229241 │166788.0│82853.0 │ ...  │  510306.0  │
└─────────────┴────────┴────────┴────────┴──────┴────────────┘

┌──────────────────────────────────────────────┐
│ LONG FORMAT (Direkomendasikan untuk ETL)     │
├──────────────┬──────┬───────┬────────────┤
│ Rute         │ Tahun│ Bulan │ Penumpang  │
├──────────────┼──────┼───────┼────────────┤
│ CGK-SIN      │ 2020 │ Jan   │ 334069       │
│ CGK-SIN      │ 2020 │ Feb   │ 169342       │
│ CGK-SIN      │ 2020 │ Mar   │ 73928        │
└──────────────┴──────┴───────┴────────────┘
```

---

### 4. Nomor Urut Tidak Konsisten (Ada Skip)

| Properti | Detail |
|----------|--------|
| **Masalah** | Nomor urut tidak sequential: 140, 141, ..., 147, 148, 149, 150, 151, 152, **155**, **154**, **153**, **156**, **157** |
| **Dampak** | • Tidak bisa pakai `NO` sebagai primary key reliable<br>• Indikasi ada baris yang dihapus/difilter di sumber |
| **Saran** | **Generate surrogate key** (auto-increment ID) saat load ke database |

**Visualisasi Inkonsistensi:**
```
┌─────┬──────────────────────────┐
│ NO  │ RUTE                     │
├─────┼──────────────────────────┤
│ 147 │ CGK-SUB (Kargo)          │
│ 148 │ KUL-BPN (Kargo)          │
│ 149 │ SEM-HAK (kosong)         │
│ 150 │ CGK-HGH (kosong)         │
│ 151 │ TKG-KUL (kosong)         │
│ 152 │ SOC-HAK (kosong)         │
│ 155 │ XMN-DPS (ada data)       │ ← SKIP 153, 154
│ 154 │ CGK-HAN (Kargo)          │ ← Out of order
│ 153 │ SIN-HLP (Kargo)          │ ← Out of order
│ 156 │ CGK-SZB (Kargo)          │
│ 157 │ CGK-LUX (Kargo)          │
└─────┴──────────────────────────┘
```

---

### 5. Baris Total & Footer Metadata

| Properti | Detail |
|----------|--------|
| **Masalah** | Baris terakhir `Total,,...` dan footer `* Rute Codeshare Niaga Berjadwal Luar Negeri` adalah metadata, bukan data rute |
| **Dampak** | Jika dimuat ke database, akan jadi noise/data kotor |
| **Saran** | **Hapus atau pisahkan:** Baris Total → flag `is_total_row = TRUE`. Footer → simpan sebagai metadata terpisah, bukan di tabel utama. |

**Visualisasi:**
```
┌─────┬──────────┬────────┬─────────┬─────────────┐
│ NO  │ RUTE     │ Jan-20 │ Feb-20  │ TOTAL 2020  │
├─────┼──────────┼────────┼─────────┼─────────────┤
│ 1   │ CGK-SIN  │ 334069 │ 169342  │ 618117.0    │
│ ... │ ...      │ ...    │ ...     │ ...         │
│ -   │ **Total**│ -      │ -       │**7187439.0**│ ⚠️
│ *   │ **Rute Codeshare Niaga Berjadwal Luar Negeri** (bukan data) │ ⚠️
└─────┴──────────┴────────┴─────────┴─────────────┘
```

---

### 6. Format Rute dengan Variasi Naming

| Properti | Detail |
|----------|--------|
| **Masalah** | Format rute tidak konsisten — ada yang uppercase semua, ada yang title case, ada yang nama kota panjang |
| **Dampak** | • Sulit join dengan tabel referensi bandara<br>• Sulit query berdasarkan kota |
| **Saran** | **Standardisasi + parse** menjadi kolom terpisah: `asal_kota`, `asal_iata`, `tujuan_kota`, `tujuan_iata` |

**Contoh Inkonsistensi:**
```
┌──────────────────────────────────────────────────────┐
│ VARIASI FORMAT RUTE                                  │
├──────────────────────────────────────────────────────┤
│ "Jakarta (CGK)-SINGAPURA (SIN)"   ← SIN uppercase    │
│ "Kuala Lumpur (KUL)-Denpasar (DPS)" ← Title case     │
│ "Manado (MDC)-Catitipan, Barangay Buhangin (DVO)" ← Panjang │
│ "SINGAPURA (SIN)-Denpasar (DPS)"  ← SIN di depan     │
└──────────────────────────────────────────────────────┘
```

---

### 7. Data COVID-19 Impact (Anomali 2020)

| Properti | Detail |
|----------|--------|
| **Observasi** | Total penumpang 2020 (`7.2M`) turun drastis dari 2019 (estimasi ~50M+) → **↓85%+** |
| **Dampak** | • Data 2020 sangat tidak representatif<br>• Banyak rute cuma operate Jan-Mar<br>• Rute kargo muncul karena konversi dari penumpang |
| **Saran** | **Beri konteks metadata:** Tambahkan flag `is_pandemic_year = TRUE` dan dokumentasi bahwa 2020 adalah outlier ekstrem |

**Visualisasi Dampak COVID:**
```
┌─────────────────────────────────────────────────────┐
│ CONTOH: CGK-SIN (Jakarta-Singapore)                 │
├───────┬──────────────┬──────────────┬───────────────┤
│ Bulan │ 2020         │ 2019 (avg)   │ Perubahan     │
├───────┼──────────────┼──────────────┼───────────────┤
│ Jan   │ 334,069      │ ~350,000     │ ↓ -4.5%       │
│ Feb   │ 169,342      │ ~350,000     │ ↓ -51.6%      │
│ Mar   │ 73,928       │ ~350,000     │ ↓ -78.9%      │
│ Apr   │ 2,604        │ ~350,000     │ ↓ -99.3% ⚠️   │
│ May   │ 1,431        │ ~350,000     │ ↓ -99.6% ⚠️   │
└───────┴──────────────┴──────────────┴───────────────┘
```

---

## 📐 Rekomendasi Skema Database (Gambaran)

### Opsi A: Wide Format (Seperti CSV Asli)

**Konsep:** Satu tabel dengan kolom bulan melebar

**Struktur Logis:**
```
┌──────┬──────────────┬────────┬────────┬──────┬────────┬─────────┐
│ ID   │ Rute         │Jan-20  │Feb-20  │ ...  │Dec-20  │ TOTAL20 │
├──────┼──────────────┼────────┼────────┼──────┼────────┼─────────┤
│ 1    │ CGK-SIN      │ 334069 │169342.0│ ...  │10859.0 │ 618117  │
│ 2    │ CGK-KUL      │ 229241 │166788.0│ ...  │3984.0  │ 510306  │
└──────┴──────────────┴────────┴────────┴──────┴────────┴─────────┘
```

**Kolom yang Dibutuhkan:**
- **Primary Key** (auto-generated ID)
- **Rute** (VARCHAR): format "Asal (IATA)-Tujuan (IATA)"
- **Kolom per Bulan** (DECIMAL): m01_2020, m02_2020, ..., m12_2020
- **Kolom Total Tahun** (DECIMAL): total_2020, total_2019, total_2018
- **Flag Kargo** (BOOLEAN): untuk tandai baris yang ada nilai "KARGO"
- **Flag Total Row** (BOOLEAN): untuk exclude agregasi

**Kelebihan:** 
- ✅ Simple, sesuai format sumber
- ✅ Query langsung tanpa JOIN

**Kekurangan:**
- ❌ Sulit query trend bulanan
- ❌ Row lebar (18 kolom)
- ❌ Nilai "KARGO" perlu handling khusus

**Kapan Pakai Opsi Ini?**
→ Jika hanya untuk **reporting static 2020**

---

### Opsi B: Long Format (Recommended)

**Konsep:** Satu tabel vertikal dengan satu baris = satu rute + satu bulan

**Tabel: Faktapenumpang_bulanan_internasional (Fact Table)**
```
┌──────────┬──────────────┬──────┬───────┬────────────┬──────────┐
│ ID (PK)  │ Rute         │ Tahun│ Bulan │ Penumpang  │ Is_Cargo │
├──────────┼──────────────┼──────┼───────┼────────────┼──────────┤
│ 1        │ CGK-SIN      │ 2020 │ 01    │ 334065     │ FALSE    │
│ 2        │ CGK-SIN      │ 2020 │ 02    │ 169342     │ FALSE    │
│ 3        │ CGK-HAN      │ 2020 │ 01    │ NULL       │ TRUE     │
└──────────┴──────────────┴──────┴───────┴────────────┴──────────┘
```

**Struktur Logis:**
- **Primary Key** (ID unik per record)
- **Rute** (VARCHAR): atau Foreign Key ke tabel master rute
- **Tahun** (INT): 2020, 2019, 2018
- **Bulan** (INT): 1-12
- **Penumpang** (DECIMAL): jumlah penumpang (NULL jika kargo)
- **Is_Cargo** (BOOLEAN): flag rute kargo di bulan tersebut
- **Kategori Rute** (VARCHAR): "Internasional"

**Kelebihan:**
- ✅ Mudah query trend & time-series
- ✅ Bisa track rute kargo dengan flag
- ✅ Scalable untuk data tahun baru

**Kekurangan:**
- ❌ Baris lebih banyak (~1,764 rows untuk 147 rute × 12 bulan)
- ❌ Kolom TOTAL 2018/2019 perlu handling terpisah

**Kapan Pakai Opsi Ini?**
→ Jika data akan dipakai untuk **trend analysis, international route comparison, atau dashboard**

---

### 📊 Perbandingan Kedua Opsi

| Aspek | Wide Format | Long Format |
|-------|-------------|-------------|
| **Jumlah Tabel** | 1 | 1 (atau 2 jika ada master rute) |
| **Jumlah Baris** | ~147 | ~1,764+ (147 rute × 12 bulan) |
| **Jumlah Kolom** | 18 | 6-7 |
| **Handling KARGO** | Sulit (mixed type) | Mudah (flag boolean) |
| **Query Trend Bulanan** | Kompleks (unpivot) | Simple (GROUP BY) |
| **Cocok untuk** | Reporting statis | Analytics & BI |
| **Kompleksitas** | Rendah | Medium |

---

### 🎯 Rekomendasi Final

**Untuk Use Case Data Warehouse:**

```
Pakai LONG FORMAT (Opsi B) karena:
  ✅ Bisa handle nilai "KARGO" dengan flag boolean
  ✅ Mudah bandingkan performa antar bulan/tahun
  ✅ Skalabel jika ada data 2021, 2022, dst
  ✅ Optimal untuk dashboard & international route analysis
```

**Alur ETL Sederhana:**
```
CSV Mentah → Pre-Processing → Load ke Staging → Transform → Load ke Production
     ↓            ↓              ↓              ↓            ↓
  (Parsing    (Clean NULL,   (Tabel       (Unpivot,    (Tabel final
   CSV)        Replace       Sementara)   Flag Kargo,  siap pakai)
               KARGO, Parse                Add Tahun)
               Rute)
```

---

## 🎯 Kesimpulan & Next Steps

### Masalah Kritikal (Harus Ditangani)
1. ✅ Nilai "KARGO" → replace dengan `NULL` + flag `is_cargo`
2. ✅ Missing value (sel kosong → `NULL`)
3. ✅ Baris Total & footer metadata perlu isolasi
4. ✅ Primary key surrogate (kolom `NO` tidak reliable)

### Masalah Struktural (Pertimbangkan Transformasi)
1. ⚠️ Wide → Long format (untuk scalability)
2. ⚠️ Parse rute menjadi asal/tujuan + IATA code
3. ⚠️ Context metadata (COVID-19 impact ekstrem di 2020)

### Next Steps untuk File Ini
- [ ] Tentukan format target (wide vs long)
- [ ] List semua rute dengan "KARGO" untuk dokumentasi
- [ ] Cek konsistensi dengan file Domestik (struktur kolom sama?)
- [ ] Buat script pre-processing
- [ ] Validasi hasil cleaning

---

## 📝 Metadata Tambahan

| Properti | Nilai |
|----------|-------|
| **Analysis Date** | 2026-04-10 |
| **Analyzed By** | Data Engineer (AI Assistant) |
| **Jumlah Rute Unik** | ~147 (perlu verifikasi) |
| **Total Penumpang 2020** | 7,187,439 |
| **Jumlah Rute KARGO** | ~7 baris |
| **Missing Value** | Sel kosong (bukan `-` atau `NULL`) |
| **Encoding** | UTF-8 (asumsi) |
| **Delimiter** | `,` (comma) |

---

> **Catatan:** Dokumen ini hanya fokus pada file Internasional Bulanan 2020. Untuk analisis file lain dalam BAB VI, lihat file markdown terpisah.
