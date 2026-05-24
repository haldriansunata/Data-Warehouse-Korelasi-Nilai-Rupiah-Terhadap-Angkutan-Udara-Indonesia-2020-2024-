# Analisis Data Warehouse Bulanan — Korelasi Rupiah × Angkutan Udara Indonesia

> **Tujuan folder ini**: menjalankan **seluruh analisis 5 bab × ~5 WS** dengan Python (pandas + scipy + matplotlib) untuk menghasilkan *benchmark numerik & visual* yang harus match dengan worksheet Tableau yang akan kamu buat nanti.
>
> **Cara pakai**: tiap subfolder `bab_X/wsY/` punya `analysis.py` (kode), `plot.png` (visual), `metrics.txt`/`.csv` (angka), dan `penjelasan.md` (teori + interpretasi).

---

## Struktur Folder

```
analisis/
├── README.md                     (file ini)
├── _utils.py                     (helper bersama: load_data, regresi, dll)
│
├── data_profiling/
│   ├── explore.py                (script profil tiap kolom)
│   ├── profil_raw_stats.txt      (output mentah explore.py)
│   └── data_profiling.md         (skema lengkap + lineage ETL + caveat data)
│
├── bab_1_konteks/                (Anggota 1 — Lanskap)
│   ├── ws1_multi_panel/          (4-panel time series)
│   ├── ws2_kurs_band/            (kurs + min/max band)
│   ├── ws3_inflasi_covid/        (dual axis inflasi)
│   └── ws4_seasonal_heatmap/     (heatmap tahun × bulan)
│
├── bab_2_hipotesis/              (Anggota 2 — Hipotesis Utama)
│   ├── ws1_scatter_total/        (kurs × total pax)
│   ├── ws2_scatter_int/          (filter INT)
│   ├── ws3_scatter_dom/          (filter DOM)
│   └── ws4_lag_analysis/         (lag 0-6 bulan)
│
├── bab_3_mekanisme/              (Anggota 3 — Channel Transmisi)
│   ├── ws1_kurs_brent_idr/       (Channel 1A: kurs × Brent IDR)
│   ├── ws2_brent_idr_tarif/      (Channel 1B: Brent IDR × tarif tiket)
│   ├── ws3_tarif_pax/            (Channel 1C: tarif × pax)
│   ├── ws4_kurs_birate/          (Channel 2: kurs × BI rate)
│   └── ws5_kurs_inflasi/         (Channel 3: kurs × inflasi)
│
├── bab_4_robustness/             (Anggota 4 — Kontrol Confounder)
│   ├── ws1_facet_covid/          (scatter per covid_phase)
│   ├── ws2_volatilitas/          (spread kurs × pax)
│   ├── ws3_lebaran/              (efek Lebaran)
│   ├── ws4_natal/                (efek Natal)
│   ├── ws5_hari_libur/           (kontrol kontinyu)
│   └── ws6_peak_season_interaction/  (peak × kurs)
│
└── bab_5_heterogenitas/          (Anggota 5 — Geografi & Per-Rute)
    ├── ws1_top_rute/             (top 15 rute)
    ├── ws2_sensitivitas_int/     (slope per rute INT)
    ├── ws3_per_negara/           (slope per negara destinasi)
    ├── ws4_od_matrix/            (OD heatmap)
    └── ws5_provinsi/             (top 15 provinsi)
```

---

## Findings Inti (Ringkasan Eksekutif)

### 1. **Brent terkonfirmasi dalam USD/bbl, bukan IDR** (range 26-115 USD)
Untuk channel cost-push, hitung calculated field `Brent IDR = brent_usd_bbl × avg_kurs_tengah`. Lihat `bab_3_mekanisme/ws1_kurs_brent_idr/penjelasan.md`.

### 2. **Korelasi naive kurs–penumpang SLOPE POSITIF (bukan negatif)**

| Sheet | R² | Slope |
|---|---:|---:|
| Total (Bab 2 WS1) | 0,35 | **+2.294 pax/IDR** |
| Internasional (WS2) | **0,49** | +1.176 |
| Domestik (WS3) | 0,23 | +1.119 |

**Ini spurious** karena confounder COVID, bukan konfirmasi hipotesis "kurs ↑ → demand ↓". Detail di `bab_2_hipotesis/ws1_scatter_total/penjelasan.md`.

### 3. **Setelah kontrol COVID phase, slope di lockdown menjadi NEGATIF**

| Phase | n | Slope | R² | p |
|---|---:|---:|---:|---:|
| pre_pandemic | 2 | — | — | — |
| **lockdown** | 19 | **−318** | 0,01 | 0,65 |
| transisi | 15 | +1.555 | 0,58 | 0,001 |
| recovery | 24 | +706 | 0,18 | 0,04 |

**Hanya lockdown phase yang slope-nya konsisten dengan teori** (negatif), tapi tidak signifikan. Detail di `bab_4_robustness/ws1_facet_covid/penjelasan.md`.

### 4. **Channel transmisi terkuat: Moneter (Kurs → BI Rate)**

| Channel | R² | Status |
|---|---:|---|
| 1: Cost-push (kurs→brent_idr→tarif→pax) | 0,12 → 0,35 → 0,71* | Step C spurious COVID |
| **2: Moneter (kurs → BI rate)** | **0,65** | **Slope POSITIF sesuai teori** |
| 3: Daya beli (kurs → inflasi YoY) | 0,07 | Tidak signifikan |

Detail per channel di `bab_3_mekanisme/`.

### 5. **Heterogenitas per negara — ASEAN paling sensitif**

| Negara | Slope | R² | Total Pax |
|---|---:|---:|---:|
| **MALAYSIA** | +342 | 0,50 | 20,5M |
| **SINGAPURA** | +278 | 0,46 | 18,9M |
| AUSTRALIA | +123 | 0,48 | 7,9M |
| ARAB SAUDI | +45 | 0,25 (rendah!) | 3,9M |
| JEPANG | +24 | 0,33 (rendah!) | 2,2M |

Rute ke Arab Saudi & Jepang R² rendah → driver lain (haji, visa). Detail di `bab_5_heterogenitas/ws3_per_negara/penjelasan.md`.

### 6. **Sensitivitas berbeda peak vs non-peak season**

R² peak season **2,2× lebih tinggi** (0,55 vs 0,24). Detail di `bab_4_robustness/ws6_peak_season_interaction/penjelasan.md`.

---

## Bagaimana Pakai Output Ini

### Saat membuat Tableau worksheet:
1. Baca `penjelasan.md` WS yang relevan → pahami pendekatan + makna angka.
2. Buat sheet di Tableau persis seperti instruksi "Target Tableau" di tiap penjelasan.
3. **Cross-check**: angka R², slope, p-value di Tableau harus **MATCH** dengan `metrics.txt`/`.csv` di Python. Kalau tidak match → ada masalah di join atau aggregation (lihat catatan agregasi di bawah).

### Untuk presentasi:
- PNG di setiap WS langsung bisa di-screenshot ke slide.
- Tabel R²/slope di `penjelasan.md` bisa di-copy ke caption slide.
- "Pesan utama" di akhir tiap `penjelasan.md` adalah satu kalimat tag-line yang bisa langsung diucapkan.

---

## Catatan Agregasi (Wajib di Tableau)

Setelah physical join, **measure makro ter-replikasi**. Default aggregation harus:

| Field | Default Agg |
|---|---|
| `jumlah_penumpang` | **SUM** |
| `avg_kurs_*`, `min/max_kurs`, `bi_rate`, `inflasi_*`, `tarif_tiket_ihk`, `brent_*` | **AVG** |
| `jumlah_hari_libur`, `jumlah_hari_trading` | AVG |

Setting: klik kanan tiap measure di Data pane → Default Properties → Aggregation → Average.

**Mismatch utama yang muncul tanpa ini**: chart kamu akan tampak angka 100-1000× lebih besar dari Python karena Tableau SUM 553 baris yang sama.

---

## Cara Re-run Semua Analisis

```bash
cd D:\Kuliah\projek_dw
# Single WS:
python output/BULANAN/analisis/bab_2_hipotesis/ws1_scatter_total/analysis.py

# Semua (bash loop):
for f in output/BULANAN/analisis/bab_*/ws*/analysis.py; do python "$f"; done
```

**Dependency**: `pandas`, `numpy`, `matplotlib`, `scipy` (sudah installed). Set `PYTHONIOENCODING=utf-8` di Windows untuk emoji/karakter Indonesia.

---

## Pesan Penting untuk Paper

Setelah seluruh analisis ini, **finding utama yang harus disampaikan**:

1. **Naive correlation menyesatkan** — slope positif di Bab 2 adalah artefak COVID, bukan konfirmasi teori.
2. **Channel transmisi yang aktif**: respons moneter BI Rate (R²=0,65) dan pass-through biaya bahan bakar (Brent IDR sebagai proxy upstream avtur) ke tarif (R²=0,35). Channel inflasi tidak signifikan.
3. **Heterogenitas geografis**: rute ASEAN paling sensitif, rute Arab/Jepang punya driver non-kurs.
4. **Caveat scientific**: dengan data 60 bulan dan structural break COVID, tidak ada satu fase pun (kecuali lockdown dengan n=19) yang menunjukkan slope kurs–pax negatif signifikan. Honest reporting > over-claim.

Paper kelompok kamu akan **lebih kuat secara akademik** dengan honest reporting ini daripada hanya melapor R² naive yang tampak meyakinkan.
