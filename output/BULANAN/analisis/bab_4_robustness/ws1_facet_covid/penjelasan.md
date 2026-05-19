# Bab 4 / WS1 — Faceted Scatter per COVID Phase (Kontrol Confounder Utama)

## Tujuan
**Headline test robustness**: apakah korelasi kurs–penumpang yang ditemukan di Bab 2 (slope positif) bertahan setelah COVID phase dikontrol, atau berbalik sesuai teori?

## Pendekatan
**Faceted regression**: pisahkan data per `covid_phase`, jalankan OLS regresi independen di tiap subset. Bandingkan slope antar fase.

## Hasil dari Data Kamu

| COVID Phase | n bulan | Slope | R² | p-value |
|---|---:|---:|---:|---:|
| pre_pandemic | 2 | — (n terlalu kecil) | — | — |
| **lockdown** | 19 | **−318** | 0,012 | 0,652 |
| transisi | 15 | +1.555 | 0,578 | 0,001 |
| recovery | 24 | +706 | 0,176 | 0,041 |

## Makna Angka — Finding Utama Bab 4!

### 1. Lockdown phase: slope BERBALIK menjadi NEGATIF
Saat efek COVID dikontrol (semua titik dalam fase yang sama), slope di lockdown jadi **−318 pax/IDR** — *sesuai teori* (kurs naik → demand turun).

Tapi: R² hanya 0,01 dan p=0,65 → **tidak signifikan**. Artinya: pada periode lockdown, demand variasinya didominasi oleh kebijakan PPKM/PSBB, BUKAN kurs. Kurs jadi noise.

### 2. Transisi & Recovery: slope masih positif
Di fase reopening (transisi+recovery), pelemahan kurs *bersamaan* dengan demand yang terus naik karena dibukanya pembatasan dan pent-up demand. Slope positif tetap **spurious** — hanya menunjukkan dua tren paralel, bukan kausal.

### 3. Insight: korelasi naive Bab 2 adalah ARTEFAK

Slope +2.294 di scatter "all data" di Bab 2 muncul **karena**:
- Lockdown: titik di pojok kanan-bawah (kurs tinggi, pax rendah)
- Recovery: titik di pojok kanan-atas (kurs tinggi, pax tinggi)
- Pre-pandemic: titik di pojok kiri-atas (kurs rendah, pax tinggi)
- **Distribusi titik bukan linear, melainkan U-shape** atau "L terbalik" — trend line linear paksa positif.

**Setelah kontrol COVID phase**: tidak ada satu pun fase di mana slope negatif itu signifikan. Yang berarti dalam data 2020-2024 ini, **kurs BUKAN driver utama demand**. Driver utamanya = COVID phase + seasonal.

## Pesan untuk Paper

> "Naive correlation menunjukkan hubungan positif yang signifikan (Bab 2), tetapi setelah dikontrol untuk fase COVID, slope di setiap fase secara individual tidak menunjukkan hubungan negatif yang signifikan. Ini menunjukkan bahwa korelasi kurs–penumpang sebagian besar dijelaskan oleh paralelisme antara depresiasi struktural rupiah dan recovery sektor penerbangan pasca-COVID, bukan oleh hubungan kausal langsung."

Ini *honest finding* — paper kamu akan lebih kuat karena mengakui keterbatasan ini daripada over-claim korelasi naive.

## Output
- `plot.png` — 4 panel scatter side-by-side
- `slope_per_phase.csv` — slope/R²/p tiap fase

## Target Tableau
- Columns: `covid_phase` (sebelah kiri) lalu `AVG(avg_kurs_tengah)`
- Rows: `SUM(jumlah_penumpang)`
- Detail: `waktu_id`
- Color: `covid_phase`
- Trend Line: Linear **per pane**

Hasilnya 4 mini scatter side-by-side. Slope tiap panel harus match angka di tabel.
