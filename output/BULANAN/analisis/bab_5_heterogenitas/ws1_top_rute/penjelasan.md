# Bab 5 / WS1 — Top 15 Rute by Total Penumpang

## Tujuan
Memberi konteks "rute mana yang paling penting" sebelum bicara sensitivitas. Audience perlu tahu skala flow sebelum bicara per-rute elastisitas.

## Pendekatan
Aggregate `SUM(jumlah_penumpang)` per `kode_rute` selama 60 bulan, sort descending, ambil top 15. Color by `kategori` (DOM/INT).

## Perhitungan
```python
top15 = (df.groupby(["kode_rute", "kategori"])["jumlah_penumpang"]
           .sum()
           .nlargest(15))
```

## Hasil dari Data Kamu

| Rank | Rute | Kategori | Total Penumpang (juta) |
|---:|---|---|---:|
| 1 | **CGK-DPS** | DOMESTIK | **16,82** |
| 2 | CGK-KNO | DOMESTIK | 12,35 |
| 3 | CGK-SUB | DOMESTIK | 11,51 |
| 4 | CGK-UPG | DOMESTIK | 10,96 |
| 5 | **CGK-SIN** | INTERNASIONAL | **8,49** |
| 6 | DPS-SIN | INTERNASIONAL | 6,89 |
| 7 | CGK-PNK | DOMESTIK | 6,21 |
| 8 | CGK-KUL | INTERNASIONAL | 5,91 |
| 9 | CGK-PLM | DOMESTIK | 5,83 |
| 10 | BPN-CGK | DOMESTIK | 5,80 |
| 11 | CGK-PDG | DOMESTIK | 5,71 |
| 12 | SUB-UPG | DOMESTIK | 5,43 |
| 13 | CGK-PKU | DOMESTIK | 5,42 |
| 14 | BTH-CGK | DOMESTIK | 5,37 |
| 15 | CGK-YIA | DOMESTIK | 5,12 |

## Makna

### Pola dominan: CGK adalah jantung sistem
- **12 dari 15 rute top melibatkan CGK** (Soekarno-Hatta) sebagai salah satu endpoint.
- Hanya 3 rute non-CGK: DPS-SIN (Bali↔SG), SUB-UPG (Surabaya↔Makassar), BTH-CGK (Batam) – wait BTH-CGK juga CGK. Jadi efektif **14 dari 15 rute via CGK**.
- Implikasi: CGK adalah single point of failure & dominasi hub. Kebijakan terkait CGK punya leverage besar.

### Domestik vs Internasional
- **12 rute domestik, 3 rute internasional** di top 15.
- Top INT: CGK-SIN, DPS-SIN, CGK-KUL — semuanya ASEAN. Tidak ada rute ke Eropa/AS di top 15.

### Implikasi untuk Bab 5 selanjutnya
Karena flow terpusat di beberapa hub, analisis per-rute (WS2) dan per-negara (WS3) akan dipengaruhi kuat oleh CGK-DPS dan CGK-SIN. Filter top-10 INT di WS2 akan mencakup rute-rute ini.

## Output
- `plot.png` — horizontal bar chart top 15
- `top15_rute.csv`

## Target Tableau — Step by Step

### Langkah Pembuatan Sheet
1. **Buat worksheet baru** `Bab5_WS1_TopRute`.
2. **Drag `kode_rute` ke Rows**. Pil biru.
3. **Drag `jumlah_penumpang` ke Columns**. Pil SUM hijau.
4. **Filter Top 15**:
   - Klik kanan `kode_rute` di Rows → **Filter** → tab **Top** → centang **"By field"** → set: Top **15** by `SUM([jumlah_penumpang])` → OK.
5. **Sort descending**:
   - Klik kanan `kode_rute` di Rows → **Sort** → By Field → Descending → SUM(jumlah_penumpang).
   - Atau toolbar: klik icon "Sort descending" (icon panah turun) di toolbar atas.
6. **Drag `kategori` ke Color** (dim_rute). Akan tampak 2 warna: DOM (mis. biru), INT (mis. merah).
7. **Drag `SUM(jumlah_penumpang)` ke Label** di Marks card. Format: Number Custom → `#,##0,,"M"` untuk tampilan dalam juta.

### Cross-check ke Python
File `top15_rute.csv` — Top 5 dari Python:

| Rank | Rute | Kategori | Total (juta) |
|---:|---|---|---:|
| 1 | CGK-DPS | DOMESTIK | 16,82 |
| 2 | CGK-KNO | DOMESTIK | 12,35 |
| 3 | CGK-SUB | DOMESTIK | 11,51 |
| 4 | CGK-UPG | DOMESTIK | 10,96 |
| 5 | CGK-SIN | INTERNASIONAL | 8,49 |

Bar paling panjang Tableau = CGK-DPS = 16,82M.

### Catatan untuk Presentasi
- **14 dari 15 rute melibatkan CGK** — beri annotation manual untuk highlight dominasi hub.
- Tambah title sheet: "Top 15 Rute by Total Penumpang Bulanan (60 bulan)".
