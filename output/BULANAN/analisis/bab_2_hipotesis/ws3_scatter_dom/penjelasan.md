# Bab 2 / WS3 — Scatter Kurs × Penumpang DOMESTIK

## Hasil

| Metrik | Nilai | vs INT (WS2) |
|---|---:|---|
| Slope | +1.119 pax/IDR | mirip |
| R² | **0,226** | jauh lebih rendah |
| Pearson r | +0,475 | lebih lemah |
| p-value | 1,25 × 10⁻⁴ | masih signifikan |

## Makna

R² DOMESTIK paling rendah (0,23) dari ketiga sheet (Total 0,35, INT 0,49). Maknanya: variasi penumpang DOM kurang dijelaskan oleh kurs.

Ini sesuai ekspektasi teoritis:
- Travel **domestik** tidak ter-denominasi USD secara langsung.
- Channel pengaruh kurs ke DOM melalui *cost-push* lewat biaya bahan bakar penerbangan (USD-denominated, di-proksi dengan Brent crude oil karena data avtur langsung tidak tersedia), tapi pass-through-nya tidak penuh (regulasi tarif batas atas membatasi).
- Lebih banyak faktor lokal (Lebaran, libur sekolah, kondisi ekonomi domestik) yang mempengaruhi DOM.

## Sintesis Bab 2 (WS1+WS2+WS3)

| Segmen | R² naive | Slope |
|---|---:|---:|
| Total | 0,347 | +2.294 |
| INT | **0,486** | +1.176 |
| DOM | 0,226 | +1.119 |

**Ranking sensitivitas (R²)**: INT > Total > DOM ✓ Sesuai teori.

**Tapi**: semua slope positif karena confounder COVID. Hubungan sebenarnya menanti di Bab 4 (kontrol per covid_phase).

## Target Tableau
Duplicate WS1, filter `kategori = DOMESTIK`. R² akan jadi 0,226.
