# Bab 4 / WS6 — Interaksi `is_peak_season` × Kurs

## Tujuan
Apakah sensitivitas demand ke kurs **berbeda** antara peak season (Lebaran, libur sekolah, Natal) dan non-peak season?

## Pendekatan
Pisah data ke `is_peak_season=0` (40 bulan) vs `is_peak_season=1` (20 bulan), jalankan regresi terpisah, bandingkan slope dan R².

## Hasil

| Segment | n bulan | Slope | R² |
|---|---:|---:|---:|
| Non-peak | 40 | **+1.841** | 0,244 |
| Peak | 20 | **+3.087** | **0,547** |

## Makna

### 1. R² lebih tinggi di peak season (0,55 vs 0,24)
Pergerakan kurs **lebih banyak** menjelaskan variasi demand saat peak season. Interpretasi: keputusan travel di peak season (mudik, liburan) lebih sensitif terhadap kondisi makro karena:
- Volume booking besar → harga lebih ter-noticed.
- Sebagian peak season adalah leisure (Lebaran mudik, libur sekolah, Natal) — discretionary, lebih elastis ke harga.

### 2. Slope peak > non-peak (3.087 vs 1.841)
Slope-nya **lebih curam**, meskipun masih positif (spurious COVID). Magnitude perbedaan menarik untuk paper.

### Catatan caveat
Slope positif di kedua segmen = artefak COVID yang sama dengan Bab 2. Yang valid adalah **relative comparison** (peak vs non-peak), bukan slope absolut.

## Pesan untuk Paper

> "Sensitivitas demand terhadap kurs (diukur lewat R²) **1,7× lebih tinggi di peak season** (0,55) dibanding non-peak (0,24). Ini konsisten dengan literatur travel demand bahwa segmen leisure lebih elastis ke harga dibanding segmen bisnis."

Ini insight yang bisa diangkat sebagai *contribution* kelompok kamu — tidak banyak paper Indonesia yang memecah elastisitas kurs–demand by season.

## Target Tableau
- Columns: `AVG(avg_kurs_tengah)`
- Rows: `SUM(jumlah_penumpang)`
- Detail: `waktu_id`
- Color: `is_peak_season` (akan jadi 2 warna)
- Trend Line: Linear **per color** (centang "Linear trend lines per Color")

Hasil: 2 trend lines, slope dan R² match angka di atas.
