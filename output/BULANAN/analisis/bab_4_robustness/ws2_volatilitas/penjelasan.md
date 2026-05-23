# Bab 4 / WS2 — Volatilitas Kurs × Penumpang

## Tujuan
Apakah **volatilitas** kurs (terlepas dari level-nya) ikut menekan demand? Hipotesis: bulan dengan spread besar = uncertainty → konsumen tunda travel.

## Pendekatan
Calculated field `spread_kurs = max_kurs_tengah - min_kurs_tengah`. Regress penumpang terhadap spread.

## Hasil

| Metrik | Nilai |
|---|---:|
| R² | **0,0006** (essentially nol) |
| Slope | +175 (tidak signifikan) |
| p-value | high |

## Makna

**Hipotesis ditolak**: volatilitas kurs **tidak** punya korelasi independen dengan penumpang dalam data ini.

Kenapa? Karena bulan-bulan paling volatil (Mar-Apr 2020 dengan spread 2.440 IDR) adalah juga bulan-bulan **lockdown paling parah** — pax turun bukan karena volatility, tapi karena PSBB. Jadi sinyal volatility tertelan oleh sinyal COVID.

### Implikasi Honest Reporting

Tidak semua hipotesis yang kelihatan masuk akal didukung data. Ini OK untuk paper — penolakan hipotesis sama berharganya dengan konfirmasi.

Kalau mau argumen lebih kuat: ulangi analisis dengan **filter recovery saja** (lockdown sudah lewat). Volatility di recovery (mis. Aug 2024 spread 914) mungkin punya signal yang lebih bersih.

## Target Tableau — Step by Step

### Persiapan: Calculated Field
**Buat calculated field `Spread Kurs`** (klik kanan Data pane → Create Calculated Field):
```
AVG([max_kurs_tengah]) - AVG([min_kurs_tengah])
```
Klik OK.

### Langkah Pembuatan Sheet
1. **Buat worksheet baru** `Bab4_WS2_Volatilitas`.
2. **Drag `Spread Kurs` ke Columns**. Pil hijau.
3. **Drag `jumlah_penumpang` ke Rows**. Pil SUM.
4. **Drag `waktu_id` ke Detail** → klik kanan → **Dimension**.
5. **Marks**: Circle.
6. **Drag `covid_phase` ke Color** (untuk identifikasi mana titik volatile).
7. **Trend Line**: Analytics → Linear.

### Cross-check ke Python
File `metrics.txt`:
- slope = **+175** pax per 1 IDR spread
- R² = **0,0006** (essentially nol)
- p-value: tidak signifikan

### Catatan untuk Presentasi
- **Hipotesis volatilitas DITOLAK**. Slope ~0, R² ~0.
- Hover ke titik dengan spread terbesar (Mar 2020, ~2.440 IDR) — akan terlihat di pojok kanan-bawah (volatile + pax rendah). Tapi pola umumnya random.
- Beri annotation: "Volatilitas kurs tidak punya signal independen — bulan paling volatil (Mar 2020) bertepatan dengan PSBB, sinyal tertelan COVID."

---

## ⚙️ Update — Catatan Implementasi Tableau

### 1. `covid_phase` memecah trend line
Solusi standar: Edit Trend Lines → uncheck `Allow a trend line per color`. Trend line jadi 1 (slope ≈ +175, R² ≈ 0,0006), titik tetap berwarna.

### 2. `AGG(Spread Kurs)` apakah benar?
**BENAR**. Calculated field-mu:
```
Spread Kurs = AVG([max_kurs_tengah]) - AVG([min_kurs_tengah])
```
karena formula sudah pakai `AVG(...)` di dalamnya, Tableau otomatis bungkus jadi `AGG(Spread Kurs)` saat di-drag ke Columns. Jangan dibungkus AVG lagi — error "Cannot mix aggregate and non-aggregate".

Lihat `solusi_masalah.md` Solusi #1 dan #5.
