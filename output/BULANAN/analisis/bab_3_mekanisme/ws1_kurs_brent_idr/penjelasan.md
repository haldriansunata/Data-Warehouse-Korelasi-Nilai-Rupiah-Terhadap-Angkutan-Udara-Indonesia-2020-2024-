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

## Target Tableau — Step by Step

### Persiapan: Set Default Aggregation
Kolom `brent_idr_per_bbl` sudah tersedia langsung di `fact_makro_bulanan.csv` (tidak perlu calculated field). Set default aggregation-nya sekali:

1. Di Data pane, klik kanan field `brent_idr_per_bbl` → **Default Properties → Aggregation → Average**.

### Langkah Pembuatan Sheet
1. **Buat worksheet baru** `Bab3_WS1_KursBrentIDR`.
2. **Drag `avg_kurs_tengah` ke Columns**. Pil `AVG(avg_kurs_tengah)`, hijau.
3. **Drag `brent_idr_per_bbl` ke Rows**. Pil `AVG(brent_idr_per_bbl)`, hijau.
4. **Drag `waktu_id` ke Detail** → klik kanan pil → **Dimension**. 60 titik muncul.
5. **Marks**: Circle.
6. **Drag `covid_phase` ke Color**.
7. **Trend Line**: Analytics → Trend Line → Linear.
8. **Hover trend line** untuk lihat R² di tooltip.

### Catatan: Alternatif dengan Calculated Field
Kalau di versi `fact_makro_bulanan.csv` kamu **belum ada** kolom `brent_idr_per_bbl` (mis. dataset lama atau snapshot sebelum patch), buat calculated field:
```
Brent IDR per Bbl = AVG([brent_usd_bbl]) * AVG([avg_kurs_tengah])
```
Hasil dan R² akan **sama persis** dengan versi native, karena formula identik.

### Cross-check ke Python
File `metrics.txt`:
- slope = **159,91** (IDR Brent per 1 IDR kurs)
- R² = **0,1195**
- p-value < 0,01

Range Brent IDR di tooltip 60 titik:
- Min: ~**400.000** IDR/bbl (Apr 2020, oil crash)
- Max: ~**1.689.000** IDR/bbl (Jun 2022, Russia-Ukraine peak)

### Catatan Khusus
- R² rendah (0,12) bukan berarti channel ini tidak ada — itu berarti kontribusi *kurs saja* terhadap variasi Brent IDR kecil. Brent USD sendiri sangat volatil secara independen.
- Untuk lebih informatif, tambah **time series Brent IDR** di worksheet terpisah dengan Tanggal Analisis di Columns → tunjukkan double-shock visual.

---

## ⚙️ Update — Catatan Implementasi Tableau

**Masalah `covid_phase` memecah trend line** → solusi standar:
1. Klik kanan trend line → **Edit Trend Lines**.
2. Uncheck `[ ] Allow a trend line per color`.
3. OK. Trend line jadi 1 (slope ≈ 159,91), titik tetap berwarna per fase.

Lihat `output/BULANAN/analisis/masalah/solusi_masalah.md` Solusi #1.
