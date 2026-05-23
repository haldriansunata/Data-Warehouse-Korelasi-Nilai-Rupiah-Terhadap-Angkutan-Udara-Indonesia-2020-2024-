# Bab 1 / WS3 — Inflasi YoY & MtM + COVID Phase Background

## Tujuan
Menampilkan rezim inflasi yang berbeda di setiap fase COVID, mempersiapkan argumen Bab 4 bahwa **COVID adalah confounder** yang harus dikontrol.

## Pendekatan
**Dual-axis line chart** untuk dua jenis inflasi:
- **Inflasi YoY** (year-on-year): inflasi tahun-ke-tahun, sumbu kiri.
- **Inflasi MtM** (month-to-month): inflasi bulan-ke-bulan, sumbu kanan.

Background di-shade dengan warna per `covid_phase` untuk membantu audience mengaitkan rezim inflasi dengan rezim COVID.

## Perhitungan
Inflasi sudah dalam **persen (%)**, tidak perlu konversi:
- YoY: tingkat harga umum tahun ini vs tahun lalu (kira-kira berapa % barang lebih mahal dari tahun lalu).
- MtM: perubahan dari bulan sebelumnya (bisa negatif = deflasi).

```python
# Rata-rata inflasi per fase COVID
phase_avg = df.groupby("covid_phase")["inflasi_yoy"].mean()
```

## Hasil dari Data Kamu

| COVID Phase | n bulan | Inflasi YoY rata-rata | Inflasi MtM rata-rata | BI rate rata-rata |
|---|---:|---:|---:|---:|
| pre_pandemic | 2 | 2,83% | 0,34% | 4,88% |
| lockdown | 19 | **1,70%** | 0,10% | **3,84%** |
| transisi | 15 | **3,72%** | 0,43% | 3,90% |
| recovery | 24 | 2,99% | 0,17% | **5,96%** |

## Makna Angka
Empat rezim berbeda:
1. **Lockdown (Mar 2020–Sep 2021)**: inflasi tertekan (1,70%) karena demand collapse. BI rate diturunkan ke 3,84% — kebijakan moneter longgar untuk stimulus.
2. **Transisi (Okt 2021–Des 2022)**: lonjakan inflasi (3,72%) karena reopening + shock minyak Russia-Ukraine (Feb 2022). BI baru mulai naik.
3. **Recovery (Jan 2023–Des 2024)**: inflasi normalize ke 3%, tapi **BI rate ditahan tinggi (5,96%)** untuk menjaga rupiah.
4. **Pre-pandemic**: hanya 2 bulan, tidak cukup untuk regresi terpisah → biasanya digabung ke lockdown.

## Insight untuk Topik
**Inflasi dan COVID phase berkorelasi**. Kalau di Bab 2 kita menemukan kurs–penumpang ber-korelasi negatif, kita tidak bisa langsung simpulkan "kurs penyebab" — bisa juga "COVID phase yang menyebabkan keduanya". Inilah yang dimaksud *confounder*.

Solusi di Bab 4: regresi/scatter **per fase COVID** untuk memastikan slope bertahan.

## Output
- `plot.png` — dual-axis line dengan background COVID
- `phase_summary.csv` — rata-rata indikator per fase

## Target Tableau — Step by Step

### Langkah Pembuatan Sheet
1. **Buat worksheet baru**, beri nama `Bab1_WS3_InflasiCOVID`.
2. **Drag `Tanggal Analisis` ke Columns** → Month (Continuous).
3. **Drag `AVG(inflasi_yoy)` ke Rows**. Marks = Line, warna merah.
4. **Drag `AVG(inflasi_mtm)` ke Rows** di sebelahnya. Marks = Line, warna biru.
5. **Buat dual axis**: klik kanan pil `AVG(inflasi_mtm)` → **Dual Axis**.
6. **JANGAN Synchronize Axis** (range YoY 1–6% vs MtM −0,21–1,17% sangat berbeda).
7. **Tambah background COVID phase** (pakai Reference Bands):
   - Buka tab **Analytics** (panel kiri atas, sebelah Data).
   - Drag **Reference Band** ke chart, lepaskan di "Pane" untuk sumbu X.
   - Set:
     - *Band From*: nilai minimum `waktu_id`
     - *Band To*: nilai maximum `waktu_id`
     - *Label*: dari `covid_phase`
     - *Fill*: warna per fase (atur manual)
   - Alternatif lebih mudah: buat 4 reference bands manual, masing-masing untuk 1 fase, dengan tanggal start/end yang sudah diketahui:
     - pre_pandemic: 01-Jan-2020 sampai 29-Feb-2020 (biru)
     - lockdown: 01-Mar-2020 sampai 30-Sep-2021 (merah)
     - transisi: 01-Oct-2021 sampai 31-Dec-2022 (oranye)
     - recovery: 01-Jan-2023 sampai 31-Dec-2024 (hijau)
   - Set Fill opacity ~20% supaya line tetap terlihat di atasnya.
8. **Label sumbu kanan**: pastikan sumbu kanan adalah MtM, kiri YoY. Tambah judul sumbu via klik kanan sumbu → Edit Axis → Title.

### Cross-check ke Python
- Inflasi YoY mean per fase: lockdown=1,70%, transisi=3,72%, recovery=2,99%.
- Lihat `phase_summary.csv` untuk angka penuh — Tableau harus tunjukkan rata-rata yang sama kalau di-hover atau di-bar per phase.

### Catatan Khusus
- Reference Band di Tableau punya keterbatasan untuk membuat background shaded yang berubah-ubah per dimensi. Workaround alternatif: pakai **Dual Axis dengan Bar Chart**:
  - Buat field konstan = 1, drag ke Rows sebagai bar.
  - Color = `covid_phase`, opacity 20%, di-link sebagai axis kedua di belakang line YoY/MtM.
  - Hide sumbu Y bar tersebut.

---

## ⚙️ Update — Catatan Implementasi Tableau (Konfirmasi)

Solusi AI yang kamu pakai (dari `gabisa.txt`) untuk 4 **Reference Band** manual (pre_pandemic/lockdown/transisi/recovery) dengan tanggal:
- Fase 1 (pre_pandemic): `01-Jan-2020` – `29-Feb-2020`, biru, opacity 20%
- Fase 2 (lockdown): `01-Mar-2020` – `30-Sep-2021`, merah
- Fase 3 (transisi): `01-Oct-2021` – `31-Dec-2022`, oranye
- Fase 4 (recovery): `01-Jan-2023` – `31-Dec-2024`, hijau

**Sudah BENAR**. Tanggal-tanggal ini match dengan fungsi `covid_phase()` di `etl_bulanan/build_makro_warehouse.py`:
```python
if wid <= 202002: return 'pre_pandemic'   # ≤ Feb 2020
if wid <= 202109: return 'lockdown'        # ≤ Sep 2021
if wid <= 202212: return 'transisi'        # ≤ Dec 2022
return 'recovery'                          # 2023+
```
Tidak perlu diubah.
