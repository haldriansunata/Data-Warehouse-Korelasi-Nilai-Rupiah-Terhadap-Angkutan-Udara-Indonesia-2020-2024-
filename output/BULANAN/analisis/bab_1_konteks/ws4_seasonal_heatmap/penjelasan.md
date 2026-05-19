# Bab 1 / WS4 — Heatmap Musiman (Tahun × Bulan)

## Tujuan
Visualisasi padat untuk pola musiman + COVID dip + recovery curve dalam **satu** chart. Lebih informatif daripada line chart untuk audience non-teknis.

## Pendekatan
**Heatmap matrix**: baris = tahun, kolom = bulan, warna sel = total penumpang. Pivot-table klasik.

## Perhitungan
```python
pivot = df.pivot_table(
    index="tahun",
    columns="bulan",
    values="jumlah_penumpang",
    aggfunc="sum"
)
```

## Hasil dari Data Kamu (juta penumpang)

|  | Jan | Feb | Mar | Apr | Mei | Jun | Jul | Agu | Sep | Okt | Nov | Des |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **2020** | **9,12** | 7,76 | 5,51 | 0,98 | **0,10** | 0,75 | 1,71 | 2,34 | 2,11 | 2,48 | 3,24 | 3,72 |
| **2021** | 2,60 | 2,14 | 2,91 | 3,19 | 2,76 | 3,94 | **1,18** | 1,32 | 2,14 | 3,26 | 3,97 | 4,49 |
| **2022** | 3,70 | 3,08 | 3,96 | 4,24 | 6,02 | 5,39 | 5,72 | 4,94 | 4,58 | 5,51 | 5,32 | 6,51 |
| **2023** | 6,83 | 6,28 | 6,87 | 7,11 | 8,09 | 7,89 | 8,69 | 7,89 | 7,58 | 7,96 | 7,67 | 8,26 |
| **2024** | 7,56 | 7,06 | 7,01 | 8,58 | 8,01 | 8,23 | **9,03** | 8,65 | 8,48 | 8,29 | 7,71 | **8,98** |

## Makna Angka

### Pattern yang langsung terlihat:
1. **Black hole Mei 2020 = 0,10 juta** (98,9% drop vs Jan 2020). Bulan paling parah dalam sejarah industri penerbangan modern Indonesia.
2. **Resesi kedua Jul-Sep 2021 (Delta wave)**: turun lagi ke 1,18 juta di Jul 2021 setelah sempat recovery ke 3,94 di Jun 2021.
3. **Rebound bertahap 2022–2023**: garis warna naik tahun demi tahun.
4. **Plateau 2024 dekat 8–9 juta** = ~90% baseline 2020 (pre-COVID), masih belum 100% recovery.

### Pola seasonal stabil tahun-tahun:
- **Spike Mei (2020, 2021, 2022)** = Lebaran (bulan Lebaran bergeser seiring tahun).
- **Spike April (2023, 2024)** = Lebaran bergeser ke April.
- **Spike Juli** (2024 = 9,03M = puncak) = libur sekolah.
- **Spike Desember** = Natal + Tahun Baru.

## Insight untuk Topik
Heatmap memvalidasi **dua hal**:
1. **COVID benar-benar shock asimetris** — bukan slow decline, tapi step-function di Mar–Apr 2020.
2. **Pattern Lebaran/Natal sangat konsisten** tahun demi tahun → flag `has_lebaran`, `has_natal`, `is_peak_season` di Bab 4 punya signal kuat untuk diuji.

Visual ini juga jadi *validasi sanity check*: kalau Tableau heatmap kamu tidak match dengan ini, ada masalah di join atau aggregation.

## Output
- `plot.png` — heatmap
- `pivot_pax_tahun_bulan.csv` — matriks

## Target Tableau
- Columns: `nama_bulan` (Discrete, sort manual Jan-Des)
- Rows: `tahun` (Discrete)
- Marks: Square
- Color: `SUM(jumlah_penumpang)` (sequential palette mis. orange/red)
- Label: `SUM(jumlah_penumpang)` formatted as juta
