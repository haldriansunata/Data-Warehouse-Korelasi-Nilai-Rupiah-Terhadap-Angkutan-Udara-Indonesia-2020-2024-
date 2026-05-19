# Bab 5 / WS2 — Sensitivitas Slope per Rute INTERNASIONAL

## Tujuan
Per-rute INT yang mana **paling sensitif** ke kurs? Mengidentifikasi rute-rute dengan slope paling negatif/curam.

## Pendekatan
Untuk tiap rute INT (top 10 by total penumpang), jalankan **OLS regresi terpisah**: `penumpang(t) ~ kurs(t)`. Bandingkan slope antar rute.

## Hasil (sorted by slope ascending)

| Rute | Slope | R² | p |
|---|---:|---:|---:|
| DPS-SYD | +17,48 | 0,27 | 0,001 |
| DPS-MEL | +17,62 | 0,23 | 0,002 |
| CGK-DOH | +23,54 | 0,49 | 0,000 |
| SIN-SUB | +26,43 | 0,46 | 0,000 |
| CGK-JED | +36,27 | 0,31 | 0,000 |
| KNO-KUL | +38,47 | **0,59** | 0,000 |
| DPS-KUL | +45,50 | 0,31 | 0,000 |
| DPS-SIN | +63,32 | 0,37 | 0,000 |
| CGK-KUL | +94,72 | 0,50 | 0,000 |
| **CGK-SIN** | **+114,33** | 0,40 | 0,000 |

## Makna — Hati-hati interpretasi!

### Semua slope POSITIF (spurious COVID lagi)
Pattern yang sama dengan Bab 2: lockdown rute INT mati total, recovery rute INT meledak. Karena dua-duanya happen bersamaan dengan rezim kurs yang berbeda, slope tampak positif.

### Slope mencerminkan **VOLUME**, bukan elastisitas
Slope CGK-SIN = 114 pax/IDR, sedangkan DPS-SYD = 17 pax/IDR. Tapi CGK-SIN volume-nya **5× lebih besar** dari DPS-SYD. Slope absolute tidak fair untuk membandingkan elastisitas.

### Yang lebih bermakna: R²
R² mengukur **proporsi variasi yang dijelaskan kurs** — independen dari skala volume:
- **KNO-KUL: R² = 0,59** (tertinggi) — variasi pax di rute ini paling banyak dijelaskan kurs.
- **DPS-MEL: R² = 0,23** (terendah) — rute Australia paling **resilient** terhadap kurs (mungkin karena inbound wisman Aussie yang justru terdorong rupiah lemah).

## Insight untuk Topik

Rute ke **Australia (DPS-SYD, DPS-MEL)** menunjukkan R² paling rendah → konsisten dengan teori inbound: turis Australia masuk ke Bali, kurs rupiah lemah justru *menguntungkan* mereka. Demand inbound mengkompensasi penurunan outbound.

Rute ke **Singapura/Malaysia (KNO-KUL, CGK-KUL, CGK-SIN)** menunjukkan R² lebih tinggi — flow lebih dominan outbound Indonesia → ASEAN dekat. Outbound ini lebih sensitif ke kurs (USD-pegged SGD/MYR).

## Output
- `plot.png` — horizontal bar slope per rute
- `sensitivity_per_int_route.csv`

## Target Tableau
- Filter: `kategori = INTERNASIONAL`, top 10 by total pax
- Columns: `AVG(avg_kurs_tengah)`, Rows: `SUM(jumlah_penumpang)`
- Detail: `waktu_id`, Color: `kode_rute`
- Trend Line: Linear **per color** (centang "Linear trend lines per Color")

Slope tiap line akan match angka di atas.

## Caveat untuk Paper
Jangan klaim "rute X paling elastis ke kurs" hanya dari slope. Gunakan **R² + slope/mean(pax)** sebagai metrik elastisitas yang lebih fair.
