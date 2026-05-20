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

## Target Tableau — Step by Step

### Langkah Pembuatan Sheet
1. **Buat worksheet baru** `Bab5_WS2_SensitivitasINT`.
2. **Filter kategori**: drag `kategori` ke Filters → centang hanya `INTERNASIONAL`.
3. **Filter Top 10 rute INT**: drag `kode_rute` ke Filters → tab Top → "By field" → Top 10 by `SUM([jumlah_penumpang])` → OK.
4. **Drag `avg_kurs_tengah` ke Columns**. Pil `AVG`.
5. **Drag `jumlah_penumpang` ke Rows**. Pil SUM.
6. **Drag `waktu_id` ke Detail** → klik kanan → **Dimension**.
7. **Marks**: Circle.
8. **Drag `kode_rute` ke Color** di Marks card. Akan tampak 10 warna.
9. **Trend Line per color**:
   - Analytics → Trend Line → Linear.
   - Klik kanan trend line → **Edit Trend Lines** → centang **"Allow a trend line per color"** → klik OK.
   - Tableau akan menggambar 10 garis trend, satu per rute.
10. **Hover tiap line** untuk lihat slope dan R² masing-masing rute.

### Cross-check ke Python
File `sensitivity_per_int_route.csv` — sorted by slope ascending:

| Rute | Slope | R² |
|---|---:|---:|
| DPS-SYD | +17,48 | 0,272 |
| DPS-MEL | +17,62 | 0,234 |
| CGK-DOH | +23,54 | 0,488 |
| ... | ... | ... |
| CGK-KUL | +94,72 | 0,500 |
| **CGK-SIN** | **+114,33** | 0,402 |

Trend line paling curam (slope absolute terbesar) di Tableau = CGK-SIN (114).

### Catatan untuk Presentasi
- **Jangan klaim "rute X paling elastis ke kurs"** hanya dari slope — slope mencerminkan volume.
- Beri **annotation membandingkan R²**: rute Australia (DPS-SYD, DPS-MEL) R² paling rendah → paling resilient.
- Tambah text box di dashboard untuk caveat.
