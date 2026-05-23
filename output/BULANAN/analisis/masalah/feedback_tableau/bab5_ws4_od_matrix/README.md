# Upload Bukti — Bab 5 WS4 OD Matrix

## File yang aku butuh

1. **export_top10_origin.csv**
   Cara dapat:
   - Buat sheet kosong baru di Tableau (jangan rusak WS4 yang sudah ada).
   - Drag `o_iata` ke Rows.
   - Drag `jumlah_penumpang` ke Columns (pil SUM).
   - Sort descending by SUM.
   - Klik kanan area sheet → **View Data → Full Data → Download** → simpan sebagai `export_top10_origin.csv`.

2. **export_top10_destination.csv**
   Sama persis dengan langkah di atas, tapi pakai `d_iata` di Rows.

3. **SS_od_matrix_sekarang.png**
   Screenshot worksheet `Bab5_WS4_ODMatrix` apa adanya sekarang. Termasuk Marks card, Filters, Columns, Rows, dan legenda yang ada.

## Tujuan
Setelah aku lihat 3 file di atas, aku akan:
- Bandingkan top 10 origin vs top 10 destination di Tableau-mu dengan output Python (`od_matrix.csv`).
- Tentukan apakah perlu pakai **union filter** (gabung top 10 origin + top 10 destination jadi 1 daftar) atau hard-code list IATA.
- Update tutorial WS4 supaya hasilnya bisa konsisten.

## Catatan
List IATA origin **memang akan berbeda** dengan destination karena ETL `dim_rute` menormalisasi pasangan secara alfabetis (`bandara_1_id` = yang alfabet lebih awal). Jadi ini bukan bug — tapi solusinya perlu disesuaikan.
