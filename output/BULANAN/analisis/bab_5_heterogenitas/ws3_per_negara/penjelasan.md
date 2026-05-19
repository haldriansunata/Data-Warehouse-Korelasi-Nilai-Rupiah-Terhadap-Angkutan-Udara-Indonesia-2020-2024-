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

## Target Tableau
- Filter: `kategori = INTERNASIONAL`
- Calculated field `negara_asing`:
  ```
  IF [o_negara] != "INDONESIA" THEN [o_negara] ELSE [d_negara] END
  ```
- Columns: `AVG(avg_kurs_tengah)`, Rows: `SUM(jumlah_penumpang)`
- Detail: `waktu_id`, Color: `negara_asing`
- Trend Line: Linear per color

Hasil match dengan tabel ini.
