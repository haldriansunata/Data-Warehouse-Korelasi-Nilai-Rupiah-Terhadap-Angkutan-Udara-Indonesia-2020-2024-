# Upload Bukti — Bab 5 WS3 Sensitivitas Per Negara

## File yang aku butuh

1. **SS1_data_pane.png**
   Screenshot Data pane Tableau (panel kiri yang berisi field-field). Aku perlu lihat **nama exact** field hasil self-join dim_bandara. Khusus zoom ke field-field yang berkaitan dengan `negara`, `iata`, `kota` dari **kedua instance** (origin dan destination).

2. **SS2_data_source_tab.png**
   Klik tab **Data Source** di pojok kiri bawah Tableau. Screenshot relasi/join antar table — aku mau verifikasi:
   - `fact_penumpang_rute.bandara_1_id` ↔ `dim_bandara_origin.bandara_id`
   - `fact_penumpang_rute.bandara_2_id` ↔ `dim_bandara_destination.bandara_id`

3. **SS3_chart_sekarang.png**
   Screenshot worksheet `Bab5_WS3_PerNegara` apa adanya sekarang. Pastikan terlihat:
   - Columns, Rows
   - Marks card (Color, Detail, Size, dll)
   - Filters yang aktif
   - Trend line (kalau ada)
   - Legenda negara di kanan

4. **export_negara_visible.csv**
   Di worksheet WS3:
   - Klik kanan area worksheet (bukan field) → **View Data**
   - Pilih tab **Full Data**
   - Klik **Download all rows as a text file** → simpan sebagai `export_negara_visible.csv`

## Tujuan
Setelah aku lihat file-file di atas, aku akan:
- Tulis ulang calculated field `negara_asing` dengan nama field yang benar (sesuai data structure-mu)
- Pastikan filter Top 14 menghasilkan Filipina (yang kamu bilang belum muncul)
- Update tutorial WS3 supaya match data-mu
