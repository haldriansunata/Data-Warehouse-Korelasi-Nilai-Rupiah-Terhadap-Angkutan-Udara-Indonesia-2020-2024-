# Bab 2 / WS2 — Scatter Kurs × Penumpang INTERNASIONAL

## Tujuan
Apakah hubungan kurs–penumpang lebih kuat di segmen INTERNASIONAL dibanding total/domestik? Secara teori harusnya iya, karena tiket INT dalam USD.

## Pendekatan
Sama dengan WS1 (OLS linear regression + scatter), tapi data difilter ke rute `kategori = INTERNASIONAL` saja sebelum agregat bulanan.

## Hasil

| Metrik | Nilai | vs Total (WS1) |
|---|---:|---|
| Slope | +1.176 pax/IDR | Lebih kecil dalam magnitude absolut |
| **R²** | **0,486** | **Lebih tinggi dari Total (0,347)** ✓ |
| Pearson r | +0,697 | Lebih kuat |
| p-value | 6 × 10⁻¹⁰ | Lebih signifikan |
| n | 60 | sama |

## Makna Angka

- **R² lebih tinggi (0,49 vs 0,35)** = pergerakan kurs lebih banyak menjelaskan variasi penumpang INT daripada penumpang total. Ini *konsisten dengan teori* meskipun arahnya masih spurious.
- **Slope positif lagi** = artefak COVID yang sama (lockdown menutup penerbangan internasional, recovery membukanya — bersamaan dengan tren depresiasi rupiah).

### Insight tambahan
Travel internasional **lebih sensitif terhadap rezim COVID** daripada domestik:
- Saat lockdown (Mar 2020–Sep 2021), penerbangan INT hampir mati total (pembatasan VOA).
- Saat reopening (Mei 2022), demand INT meledak.

Itu sebabnya R² INT > Total — karena COVID mempengaruhi INT lebih ekstrem daripada DOM, sehingga COVID-as-confounder menghasilkan korelasi yang lebih ketat (semu) di INT.

## Output
- `plot.png`, `metrics.txt`

## Target Tableau
Duplicate sheet WS1, filter `kategori = INTERNASIONAL`. R² akan jadi 0,486.
