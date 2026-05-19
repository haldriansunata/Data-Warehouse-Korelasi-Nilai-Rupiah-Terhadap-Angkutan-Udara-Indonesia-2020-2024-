# Bab 1 / WS3 — Inflasi YoY & MtM + COVID Phase Background

## Tujuan
Menampilkan rezim inflasi yang berbeda di setiap fase COVID, mempersiapkan argumen Bab 4 bahwa **COVID adalah confounder** yang harus dikontrol.

## Pendekatan
**Dual-axis line chart** untuk dua jenis inflasi:
- **Inflasi YoY** (year-on-year): inflasi tahun-ke-tahun, sumbu kiri.
- **Inflasi MtM** (month-to-month): inflasi bulan-ke-bulan, sumbu kanan.

Background di-shade dengan warna per `covid_phase` untuk membantu audience mengaitkan rezim inflasi dengan rezim COVID.

## Perhitungan
Inflasi sudah dalam **persen (%)**, tidak perlu konversi:
- YoY: tingkat harga umum tahun ini vs tahun lalu (kira-kira berapa % barang lebih mahal dari tahun lalu).
- MtM: perubahan dari bulan sebelumnya (bisa negatif = deflasi).

```python
# Rata-rata inflasi per fase COVID
phase_avg = df.groupby("covid_phase")["inflasi_yoy"].mean()
```

## Hasil dari Data Kamu

| COVID Phase | n bulan | Inflasi YoY rata-rata | Inflasi MtM rata-rata | BI rate rata-rata |
|---|---:|---:|---:|---:|
| pre_pandemic | 2 | 2,83% | 0,34% | 4,88% |
| lockdown | 19 | **1,70%** | 0,10% | **3,84%** |
| transisi | 15 | **3,72%** | 0,43% | 3,90% |
| recovery | 24 | 2,99% | 0,17% | **5,96%** |

## Makna Angka
Empat rezim berbeda:
1. **Lockdown (Mar 2020–Sep 2021)**: inflasi tertekan (1,70%) karena demand collapse. BI rate diturunkan ke 3,84% — kebijakan moneter longgar untuk stimulus.
2. **Transisi (Okt 2021–Des 2022)**: lonjakan inflasi (3,72%) karena reopening + shock minyak Russia-Ukraine (Feb 2022). BI baru mulai naik.
3. **Recovery (Jan 2023–Des 2024)**: inflasi normalize ke 3%, tapi **BI rate ditahan tinggi (5,96%)** untuk menjaga rupiah.
4. **Pre-pandemic**: hanya 2 bulan, tidak cukup untuk regresi terpisah → biasanya digabung ke lockdown.

## Insight untuk Topik
**Inflasi dan COVID phase berkorelasi**. Kalau di Bab 2 kita menemukan kurs–penumpang ber-korelasi negatif, kita tidak bisa langsung simpulkan "kurs penyebab" — bisa juga "COVID phase yang menyebabkan keduanya". Inilah yang dimaksud *confounder*.

Solusi di Bab 4: regresi/scatter **per fase COVID** untuk memastikan slope bertahan.

## Output
- `plot.png` — dual-axis line dengan background COVID
- `phase_summary.csv` — rata-rata indikator per fase

## Target Tableau
- Columns: `Tanggal Analisis` (continuous)
- Rows: `AVG(inflasi_yoy)` + `AVG(inflasi_mtm)` sebagai dual-axis (jangan synchronize, beda skala)
- Tambah background shading via Reference Band dengan field `covid_phase`. Caranya: drag `covid_phase` ke Color di Marks card → pilih Bar di Marks → buat axis dummy dengan field konstan.
