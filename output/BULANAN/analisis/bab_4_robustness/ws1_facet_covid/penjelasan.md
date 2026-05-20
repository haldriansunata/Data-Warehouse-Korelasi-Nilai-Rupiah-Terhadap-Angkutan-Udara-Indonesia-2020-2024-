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

## Target Tableau — Step by Step

### Langkah Pembuatan Sheet
1. **Buat worksheet baru** `Bab4_WS1_FacetCOVID`.
2. **Drag `avg_kurs_tengah` ke Columns**. Pil `AVG(avg_kurs_tengah)` hijau.
3. **Drag `covid_phase` ke Columns** dan letakkan **di sebelah KIRI** pil `AVG(avg_kurs_tengah)` (drop di area sebelum pil hijau). Pil biru `covid_phase` akan muncul.
   - Layar akan otomatis terbelah menjadi **4 kolom** sesuai 4 fase COVID.
4. **Drag `jumlah_penumpang` ke Rows**. Pil `SUM(jumlah_penumpang)` hijau.
5. **Drag `waktu_id` ke Detail di Marks card** → klik kanan → **Dimension**.
6. **Marks**: Circle.
7. **Drag `covid_phase` ke Color** (drag lagi dari Dimensions).
8. **Trend Line per pane**:
   - Analytics → Trend Line → Linear.
   - Klik kanan trend line → **Edit Trend Lines**.
   - Centang **"Allow a trend line per color"** AND **"Force y-intercept to zero"** UN-centang.
   - Penting: Tableau secara default akan fit trend line per *color*, dan karena Color = `covid_phase` = sama dengan panel, hasilnya = 1 trend line per panel. ✓

### Cross-check ke Python
File `slope_per_phase.csv`:

| Phase | n | Slope | R² | p |
|---|---:|---:|---:|---:|
| pre_pandemic | 2 | (tidak dihitung — n terlalu kecil) | — | — |
| lockdown | 19 | **−317,59** | 0,012 | 0,652 |
| transisi | 15 | **+1.555,50** | 0,578 | 0,001 |
| recovery | 24 | **+706,28** | 0,176 | 0,041 |

Hover trend line tiap panel → angka harus match.

### Catatan KRUSIAL untuk Presentasi
- **Panel `lockdown` menunjukkan slope NEGATIF (−318)** — *sesuai teori* meskipun tidak signifikan (p=0,65). Beri annotation di chart.
- **Panel `transisi` dan `recovery` slope POSITIF** — spurious sisa.
- **Panel `pre_pandemic`** hanya 2 titik → trend line tidak meaningful. Tableau akan tetap menggambar garis tapi tooltip tidak akan tunjukkan R² yang valid. Pertimbangkan hide panel ini atau beri caveat.

### Implikasi Paper
Ini sheet **PALING PENTING** dari seluruh analisis kalian. Saat presentasi Bab 4:
1. Tunjukkan slope per pane.
2. Highlight: "Hanya lockdown phase yang slope negatif sesuai teori, tapi tidak signifikan."
3. Konklusi: "Korelasi naive di Bab 2 adalah artefak structural break COVID."
