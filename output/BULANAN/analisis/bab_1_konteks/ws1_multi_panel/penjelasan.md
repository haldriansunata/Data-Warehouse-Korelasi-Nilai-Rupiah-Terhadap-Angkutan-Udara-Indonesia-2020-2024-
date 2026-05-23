# Bab 1 / WS1 — Multi-panel Time Series

## Tujuan
Menampilkan **empat indikator inti** (penumpang, kurs, Brent, BI rate) dalam satu visual timeline 60 bulan supaya audience paham *konteks* sebelum bicara korelasi.

## Pendekatan
**Time series chart** (line plot) berlapis dalam 4 panel sejajar ke bawah dengan sumbu X tanggal yang sama. Ini paling efektif untuk membandingkan pergerakan multi-variabel di rezim waktu yang sama tanpa berebut skala Y.

## Perhitungan
Tidak ada perhitungan statistik — murni penyajian nilai mentah per bulan:
- Penumpang: `SUM(jumlah_penumpang)` per `waktu_id` (semua rute dijumlahkan).
- Kurs / Brent / BI rate: nilai per bulan langsung dari `fact_makro_bulanan` (sudah agregat bulanan).

```python
# Penumpang per bulan = total semua rute
monthly_pax_sum = pax.groupby("waktu_id")["jumlah_penumpang"].sum()
```

## Hasil dari Data Kamu

| Indikator | Min | Max | Bulan min | Bulan max |
|---|---:|---:|---|---|
| Penumpang | 96.452 | 9.122.039 | Mei 2020 (lockdown puncak) | Jan 2020 (pre-COVID) |
| Kurs | 13.732 | 16.329 | Jan 2020 | Des 2024 |
| Brent | 26,35 | 115,60 | Mar 2020 (oil crash) | Jun 2022 (Russia-Ukraine) |
| BI rate | 3,50 | 6,25 | era PPKM | era pengetatan 2023-2024 |

## Makna Angka
- **Penumpang 96K di Mei 2020** vs 9.12M di Jan 2020 = drop ~99%. Ini *base rate* benchmark crisis untuk industri ini.
- **Kurs naik 19%** (13.732 → 16.329) sepanjang 5 tahun. Bukan crash satu kali, melainkan pelemahan struktural.
- **Brent crash 53%** Jan→Mar 2020 (56,62 → 26,35) lalu lompat 339% ke Jun 2022 — shock minyak ganda.
- **BI rate naik 79%** (3,5 → 6,25) di periode 2022–2023 — respons agresif terhadap pelemahan rupiah & inflasi.

## Reference Lines (event annotations)
Garis vertikal putus-putus menandai 6 event eksternal:
1. PSBB (Mar 2020)
2. PPKM Darurat / Delta wave (Jul 2021)
3. Invasi Rusia–Ukraina (Feb 2022)
4. VOA dibuka (Mei 2022)
5. PPKM dicabut (Jan 2023)
6. Rupiah tembus Rp 16.000 (Apr 2024)

Fungsi: audience bisa langsung mencocokkan perubahan visual di chart dengan event eksternal yang menyebabkannya.

## Output
- `plot.png` — 4-panel chart
- `data_4panel.csv` — data per bulan (60 baris)

## Target Tableau — Step by Step

### Persiapan (sekali saja untuk seluruh workbook)
1. **Set default aggregation**: klik kanan `avg_kurs_tengah` di Data pane → **Default Properties → Aggregation → Average**. Ulangi untuk `brent_usd_bbl`, `bi_rate`, `inflasi_yoy`, `inflasi_mtm`, `tarif_tiket_ihk`, `min_kurs_tengah`, `max_kurs_tengah`. (`jumlah_penumpang` tetap SUM — itu default-nya.)
2. **Buat calculated field `Tanggal Analisis`**: klik kanan area kosong Data pane → Create Calculated Field → nama "Tanggal Analisis" → formula:
   ```
   DATEPARSE('yyyyMM', STR([waktu_id]))
   ```
   Klik OK. Field baru akan muncul di Dimensions.

### Langkah Pembuatan Sheet
1. **Buat worksheet baru**, beri nama `Bab1_WS1_MultiPanel`.
2. **Drag `Tanggal Analisis` ke Columns**. Klik kanan pil → pilih **Month** di bagian *Continuous* (warna pil = hijau). Pastikan format bulanan, bukan diskret tahun.
3. **Drag 4 measure berikut ke Rows secara berurutan** (akan menumpuk ke bawah membentuk 4 panel):
   - `SUM(jumlah_penumpang)`
   - `AVG(avg_kurs_tengah)`
   - `AVG(brent_usd_bbl)`
   - `AVG(bi_rate)`
4. **Pilih Marks card untuk masing-masing panel**: pastikan tipe Mark = **Line**. (Di Marks card atas ada dropdown "All", lalu di bawahnya ada satu Marks card per measure di Rows — set Line untuk semua.)
5. **Tambah Reference Lines** untuk event eksternal:
   - Klik kanan sumbu X (tanggal) di panel paling atas → **Add Reference Line** → pilih *Line* (bukan Band) → *Constant* (manual ketik tanggal) atau pakai *Per Cell*.
   - Tambah 7 reference lines pada tanggal: 01-Mar-2020 (PSBB), 01-Jul-2021 (PPKM Darurat), 01-Feb-2022 (Russia-Ukraine), 01-May-2022 (VOA dibuka), 01-Jan-2023 (PPKM dicabut), 01-Apr-2024 (Rupiah > 16K), 01-Oct-2024 (eskalasi Timur Tengah).
   - Atau lebih praktis: buat **Parameter** `Event Date` dengan list 7 tanggal, lalu reference line di-link ke parameter.
6. **Format**: klik kanan sumbu Y kiri tiap panel → Format → set decimal/satuan. Misal panel pertama (penumpang) → Number (Custom) → "#,##0,M" supaya tampak juta.

### Cross-check ke Python
Hover ke titik tertinggi/terendah:
- Panel penumpang: max **Jan 2020 = 9.122.039**, min **Mei 2020 = 96.452**.
- Panel kurs: min Jan 2020 = **13.732**, max Des 2024 = **16.329**.
- Panel Brent: min Apr 2020 = **26,35**, max Jun 2022 = **115,60** (kalau range tidak match, kemungkinan default agg masih SUM).
- Panel BI Rate: min era PPKM = **3,5%**, max akhir 2024 = **6,25%**.

### Catatan Khusus
- Kalau panel kelihatan datar (semua nilai jadi besar/akumulatif), itu karena `avg_kurs_tengah` masih ber-aggregation SUM. Kembali ke Step 1 Persiapan.
- Untuk presentasi: pakai **Dashboard** terpisah dan susun ke-4 panel ini side-by-side untuk visual yang lebih rapi.

---

## ⚙️ Update — Catatan Implementasi Tableau

**Format angka `#,##0,,M` (0M untuk angka < 1 juta)**:
Format ini terlalu kasar untuk panel penumpang yang range-nya 96K–9M (jadi 0M-9M, hilang detail).

**Ganti ke format yang lebih informatif**:
- Custom format: `#,##0.0,,"M"` (decimal 1 angka) → 9,1M dan 0,1M.
- Atau biarkan default (angka penuh tampil seperti `9,122,039`) seperti yang kamu lakukan sekarang — tidak salah.

Lihat `solusi_masalah.md` Solusi #2.
