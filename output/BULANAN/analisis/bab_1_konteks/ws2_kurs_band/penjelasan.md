# Bab 1 / WS2 — Kurs Band (Volatilitas Bulanan)

## Tujuan
Menampilkan kurs **bukan sebagai satu angka per bulan**, melainkan sebagai *range* harian (min sampai max). Volatilitas adalah informasi yang hilang kalau cuma melihat rata-rata.

## Pendekatan
**Filled band chart**: area antara `min_kurs_tengah` dan `max_kurs_tengah` di-shade transparan, dengan line `avg_kurs_tengah` di tengahnya. Tebal-tipis band menunjukkan stres pasar.

## Perhitungan
```
spread = max_kurs_tengah − min_kurs_tengah   # untuk setiap bulan
```

Spread besar = pasar volatil dalam bulan itu (intervensi BI, sentimen risiko, capital outflow, dll).

## Hasil dari Data Kamu

| Statistik | Nilai |
|---|---:|
| Spread rata-rata | 385 IDR/bulan |
| Spread max (paling volatil) | **2.440 IDR** (Mar 2020) |
| Spread min (paling stabil) | ~50 IDR (banyak bulan tenang) |

### Top 5 bulan paling volatil

| Tanggal | Min | Max | Spread |
|---|---:|---:|---:|
| Mar 2020 | 14.168 | 16.608 | **2.440** |
| Apr 2020 | 15.157 | 16.741 | **1.584** |
| Aug 2024 | 15.380 | 16.294 | 914 |
| Jan 2023 | 14.930 | 15.635 | 705 |
| Nov 2020 | 14.015 | 14.718 | 703 |

## Makna Angka
- **Mar 2020 dengan spread 2.440 IDR** = pasar valas chaos awal pandemi. Range 14.168–16.608 dalam satu bulan = pergerakan 17%. Ini adalah event volatilitas terbesar dalam periode analisis.
- **Aug 2024 spread 914** = bulan menjelang puncak pelemahan rupiah pasca eskalasi Timur Tengah.
- **Bulan dengan spread <100 IDR** (mayoritas 2022–2023 awal recovery) = pasar tenang, intervensi BI berhasil.

## Insight untuk Topik
Volatilitas kurs adalah **sinyal stres yang independen dari level kurs**. Bulan dengan kurs "lumayan" tapi spread besar bisa lebih menghambat keputusan travel daripada bulan dengan kurs "tinggi" tapi stabil — karena konsumen dan maskapai menghadapi *ketidakpastian* dalam pricing.

Ini setup untuk Bab 4 WS2 yang akan menguji **apakah volatilitas spread → penumpang punya korelasi independen dari level kurs**.

## Output
- `plot.png` — band chart kurs
- `top5_volatile_months.csv` — 5 bulan paling volatil

## Target Tableau — Step by Step

### Langkah Pembuatan Sheet
1. **Buat worksheet baru**, beri nama `Bab1_WS2_KursBand`.
2. **Drag `Tanggal Analisis` ke Columns** → klik kanan pil → **Month (Continuous)**, pil hijau.
3. **Drag `AVG(min_kurs_tengah)` ke Rows**. Pil hijau.
4. **Drag `AVG(max_kurs_tengah)` ke Rows** (di sebelah pil min). Akan jadi 2 panel terpisah.
5. **Buat dual axis**: klik kanan pil `AVG(max_kurs_tengah)` di Rows → pilih **Dual Axis**. Dua panel akan tumpang-tindih.
6. **Synchronize axis**: klik kanan sumbu Y kanan → **Synchronize Axis** (penting karena range sama).
7. **Marks card**: sekarang ada 3 Marks card (All, AVG(min), AVG(max)):
   - Di Marks card `AVG(min_kurs_tengah)`: pilih **Area** sebagai tipe Mark.
   - Di Marks card `AVG(max_kurs_tengah)`: pilih **Area** juga.
   - Set warna area kedua = sama (mis. ungu/merah muda) dengan opacity ~40% — ini akan membentuk band.
8. **Tambah line rata-rata**: drag `AVG(avg_kurs_tengah)` ke Rows. Pilihan: ubah jadi triple axis (right-click → Dual Axis lagi) atau pakai Reference Line.
   - **Cara mudah**: drag `AVG(avg_kurs_tengah)` ke sumbu Y kiri (akan menambah measure ke axis yang sudah ada). Marks = Line, warna lebih gelap dari area.
9. **Sembunyikan sumbu Y kanan**: klik kanan sumbu kanan → uncheck "Show Header".

### Cross-check ke Python
Pada Maret 2020:
- Area band paling tebal (volatil): min ≈ 14.168, max ≈ 16.608, spread ≈ **2.440 IDR**.
- Tooltip harus tunjukkan angka ini.

### Catatan Khusus
- Triple axis tidak native di Tableau. Pakai trik: 2 measure di dual axis + 1 measure sebagai overlay manual.
- Alternatif lebih sederhana: pakai **Reference Band** (Analytics pane → Reference Band → Per Cell, dengan field min sebagai lower, max sebagai upper). Tidak butuh dual axis.
