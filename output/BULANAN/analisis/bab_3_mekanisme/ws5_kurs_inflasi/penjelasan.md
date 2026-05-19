# Bab 3 / WS5 — Channel 3: Kurs × Inflasi YoY (Pass-through ke Harga Umum)

## Tujuan
Apakah pelemahan kurs menyebabkan inflasi umum (bukan cuma tarif tiket)? Channel **daya beli**: kurs ↑ → inflasi ↑ → real income ↓ → travel demand ↓.

## Hasil

| Metrik | Nilai |
|---|---:|
| R² | **0,074** (sangat lemah) |
| Slope | 0,00054 % per 1 IDR |
| p-value | marginal |

## Makna

**Channel ini LEMAH** di data Indonesia 2020–2024.

R² hanya 7% — pergerakan kurs sangat sedikit menjelaskan inflasi umum. Kenapa?
1. **Pass-through kurs ke inflasi Indonesia secara historis rendah** (~10-20% dalam jangka panjang), karena banyak harga diatur (BBM, listrik) dan struktur konsumsi domestik.
2. **Periode COVID mengganggu pola normal** — inflasi tertekan di lockdown (demand collapse) meskipun kurs melemah.
3. **Inflasi YoY** adalah rolling 12-bulan; ada efek base period yang menutupi sinyal.

### Apa artinya untuk topik?

Channel daya beli **bukan jalur utama** kurs → demand penumpang di periode ini. Kalau kamu mau menggunakan ini di paper, framing-nya: "Kurs tidak signifikan menjelaskan inflasi umum, jadi channel ini bukan yang dominan."

Channel yang **dominan** adalah:
- Channel 1 cost-push (kurs → Brent IDR → tarif tiket; Brent sebagai *proxy upstream* biaya bahan bakar penerbangan): R² step Brent→Tarif = 0,35
- Channel 2 moneter (kurs → BI rate): R² = 0,65 (paling kuat)

## Sintesis Bab 3

| Channel | R² puncak | Status |
|---|---:|---|
| 1: Cost-push (kurs→brent_idr→tarif→pax) | 0,12 → 0,35 → 0,71* | *Step C spurious (COVID) |
| 2: Moneter (kurs→BI rate) | 0,65 | **Paling kuat, slope sesuai teori** |
| 3: Daya beli (kurs→inflasi) | 0,07 | **Lemah/tidak relevan** |

**Pesan utama Bab 3**: kurs mempengaruhi sektor angkutan udara terutama lewat **respons moneter BI** (yang mengetatkan kondisi kredit konsumen) dan lewat **cost-push bahan bakar** (kurs → Brent IDR → tarif). Channel inflasi umum tidak signifikan.

*Catatan data*: kita tidak punya data harga avtur langsung; analisis channel cost-push menggunakan **Brent crude oil × kurs** sebagai *proxy upstream* karena avtur disuling dari crude oil dan harganya berkorelasi ~80–90% dengan Brent (lag 1–2 bulan).

## Target Tableau
Columns: `AVG(avg_kurs_tengah)`. Rows: `AVG(inflasi_yoy)`. Detail: `waktu_id`. Color: `covid_phase`. Trend linear. R² akan match 0,074.
