# Bab 3 / WS4 — Channel 2: Kurs × BI Rate (Respons Moneter)

## Tujuan
Apakah BI menaikkan suku bunga sebagai respons terhadap pelemahan rupiah? Ini channel **moneter** — efek tidak langsung ke demand penumpang via biaya kapital, KPR, kredit konsumen.

## Hasil

| Metrik | Nilai |
|---|---:|
| R² | **0,645** (kuat) |
| Slope | 0,00132 % per 1 IDR pelemahan |
| Interpretasi praktis | **+1,32% BI rate per 1.000 IDR pelemahan kurs** |
| p-value | <0,001 |

## Makna

**R² = 0,65** menunjukkan **65% variasi BI rate dijelaskan oleh pergerakan kurs**. Ini hubungan yang kuat dan **slope POSITIF sesuai teori**:
- Kurs melemah → BI menaikkan suku bunga untuk menarik kembali capital flow & menstabilkan rupiah.
- Implementasi: BI Rate turun dari 5% (awal 2020) → 3,5% (2021 stimulus COVID) → naik agresif ke 6,25% (2024 untuk defend rupiah).

### Interpretasi numerik
Setiap pelemahan kurs **1.000 IDR**, BI rate naik **1,32%** (rata-rata historis 2020–2024).

Range kurs Rp 13.732 → 16.329 = pelemahan 2.597 IDR. Prediksi delta BI rate dari slope: 2.597 × 0,00132 = **3,43%**. Realita: BI rate naik dari 5,00% → 6,25% = 1,25%. Selisih: model overpredict karena tidak semua variasi BI rate eksklusif karena kurs (BI juga merespon inflasi global, Fed funds rate).

## Implikasi untuk Demand

Channel 2 menjelaskan demand penumpang **secara tidak langsung**:
1. Kurs ↑ → BI rate ↑
2. BI rate ↑ → biaya kapital naik, KPR naik, kredit konsumtif lebih mahal
3. Daya beli diskresioner ↓ → travel (yang termasuk pengeluaran diskresioner) ditunda

Effect size-nya lebih kecil dari channel cost-push (pengaruhnya lewat tabungan/biaya kapital konsumen, bukan langsung ke harga tiket).

## Target Tableau
Columns: `AVG(avg_kurs_tengah)`. Rows: `AVG(bi_rate)`. Detail: `waktu_id`. Color: `covid_phase`. Trend linear. R² akan match 0,645.
