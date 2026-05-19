# Bab 4 / WS5 — Hari Libur Nasional × Penumpang

## Tujuan
Selain flag binary (Lebaran/Natal), pakai variabel kontinyu `jumlah_hari_libur` (0–5 per bulan) sebagai kontrol musiman granular.

## Hasil

| Metrik | Nilai |
|---|---:|
| R² | **0,0014** (essentially nol) |
| Slope | −86.534 pax per +1 hari libur (negatif!) |
| p-value | tidak signifikan |

## Makna — Counter-intuitive

**Slope NEGATIF**: tambah hari libur, penumpang turun? Ini *spurious* lagi.

Pattern di data:
- Mei (umumnya 4–5 hari libur karena Lebaran + Waisak) → tertumpuk di Mei 2020 (lockdown).
- Bulan dengan 0–1 hari libur → tersebar di pre-pandemic + recovery (pax baseline tinggi).

Jadi `jumlah_hari_libur` berkorelasi dengan COVID phase, dan efeknya tertelan.

### Insight

Variabel kontinyu hari libur **tidak menggantikan flag Lebaran/Natal**. Yang bekerja:
- `has_lebaran` (5 bulan saja) → boost moderat tapi noisy karena COVID
- `has_natal` (5 bulan Des) → boost kuat & konsisten (32%)
- `is_peak_season` (Lebaran + Jun + Jul + Des) → variabel komposit terbaik

Kalau mau pakai `jumlah_hari_libur`, kombinasi dengan covid_phase control:
```
Penumpang ~ jumlah_hari_libur + covid_phase
```
(regresi multivariate, di luar capability Tableau native).

## Target Tableau
Drag `jumlah_hari_libur` (continuous) ke Columns, `SUM(jumlah_penumpang)` ke Rows. Trend line akan menunjukkan slope kecil ~0 atau negatif kecil — match Python.

Kalau mau lebih bermakna: pakai sebagai **Color** atau **Size** di scatter kurs×pax sebagai control variabel kedua.
