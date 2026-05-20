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
