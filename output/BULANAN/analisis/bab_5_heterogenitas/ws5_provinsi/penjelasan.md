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

## Target Tableau
- Filter: `kategori = DOMESTIK`
- Rows: `[dim_bandara_origin].provinsi` (gunakan field yang sudah di-grouping di Tableau)
- Columns: `SUM(jumlah_penumpang)`
- Sort: descending

**Untuk peta**: Tableau bisa auto-detect provinsi Indonesia kalau nama-nya match dengan basemap-nya. Karena ada nama Inggris di data, mungkin perlu Edit Locations manual (Map → Edit Locations → pilih country Indonesia, lalu map nama-nama yang tidak match).
