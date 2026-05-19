# Bab 1 / WS1 — Multi-panel Time Series

## Tujuan
Menampilkan **empat indikator inti** (penumpang, kurs, Brent, BI rate) dalam satu visual timeline 60 bulan supaya audience paham *konteks* sebelum bicara korelasi.

## Pendekatan
**Time series chart** (line plot) berlapis dalam 4 panel sejajar ke bawah dengan sumbu X tanggal yang sama. Ini paling efektif untuk membandingkan pergerakan multi-variabel di rezim waktu yang sama tanpa berebut skala Y.

## Perhitungan
Tidak ada perhitungan statistik — murni penyajian nilai mentah per bulan:
- Penumpang: `SUM(jumlah_penumpang)` per `waktu_id` (semua rute dijumlahkan).
- Kurs / Brent / BI rate: nilai per bulan langsung dari `fact_makro_bulanan` (sudah agregat bulanan).

```python
# Penumpang per bulan = total semua rute
monthly_pax_sum = pax.groupby("waktu_id")["jumlah_penumpang"].sum()
```

## Hasil dari Data Kamu

| Indikator | Min | Max | Bulan min | Bulan max |
|---|---:|---:|---|---|
| Penumpang | 96.452 | 9.122.039 | Mei 2020 (lockdown puncak) | Jan 2020 (pre-COVID) |
| Kurs | 13.732 | 16.329 | Jan 2020 | Des 2024 |
| Brent | 26,35 | 115,60 | Mar 2020 (oil crash) | Jun 2022 (Russia-Ukraine) |
| BI rate | 3,50 | 6,25 | era PPKM | era pengetatan 2023-2024 |

## Makna Angka
- **Penumpang 96K di Mei 2020** vs 9.12M di Jan 2020 = drop ~99%. Ini *base rate* benchmark crisis untuk industri ini.
- **Kurs naik 19%** (13.732 → 16.329) sepanjang 5 tahun. Bukan crash satu kali, melainkan pelemahan struktural.
- **Brent crash 53%** Jan→Mar 2020 (56,62 → 26,35) lalu lompat 339% ke Jun 2022 — shock minyak ganda.
- **BI rate naik 79%** (3,5 → 6,25) di periode 2022–2023 — respons agresif terhadap pelemahan rupiah & inflasi.

## Reference Lines (event annotations)
Garis vertikal putus-putus menandai 6 event eksternal:
1. PSBB (Mar 2020)
2. PPKM Darurat / Delta wave (Jul 2021)
3. Invasi Rusia–Ukraina (Feb 2022)
4. VOA dibuka (Mei 2022)
5. PPKM dicabut (Jan 2023)
6. Rupiah tembus Rp 16.000 (Apr 2024)

Fungsi: audience bisa langsung mencocokkan perubahan visual di chart dengan event eksternal yang menyebabkannya.

## Output
- `plot.png` — 4-panel chart
- `data_4panel.csv` — data per bulan (60 baris)

## Target Tableau
Buat satu **sheet** dengan `Tanggal Analisis` di Columns (continuous), 4 measure (`SUM(jumlah_penumpang)`, `AVG(avg_kurs_tengah)`, `AVG(brent_usd_bbl)`, `AVG(bi_rate)`) sebagai 4 pil terpisah di Rows. Tambah Reference Lines di tanggal-tanggal di atas. Tableau akan menghasilkan grafik yang sangat mirip dengan PNG di folder ini.
