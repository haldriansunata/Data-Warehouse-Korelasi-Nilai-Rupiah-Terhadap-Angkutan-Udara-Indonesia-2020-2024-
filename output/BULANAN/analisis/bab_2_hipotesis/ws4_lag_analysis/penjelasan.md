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

## Target Tableau — Step by Step

### Langkah Pembuatan Calculated Field
1. **Buat 6 calculated field** (klik kanan area Data pane → Create Calculated Field):

   **`Kurs Lag 1`**:
   ```
   LOOKUP(AVG([avg_kurs_tengah]), -1)
   ```

   **`Kurs Lag 2`**:
   ```
   LOOKUP(AVG([avg_kurs_tengah]), -2)
   ```

   Begitu seterusnya untuk Lag 3, 4, 5, 6 (ganti angka -3, -4, dst).

### Langkah Pembuatan Sheet (untuk Lag = 3, contoh)
1. **Buat worksheet baru** `Bab2_WS4_LagAnalysis_L3`.
2. **Drag `Kurs Lag 3` ke Columns**. Pil hijau.
3. **Drag `jumlah_penumpang` ke Rows**. Pil hijau SUM.
4. **Drag `waktu_id` ke Detail di Marks card**. Klik kanan → **Dimension**.
5. **Marks**: Circle.
6. **Drag `covid_phase` ke Color**.
7. **Trend Line**: Analytics → Trend Line → Linear.
8. **PENTING — set Table Calculation address**:
   - Klik kanan pil `Kurs Lag 3` di Columns → **Edit Table Calculation**.
   - *Compute Using*: `Specific Dimensions` → centang **`waktu_id`** (hanya `waktu_id`).
   - *Sort order*: `waktu_id` Ascending.
   - Klik OK.
   - Tanpa langkah ini, `LOOKUP` akan menghitung lag berdasar order tampilan, bukan kronologis. R² akan salah.

### Ulangi untuk Lag 0, 1, 2, 4, 5, 6
Buat 6 sheet terpisah (Lag 0 sampai Lag 6), atau pakai 1 sheet dengan parameter `Lag Selector`:
- Buat Parameter `Lag Bulan` (integer, allowable values: 0–6).
- Buat calculated field `Kurs Lag Dynamic = LOOKUP(AVG([avg_kurs_tengah]), -[Lag Bulan])`.
- Pakai di Columns, lalu pilih nilai parameter untuk switch lag interaktif.

### Cross-check ke Python
File `lag_r2.csv`:

| Lag | TOTAL | INT | DOM |
|---:|---:|---:|---:|
| 0 | 0,347 | 0,486 | 0,226 |
| 1 | 0,351 | 0,554 | 0,198 |
| 2 | 0,444 | 0,624 | 0,286 |
| **3** | **0,512** | **0,637** | 0,373 |
| 6 | 0,509 | 0,578 | 0,401 |

Hover trend line → R² Tableau harus match.

### Catatan Khusus
- `LOOKUP` adalah **Table Calculation**, bukan formula biasa. Hasilnya tergantung "Compute Using". Salah setting = salah angka.
- Untuk lag 6 di TOTAL, R² masih naik (0,51) — efek kurs ke demand transport ternyata punya pengaruh jangka panjang (>6 bulan).
- Slope semua lag tetap **POSITIF** (spurious dari COVID). Tidak menyelesaikan masalah utama Bab 2.
