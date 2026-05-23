# Bab 5 / WS3 — Sensitivitas per Negara Destinasi (Headline Internasional)

## Tujuan
**Headline analysis Bab 5**: negara tujuan mana yang paling sensitif terhadap pelemahan rupiah?

Teori: rute ke negara dengan ekonomi besar/USD-pegged seharusnya lebih sensitif daripada ASEAN.

## Pendekatan
1. Untuk tiap rute INT, identifikasi `negara_asing` = negara dari endpoint yang bukan INDONESIA.
2. Filter ke negara dengan total pax > 500.000.
3. Untuk tiap negara, agregat pax bulanan dan jalankan regresi `pax ~ kurs`.
4. Bandingkan slope dan R².

```python
df_int["negara_asing"] = np.where(
    df_int["o_negara"] != "INDONESIA",
    df_int["o_negara"],
    df_int["d_negara"]
)
```

## Hasil (14 negara, sorted by slope ascending)

| Negara | Slope | R² | Total Pax (juta) |
|---|---:|---:|---:|
| TURKI | +13,5 | 0,41 | 1,3 |
| FILIPINA | +20,7 | **0,53** | 1,2 |
| JEPANG | +24,3 | 0,33 | 2,2 |
| THAILAND | +25,4 | 0,51 | 1,5 |
| TAIWAN | +26,6 | 0,40 | 1,9 |
| KOREA SELATAN | +30,5 | 0,45 | 2,2 |
| UNI EMIRAT ARAB | +39,1 | 0,47 | 3,2 |
| HONG KONG | +41,7 | 0,40 | 2,5 |
| ARAB SAUDI | +44,6 | 0,25 | **3,9** |
| QATAR | +50,3 | 0,51 | 3,8 |
| CHINA | +72,1 | 0,48 | 3,4 |
| AUSTRALIA | +123,4 | 0,48 | 7,9 |
| SINGAPURA | +277,6 | 0,46 | 18,9 |
| **MALAYSIA** | **+342,1** | **0,50** | **20,5** |

## Makna — Findings Bernilai untuk Paper

### Slope = pax per 1 IDR kurs, **direlasi VOLUME**
Negara besar volume (MALAYSIA, SINGAPURA) punya slope absolute lebih besar — bukan karena lebih elastis, tapi karena 1% perubahan dari volume besar = banyak orang.

### Elastisitas relatif (R²) lebih informatif
- **R² tertinggi**: FILIPINA (0,53), QATAR (0,51), THAILAND (0,51), MALAYSIA (0,50). Rute-rute ini variasinya paling banyak dijelaskan oleh dinamika kurs/COVID.
- **R² terendah**: ARAB SAUDI (0,25), JEPANG (0,33). Demand ke negara-negara ini punya driver lain yang dominan:
  - Arab Saudi → umroh/haji (terkait kuota & musim haji, bukan kurs)
  - Jepang → wisata kultural & kebijakan visa (Visa-free Jepang penting)

### Pola geopolitik & ekonomi tampak jelas
- **ASEAN dominan** (MY, SG): slope absolute terbesar — gerbang terdekat, volume terbesar, paling responsif ke shock makro.
- **Timur Tengah** (UAE, QSA, QAT): slope sedang, R² sedang — rute haji/umroh atau transit ke Eropa.
- **Australia**: volume besar (7,9M) tapi slope per-unit-volume sebenarnya kecil — mendukung argumen "inbound Aussie tahan kurs lemah".

## Yang Bisa Dijadikan Insight Paper

> "Dalam periode 2020-2024, **rute ke ASEAN** (Malaysia, Singapura, Filipina, Thailand) menunjukkan korelasi paling kuat dengan dinamika kurs IDR/USD, sedangkan **rute ke Arab Saudi dan Jepang** lebih dipengaruhi faktor non-kurs (kuota haji, kebijakan visa). Findings ini menyarankan bahwa kebijakan tarif batas atas dan stimulus sektor penerbangan perlu berbeda pendekatan per-koridor: koridor ASEAN bisa fokus pada *price competitiveness*, koridor Timur Tengah/Jepang lebih sensitif ke kebijakan visa/diplomasi."

## Output
- `plot.png` — horizontal bar slope per negara
- `sensitivity_per_negara.csv`

## Target Tableau — Step by Step

### Persiapan: Calculated Field
**Buat calculated field `negara_asing`** (klik kanan Data pane → Create Calculated Field):
```
IF [o_negara] != "INDONESIA" THEN [o_negara] ELSE [d_negara] END
```

Catatan: nama field `o_negara` dan `d_negara` ini adalah hasil prefix dari dua instance `dim_bandara` (origin dan destination). Cek di Data pane Tableau — kalau nama-nya beda (mis. `dim_bandara_origin.negara`), sesuaikan formula.

### Langkah Pembuatan Sheet
1. **Buat worksheet baru** `Bab5_WS3_PerNegara`.
2. **Filter kategori INT**: drag `kategori` ke Filters → centang `INTERNASIONAL`.
3. **Filter negara dengan volume signifikan**:
   - Drag `negara_asing` ke Filters → tab Top → "By field" → Top 14 by `SUM([jumlah_penumpang])`.
   - Atau pakai filter manual untuk exclude "INDONESIA" jika muncul.
4. **Drag `avg_kurs_tengah` ke Columns**. Pil `AVG`.
5. **Drag `jumlah_penumpang` ke Rows**. Pil SUM.
6. **Drag `waktu_id` ke Detail** → klik kanan → **Dimension**.
7. **Marks**: Circle.
8. **Drag `negara_asing` ke Color**.
9. **Trend Line per color**:
   - Analytics → Trend Line → Linear.
   - Edit Trend Lines → centang **"Allow a trend line per color"**.

### Cross-check ke Python
File `sensitivity_per_negara.csv` — sorted by R²:

| Negara | R² | Slope |
|---|---:|---:|
| **FILIPINA** | **0,532** | +20,7 |
| QATAR | 0,507 | +50,3 |
| THAILAND | 0,509 | +25,4 |
| MALAYSIA | 0,501 | +342,1 |
| SINGAPURA | 0,463 | +277,6 |
| AUSTRALIA | 0,481 | +123,4 |
| ... | ... | ... |
| **ARAB SAUDI** | **0,246** | +44,6 |

R² terendah (Saudi 0,25 dan Jepang 0,33) menunjukkan rute-rute ini punya driver non-kurs (haji, visa).

### Catatan untuk Presentasi
- **Ini HEADLINE Bab 5**. Tampilkan annotation: "Rute ke Filipina, Qatar, Thailand, Malaysia paling sensitif (R²>0,50). Saudi & Jepang tidak (R²<0,35) — driver kuota haji & kebijakan visa."
- Banyak warna (14 negara) bisa membuat chart ramai. Pertimbangkan **filter pertahap** — tunjukkan 5 negara dulu, lalu zoom ke 14.

---

## ⚙️ Update — Catatan Implementasi Tableau (BUTUH BUKTI VISUAL)

### Masalah yang kamu temukan
- Tutorial menyebut field `o_negara` / `d_negara`, tapi setelah self-join `dim_bandara` 2x di Tableau-mu, **nama field-nya beda** (misal `Negara` dan `Negara (Dim Bandara.csv1)`).
- Calculated field `negara_asing` jadi tidak bisa dibuat dengan formula di tutorial.
- Filipina tidak muncul di legend; list negara berbeda dengan contoh.
- Total pax per negara tidak ter-display di scatter trend line (beda dengan bar chart Python).

### Untuk diperbaiki, aku butuh bukti dari kamu

Upload ke folder `output/BULANAN/analisis/masalah/feedback_tableau/bab5_ws3_per_negara/`:
1. **SS1_data_pane.png** — Screenshot Data pane (nama-nama field hasil self-join).
2. **SS2_data_source_tab.png** — Screenshot tab Data Source (join structure).
3. **SS3_chart_sekarang.png** — Screenshot WS3 apa adanya.
4. **export_negara_visible.csv** — View Data → Full Data → Download.

Detail lengkap di `feedback_tableau/bab5_ws3_per_negara/README.md` dan `solusi_masalah.md` Solusi #7.

### Setelah file di atas masuk, aku akan
- Rewrite calculated field `negara_asing` dengan nama field yang match data-mu.
- Cek kenapa Filipina tidak muncul (filter Top 14 mungkin perlu disesuaikan).
- Update tutorial WS3 supaya match data structure-mu.

---

## 🔧 PERBAIKAN FINAL — Setelah Cek SS dan CSV Export-mu

### Diagnosis dari SS yang kamu upload
Dari `SS1_data_pane.png`, field hasil self-join `dim_bandara` di Tableau-mu adalah:

| Instance | Nama field di Data pane |
|---|---|
| Origin (dari `bandara_1_id`) | **`Negara`** (tanpa suffix) |
| Destination (dari `bandara_2_id`) | **`Negara (Dim Bandara Destination.Csv)`** |

Sama dengan `Iata`, `Kota`, `Nama Bandara`, `Provinsi` — kedua instance punya nama yang dibedakan dengan suffix.

### Masalah utama: di chart-mu (`SS3_chart_sekarang.png`)
Filter pakai field `Negara` (origin only) → akibatnya:
- Filipina (yang muncul sebagai `Negara (Destination)` di rute CGK-MNL) **TIDAK muncul** di legend.
- Daftar negara di legend cuma 13 (Australia, Selandia Baru, Malaysia, Thailand, China, dst) — bukan 14 seperti analisis Python.
- Negara dengan IATA destination "alfabet belakang" (Jepang/NRT, Korea/ICN, dst.) hilang karena `dim_rute` di proyek ini normalisasi alfabetis (`bandara_1` = alfabet lebih awal).

### Solusi: pakai calculated field `negara_asing` yang benar

#### Step 1 — Hapus filter Negara yang lama
1. Klik kanan pil `Negara` di **Filters** → **Remove**.
2. Klik kanan pil `Negara` di **Color** di Marks card → **Remove**.

#### Step 2 — Buat calculated field `Negara Asing` dengan formula yang BENAR
1. Klik kanan area kosong di Data pane → **Create Calculated Field**.
2. Nama: **`Negara Asing`**.
3. Formula (copy-paste persis):
   ```
   IF [Negara] != "INDONESIA" THEN [Negara]
   ELSE [Negara (Dim Bandara Destination.Csv)]
   END
   ```
4. Pastikan ada "*The calculation is valid*" → klik OK.

> **Catatan**: nama `Negara (Dim Bandara Destination.Csv)` harus ditulis **persis** sesuai data pane-mu. Kalau Tableau auto-complete tidak menampilkan, ketik manual sambil di-bracketed.

#### Step 3 — Setup filter dan visualisasi
1. **Drag `kategori` ke Filters** → centang `INTERNASIONAL` → OK.
2. **Drag `Negara Asing` ke Filters** → tab **Condition** → "By field" → `SUM(jumlah_penumpang)` `>=` `500000` → OK.
   - Atau lebih simple: tab **Top** → Top 14 by `SUM(jumlah_penumpang)`.
3. **Drag `avg_kurs_tengah` ke Columns** (pil AVG hijau).
4. **Drag `jumlah_penumpang` ke Rows** (pil SUM hijau).
5. **Drag `waktu_id` ke Detail** di Marks card → klik kanan → **Dimension**.
6. **Marks**: Circle.
7. **Drag `Negara Asing` ke Color** (field calculated yang baru).
8. **Trend Line per color**:
   - Analytics → Trend Line → Linear.
   - Klik kanan trend line → **Edit Trend Lines** → centang `[x] Allow a trend line per color`.

#### Step 4 — Tambah info total pax (yang tadinya bingung)
Untuk menampilkan jumlah penumpang di setiap titik (atau di tooltip):
1. **Drag `SUM(jumlah_penumpang)` ke Tooltip** di Marks card → muncul saat hover.
2. **(Opsional)** Buat sheet pendamping bar chart:
   - Worksheet baru `Bab5_WS3b_TotalPaxPerNegara`.
   - `Negara Asing` di Rows, `SUM(jumlah_penumpang)` di Columns.
   - Sort descending, filter sama (INT + top 14).
   - Drag ke dashboard di samping scatter WS3 supaya pembaca lihat slope+total bersamaan.

### Validasi: 14 negara yang harus muncul (dari Python)
| Rank | Negara | Total Pax (juta) | R² |
|---:|---|---:|---:|
| 1 | MALAYSIA | 20,5 | 0,50 |
| 2 | SINGAPURA | 18,9 | 0,46 |
| 3 | AUSTRALIA | 7,9 | 0,48 |
| 4 | ARAB SAUDI | 3,9 | 0,25 |
| 5 | QATAR | 3,8 | 0,51 |
| 6 | CHINA | 3,4 | 0,48 |
| 7 | UNI EMIRAT ARAB | 3,2 | 0,47 |
| 8 | HONG KONG | 2,5 | 0,40 |
| 9 | KOREA SELATAN | 2,2 | 0,45 |
| 10 | JEPANG | 2,2 | 0,33 |
| 11 | TAIWAN | 1,9 | 0,40 |
| 12 | THAILAND | 1,5 | 0,51 |
| 13 | TURKI | 1,3 | 0,41 |
| 14 | **FILIPINA** | **1,2** | **0,53** |

Setelah Step 1-3 di atas, **Filipina** akan muncul di legend, dan ke-14 negara akan match dengan Python.

### Catatan data quality
Beberapa entry di `dim_bandara.negara` masih berupa kode 2-huruf ISO (EG=Egypt, ET=Ethiopia, FJ=Fiji, RU=Russia, dll) karena library `airportsdata` default-nya kode ISO. Negara-negara ini volume-nya kecil, tidak masuk top 14, jadi tidak mempengaruhi headline. Kalau muncul di chart, kamu bisa filter manual exclude mereka.
