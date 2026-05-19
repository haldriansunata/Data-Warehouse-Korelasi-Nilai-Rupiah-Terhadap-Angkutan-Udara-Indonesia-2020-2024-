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

## Target Tableau
Calculated field:
```
Spread Kurs = AVG([max_kurs_tengah]) - AVG([min_kurs_tengah])
```
Scatter: Columns=Spread Kurs, Rows=SUM(jumlah_penumpang). R² akan ~0.
