# Bab 1 / WS4 — Heatmap Musiman (Tahun × Bulan)

## Tujuan
Visualisasi padat untuk pola musiman + COVID dip + recovery curve dalam **satu** chart. Lebih informatif daripada line chart untuk audience non-teknis.

## Pendekatan
**Heatmap matrix**: baris = tahun, kolom = bulan, warna sel = total penumpang. Pivot-table klasik.

## Perhitungan
```python
pivot = df.pivot_table(
    index="tahun",
    columns="bulan",
    values="jumlah_penumpang",
    aggfunc="sum"
)
```

## Hasil dari Data Kamu (juta penumpang)

|  | Jan | Feb | Mar | Apr | Mei | Jun | Jul | Agu | Sep | Okt | Nov | Des |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **2020** | **9,12** | 7,76 | 5,51 | 0,98 | **0,10** | 0,75 | 1,71 | 2,34 | 2,11 | 2,48 | 3,24 | 3,72 |
| **2021** | 2,60 | 2,14 | 2,91 | 3,19 | 2,76 | 3,94 | **1,18** | 1,32 | 2,14 | 3,26 | 3,97 | 4,49 |
| **2022** | 3,70 | 3,08 | 3,96 | 4,24 | 6,02 | 5,39 | 5,72 | 4,94 | 4,58 | 5,51 | 5,32 | 6,51 |
| **2023** | 6,83 | 6,28 | 6,87 | 7,11 | 8,09 | 7,89 | 8,69 | 7,89 | 7,58 | 7,96 | 7,67 | 8,26 |
| **2024** | 7,56 | 7,06 | 7,01 | 8,58 | 8,01 | 8,23 | **9,03** | 8,65 | 8,48 | 8,29 | 7,71 | **8,98** |

## Makna Angka

### Pattern yang langsung terlihat:
1. **Black hole Mei 2020 = 0,10 juta** (98,9% drop vs Jan 2020). Bulan paling parah dalam sejarah industri penerbangan modern Indonesia.
2. **Resesi kedua Jul-Sep 2021 (Delta wave)**: turun lagi ke 1,18 juta di Jul 2021 setelah sempat recovery ke 3,94 di Jun 2021.
3. **Rebound bertahap 2022–2023**: garis warna naik tahun demi tahun.
4. **Plateau 2024 dekat 8–9 juta** = ~90% baseline 2020 (pre-COVID), masih belum 100% recovery.

### Pola seasonal stabil tahun-tahun:
- **Spike Mei (2020, 2021, 2022)** = Lebaran (bulan Lebaran bergeser seiring tahun).
- **Spike April (2023, 2024)** = Lebaran bergeser ke April.
- **Spike Juli** (2024 = 9,03M = puncak) = libur sekolah.
- **Spike Desember** = Natal + Tahun Baru.

## Insight untuk Topik
Heatmap memvalidasi **dua hal**:
1. **COVID benar-benar shock asimetris** — bukan slow decline, tapi step-function di Mar–Apr 2020.
2. **Pattern Lebaran/Natal sangat konsisten** tahun demi tahun → flag `has_lebaran`, `has_natal`, `is_peak_season` di Bab 4 punya signal kuat untuk diuji.

Visual ini juga jadi *validasi sanity check*: kalau Tableau heatmap kamu tidak match dengan ini, ada masalah di join atau aggregation.

## Output
- `plot.png` — heatmap
- `pivot_pax_tahun_bulan.csv` — matriks

## Target Tableau — Step by Step

### Langkah Pembuatan Sheet
1. **Buat worksheet baru**, beri nama `Bab1_WS4_HeatmapSeasonal`.
2. **Drag `nama_bulan` ke Columns**. Pil biru (Discrete). Default order alfabetis — kita perlu manual sort.
3. **Sort manual `nama_bulan` Jan–Des**:
   - Klik kanan field `nama_bulan` di Data pane → **Default Properties → Sort** → Manual.
   - Atur urutan: Januari, Februari, Maret, April, Mei, Juni, Juli, Agustus, September, Oktober, November, Desember.
   - Atau lebih cepat: pakai field `bulan` (angka 1–12) sebagai sort key — klik kanan `nama_bulan` di Columns → Sort → By Field → `bulan` ascending.
4. **Drag `tahun` ke Rows**. Pil biru (Discrete).
5. **Pilih Marks card**: ubah tipe Mark dari Automatic ke **Square**.
6. **Drag `SUM(jumlah_penumpang)` ke Color di Marks card**.
7. **Pilih palette**: klik dropdown Color di Marks card → Edit Colors → palette **Orange-Red** (sequential, dark = high). Centang "Stepped Color" kalau mau diskrit.
8. **Tambah label angka di tiap sel**:
   - Drag `SUM(jumlah_penumpang)` ke **Label** di Marks card.
   - Klik kanan label → Format → Numbers → Custom → ketik `#,##0,,"M"` (akan tampak "9M" untuk 9.000.000).
9. **Resize sel**: drag border kolom/baris untuk membuat heatmap proporsional (mis. lebar = tinggi).

### Cross-check ke Python
- Cell Mei 2020 = **0,1 juta** (warna paling gelap kalau pakai sequential).
- Cell Jan 2020 = **9,12 juta** (warna paling terang).
- Cell Jul 2024 = **9,03 juta** — peak recovery.

### Catatan Khusus
- Kalau sel terlalu kecil dan label tidak muat, perbesar zoom (Fit → Fit Width).
- Untuk presentasi, beri **Title sheet** "Heatmap Penumpang Nasional (juta) — Tahun × Bulan".
- Color legend: tampilkan dengan klik tombol "Show Color Legend" di toolbar Tableau.

---

## ⚙️ Update — Catatan Implementasi Tableau

**Format angka `#,##0,,M`**: untuk heatmap, format `#,##0.0,,"M"` (decimal 1 angka) lebih readable karena nilai sel ada yang 0,1M (Mei 2020) dan 9,1M (Jan 2020). Atau pakai format default kalau cell-nya cukup besar untuk menampilkan angka penuh.

Lihat `solusi_masalah.md` Solusi #2.
