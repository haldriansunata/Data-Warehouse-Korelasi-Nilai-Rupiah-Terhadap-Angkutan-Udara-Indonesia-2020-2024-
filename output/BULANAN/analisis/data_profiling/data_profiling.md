# Data Profiling — Data Warehouse Bulanan

> Dokumen ini bertujuan supaya **siapapun** (tim, dosen, reviewer paper) bisa memahami struktur data warehouse kami tanpa harus baca kode ETL. Mencakup: skema, sumber data, kolom & tipe, lineage ETL, dan catatan kualitas data.

**Dataset**: Korelasi Nilai Rupiah terhadap Angkutan Udara Indonesia (2020–2024)
**Grain bulanan**: 60 bulan × ~286 rute aktif
**Hasil cek terakhir**: lihat `profil_raw_stats.txt` (output `explore.py`)

---

## 1. Overview Skema (Star Schema)

```
                     ┌────────────────────────┐
                     │  dim_waktu_bulanan     │
                     │  (60 baris, 11 kolom)  │
                     │  PK: waktu_id          │
                     └──────────┬─────────────┘
                                │ 1
                                │
                                │ N
                                ▼
   ┌──────────────────┐    ┌──────────────────────┐    ┌──────────────────────┐
   │  dim_bandara     │    │ fact_penumpang_rute  │    │ fact_makro_bulanan   │
   │  (235 baris, 6)  │    │  (17.118 baris, 3)   │    │  (60 baris, 15)      │
   │  PK: bandara_id  │    │  grain: (waktu, rute)│    │  grain: bulanan      │
   └────────┬─────────┘    │  FK: waktu_id, rute  │    │  FK: waktu_id        │
            │ 1            └──────────┬───────────┘    └──────────────────────┘
            │                          │ N
            │ N                        │
            │              ┌───────────▼─────────────┐
            │              │  dim_rute               │
            └──── 2× ──────┤  (553 baris, 5 kolom)   │
                           │  PK: rute_id            │
                           │  FK: bandara_1_id,      │
                           │      bandara_2_id       │
                           └─────────────────────────┘
```

**Catatan join**:
- `dim_bandara` di-join **2 kali** ke `dim_rute` (origin via `bandara_1_id`, destination via `bandara_2_id`). Self-join klasik untuk OD pair.
- `fact_makro_bulanan` tidak punya FK ke rute — makro variable sifatnya nasional/bulanan.

---

## 2. Daftar Tabel & Ukuran

| Tabel | Tipe | Baris | Kolom | File CSV |
|---|---|---:|---:|---|
| `dim_waktu_bulanan` | Dimension | **60** | 11 | `dim_waktu_bulanan.csv` |
| `dim_bandara` | Dimension | **235** | 6 | `dim_bandara.csv` |
| `dim_rute` | Dimension | **553** | 5 | `dim_rute.csv` |
| `fact_makro_bulanan` | Fact | **60** | 15 | `fact_makro_bulanan.csv` |
| `fact_penumpang_rute` | Fact | **17.118** | 3 | `fact_penumpang_rute.csv` |

Lokasi: semua di `output/BULANAN/`. ETL script: `output/BULANAN/etl_bulanan/`.

---

## 3. Detail Per Tabel

### 3.1 `dim_waktu_bulanan` — Dimensi Waktu

**Grain**: 1 baris = 1 bulan kalender. 60 baris = Januari 2020 sampai Desember 2024.

**Source ETL**: `etl_bulanan/01_dim_waktu.py` (basic) + di-enrich oleh `build_makro_warehouse.py` (covid_phase, hari libur, dll).

**Schema**:
| Kolom | Tipe | Contoh | Satuan / Domain | Keterangan |
|---|---|---|---|---|
| `waktu_id` | int64 (PK) | 202001 | YYYYMM | Surrogate key, format `tahun*100+bulan` |
| `tahun` | int64 | 2020 | 2020-2024 | |
| `bulan` | int64 | 1 | 1-12 | |
| `nama_bulan` | str | Januari | Januari-Desember | Nama bulan Bahasa Indonesia |
| `kuartal` | int64 | 1 | 1-4 | Q1=Jan-Mar, dst |
| `semester` | int64 | 1 | 1-2 | S1=Jan-Jun, S2=Jul-Des |
| `covid_phase` | str | pre_pandemic | 4 nilai (lihat ↓) | Fase pandemi yang dipakai untuk faceted regression (Bab 4) |
| `has_lebaran` | int64 (0/1) | 0 | flag | 1 = bulan ini termasuk hari raya Idul Fitri |
| `has_natal` | int64 (0/1) | 0 | flag | 1 = bulan Desember (semua tahun) |
| `is_peak_season` | int64 (0/1) | 0 | flag | 1 = bulan peak season (Lebaran OR Juni-Juli OR Desember) |
| `jumlah_hari_libur` | int64 | 2 | 0-5 hari | Jumlah hari libur nasional di bulan tsb |

**4 nilai `covid_phase`** (dari ETL `build_makro_warehouse.py`):

| Phase | Periode | n bulan | Definisi |
|---|---|---:|---|
| `pre_pandemic` | ≤ Feb 2020 | 2 | Sebelum WHO declare pandemic |
| `lockdown` | Mar 2020 – Sep 2021 | 19 | PSBB → PPKM Darurat era |
| `transisi` | Okt 2021 – Des 2022 | 15 | Reopening bertahap |
| `recovery` | Jan 2023 – Des 2024 | 24 | PPKM resmi dicabut |

**Bulan Lebaran** (`has_lebaran=1`): Mei 2020, Mei 2021, Mei 2022, April 2023, April 2024.

---

### 3.2 `dim_bandara` — Dimensi Bandara

**Grain**: 1 baris = 1 bandara unik (IATA-based).

**Source ETL**: `etl_bulanan/03_dim_bandara.py`
**Source data**:
- `DJPU/Table_Pilihan/BAB III — Rute & Bandara/*` (CSV tahunan)
- `DJPU/Table_Pilihan/BAB VI — Penumpang Per Rute/*` (CSV tahunan)
- Library Python `airportsdata` (lookup nama bandara, kota, provinsi, negara berdasar IATA)
- **8 manual overrides** untuk nama kota yang kotor di source asli (lihat `CITY_OVERRIDES` di `03_dim_bandara.py`).

**Schema**:
| Kolom | Tipe | Contoh | Catatan |
|---|---|---|---|
| `bandara_id` | int64 (PK) | 1 | Surrogate key (auto-increment) |
| `nama_bandara` | str | AJI PANGERAN TUMENGGUNG PRANOTO INTL | Dari airportsdata, kapitalisasi UPPER |
| `iata` | str (3 char) | AAP | IATA code, unique |
| `kota` | str | SAMARINDA | Kota Bahasa Indonesia |
| `provinsi` | str | KALIMANTAN TIMUR | ⚠️ **MIX Inggris/Indonesia** (lihat §5.2) |
| `negara` | str | INDONESIA | ⚠️ **Sebagian kode ISO 2-letter** (lihat §5.1) |

**Distribusi**: ~210 bandara domestik (Indonesia), ~25 internasional.

---

### 3.3 `dim_rute` — Dimensi Rute

**Grain**: 1 baris = 1 pasangan bandara unik (sorted alphabetically).

**Source ETL**: `etl_bulanan/04_dim_rute.py`
**Source data**: `DJPU/Table_Pilihan/BAB III — Rute & Bandara/*` (CSV tahunan)
**Depend on**: `dim_bandara.csv` (untuk lookup `bandara_id`)

**Schema**:
| Kolom | Tipe | Contoh | Catatan |
|---|---|---|---|
| `rute_id` | int64 (PK) | 1 | Surrogate key |
| `kode_rute` | str | AAP-BDJ | Format `IATA1-IATA2`, **alphabetically sorted** (PENTING — lihat catatan ↓) |
| `bandara_1_id` | int64 (FK) | 1 | → `dim_bandara.bandara_id` (IATA awal alfabet) |
| `bandara_2_id` | int64 (FK) | 12 | → `dim_bandara.bandara_id` (IATA akhir alfabet) |
| `kategori` | str | DOMESTIK | DOMESTIK (397) atau INTERNASIONAL (156) |

**⚠️ Catatan kritikal — alfabetis sort**:
ETL menyimpan pasangan bandara dengan IATA terurut alfabetis. Akibat:
- Rute CGK→DPS dan DPS→CGK **digabung jadi 1 entry** `kode_rute = CGK-DPS` (karena C < D).
- `bandara_1_id` = bandara dengan IATA alfabet **lebih awal** (mis. AAP, BDJ, BPN, CGK).
- `bandara_2_id` = bandara dengan IATA alfabet **lebih akhir** (mis. UPG, SUB, YIA).
- Konsekuensi untuk OD matrix (Bab 5 WS4): top 10 origin ≠ top 10 destination — bukan bug, struktur.

---

### 3.4 `fact_makro_bulanan` — Fact Makro Bulanan

**Grain**: 1 baris = 1 bulan. 60 baris = 5 tahun × 12 bulan. **Tidak ada relasi ke rute** (sifatnya nasional).

**Source ETL**: `etl_bulanan/05_fact_kurs.py` (intermediate) + `build_makro_warehouse.py` (final merge dengan 5 sumber lain).

**Source data — 6 sumber**:
| Field | Source File | Origin |
|---|---|---|
| `avg/min/max_kurs_*` | `KURS/BI.csv` | Bank Indonesia kurs harian |
| `jumlah_hari_trading` | `KURS/BI.csv` | hitungan otomatis (count hari kerja BI) |
| `tarif_tiket_ihk` | `data_tambahan/BPS/Survei Harga Konsumen.../harga-konsumen-nasional-beberapa-barang-dan-jasa(2020-2024).csv` | BPS SHK |
| `inflasi_yoy` | `data_tambahan/BI/Data Inflasi.xlsx` | Bank Indonesia inflasi YoY |
| `inflasi_mtm` | `data_tambahan/BPS/Inflasi Bulanan (M-to-M) (Persen)/...` | BPS inflasi MoM |
| `bi_rate` | `data_tambahan/BPS/BI RATE/BI_RATE_2020-2024.csv` | Bank Indonesia BI Rate |
| `brent_usd_bbl`, `brent_high`, `brent_low` | `data_tambahan/BRENT/Brent Oil Futures Historical Data.csv` | Investing.com Brent futures |
| `brent_idr_per_bbl` | **derived** | `brent_usd_bbl × avg_kurs_tengah` (dihitung di ETL, lihat §5.5) |

**Schema** (15 kolom):
| Kolom | Tipe | Range | Satuan | Catatan |
|---|---|---|---|---|
| `waktu_id` | int64 (PK, FK) | 202001-202412 | YYYYMM | → `dim_waktu_bulanan` |
| `avg_kurs_jual` | float | 13.800 – 16.404 | **IDR per 1 USD** | Rata-rata harian kurs jual dalam 1 bulan |
| `avg_kurs_beli` | float | 13.663 – 16.249 | IDR per 1 USD | Rata-rata harian kurs beli |
| `avg_kurs_tengah` | float | **13.732 – 16.329** | IDR per 1 USD | (avg_jual + avg_beli) / 2 — yang dipakai analisis |
| `min_kurs_tengah` | float | 13.612 – 16.277 | IDR per 1 USD | Min harian dalam bulan tsb |
| `max_kurs_tengah` | float | 13.961 – 16.741 | IDR per 1 USD | Max harian dalam bulan tsb |
| `jumlah_hari_trading` | int | 14 – 23 | hari | Berapa hari BI publish kurs (= hari kerja) |
| `tarif_tiket_ihk` | int | 1.248 – 1.788 | **Indeks BPS** (base 100) | ⚠️ BUKAN harga rupiah |
| `inflasi_yoy` | float | 1,32 – 5,95 | **% tahunan** | Sudah dalam %, jangan dikali 100 |
| `inflasi_mtm` | float | -0,21 – 1,17 | **% bulanan** | Bisa negatif (deflasi) |
| `bi_rate` | float | 3,50 – 6,25 | **% per tahun** | Suku bunga acuan BI |
| `brent_usd_bbl` | float | 26,35 – 115,60 | **USD per barrel** | Brent crude, BUKAN avtur (lihat §5.4) |
| `brent_high` | float | – 134,91 | USD per barrel | Max harian dalam bulan tsb |
| `brent_low` | float | 19,99 – | USD per barrel | Min harian dalam bulan tsb |
| `brent_idr_per_bbl` | float | 420.183 – 1.746.844 | **IDR per barrel** | Derived: `brent_usd_bbl × avg_kurs_tengah`, untuk channel cost-push (Bab 3) |

**Periode**: 202001 (Jan 2020) – 202412 (Des 2024), tidak ada gap.

---

### 3.5 `fact_penumpang_rute` — Fact Penumpang per Rute Bulanan

**Grain**: 1 baris = 1 kombinasi (bulan × rute). 17.118 baris ≈ 60 bulan × 286 rute aktif rata-rata (banyak rute tidak operasi tiap bulan).

**Source ETL**: `etl_bulanan/06_fact_penumpang_rute.py`
**Source data**: `DJPU/Table_Pilihan/BAB VI — Penumpang Per Rute/*` (CSV tahunan)
**Depend on**: `dim_rute.csv` (untuk lookup `rute_id`)

**Schema**:
| Kolom | Tipe | Range | Catatan |
|---|---|---|---|
| `waktu_id` | int64 (FK) | 202001-202412 | → `dim_waktu_bulanan` |
| `rute_id` | int64 (FK) | 1-553 | → `dim_rute` |
| `jumlah_penumpang` | int | **1 – 501.516** | per (bulan × rute). PP digabung di pair alfabetis. |

**Distribusi jumlah_penumpang per row**:
- Median: 5.963 orang/rute/bulan
- Mean: 18.775 (right-skewed — beberapa rute besar dominan)
- Max: 501.516 (kemungkinan CGK-DPS di bulan puncak)

**Distribusi total nasional per bulan** (SUM semua rute):
- Min: 96.452 (Mei 2020, puncak lockdown)
- Max: 9.122.039 (Januari 2020, pre-pandemic)
- 5 tahun: drop dari 9M → 96K → recovery ke ~8M.

**Implikasi statistik**: untuk per-rute, pakai **median** (Mann-Whitney Bab 4 WS3/4). Untuk total nasional, **sum** OK.

---

## 4. Lineage ETL — Urutan Eksekusi

ETL dijalankan via `run_all_bulanan.py`:

```
RAW INPUT                                ETL SCRIPT                        OUTPUT
────────────────────────────────────────────────────────────────────────────────────
KURS/BI.csv (harian)                  → 05_fact_kurs.py                  → _tmp/fact_kurs_bulanan.csv
DJPU/BAB III/* (rute)                 → 03_dim_bandara.py                → dim_bandara.csv (FINAL)
DJPU/BAB III/* + dim_bandara          → 04_dim_rute.py                   → dim_rute.csv (FINAL)
DJPU/BAB VI/* (penumpang) + dim_rute  → 06_fact_penumpang_rute.py        → fact_penumpang_rute.csv (FINAL)
(no input)                            → 01_dim_waktu.py                  → _tmp/dim_waktu_bulanan.csv (basic)

fact_kurs + dim_waktu basic + 5       → build_makro_warehouse.py         → dim_waktu_bulanan.csv (FINAL, enriched)
sumber makro (BI rate, inflasi,                                          → fact_makro_bulanan.csv (FINAL)
SHK tarif, Brent)
```

**Script tambahan**:
- `patch_brent_idr.py` — patch `fact_makro_bulanan.csv` untuk tambah kolom `brent_idr_per_bbl` tanpa rebuild full ETL.

---

## 5. Catatan Kualitas Data & Caveat Penting

### 5.1 `dim_bandara.negara` — Campuran Nama Lengkap & Kode ISO

Library `airportsdata` mengisi field `negara` dengan:
- **Nama lengkap** untuk negara utama (INDONESIA, MALAYSIA, SINGAPURA, FILIPINA, JEPANG, dll).
- **Kode ISO 2-letter** untuk negara yang tidak di-override manual (EG=Egypt, ET=Ethiopia, FJ=Fiji, HN=Honduras, LU=Luxembourg, MO=Macau, OM=Oman, PG=Papua Nugini, RU=Russia, UZ=Uzbekistan, VU=Vanuatu).

**Skala**: ~11 negara kode ISO. Tidak masuk Top 14 by traffic, jadi tidak mempengaruhi headline analisis Bab 5 WS3.

### 5.2 `dim_bandara.provinsi` — Mix Bahasa Indonesia & Inggris

Field `provinsi` punya **18 pasangan duplikat** karena ETL campur:
- Library `airportsdata` default Bahasa Inggris (EAST KALIMANTAN, JAKARTA, WEST PAPUA, dll)
- Override manual Bahasa Indonesia (KALIMANTAN TIMUR, DKI JAKARTA, PAPUA BARAT, dll)

Contoh duplikat:
- JAKARTA + DKI JAKARTA
- EAST KALIMANTAN + KALIMANTAN TIMUR
- RIAU ISLANDS + KEPULAUAN RIAU
- (15 pasangan lainnya — lihat tutorial `bab_5_heterogenitas/ws5_provinsi/penjelasan.md` Step 1)

**Solusi di Tableau**: pakai **Group** di field `Provinsi` untuk konsolidasi (lihat tutorial WS5).

Plus **25 row dengan provinsi = "UNKNOWN"** — bandara domestik kecil yang library tidak kenal provinsinya (BWX Banyuwangi, EWE Merauke, SRI Samarinda, dll). Total ~0,3% pax — exclude saat presentasi.

### 5.3 `dim_rute.kode_rute` — Pair Alfabetis

`kode_rute` di-normalize alfabetis (`A-B` di mana A < B). PP (pulang-pergi) digabung. Lihat §3.3.

Implikasi untuk Bab 5 WS4 OD Matrix: top 10 origin ≠ top 10 destination — solusi pakai daftar IATA tunggal untuk kedua axis.

### 5.4 `brent_usd_bbl` — Brent ≠ Avtur

Data yang dimiliki adalah **Brent crude oil** (minyak mentah, USD/bbl), BUKAN harga avtur langsung. Avtur disuling dari crude oil, dalam literatur transportasi udara **Brent × FX dipakai sebagai *proxy upstream* biaya avtur** ketika data avtur langsung tidak tersedia.

**Implikasi paper**: Bab 3 channel cost-push diuji sebagai `kurs → Brent IDR → tarif tiket → penumpang`. Step intermediate "avtur" **tidak diuji langsung** — paper harus eksplisit menyatakan ini sebagai *acknowledged limitation*.

### 5.5 `brent_idr_per_bbl` — Derived Column

Bukan dari source mentah, tapi dihitung di ETL:
```python
brent_idr_per_bbl = brent_usd_bbl × avg_kurs_tengah
```

Contoh:
- Jan 2020: 56,62 × 13.732,23 ≈ 777.412 IDR/bbl
- Jul 2022 (puncak Russia-Ukraine): 105,11 × 14.965,52 ≈ 1.572.876 IDR/bbl (naik ~2× lipat — fenomena **double-shock**: Brent naik DAN kurs melemah).

Range: 420.183 – 1.746.844 IDR/bbl (Apr 2020 oil crash sampai Jun 2022 peak).

### 5.6 Tarif IHK ≠ Harga Rupiah

`tarif_tiket_ihk` (1.248 – 1.788) adalah **Indeks SHK BPS** (base 100), BUKAN harga tiket dalam rupiah. Angka 1.788 = harga tiket ~17,88× harga base tahun referensi. Interpretasi slope di Bab 3 WS3 harus dalam unit **indeks**, bukan rupiah.

---

## 6. Cek Data Cepat (untuk Verifikasi Tim)

Jalankan untuk regenerate `profil_raw_stats.txt`:
```bash
python output/BULANAN/analisis/data_profiling/explore.py
```

Output: dtype + describe() + sample 5 baris tiap tabel.

Untuk regenerate semua CSV dari scratch (kalau curiga ada corruption):
```bash
python output/BULANAN/etl_bulanan/run_all_bulanan.py
```

Output `output/BULANAN/*.csv` akan **byte-identical** dengan versi yang di-commit (verified earlier).

---

## 7. Referensi Cepat Foreign Key

```
dim_waktu_bulanan.waktu_id
  ← fact_makro_bulanan.waktu_id   (1:1, exactly 60)
  ← fact_penumpang_rute.waktu_id  (1:N, ~286 rute per bulan)

dim_rute.rute_id
  ← fact_penumpang_rute.rute_id   (1:N, ~30 bulan aktif per rute)

dim_bandara.bandara_id
  ← dim_rute.bandara_1_id  (1:N, sebagai origin)
  ← dim_rute.bandara_2_id  (1:N, sebagai destination)
```

Di Tableau, join di-set di Data Source tab:
- `fact_penumpang_rute.waktu_id` ↔ `dim_waktu_bulanan.waktu_id`
- `fact_penumpang_rute.rute_id` ↔ `dim_rute.rute_id`
- `dim_rute.bandara_1_id` ↔ `dim_bandara_origin.bandara_id`
- `dim_rute.bandara_2_id` ↔ `dim_bandara_destination.bandara_id` (instance kedua)
- `fact_penumpang_rute.waktu_id` ↔ `fact_makro_bulanan.waktu_id`

---

## 8. Glossary Singkat (untuk Dosen / Reviewer)

| Istilah | Arti |
|---|---|
| **Star schema** | Skema data warehouse dengan 1 fact di tengah + multiple dim di sekitar (seperti bintang) |
| **Grain** | Tingkat detail 1 baris fact (di sini: bulan × rute, atau bulan saja) |
| **Surrogate key** | Primary key buatan ETL (bukan dari source), mis. `bandara_id` auto-increment |
| **OD pair** | Origin-Destination pair (pasangan bandara) |
| **YoY / MoM** | Year-on-Year / Month-on-Month (tahun-ke-tahun / bulan-ke-bulan) |
| **IHK / SHK** | Indeks Harga Konsumen / Survei Harga Konsumen (BPS) |
| **Spurious correlation** | Korelasi yang muncul karena variabel ketiga (confounder), bukan kausal langsung |
| **COVID phase** | Stratifikasi 60 bulan ke 4 fase: pre_pandemic, lockdown, transisi, recovery |
| **Pass-through** | Mekanisme harga naik di hulu (Brent, FX) "diteruskan" ke hilir (tarif tiket) |
