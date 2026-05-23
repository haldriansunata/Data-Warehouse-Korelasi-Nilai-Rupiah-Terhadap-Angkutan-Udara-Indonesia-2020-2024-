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

## Target Tableau — Step by Step

### Langkah Pembuatan Sheet
1. **Buat worksheet baru** `Bab3_WS3_TarifPax`.
2. **Drag `tarif_tiket_ihk` ke Columns**. Pil `AVG(tarif_tiket_ihk)` hijau.
3. **Drag `jumlah_penumpang` ke Rows**. Pil `SUM(jumlah_penumpang)` hijau.
4. **Drag `waktu_id` ke Detail** → klik kanan → **Dimension**.
5. **Marks**: Circle.
6. **Drag `covid_phase` ke Color**.
7. **Trend Line**: Analytics → Linear.

### Cross-check ke Python
File `metrics.txt`:
- slope = **+15.192,52** pax per 1 poin IHK
- R² = **0,7086** (tertinggi di Bab 3, tapi SPURIOUS)
- p-value < 10⁻⁹

### Catatan KHUSUS untuk Presentasi
- Slope **POSITIF**: tarif naik → penumpang juga naik. Ini *spurious* karena COVID:
  - 2020 lockdown: tarif IHK rendah (1.248) + penumpang rendah (~1 juta)
  - 2024 recovery: tarif IHK tinggi (1.788) + penumpang tinggi (~8 juta)
- **JANGAN** klaim "tarif naik bikin penumpang naik" — itu absurd secara teori.
- Tambah annotation manual di chart: "*R²=0,71 spurious karena confounder COVID; lihat Bab 4 WS1*".
- Saat presentasi, gunakan chart ini untuk menunjukkan **bahaya naive interpretation** — bukan untuk klaim positif.

---

## ⚙️ Update — Catatan Implementasi Tableau

**Masalah `covid_phase` memecah trend line** → solusi standar: Edit Trend Lines → uncheck `Allow a trend line per color`. Lihat `solusi_masalah.md` Solusi #1.
