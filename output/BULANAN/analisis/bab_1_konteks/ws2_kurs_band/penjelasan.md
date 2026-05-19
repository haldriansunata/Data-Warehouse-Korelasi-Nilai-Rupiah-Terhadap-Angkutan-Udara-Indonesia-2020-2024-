# Bab 1 / WS2 — Kurs Band (Volatilitas Bulanan)

## Tujuan
Menampilkan kurs **bukan sebagai satu angka per bulan**, melainkan sebagai *range* harian (min sampai max). Volatilitas adalah informasi yang hilang kalau cuma melihat rata-rata.

## Pendekatan
**Filled band chart**: area antara `min_kurs_tengah` dan `max_kurs_tengah` di-shade transparan, dengan line `avg_kurs_tengah` di tengahnya. Tebal-tipis band menunjukkan stres pasar.

## Perhitungan
```
spread = max_kurs_tengah − min_kurs_tengah   # untuk setiap bulan
```

Spread besar = pasar volatil dalam bulan itu (intervensi BI, sentimen risiko, capital outflow, dll).

## Hasil dari Data Kamu

| Statistik | Nilai |
|---|---:|
| Spread rata-rata | 385 IDR/bulan |
| Spread max (paling volatil) | **2.440 IDR** (Mar 2020) |
| Spread min (paling stabil) | ~50 IDR (banyak bulan tenang) |

### Top 5 bulan paling volatil

| Tanggal | Min | Max | Spread |
|---|---:|---:|---:|
| Mar 2020 | 14.168 | 16.608 | **2.440** |
| Apr 2020 | 15.157 | 16.741 | **1.584** |
| Aug 2024 | 15.380 | 16.294 | 914 |
| Jan 2023 | 14.930 | 15.635 | 705 |
| Nov 2020 | 14.015 | 14.718 | 703 |

## Makna Angka
- **Mar 2020 dengan spread 2.440 IDR** = pasar valas chaos awal pandemi. Range 14.168–16.608 dalam satu bulan = pergerakan 17%. Ini adalah event volatilitas terbesar dalam periode analisis.
- **Aug 2024 spread 914** = bulan menjelang puncak pelemahan rupiah pasca eskalasi Timur Tengah.
- **Bulan dengan spread <100 IDR** (mayoritas 2022–2023 awal recovery) = pasar tenang, intervensi BI berhasil.

## Insight untuk Topik
Volatilitas kurs adalah **sinyal stres yang independen dari level kurs**. Bulan dengan kurs "lumayan" tapi spread besar bisa lebih menghambat keputusan travel daripada bulan dengan kurs "tinggi" tapi stabil — karena konsumen dan maskapai menghadapi *ketidakpastian* dalam pricing.

Ini setup untuk Bab 4 WS2 yang akan menguji **apakah volatilitas spread → penumpang punya korelasi independen dari level kurs**.

## Output
- `plot.png` — band chart kurs
- `top5_volatile_months.csv` — 5 bulan paling volatil

## Target Tableau
- Columns: `Tanggal Analisis` (continuous)
- Rows: `AVG(avg_kurs_tengah)` (line)
- Tambahan: `AVG(min_kurs_tengah)` dan `AVG(max_kurs_tengah)` sebagai **dual axis area chart** di belakang. Atau pakai Reference Band (Analytics pane) dengan computed field.
