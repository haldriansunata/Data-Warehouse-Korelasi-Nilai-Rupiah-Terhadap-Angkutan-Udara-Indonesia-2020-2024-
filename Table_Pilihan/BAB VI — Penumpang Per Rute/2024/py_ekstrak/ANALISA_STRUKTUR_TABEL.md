# ANALISA STRUKTUR TABEL

## Ringkasan

| No | Nama File | Halaman | Total Baris Data | Kolom |
|----|-----------|---------|------------------|-------|
| 1 | JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI JAN-DES 2024.pdf | 6 | 318 (271 routes + TOTAL row + headers) | 15 |
| 2 | STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2024 BERDASARKAN URUTAN JUMLAH PENUMPANG.pdf | 6 | 308 (307 routes + TOTAL row) | 8 |
| 3 | JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI BULAN JANUARI S.D DESEMBER TAHUN 2024.pdf | 3 | 104 (103 routes + TOTAL row) | 15 |
| 4 | STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI TAHUN 2024 BERDASARKAN URUTAN JUMLAH PENUMPANG.pdf | 3 | 124 (123 routes + TOTAL row) | 8 |

---

## File 1: JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI JAN-DES 2024.pdf

### Struktur Header (Konsisten di semua halaman)
```
['NO', 'RUTE PP', 'Jan-24', 'Feb-24', 'Mar-24', 'Apr-24', 'May-24', 'Jun-24', 
 'Jul-24', 'Aug-24', 'Sep-24', 'Oct-24', 'Nov-24', 'Dec-24', 'TOTAL 2024']
```

### Detail Per Halaman
| Halaman | Baris | Nomor Urut | Keterangan |
|---------|-------|------------|------------|
| 1 | 52 | Header + 1-51 | Header hanya di halaman 1 |
| 2 | 55 | 52-106 | Data berlanjut, no header |
| 3 | 55 | 107-161 | Data berlanjut, no header |
| 4 | 55 | 162-216 | Data berlanjut, no header |
| 5 | 55 | 217-271 | Data berlanjut, no header |
| 6 | 44 | 272-274 + TOTAL | Data berakhir + baris TOTAL |

### Perilaku Tabel
- ✅ **Konsisten**: Header hanya muncul di halaman 1
- ✅ **Kontinu**: Nomor urut berlanjut antar halaman (1→271)
- ✅ **Tidak ada merged cells**
- ✅ **Baris TOTAL** ada di halaman terakhir

### Format Data Khusus
- **Angka**: Menggunakan titik sebagai pemisah ribuan (contoh: `380.993`)
- **Null values**: Ada nilai `0` dan beberapa `None` di kolom RUTE PP pada baris TOTAL
- **No anomali spasi** pada angka

---

## File 2: STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2024 BERDASARKAN URUTAN JUMLAH PENUMPANG.pdf

### Struktur Header (Multi-line)
```
['NO', 'RUTE PP', 'JUMLAH\nPENERBANGAN', 'JUMLAH\nPENUMPANG', 
 'KAPASITAS\nSEAT', 'JUMLAH\nBARANG KG', 'JUMLAH\nPOS KG', 'LF %']
```

### Detail Per Halaman
| Halaman | Baris | Nomor Urut | Keterangan |
|---------|-------|------------|------------|
| 1 | 57 | Header + 1-56 | Header dengan multi-line |
| 2 | 62 | 57-118 | Data berlanjut, no header |
| 3 | 62 | 119-180 | Data berlanjut, no header |
| 4 | 62 | 181-242 | Data berlanjut, no header |
| 5 | 62 | 243-304 | Data berlanjut, no header |
| 6 | 12 | 305-307 + TOTAL | Data berakhir + baris TOTAL |

### Perilaku Tabel
- ✅ **Konsisten**: Header hanya di halaman 1
- ✅ **Kontinu**: Nomor urut berlanjut (1→307)
- ⚠️ **Multi-line headers**: Perlu dijoin (contoh: `JUMLAH\nPENERBANGAN` → `JUMLAH PENERBANGAN`)
- ✅ **Baris TOTAL** ada di halaman terakhir

### Format Data Khusus
- **Angka**: Titik sebagai pemisah ribuan (contoh: `4.722.720`)
- **Persentase**: Format `87%` di kolom LF
- **Null values**: Beberapa kolom `0` dan `None` di baris TOTAL

---

## File 3: JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI BULAN JANUARI S.D DESEMBER TAHUN 2024.pdf

### Struktur Header (Konsisten)
```
['NO', 'RUTE PP', 'Jan-24', 'Feb-24', 'Mar-24', 'Apr-24', 'May-24', 'Jun-24', 
 'Jul-24', 'Aug-24', 'Sep-24', 'Oct-24', 'Nov-24', 'Dec-24', 'TOTAL 2024']
```

### Detail Per Halaman
| Halaman | Baris | Nomor Urut | Keterangan |
|---------|-------|------------|------------|
| 1 | 49 | Header + 1-48 | Header hanya di halaman 1 |
| 2 | 52 | 49-100 | Data berlanjut, no header |
| 3 | 35 | 101-103 + TOTAL | Data berakhir + baris TOTAL |

### Perilaku Tabel
- ✅ **Konsisten**: Header hanya di halaman 1
- ✅ **Kontinu**: Nomor urut berlanjut (1→103)
- ⚠️ **Typo di TOTAL**: Baris TOTAL tertulis `'OTAL'` (huruf T hilang)
- ✅ **Tidak ada merged cells**

### Format Data Khusus
- **Angka**: Titik sebagai pemisah ribuan
- **Null values**: Beberapa nilai `0` dan `None` di baris TOTAL
- **Angka kecil**: Ada format tanpa titik (contoh: `947`, `892`)

---

## File 4: STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI TAHUN 2024 BERDASARKAN URUTAN JUMLAH PENUMPANG.pdf

### Struktur Header (Multi-line)
```
['NO', 'RUTE PP', 'JUMLAH\nPENERBANGAN', 'JUMLAH\nPENUMPANG', 
 'KAPASITAS\nSEAT', 'JUMLAH\nBARANG KG', 'JUMLAH\nPOS KG', 'LF %']
```

### Detail Per Halaman
| Halaman | Baris | Nomor Urut | Keterangan |
|---------|-------|------------|------------|
| 1 | 58 | Header + 1-57 | Header dengan multi-line |
| 2 | 63 | 58-120 | Data berlanjut, no header |
| 3 | 15 | 121-123 + TOTAL | Data berakhir + baris TOTAL |

### Perilaku Tabel
- ✅ **Konsisten**: Header hanya di halaman 1
- ✅ **Kontinu**: Nomor urut berlanjut (1→123)
- ⚠️ **Multi-line headers**: Perlu dijoin
- ⚠️ **Typo kecil**: `'DEL-DPS\\'` ada backslash di route
- ✅ **Baris TOTAL** ada di halaman terakhir

### Format Data Khusus
- **Angka**: Titik sebagai pemisah ribuan
- **Persentase**: Format `82%`, `86%`, dll di kolom LF
- **Null values**: Beberapa `0` dan `None` di baris TOTAL

---

## Kesimpulan Umum

### Pola Konsisten
1. ✅ Semua PDF **tidak mengulang header** di setiap halaman (hanya halaman 1)
2. ✅ Nomor urut **berlanjut antar halaman**
3. ✅ Semua memiliki **baris TOTAL** di halaman terakhir
4. ✅ Format angka menggunakan **titik sebagai pemisah ribuan**

### Anomali yang Ditemukan
1. ⚠️ **Multi-line headers** pada file Statistik (File 2 & 4)
   - Solusi: Join dengan space
2. ⚠️ **Typo 'OTAL'** pada File 3 (baris TOTAL)
   - Solusi: Replace ke 'TOTAL'
3. ⚠️ **Backslash di route** `'DEL-DPS\\'` pada File 4
   - Solusi: Strip backslash
4. ⚠️ **None values** di kolom RUTE PP untuk baris TOTAL
   - Solusi: Biarkan kosong/NaN

### Data Cleaning yang Diperlukan
1. **Header normalization**: Join multi-line headers
2. **Number cleaning**: Hapus titik ribuan → integer
3. **Percentage handling**: Keep string dengan `%`
4. **Typo correction**: Fix 'OTAL' → 'TOTAL'
5. **Whitespace trim**: Hapus whitespace berlebih
6. **Null handling**: Konversi `None` → NaN/empty
