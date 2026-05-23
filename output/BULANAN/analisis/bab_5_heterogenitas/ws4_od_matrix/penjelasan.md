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

---

## Target Tableau — Tutorial Step-by-Step

> **Konteks penting sebelum mulai**: jangan pakai filter "Top 10 by SUM" native Tableau di kedua axis — hasilnya akan **berbeda** karena `dim_rute` di proyek ini me-normalize pasangan IATA alfabetis (yang awal alfabet jadi origin, yang akhir jadi destination). Yang benar: pakai **1 list IATA tetap** untuk kedua axis. List yang dipakai: **`CGK, DPS, SUB, UPG, KNO, SIN, BPN, KUL, BTH, YIA`** (= top 10 aggregate kedua sisi dari Python).

### Step 1 — Buat worksheet baru
1. Klik **icon worksheet baru** di bar bawah Tableau (icon kotak dengan tanda +).
2. Rename tab jadi **`Bab5_WS4_ODMatrix`** (double-click tab → ketik nama).

### Step 2 — Drag field ke Rows dan Columns
1. **Drag `Iata`** (dari `dim_bandara_origin`, nama field tanpa suffix) ke **Rows**. Pil biru muncul.
2. **Drag `Iata (Dim Bandara Destination.Csv)`** (dari `dim_bandara_destination`) ke **Columns**. Pil biru muncul.

> Layar sekarang akan tampak **sangat ramai** karena semua IATA muncul (200+ bandara × 200+ bandara). Tenang — akan kita filter di Step 3.

### Step 3 — Filter origin ke 10 IATA
1. **Drag `Iata`** (origin, dari Data pane) ke area **Filters**.
2. Jendela "Filter [Iata]" muncul.
3. Di tab **General**, klik **None** dulu (untuk uncheck semua), lalu **check manual** 10 IATA ini:
   - **CGK, DPS, SUB, UPG, KNO, SIN, BPN, KUL, BTH, YIA**
4. Klik **OK**.

### Step 4 — Filter destination ke 10 IATA yang sama
1. **Drag `Iata (Dim Bandara Destination.Csv)`** (destination, dari Data pane) ke area **Filters**.
2. Di tab **General**, klik **None**, lalu **check manual** 10 IATA yang **sama persis**:
   - **CGK, DPS, SUB, UPG, KNO, SIN, BPN, KUL, BTH, YIA**
3. Klik **OK**.

### Step 5 — Set Marks ke Square
1. Di **Marks card** (panel kiri tengah), klik dropdown **Automatic** di paling atas.
2. Pilih **Square**.

### Step 6 — Drag SUM(jumlah_penumpang) ke Color
1. **Drag `jumlah_penumpang`** dari Data pane ke **Color** di Marks card.
2. Pastikan agregasi-nya **SUM** (default). Pil akan tampil `SUM(jumlah_penumpang)`.
3. **Edit warna**:
   - Klik **Color** di Marks card → **Edit Colors**.
   - Pilih palette sequential, mis. **Orange-Red** atau **Green-Blue**.
   - Centang **Stepped Color** dengan 5–7 step kalau mau kontras lebih tajam.
   - Klik **Apply** → **OK**.

### Step 7 — Drag SUM(jumlah_penumpang) ke Label
1. **Drag `jumlah_penumpang`** dari Data pane ke **Label** di Marks card.
2. Pil di Label akan tampil `SUM(jumlah_penumpang)`.
3. **Format label angka**:
   - Klik kanan pil `SUM(jumlah_penumpang)` di Label → **Format**.
   - Di panel Format (sebelah kiri), klik tab **Pane**.
   - Cari **Numbers** → pilih **Custom**.
   - Ketik: **`#,##0.0,,"M"`** (perhatikan: titik koma sebelum 0, dua koma sebelum "M").
   - Contoh hasil: 16.822.345 → `16,8M`.
4. **(Opsional)** Klik kanan Label di Marks → **Format** → set warna text ke **Match Mark Color** untuk kontras.

### Step 8 — Sort manual supaya CGK di pojok kiri-atas
Tableau default sort alfabetis (AAP, AMQ, BPN, ...). CGK akan ada di tengah, bukan pojok. Sort manual:

1. **Sort Rows**:
   - Klik kanan pil `Iata` di **Rows** → **Sort**.
   - Sort By: **Manual**.
   - Drag urutan: **CGK** ke paling atas, lalu DPS, SUB, UPG, KNO, SIN, BPN, KUL, BTH, YIA.
   - Klik OK.
2. **Sort Columns**:
   - Klik kanan pil `Iata (Dim Bandara Destination.Csv)` di **Columns** → **Sort**.
   - Sort By: **Manual**.
   - Urutan sama: CGK, DPS, SUB, UPG, KNO, SIN, BPN, KUL, BTH, YIA.
   - Klik OK.

### Step 9 — Cek visual
Sekarang OD matrix-mu seharusnya menampilkan:
- 10 baris × 10 kolom (100 cell).
- Cell tergelap di **CGK-DPS = 16,8M** (pojok kiri-atas area, posisi row CGK kolom DPS).
- Banyak cell kosong di "segitiga bawah" (mis. DPS-CGK kosong tapi CGK-DPS terisi) — itu wajar, karena flow PP digabung di pair alfabetis.

---

## Cross-Check ke Python

| Origin | Destination | Pax (juta) — harus match di Tableau |
|---|---|---:|
| CGK | DPS | **16,82** |
| CGK | KNO | 12,35 |
| CGK | SUB | 11,51 |
| CGK | UPG | 10,96 |
| CGK | SIN | 8,49 |
| CGK | BPN | 5,91 |
| CGK | YIA | 5,12 |
| BPN | CGK | 5,80 |
| BTH | CGK | 5,37 |
| SUB | UPG | **5,43** (secondary corridor) |

Hover Tableau ke cell CGK-DPS → label harus tampil **16,8M**. Kalau angka berbeda jauh:
- Cek filter `kategori` tidak ter-set (Python aggregate **semua kategori**, jangan filter DOMESTIK/INTERNASIONAL di WS4).
- Cek 10 IATA yang dipilih di Step 3 dan Step 4 **sama persis**.

---

## Catatan Khusus

### Kenapa pakai filter manual, bukan Top N?
`dim_rute` menormalkan pasangan IATA alfabetis (`bandara_1_id` = yang alfabet lebih awal). Akibat:
- Top 10 origin pakai Top N native = CGK, DPS, BPN, BTH, BDJ, HLP, KNO, SUB, DJJ, KUL (IATA awal alfabet dominan).
- Top 10 destination pakai Top N native = SUB, UPG, CGK, DPS, KNO, SIN, YIA, KUL, PLM, PKU (IATA akhir alfabet dominan).
- Hasilnya **list berbeda di kedua axis** → OD matrix tidak match Python.

Solusi: hard-code list yang sama untuk kedua axis (Step 3 & 4).

### Asymmetric flow
Cell di "segitiga bawah" (mis. DPS-CGK) sering kosong karena flow PP digabung di pair alfabetis. Ini wajar, bukan bug.

### Untuk presentasi
Annotation manual: *"CGK adalah hub absolut — 7 dari 10 cell terisi di row CGK, total flow > 70M. Tidak ada bandara lain yang sebanding sebagai hub."*
