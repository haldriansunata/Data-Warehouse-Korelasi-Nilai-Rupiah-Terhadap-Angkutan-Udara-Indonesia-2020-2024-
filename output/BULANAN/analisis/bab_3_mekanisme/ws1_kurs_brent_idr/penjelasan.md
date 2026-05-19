# Bab 3 / WS1 — Channel 1 Step A: Kurs × Brent dalam IDR

## Tujuan
Step pertama dari channel **cost-push**: apakah pelemahan rupiah benar-benar membuat biaya BBM (Brent) lebih mahal *dalam mata uang lokal*?

## Pendekatan
Buat **calculated field** baru: `Brent IDR per Bbl = brent_usd_bbl × avg_kurs_tengah`. Lalu regresi `Brent IDR` terhadap `kurs`.

## Perhitungan
```python
df["brent_idr_per_bbl"] = df["brent_usd_bbl"] * df["avg_kurs_tengah"]
```

Contoh:
- Jan 2020: 56,62 × 13.732,23 ≈ **777.412 IDR/bbl**
- Apr 2020 (oil crash): 26,48 × 15.867,43 ≈ **420.183 IDR/bbl** (turun karena Brent crash mengalahkan kurs depresiasi)
- Jun 2022 (Russia-Ukraine peak): 117,30 × 14.892,11 ≈ **1.746.844 IDR/bbl** (puncak)

## Hasil

| Metrik | Nilai |
|---|---:|
| Range Brent IDR | 400.377 – 1.688.685 IDR/bbl |
| R² (kurs → Brent IDR) | **0,12** (lemah) |
| Slope | 159,91 IDR/bbl per 1 IDR kurs |
| p-value | signifikan tapi efek kecil |

## Makna Angka — Penting!

**R² hanya 0,12** karena Brent USD bergerak *independen* dari kurs — sebagian besar variasi `brent_idr` justru disebabkan oleh fluktuasi `brent_usd`, bukan kurs.

Tapi titik pentingnya: **range Brent IDR berlipat 4× lipat** (400K → 1.689K) dalam 5 tahun. Ini menunjukkan biaya BBM dalam mata uang lokal naik **dramatis**, bukan karena kurs saja, tapi karena **double-shock**: Brent USD naik + kurs depresiasi.

### Implikasi
Channel 1 step A: kurs → cost BBM dalam IDR adalah **valid secara konseptual** (kalau kurs melemah, biaya BBM dalam IDR memang lebih mahal *ceteris paribus*), tapi *kontribusi parsial* kurs ke variasi total `brent_idr` kecil karena Brent global lebih dominan. Cocok untuk argumen: "kurs sebagai *amplifier*, bukan *driver* utama biaya."

## Target Tableau
Buat calculated field:
```
Brent IDR per Bbl = AVG([brent_usd_bbl]) * AVG([avg_kurs_tengah])
```
Scatter: Columns = `AVG(avg_kurs_tengah)`, Rows = `Brent IDR per Bbl`, Detail = `waktu_id`, Color = `covid_phase`, Trend Line Linear.
