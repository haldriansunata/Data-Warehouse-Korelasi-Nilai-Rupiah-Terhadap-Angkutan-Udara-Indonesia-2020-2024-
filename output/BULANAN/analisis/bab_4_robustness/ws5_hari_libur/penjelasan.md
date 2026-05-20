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

## Target Tableau — Step by Step

### Langkah Pembuatan Sheet
1. **Buat worksheet baru** `Bab4_WS5_HariLibur`.
2. **Drag `jumlah_hari_libur` ke Columns**. Klik kanan pil → pastikan **Continuous** (pil hijau) → klik kanan → Measure → **Average** atau Sum, terserah, asal continuous.
   - **Cara cepat lain**: drag sebagai Dimension (biru) kalau ingin diskrit 0,1,2,3,4,5 — Tableau akan tampilkan sebagai box plot.
3. **Drag `jumlah_penumpang` ke Rows** sebagai `SUM`.
4. **Drag `waktu_id` ke Detail** → Dimension. 60 titik muncul.
5. **Marks**: Circle.
6. **Drag `covid_phase` ke Color**.
7. **Trend Line**: Analytics → Linear.

### Cross-check ke Python
File `metrics.txt`:
- slope = **−86.534** (negatif, tapi tidak signifikan)
- R² = **0,0014** (essentially nol)

### Catatan KHUSUS
- **Slope negatif counterintuitive**: lebih banyak hari libur → penumpang turun. Ini spurious:
  - Bulan dengan 4–5 hari libur (Mei) sering bertepatan dengan Lebaran di 2020/21 (lockdown).
  - Bulan dengan 0–1 hari libur tersebar di periode normal.
- Variabel ini **tidak menggantikan flag Lebaran/Natal**. Lebih baik kombinasi dengan covid_phase sebagai control multivariate (tidak native di Tableau, butuh Python).

### Alternative Tableau yang Lebih Bermakna
Pakai `jumlah_hari_libur` sebagai **Color** atau **Size** di scatter kurs × pax:
- Color = `jumlah_hari_libur` (sequential palette) bukan covid_phase.
- Akan terlihat bahwa bulan dengan libur banyak (titik warna gelap) cluster di kanan-bawah scatter (COVID lockdown) — visual yang sama menjelaskan spurious-nya.
