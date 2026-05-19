# Bab 3 / WS3 — Channel 1 Step C: Tarif Tiket × Penumpang

## Tujuan
Step ketiga (dan terakhir di channel cost-push): apakah harga tiket yang lebih tinggi mengurangi demand?

## Hasil

| Metrik | Nilai |
|---|---:|
| R² | **0,709** (sangat tinggi!) |
| Slope | **+15.193 pax per 1 poin IHK** |
| p-value | <0,001 |

## Makna — TWIST KEDUA!

**Slope POSITIF lagi.** Tarif naik → penumpang naik???

Ini lagi-lagi *spurious correlation* karena COVID:
- 2020 lockdown: tarif IHK paling rendah (1.248) DAN penumpang paling rendah (0,1–2 juta).
- 2024 recovery: tarif IHK paling tinggi (1.788) DAN penumpang paling tinggi (~8–9 juta).

Karena kedua variabel sama-sama mengikuti pola COVID dip + recovery, mereka berkorelasi positif secara statistik *meskipun secara teori ekonomi seharusnya negatif* (hukum demand: harga naik → quantity turun).

### Cara membaca R² yang tinggi ini
**R² = 0,71 BUKAN konfirmasi channel cost-push**. Ini hanya menunjukkan kedua variabel sama-sama digerakkan oleh COVID. Untuk menguji channel cost-push yang valid, butuh kontrol COVID phase (Bab 4) atau diff-in-diff.

### Sintesis Channel 1 (cost-push)

| Step | R² naive | Catatan |
|---|---:|---|
| A: Kurs → Brent IDR | 0,12 | Kontribusi kurs kecil, Brent USD dominan |
| B: Brent IDR → Tarif IHK | 0,35 | Pass-through valid, terhambat tarif batas atas |
| C: Tarif IHK → Penumpang | 0,71 | **Spurious dari COVID, butuh kontrol** |

Setelah dikontrol COVID, slope step C harusnya **menjadi negatif** (sesuai teori). Inilah yang akan diverifikasi di Bab 4.

## Target Tableau
Columns: `AVG(tarif_tiket_ihk)`. Rows: `SUM(jumlah_penumpang)`. Detail: `waktu_id`. Color: `covid_phase`. Trend linear. R² akan match 0,709.
