# Bab 2 / WS4 — Lag Analysis (Kurs t-k → Penumpang t)

## Tujuan
Apakah efek kurs ke penumpang **delayed**? Booking penerbangan biasa dilakukan 1–3 bulan sebelum keberangkatan, jadi kurs *bulan-bulan sebelumnya* mungkin lebih prediktif daripada kurs bulan ini.

## Pendekatan
**Lagged regression**: untuk lag k = 0, 1, 2, ..., 6 bulan, hitung regresi `penumpang(t) ~ kurs(t-k)`. Bandingkan R² antar lag. Lag dengan R² puncak = lag dominan.

```python
shifted_kurs = df["avg_kurs_tengah"].shift(k)  # kurs k bulan yang lalu
# regress jumlah_penumpang ~ shifted_kurs
```

## Perhitungan
`r²(lag=k)` = proporsi variasi penumpang bulan t yang dijelaskan oleh kurs bulan (t-k).

## Hasil dari Data Kamu

R² per lag, per segmen:

| Lag (bulan) | DOM | INT | TOTAL |
|---:|---:|---:|---:|
| 0 | 0,226 | 0,486 | 0,347 |
| 1 | 0,198 | 0,554 | 0,351 |
| 2 | 0,286 | 0,624 | 0,444 |
| 3 | **0,373** | **0,637** | **0,512** |
| 4 | 0,382 | 0,621 | 0,514 |
| 5 | 0,385 | 0,602 | 0,509 |
| 6 | **0,401** | 0,578 | 0,509 |

## Makna Angka

### Lag puncak
- **TOTAL**: lag 3–4 bulan (R² = 0,51) — kurs 3-4 bulan lalu lebih prediktif dari kurs bulan ini.
- **INT**: lag 3 bulan (R² = 0,64) — paling prediktif, dan paling tinggi R² nya.
- **DOM**: lag 6 bulan (R² = 0,40) — terus naik bahkan sampai lag 6, kemungkinan masih ada efek di lag yang lebih panjang.

### Interpretasi
Hubungan kurs-penumpang **terus menguat seiring penambahan lag**, sampai puncak di lag 3-6 bulan. Ini konsisten dengan:
1. Booking advance — konsumen lihat kurs sekarang, baru terbang 1-3 bulan kemudian.
2. Pass-through delay — kurs perlu waktu untuk masuk ke harga bahan bakar penerbangan (proxy: Brent crude oil), lalu ke harga tiket, lalu mempengaruhi keputusan booking.

### Tapi awas: lag tidak menyelesaikan masalah COVID
Slope masih positif di semua lag, karena confounder COVID juga lag-stable. Lag analysis paling bermakna **setelah kontrol COVID** (kombinasi dengan Bab 4).

## Output
- `plot.png` — R² per lag, 3 garis (TOTAL/INT/DOM)
- `lag_r2.csv` — tabel lengkap

## Target Tableau
Buat calculated field:
```
Kurs Lag 3 = LOOKUP(AVG([avg_kurs_tengah]), -3)
```
Gunakan sebagai Columns di scatter, ulangi untuk lag 1, 2, 3 dst. R² akan match dengan tabel di atas.

**Note**: `LOOKUP` butuh table calculation yang benar — pastikan address-nya `waktu_id` ascending.
