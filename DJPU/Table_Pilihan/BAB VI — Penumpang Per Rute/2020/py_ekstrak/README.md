# BAB VI — Penumpang Per Rute (2020)

## 📊 Deskripsi
Folder ini berisi data penumpang angkutan udara niaga berjadwal tahun 2020 untuk rute domestik dan internasional, diekstrak dari 4 file PDF dan dikonversi ke format CSV.

## 📁 File Input (PDF)
1. **JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI JAN-DES 2020.pdf**
   - 10 halaman, 411 rute domestik
   - Data bulanan (Jan-Des 2020) dengan perbandingan 2019 & 2018

2. **JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI BULAN JANUARI S.D DESEMBER TAHUN 2020.pdf**
   - 3 halaman, 158 rute internasional
   - Data bulanan (Jan-Des 2020) dengan perbandingan 2019 & 2018

3. **STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2020 BERDASARKAN URUTAN JUMLAH PENUMPANG.pdf**
   - 10 halaman, 411 rute domestik
   - Statistik agregat (jumlah penerbangan, penumpang, kapasitas, barang, pos, load factor)

4. **STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI TAHUN 2020 BERDASARKAN URUTAN JUMLAH PENUMPANG.pdf**
   - 3 halaman, 159 rute internasional
   - Statistik agregat (jumlah penerbangan, penumpang, kapasitas, barang, pos, load factor)

## 📄 File Output (CSV)
1. **JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI JAN-DES 2020.csv** - Data penumpang domestik per bulan (411 rows × 17 columns)
2. **JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI BULAN JANUARI S.D DESEMBER TAHUN 2020.csv** - Data penumpang internasional per bulan (158 rows × 17 columns)
3. **STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2020 BERDASARKAN URUTAN JUMLAH PENUMPANG.csv** - Statistik rute domestik (411 rows × 8 columns)
4. **STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI TAHUN 2020 BERDASARKAN URUTAN JUMLAH PENUMPANG.csv** - Statistik rute internasional (159 rows × 8 columns)

## 📋 Struktur Kolom CSV

### Monthly Files (domestic & international):
- `NO` - Nomor urut rute
- `RUTE (PP)` atau `RUTE` - Nama rute (PP = Pulang Pergi)
- `Jan-20` s/d `Dec-20` - Jumlah penumpang per bulan
- `TOTAL 2020` - Total penumpang tahun 2020
- `TOTAL 2019` - Total penumpang tahun 2019 (perbandingan)
- `TOTAL 2018` - Total penumpang tahun 2018 (perbandingan)

### Statistics Files (domestic & international):
- `NO` - Nomor urut rute
- `RUTE (PP)` atau `RUTE` - Nama rute
- `JUMLAH PENERBANGAN` - Total penerbangan dalam setahun
- `JUMLAH PENUMPANG` - Total penumpang dalam setahun
- `KAPASITAS SEAT` - Kapasitas tempat duduk total
- `JUMLAH BARANG (Kg)` atau `JUMLAH BARANG` - Total barang dalam kilogram
- `JUMLAH POS` - Total pos/mail dalam kilogram
- `L/F` - Load Factor (faktor muat) dalam persen

## 🔍 Analisa Detail
Lihat file **ANALISA_STRUKTUR_TABEL.md** untuk dokumentasi lengkap tentang:
- Karakteristik setiap PDF
- Struktur tabel per halaman
- Perilaku header yang repetitif
- Format angka yang tidak standar
- Solusi parsing yang diterapkan

## 🛠️ Scripts
- **analyze_pdfs.py** - Script untuk analisa struktur PDF
- **extract_to_csv.py** - Script untuk ekstraksi data ke CSV

## 📝 Catatan Penting
1. **Format Angka**: Angka dalam PDF menggunakan spasi sebagai pemisah ribuan (contoh: "2 31.865" → 231.865). Sudah dibersihkan di CSV.
2. **Data Kosong**: Ditandai dengan "-" di PDF, dikonversi menjadi empty/NaN di CSV.
3. **Encoding**: CSV menggunakan UTF-8 with BOM (utf-8-sig) untuk kompatibilitas Excel.
4. **Total Row**: Baris terakhir di beberapa file berisi agregat total semua rute.

## 📊 Ringkasan Data
| Kategori | Jumlah Rute | Periode | Kolom |
|----------|-------------|---------|-------|
| Domestik (Bulanan) | 411 | Jan-Des 2020 | 17 |
| Internasional (Bulanan) | 158 | Jan-Des 2020 | 17 |
| Domestik (Statistik) | 411 | Tahunan 2020 | 8 |
| Internasional (Statistik) | 159 | Tahunan 2020 | 8 |

## 📅 Metadata
- **Tahun Data**: 2020 (dengan perbandingan 2019 & 2018)
- **Sumber**: Badan Pusat Statistik (BPS) / Kementerian Perhubungan
- **Tanggal Ekstraksi**: April 8, 2026
- **Tools**: Python 3, pdfplumber, pandas
