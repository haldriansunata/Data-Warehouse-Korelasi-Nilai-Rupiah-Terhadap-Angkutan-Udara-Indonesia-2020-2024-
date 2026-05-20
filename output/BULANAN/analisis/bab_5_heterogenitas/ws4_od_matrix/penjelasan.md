# Bab 5 / WS4 — OD Matrix (Top 10 IATA × Top 10 IATA)

## Tujuan
Visualisasi **asimetri flow** antar hub utama. OD matrix klasik untuk industri transportasi.

## Pendekatan
Heatmap matrix:
- Rows: top 10 IATA sebagai origin
- Columns: top 10 IATA sebagai destination
- Cell value: SUM(jumlah_penumpang) untuk pasangan (origin, destination)

## Hasil dari Data Kamu (Top 10 IATA = CGK, DPS, SUB, UPG, KNO, SIN, BPN, KUL, BTH, YIA)

Pivot table (juta penumpang):

|  | CGK | DPS | SUB | UPG | KNO | SIN | BPN | KUL | BTH | YIA |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **CGK** | — | **16,82** | **11,51** | **10,96** | **12,35** | 8,49 | — | 5,91 | — | 5,12 |
| DPS | — | — | 4,57 | 1,89 | 0,04 | 6,89 | — | 4,05 | — | 1,18 |
| SUB | — | — | — | 5,43 | — | — | — | — | — | — |
| UPG | — | — | — | — | — | — | — | — | — | 1,33 |
| KNO | — | — | 0,02 | — | — | 0,61 | — | 2,20 | — | 0,38 |
| SIN | — | — | 1,82 | 0,13 | — | — | — | — | — | 0,37 |
| **BPN** | 5,80 | 0,52 | 3,64 | 2,05 | 0,01 | 0,09 | — | 0,06 | 0,04 | 1,56 |
| KUL | — | — | 1,80 | 0,24 | — | — | — | — | — | 0,46 |
| BTH | 5,37 | — | 1,58 | — | 2,48 | — | — | 0,04 | — | 0,25 |
| YIA | — | — | — | — | — | — | — | — | — | — |

## Makna

### 1. Asimetri di data
Banyak cell kosong di "bawah-kiri" matrix (mis. cell DPS-CGK kosong tapi CGK-DPS 16,82). Ini karena **`kode_rute` di-normalisasi alfabetis** saat ETL (`pair = sorted([a, b])`), jadi rute "PP" hanya disimpan sekali sebagai `A-B` di mana A < B alfabetis. Jadi flow CGK→DPS dan DPS→CGK *digabung* di pair CGK-DPS, dan diletakkan di sel (CGK,DPS) bukan (DPS,CGK).

**Untuk pembacaan**: cell (A,B) menunjukkan total flow **dua arah** antara A dan B, terletak di posisi alfabetis.

### 2. CGK hub absolut
Row CGK punya 7 cells terisi dengan volume besar (5–17M). Tidak ada bandara lain yang sebanding sebagai hub. Implikasi: bottleneck operasional & target kebijakan untuk decongestion.

### 3. Pola hub-and-spoke domestik
- CGK ↔ {DPS, KNO, SUB, UPG, PNK, PDG, ...} = hub-and-spoke murni
- SUB-UPG (5,43M) = satu-satunya pasangan non-CGK signifikan di top 10 = **secondary corridor** Surabaya-Makassar
- KNO-KUL (2,2M), BTH-KNO (2,48M) = local cross-border (Medan-Penang/KL-Batam) bypass CGK

### 4. International nodes
- SIN dan KUL muncul di top 10 → konfirmasi dominasi ASEAN di trafik internasional
- Tidak ada DOH, SYD, NRT di top 10 → meskipun individu rute besar (CGK-DOH dll), volume aggregate masih di bawah hub domestik

## Output
- `plot.png` — heatmap
- `od_matrix.csv` — pivot table

## Target Tableau — Step by Step

### Langkah Pembuatan Sheet
1. **Buat worksheet baru** `Bab5_WS4_ODMatrix`.
2. **Drag `o_iata` ke Rows** (atau nama field IATA dari instance origin). Pil biru.
3. **Drag `d_iata` ke Columns** (instance destination). Pil biru.
4. **Marks**: Square (dropdown atas Marks card).
5. **Drag `SUM(jumlah_penumpang)` ke Color** di Marks card.
6. **Edit Colors**: klik dropdown Color → Edit Colors → palette sequential **Orange-Red** atau **Green-Blue Diverging**. Centang "Stepped Color" kalau mau lebih kontras.
7. **Filter Top 10 di kedua axis**:
   - Klik kanan `o_iata` di Rows → Filter → tab Top → Top 10 by `SUM([jumlah_penumpang])`.
   - Klik kanan `d_iata` di Columns → Filter → tab Top → Top 10 by `SUM([jumlah_penumpang])`.
8. **Tambah label**:
   - Drag `SUM(jumlah_penumpang)` ke Label di Marks card.
   - Format: Number Custom → `#,##0,,"M"`.
   - Klik kanan Label di Marks → set warna text ke "Match Mark Color" supaya kontras.

### Cross-check ke Python
File `od_matrix.csv`. Cell tertinggi:
- CGK → DPS: **16,82 juta** (warna paling gelap di pojok)
- CGK → KNO: 12,35 juta
- CGK → SUB: 11,51 juta

### Catatan KHUSUS
- **Asymmetric flow**: karena `dim_rute` menyimpan pasangan IATA terurut alfabetis (`A-B` di mana A<B), banyak cell di "segitiga bawah" akan kosong. Ini wajar — flow PP digabung di satu cell.
- Top 10 IATA yang muncul (dari Python): CGK, DPS, SUB, UPG, KNO, SIN, BPN, KUL, BTH, YIA.
- Untuk presentasi, susun dengan **CGK** di paling atas/kiri supaya pattern hub dominan langsung terlihat. Klik kanan `o_iata` → Sort → Manual.
