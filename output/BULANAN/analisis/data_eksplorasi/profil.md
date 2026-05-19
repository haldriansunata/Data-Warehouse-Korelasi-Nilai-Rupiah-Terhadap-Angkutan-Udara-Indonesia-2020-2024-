# Profil Data Bulanan (Hasil Eksplorasi)

Hasil run `explore.py`. Detail mentah ada di `profil.txt`. Berikut ringkasan satuan & range tiap kolom:

## Tabel & Jumlah Baris

| Tabel | Baris | Kolom |
|---|---:|---:|
| `dim_waktu_bulanan` | 60 | 11 |
| `dim_rute` | 553 | 5 |
| `dim_bandara` | 232 | 6 |
| `fact_makro_bulanan` | 60 | 14 |
| `fact_penumpang_rute` | 17.118 | 3 |

## Satuan Tiap Kolom Numerik (KRUSIAL — sumber misinterpretasi)

| Kolom | Satuan | Range | Catatan |
|---|---|---|---|
| `avg_kurs_jual` / `_beli` / `_tengah` | **IDR per 1 USD** | 13.732 – 16.329 | Rata-rata harian dalam 1 bulan. |
| `min_kurs_tengah`, `max_kurs_tengah` | IDR per 1 USD | 13.612 – 16.741 | Min/max harian dalam 1 bulan. Selisih (max−min) = volatilitas. |
| `jumlah_hari_trading` | hari | 14 – 23 | Berapa hari kerja BI di bulan tsb. |
| `tarif_tiket_ihk` | **Indeks BPS** (base 100) | 1.248 – 1.788 | BUKAN harga rupiah. Indeks SHK BPS, base = 100 di tahun referensi. Angka 1500 = harga tiket 15× base. |
| `inflasi_yoy` | **% tahunan** | 1,32 – 5,95 | Inflasi umum tahun-ke-tahun. **Sudah dalam %**, jangan dikali 100 lagi. |
| `inflasi_mtm` | **% bulanan** | -0,21 – 1,17 | Inflasi bulan-ke-bulan. Bisa negatif (deflasi). |
| `bi_rate` | **% per tahun** | 3,50 – 6,25 | Suku bunga acuan BI. Sudah dalam %. |
| `brent_usd_bbl` | **USD per barrel** | 26,35 – 115,60 | **USD bukan IDR.** Kalau mau jadi IDR untuk channel cost-push, kalikan `avg_kurs_tengah`. |
| `brent_high` / `brent_low` | USD per barrel | 19,99 – 134,91 | Min/max Brent dalam 1 bulan. Volatilitas pasar minyak. |
| `jumlah_penumpang` | **orang** | per rute: 1 – 501.516; per bulan total: 96.452 – 9.122.039 | Per (waktu_id, rute_id). Sum semua rute = total per bulan. |
| `jumlah_hari_libur` | hari | 0 – 5 | Hari libur nasional dalam bulan tsb. |
| `has_lebaran`, `has_natal`, `is_peak_season` | flag 0/1 | 0 atau 1 | Boolean. |

## Konfirmasi Penting: Brent dalam USD, bukan IDR

Range Brent 26–115 — historis brent crude bergerak 20–130 USD/bbl. Kalau ini IDR, harusnya 6 digit (ratusan ribu sampai jutaan IDR/bbl).

**Implikasi untuk analisis cost-push:** Untuk mengukur biaya BBM dalam mata uang lokal (yang akhirnya muncul di tarif tiket Indonesia), kita harus hitung:

```
Brent IDR per bbl = brent_usd_bbl × avg_kurs_tengah
```

Misal Jan 2020: 56,62 × 13.732,23 ≈ Rp 777.412 per barrel
Sedangkan Jul 2022 (puncak): 105,11 × 14.965,52 ≈ Rp 1.572.876 per barrel (naik ~2× lipat — karena Brent naik DAN kurs melemah).

Ini fenomena **double-shock** yang penting untuk dijelaskan di Bab 3.

### Catatan Penting: Brent ≠ Avtur

Data yang kita miliki adalah **Brent crude oil** (minyak mentah, USD/bbl), BUKAN harga avtur (jet fuel/Jet A-1) langsung. Avtur disuling dari crude oil, sehingga harga avtur sangat berkorelasi (~80–90%, lag 1–2 bulan) dengan Brent, dan dalam literatur transportasi udara **Brent × FX standar dipakai sebagai *proxy upstream* biaya avtur** ketika data avtur langsung tidak tersedia.

**Implikasi untuk paper:** Bab 3 channel cost-push diuji sebagai `kurs → Brent IDR → tarif tiket → penumpang`. Step intermediate "avtur" **tidak diuji langsung** dan menjadi *acknowledged limitation* — paper harus secara eksplisit menyatakan bahwa Brent dipakai sebagai proxy upstream, bukan substitusi harga avtur Indonesia.

## Karakteristik Distribusi Penumpang per Rute

- Median: 5.963 orang/rute/bulan
- Mean: 18.775 (jauh lebih tinggi dari median → distribusi *right-skewed*, didominasi rute besar)
- Max: 501.516 (kemungkinan CGK-DPS di bulan puncak)

**Implikasi analisis:** untuk statistik agregat rute, gunakan **median** atau log-transform untuk menghindari distorsi oleh rute besar. Untuk total nasional, **sum** OK.

## Periode COVID Phase (dari dim_waktu_bulanan)

| Phase | Bulan | Bulan-Tahun |
|---|---:|---|
| pre_pandemic | 2 | Jan–Feb 2020 |
| lockdown | 19 | Mar 2020 – Sep 2021 |
| transisi | 15 | Okt 2021 – Des 2022 |
| recovery | 24 | Jan 2023 – Des 2024 |

Total 60 bulan, distribusi tidak seimbang — `recovery` paling banyak observasi, `pre_pandemic` hanya 2 titik (kurang untuk regresi terpisah, sering digabung ke `lockdown`).

## Field Geografis

- `dim_bandara.negara`: mayoritas INDONESIA, sisanya negara internasional (misal AUSTRALIA, JEPANG, SINGAPURA, dll).
- `dim_bandara.provinsi`: 30+ provinsi Indonesia (dengan kapitalisasi UPPER).
- `dim_rute.kategori`: hanya 2 nilai, DOMESTIK dan INTERNASIONAL.
