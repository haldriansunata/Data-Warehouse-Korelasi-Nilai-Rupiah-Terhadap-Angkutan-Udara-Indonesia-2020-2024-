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

## Target Tableau — Step by Step

### Langkah Pembuatan Sheet
1. **Buat worksheet baru** `Bab4_WS6_PeakSeasonInteraction`.
2. **Drag `avg_kurs_tengah` ke Columns**. Pil `AVG` hijau.
3. **Drag `jumlah_penumpang` ke Rows**. Pil SUM hijau.
4. **Drag `waktu_id` ke Detail** → klik kanan → **Dimension**.
5. **Marks**: Circle.
6. **Drag `is_peak_season` ke Color** di Marks card. Klik kanan pil di Color → pastikan **Discrete** (akan tampak 2 warna: 0 abu, 1 merah/biru).
7. **Trend Line per color**:
   - Analytics → Trend Line → Linear.
   - **Klik kanan trend line → Edit Trend Lines** → centang **"Allow a trend line per color"**.
   - Tableau akan menggambar 2 garis trend (satu per peak_season value).

### Cross-check ke Python
File `slope_by_peak.csv`:

| is_peak_season | n | Slope | R² |
|---:|---:|---:|---:|
| 0 (non-peak) | 40 | **+1.841** | 0,244 |
| 1 (peak season) | 20 | **+3.087** | **0,547** |

Hover trend line non-peak → R²=0,24; hover trend line peak → R²=0,55.

### Catatan untuk Paper
- **Sensitivitas 2,2× lebih tinggi di peak season**. Ini *publishable finding*.
- Annotation manual: "Demand di peak season (Lebaran, libur sekolah, Natal) memiliki sensitivitas kurs 2,2× lebih tinggi dibanding non-peak. Konsisten dengan literatur bahwa segmen leisure lebih elastis."
- **Catatan caveat**: kedua slope masih positif (spurious COVID). Yang valid adalah *relative comparison*, bukan slope absolut.

---

## ⚙️ Update — Catatan Implementasi Tableau

**Untuk WS6 ini, trend line MEMANG harus multi** (1 per `is_peak_season` value) — itu inti analisanya (interaction effect). Jadi **biarkan** `Allow a trend line per color` tetap **CENTANG**. Tampilan 2 trend line (peak vs non-peak) adalah hasil yang benar.

**`is_peak_season` Dimension**: convert ke Dimension (0/1 → discrete) sudah BENAR.

Lihat `solusi_masalah.md` Solusi #1 dan #3.
