# Bab 5 / WS5 — Top 15 Provinsi by Total Penumpang Domestik

## Tujuan
Distribusi geografis demand domestik per provinsi origin. Konteks penting untuk pembuat kebijakan: mana provinsi yang flow-nya paling besar.

## Pendekatan
Aggregate total penumpang per `o_provinsi` (provinsi asal), filter `kategori = DOMESTIK`, top 15.

## Hasil

| Rank | Provinsi (origin) | Total Pax (juta) |
|---:|---|---:|
| 1 | **JAKARTA** | **115,15** |
| 2 | EAST KALIMANTAN | 16,62 |
| 3 | RIAU ISLANDS | 14,63 |
| 4 | BALI | 13,17 |
| 5 | KALIMANTAN SELATAN | 10,70 |
| 6 | DKI JAKARTA | 9,63 |
| 7 | PAPUA | 6,97 |
| 8 | EAST JAVA | 5,88 |
| 9 | KALIMANTAN TIMUR | 4,34 |
| 10 | EAST NUSA TENGGARA | 3,74 |
| 11 | WEST PAPUA | 3,43 |
| 12 | MALUKU | 3,33 |
| 13 | SOUTHEAST SULAWESI | 3,11 |
| 14 | WEST NUSA TENGGARA | 2,89 |
| 15 | NORTH SULAWESI | 2,75 |

## Caveat Data — Inkonsistensi Nama Provinsi

Ada **dua entri Jakarta**: `JAKARTA` (115M) dan `DKI JAKARTA` (9,63M). Juga **dua entri Kalimantan Timur**: `EAST KALIMANTAN` (16,6M) dan `KALIMANTAN TIMUR` (4,3M). Ini karena `dim_bandara.csv` punya field `provinsi` yang inkonsisten — sebagian dari `airportsdata` library (Bahasa Inggris) dan sebagian dari override manual (Bahasa Indonesia).

### Implikasi
- **Jakarta + DKI Jakarta = 124,78M** sebenarnya — masih dominan absolut.
- East Kalimantan + Kalimantan Timur = 20,96M.

### Rekomendasi Cleanup (opsional, future)
Tambahkan pemetaan di ETL `03_dim_bandara.py`:
```python
PROVINSI_HARMONIZE = {
    "JAKARTA": "DKI JAKARTA",
    "EAST KALIMANTAN": "KALIMANTAN TIMUR",
    "EAST JAVA": "JAWA TIMUR",
    # ... dst
}
```
Tapi karena kamu sudah set TIDAK mengubah BULANAN, ini bisa di-handle di **Tableau dengan group manual** (klik kanan field → Group → satukan duplikat).

## Makna

### 1. Dominasi Jakarta (~125M ≈ 50% dari semua flow domestik)
Jakarta adalah origin dari hampir setengah total penumpang domestik. Bukan kejutan tapi konfirmasi numerik.

### 2. Kalimantan & Riau Islands tinggi
- Kalimantan (Timur + Selatan) total ~31M — workforce migration ke industri tambang/sawit.
- Riau Islands (Batam, Tanjung Pinang) ~14,6M — gerbang Singapura, cross-border worker.

### 3. Bali (13,2M)
Origin Bali tinggi karena wisman + outbound. Tableau peta akan menyoroti ini.

### 4. Indonesia Timur (Papua, NTT, Maluku, Sulawesi Tenggara)
Kombinasi 4 provinsi ini ~17M — penting untuk konektivitas region, biasanya rute thin & dependen subsidi.

## Output
- `plot.png` — horizontal bar top 15
- `top15_provinsi.csv`

## Target Tableau — Step by Step

### Persiapan: Konsolidasi Nama Provinsi (Group Manual)
Karena `dim_bandara.provinsi` punya inkonsistensi (mis. "JAKARTA" vs "DKI JAKARTA"; "EAST KALIMANTAN" vs "KALIMANTAN TIMUR"), buat **Group**:
1. Di Data pane, klik kanan field `o_provinsi` (origin) → **Create → Group**.
2. Beri nama group field: `Provinsi (Cleaned)`.
3. Di dialog Create Group:
   - Pilih "JAKARTA" + "DKI JAKARTA" (Ctrl+click), klik **Group** → rename "DKI JAKARTA".
   - Pilih "EAST KALIMANTAN" + "KALIMANTAN TIMUR" → Group → "KALIMANTAN TIMUR".
   - Ulangi untuk provinsi lain yang duplikat (cek dengan `Show Members`).
4. Klik OK.

### Langkah Pembuatan Sheet (Bar Chart)
1. **Buat worksheet baru** `Bab5_WS5_Provinsi`.
2. **Filter Domestik**: drag `kategori` ke Filters → centang `DOMESTIK`.
3. **Drag `Provinsi (Cleaned)` ke Rows** (bukan field provinsi original).
4. **Drag `jumlah_penumpang` ke Columns**. Pil SUM.
5. **Filter Top 15**: klik kanan `Provinsi (Cleaned)` di Rows → Filter → Top → Top 15 by SUM.
6. **Sort descending**: klik icon sort di toolbar atau klik kanan field → Sort By Field.
7. **Color**: opsional, pakai field konstan atau warna tunggal.
8. **Label**: drag `SUM(jumlah_penumpang)` ke Label, format dalam juta.

### Cross-check ke Python (Setelah Group)
File `top15_provinsi.csv`:
- DKI JAKARTA (cleaned): ~**125 juta** (Jakarta + DKI Jakarta digabung)
- KALIMANTAN TIMUR (cleaned): ~21 juta
- KEPULAUAN RIAU: 14,63 juta
- BALI: 13,17 juta

### Bonus: Peta Provinsi
1. **Buat worksheet baru** `Bab5_WS5b_PetaProvinsi`.
2. **Drag `Provinsi (Cleaned)` ke worksheet** — Tableau akan auto-detect sebagai **geographic role**.
3. Kalau muncul peta dunia (bukan Indonesia), klik kanan field → **Geographic Role → State/Province**.
4. **Edit Locations** kalau ada nama yang tidak match:
   - Map → Edit Locations.
   - Pilih country: **Indonesia**.
   - Untuk setiap unrecognized name, pilih dari dropdown (mis. "BALI" → "Bali, Indonesia").
5. **Show Me**: pilih **Symbol Map** atau **Filled Map**.
6. **Size**: `SUM(jumlah_penumpang)`.
7. **Color**: opsional, pakai sequential palette dengan field yang sama atau `AVG(avg_kurs_tengah)` di tahun 2024 (filter tahun=2024) untuk konteks.

### Catatan
- Peta provinsi Indonesia di Tableau **tidak selengkap peta US/Eropa** — beberapa provinsi mungkin perlu manual mapping (terutama provinsi baru seperti Papua Pegunungan, Papua Selatan).
- Kalau Tableau tidak punya geocoding lengkap, alternatif: pakai **bar chart horizontal** saja (lebih reliable).
