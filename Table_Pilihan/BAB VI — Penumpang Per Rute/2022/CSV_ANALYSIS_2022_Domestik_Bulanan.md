# CSV Analysis: Jumlah Penumpang Per Rute — Domestik Bulanan 2022

## 📊 Informasi Umum

| Properti | Nilai |
|----------|-------|
| **Nama File** | `JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI JAN-DES 2022.csv` |
| **Sumber** | Extract dari PDF (Kemenhub/DJPU) |
| **Periode** | Januari - Desember 2022 |
| **Jumlah Baris** | 377 (1 header + 374 rute + 1 Total + 1 empty) |
| **Jumlah Kolom** | 15 |
| **Tipe Data Utama** | Float dengan titik sebagai pemisah ribuan (contoh: `324.111`) |
| **Missing Value** | Sel kosong |

---

## ⚠️ PERBEDAAN SANGAT SIGNIFIKAN vs 2020-2021

### 1. Format Angka Berubah Total!

| Tahun | Format Angka | Contoh |
|-------|--------------|--------|
| **2020** | Integer tanpa pemisah | `231865` |
| **2021** | Float dengan `.0` suffix | `107991.0` |
| **2022** | **Float dengan titik sebagai pemisah ribuan** | `324.111` (= 324,111) |

**Ini perubahan KRUSIAL!** Titik di 2022 adalah **pemisah ribuan**, bukan desimal!

### 2. Nama Kolom Bulan

| Tahun | Format |
|-------|--------|
| **2020** | `Jan-20`, `Feb-20`, ..., `May-20`, `Aug-20`, `Oct-20`, `Dec-20` (Bahasa Inggris) |
| **2021** | `Jan-21`, `Feb-21`, ..., `Mei-21`, `Agu-21`, `Okt-21`, `Des-21` (Bahasa Indonesia) |
| **2022** | **`Jan-22`, `Feb-22`, ..., `May-22`, `Jun-22`, ...** (Bahasa Inggris kembali!) |

### 3. Format Rute

| Tahun | Format | Contoh |
|-------|--------|--------|
| **2020** | Tanpa spasi | `Jakarta (CGK)-Denpasar (DPS)` |
| **2021** | Ada spasi | `Jakarta (CGK) - Denpasar (DPS)` |
| **2022** | **Hanya IATA code** | `CGK-DPS` |

### 4. Kolom Komparasi

| Tahun | Kolom |
|-------|-------|
| **2020** | `TOTAL 2020`, `TOTAL 2019`, `TOTAL 2018` |
| **2021** | `TOTAL 2021`, `TOTAL 2020`, `TOTAL 2019` |
| **2022** | **Hanya `TOTAL 2022`** (tidak ada komparasi tahun sebelumnya!) |

### 5. Jumlah Rute

| Tahun | Jumlah Rute Domestik |
|-------|---------------------|
| **2020** | 410 |
| **2021** | 379 |
| **2022** | **374** (berkurang lagi) |

---

## 🗂️ Struktur Tabel 2022

### Skema Saat Ini

```
NO (float - ada .0)
RUTE ( PP) (string - hanya IATA code)
Jan-22 (float - titik = pemisah ribuan)
Feb-22 (float)
Mar-22 (float)
Apr-22 (float)
May-22 (float) - Bahasa Inggris
Jun-22 (float)
Jul-22 (float)
Aug-22 (float) - Bahasa Inggris
Sep-22 (float)
Oct-22 (float) - Bahasa Inggris
Nov-22 (float)
Dec-22 (float) - Bahasa Inggris
TOTAL 2022 (float)
```

### Detail Per Kolom

| No | Nama Kolom | Deskripsi | Tipe Data Saat Ini | Tipe Data Rekomendasi | Nullable | Contoh Nilai |
|----|-----------|-----------|-------------------|----------------------|----------|--------------|
| 1 | `NO` | Nomor urut rute | Float | `INT` | ❌ No | `1.0`, `2.0`, ..., `374.0` |
| 2 | `RUTE ( PP)` | Rute (hanya IATA code) | String | `VARCHAR(20)` | ❌ No | `CGK-DPS` |
| 3-14 | `Jan-22` s/d `Dec-22` | Jumlah penumpang per bulan | Float (titik = ribuan) | `INT` | ✅ Yes | `324.111` (= 324,111) |
| 15 | `TOTAL 2022` | Total akumulasi 2022 | Float | `DECIMAL(15,2)` | ✅ Yes | `4342921.0` |

**⚠️ PENTING:** 
- **Titik adalah pemisah ribuan**, BUKAN desimal!
- `324.111` = 324,111 (tiga ratus dua puluh empat ribu seratus sebelas)
- `4342921.0` di TOTAL = 4,342,921 (tanpa titik sebagai pemisah)

---

## 🔍 Analisis Nilai Unik & Distribusi

### Kolom Kategorikal

#### 1. `NO`
- **Nilai Unik:** 374 (1.0 - 374.0)
- **Format:** Float dengan `.0` (contoh: `1.0`, `2.0`)
- **Catatan:** ✅ **KONSISTEN** sequential

#### 2. `RUTE ( PP)`
- **Nilai Unik:** 374 rute domestik
- **Format:** **HANYA IATA CODE** — `CGK-DPS` (bukan nama kota lengkap)
- **Contoh:**
  - `CGK-DPS` (Jakarta-Denpasar)
  - `CGK-KNO` (Jakarta-Medan)
  - `UPG-SUB` (Makassar-Surabaya)
- **Catatan:** ⚠️ **Sangat berbeda dari 2020-2021** yang pakai nama kota lengkap!

#### 3. Kolom Bulanan
- **Format:** Float dengan titik sebagai pemisah ribuan
- **Range:** 0 hingga 484,186 (`460.495` di Des-22 untuk CGK-DPS)
- **Missing Value:** Sel kosong

#### 4. Kolom Total
- **Baris Total:** `56,408,353` (TOTAL 2022)
- **Insight:** Recovery dari 2021 (`33.3M`) → 2022 (`56.4M`) = ↑ +69.2%

---

## ⚠️ Potensi Masalah & Saran Pre-Processing

### 1. Format Angka dengan Titik sebagai Pemisah Ribuan (KRUSIAL!)

| Properti | Detail |
|----------|--------|
| **Masalah** | Angka pakai titik sebagai pemisah ribuan: `324.111` = 324,111 |
| **Dampak** | • Jika dibaca sebagai float biasa, akan jadi 324.111 (salah!)<br>• Harus parse sebagai string dulu, hapus titik, baru convert ke integer |
| **Saran** | **Parsing khusus:**<br>1. Baca sebagai string<br>2. Hapus titik: `"324.111"` → `"324111"`<br>3. Convert ke integer: `324111` |

**Visualisasi Transformasi:**
```
SEBELUM:  "324.111"   →  Hapus titik: "324111"  →  SESUDAH:  324111
SEBELUM:  "460.495"   →  Hapus titik: "460495"  →  SESUDAH:  460495
SEBELUM:  "4342921.0" →  Hapus .0: "4342921"    →  SESUDAH:  4342921
```

### 2. Format Rute Hanya IATA Code (Perlu Mapping)

| Properti | Detail |
|----------|--------|
| **Masalah** | Rute hanya IATA code: `CGK-DPS` vs 2020-2021: `Jakarta (CGK)-Denpasar (DPS)` |
| **Dampak** | • Tidak bisa join langsung dengan data 2020-2021<br>• Perlu mapping table IATA code ↔ nama kota |
| **Saran** | **Buat mapping table** atau tambahkan kolom nama kota lengkap |

**Visualisasi Mapping:**
```
2022: "CGK-DPS"         ← Hanya IATA
2021: "Jakarta (CGK) - Denpasar (DPS)"
2020: "Jakarta (CGK)-Denpasar (DPS)"

Standard: "Jakarta (CGK)-Denpasar (DPS)" ← Pilih format 2020
```

### 3. Nama Kolom Bulan Bahasa Inggris (vs 2021 Bahasa Indonesia)

| Properti | Detail |
|----------|--------|
| **Masalah** | 2022: `May-22`, `Aug-22`, `Oct-22`, `Dec-22` vs 2021: `Mei-21`, `Agu-21`, `Okt-21`, `Des-21` |
| **Saran** | **Standardisasi:** `m01_2022`, `m02_2022`, ..., `m12_2022` |

### 4. Tidak Ada Kolom Komparasi Tahun Sebelumnya

| Properti | Detail |
|----------|--------|
| **Masalah** | 2022 hanya punya `TOTAL 2022`, tidak ada `TOTAL 2021` atau `TOTAL 2020` |
| **Dampak** | • Sulit bandingkan langsung di CSV<br>• Harus join dengan file 2021 terpisah |
| **Saran** | **Join di database** setelah load ke fact table |

### 5. Jumlah Rute Berkurang Lagi

| Properti | Detail |
|----------|--------|
| **Observasi** | 2020: 410 → 2021: 379 → 2022: **374** |
| **Insight** | Ada 36 rute yang hilang dari 2020 ke 2022 |
| **Saran** | **Track route lifecycle:** flag `is_active` per tahun |

### 6. Baris Total Tanpa Label

| Properti | Detail |
|----------|--------|
| **Masalah** | Baris terakhir `,,4291237.0,...` tanpa label "Total" |
| **Saran** | **Flag** `is_total_row = TRUE` |

---

## 📐 Rekomendasi Skema Database

**Sama seperti tahun sebelumnya — Long Format recommended.**

**Catatan Khusus untuk 2022:**
- Perlu **mapping table** untuk convert IATA code ke nama kota
- Perlu **parsing khusus** untuk handle titik sebagai pemisah ribuan

---

## 🎯 Kesimpulan & Next Steps

### Masalah Kritikal (Harus Ditangani)
1. ✅ **Format angka dengan titik sebagai pemisah ribuan** (PARSE KHUSUS!)
2. ✅ **Format rute hanya IATA code** (perlu mapping ke nama kota)
3. ✅ Nama kolom bulan berbeda (Bahasa Inggris vs 2021 Bahasa Indonesia)
4. ✅ Tidak ada kolom komparasi tahun sebelumnya
5. ✅ Missing value (sel kosong → `NULL`)
6. ✅ Baris Total perlu flag

### Next Steps untuk File Ini
- [ ] Buat parser khusus untuk handle titik sebagai pemisah ribuan
- [ ] Buat mapping table IATA code ↔ nama kota
- [ ] Standardisasi nama kolom bulan
- [ ] Unpivot ke long format

---

## 📝 Metadata Tambahan

| Properti | Nilai |
|----------|-------|
| **Analysis Date** | 2026-04-10 |
| **Analyzed By** | Data Engineer (AI Assistant) |
| **Jumlah Rute Unik** | 374 |
| **Total Penumpang 2022** | 56,408,353 |
| **Growth 2022 vs 2021** | ↑ **+69.2%** (recovery dari COVID) |
| **Growth 2022 vs 2019** | ↓ -43.9% (belum full recovery) |
| **Format Angka** | **Titik = pemisah ribuan** (BERBEDA dari 2020-2021) |
| **Format Rute** | **Hanya IATA code** (BERBEDA dari 2020-2021) |

**Perbedaan Signifikan vs Tahun Sebelumnya:**
| Aspek | 2020 | 2021 | **2022** |
|-------|------|------|----------|
| **Jumlah Rute** | 410 | 379 | **374** |
| **Format Rute** | Nama kota + IATA | Nama kota + IATA | **Hanya IATA** ⚠️ |
| **Format Angka** | Integer | Float (.0) | **Titik = ribuan** ⚠️ |
| **Nama Bulan** | Inggris | Indonesia | **Inggris** |
| **Kolom Komparasi** | 2019, 2018 | 2020, 2019 | **Tidak ada** ⚠️ |
| **Jumlah Kolom** | 18 | 18 | **15** |

---

> **Catatan:** Dokumen ini hanya fokus pada file Domestik Bulanan 2022. File ini punya perbedaan SANGAT SIGNIFIKAN dari 2020-2021 yang perlu penanganan khusus saat ETL.
