# ANALISA STRUKTUR TABEL - PDF 2023

## Ringkasan

Dokumen ini berisi analisa struktur tabel dari 4 file PDF data penumpang angkutan udara niaga berjadwal tahun 2023.

---

## FILE 1: JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI JAN-DES 2023.pdf

### Statistik
- **Jumlah halaman:** 12
- **Total baris data:** ~312 (52 rute × 6 pasang halaman)
- **Struktur:** Tabel terbagi per 2 halaman (kiri: Jan-Jun, kanan: Jul-Des + Total)

### Struktur Header Kolom

**Halaman Ganjil (1, 3, 5, 7, 9, 11):**
| No | Nama Kolom | Tipe Data |
|----|-----------|-----------|
| 1 | NO | Integer (urutan) |
| 2 | RUTE ( PP) | String (kode bandara) |
| 3 | Jan-23 | Number |
| 4 | Feb-23 | Number |
| 5 | Mar-23 | Number |
| 6 | Apr-23 | Number |
| 7 | Mei-23 | Number |
| 8 | Jun-23 | Number |

**Halaman Genap (2, 4, 6, 8, 10, 12):**
| No | Nama Kolom | Tipe Data |
|----|-----------|-----------|
| 1 | Jul-23 | Number |
| 2 | Agu-23 | Number |
| 3 | Sep-23 | Number |
| 4 | Okt-23 | Number |
| 5 | Nov-23 | Number |
| 6 | Des-23 | Number |
| 7 | TOTAL 2023 | Number |

### Perilaku Tabel Antar Halaman
- ✅ **Konsisten:** Header berulang setiap 2 halaman
- ✅ **Nomor urut berlanjut:** Halaman 1 (1-52), Halaman 3 (53-104), Halaman 5 (105-156), dst
- ⚠️ **Header berulang:** Harus di-merge menjadi satu row final

### Format Data Khusus
- Angka menggunakan titik sebagai pemisah ribuan: `392.247`
- Beberapa sel kosong/`-` untuk rute yang tidak beroperasi di bulan tertentu
- Baris Total ada di akhir setiap halaman genap

### Anomali
- Beberapa rute memiliki data kosong di bulan-bulan tertentu (terutama rute baru)
- Beberapa halaman genap memiliki baris "Total" di akhir

---

## FILE 2: STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2023 BERDASARKAN URUTAN JUMLAH PENUMPANG.pdf

### Statistik
- **Jumlah halaman:** 6
- **Total baris data:** ~259 (termasuk baris Total)
- **Struktur:** Satu tabel lengkap per halaman

### Struktur Header Kolom

**Semua halaman:**
| No | Nama Kolom | Tipe Data |
|----|-----------|-----------|
| 1 | NO | Integer/String ("Total") |
| 2 | RUTE | String |
| 3 | JUMLAH PENERBANGAN | Number (multi-line header) |
| 4 | JUMLAH PENUMPANG | Number (multi-line header) |
| 5 | KAPASITAS SEAT | Number (multi-line header) |
| 6 | JUMLAH BARANG | Number (multi-line header) |
| 7 | JUMLAH POS | Number/Empty (multi-line header) |
| 8 | L/F | Percentage string |

### Perilaku Tabel Antar Halaman
- ✅ **Konsisten:** Header sama di semua halaman
- ✅ **Nomor urut berlanjut:** Halaman 1 (1-52), Halaman 2 (53-104), dst
- ⚠️ **Multi-line headers:** Perlu di-join

### Format Data Khusus
- Angka menggunakan titik sebagai pemisah ribuan
- L/F (Load Factor) dalam persentase dengan koma: `77,8%`
- Beberapa sel kosong/`-` terutama di kolom "JUMLAH POS"

### Anomali
- Multi-line headers: `JUMLAH\nPENERBANGAN`, `JUMLAH\nPENUMPANG`, dll
- Baris "Total" di halaman terakhir dengan kolom RUTE = None
- Beberapa rute memiliki data kosong (baru dimulai operasionalnya)

---

## FILE 3: JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI BULAN JANUARI S.D DESEMBER TAHUN 2023.pdf

### Statistik
- **Jumlah halaman:** 6
- **Total baris data:** ~156 rute
- **Struktur:** Tabel terbagi per 2 halaman (kiri: Jan-Jun, kanan: Jul-Des + Total)

### Struktur Header Kolom

**Halaman Ganjil (1, 3, 5):**
| No | Nama Kolom | Tipe Data |
|----|-----------|-----------|
| 1 | NO | Integer |
| 2 | RUTE ( PP) | String |
| 3 | Jan-23 | Number |
| 4 | Feb-23 | Number |
| 5 | Mar-23 | Number |
| 6 | Apr-23 | Number |
| 7 | Mei-23 | Number |
| 8 | Jun-23 | Number |

**Halaman Genap (2, 4, 6):**
| No | Nama Kolom | Tipe Data |
|----|-----------|-----------|
| 1 | Jul-23 | Number |
| 2 | Agu-23 | Number |
| 3 | Sep-23 | Number |
| 4 | Okt-23 | Number |
| 5 | Nov-23 | Number |
| 6 | Des-23 | Number |
| 7 | TOTAL 2023 | Number |

### Perilaku Tabel Antar Halaman
- ✅ **Konsisten:** Header berulang setiap 2 halaman
- ✅ **Nomor urut berlanjut**

### Format Data Khusus
- Angka menggunakan titik sebagai pemisah ribuan
- Beberapa sel kosong/`-`

### Anomali
- Halaman 6 memiliki baris kosong/`-` banyak di akhir (rute tidak beroperasi)
- Baris Total di halaman 6

---

## FILE 4: STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI TAHUN 2023 BERDASARKAN URUTAN JUMLAH PENUMPANG.pdf

### Statistik
- **Jumlah halaman:** 3
- **Total baris data:** 125 rute + 1 Total
- **Struktur:** Satu tabel lengkap per halaman

### Struktur Header Kolom

**Semua halaman:**
| No | Nama Kolom | Tipe Data |
|----|-----------|-----------|
| 1 | NO | Integer/String ("Total") |
| 2 | RUTE | String |
| 3 | JUMLAH PENERBANGAN | Number (multi-line) |
| 4 | JUMLAH PENUMPANG | Number (multi-line) |
| 5 | KAPASITAS SEAT | Number (multi-line) |
| 6 | JUMLAH BARANG | Number (multi-line) |
| 7 | JUMLAH POS | Number/Empty (multi-line) |
| 8 | L/F | Percentage string |

### Perilaku Tabel Antar Halaman
- ✅ **Konsisten:** Header sama di semua halaman
- ✅ **Nomor urut berlanjut:** Halaman 1 (1-54), Halaman 2 (55-108), Halaman 3 (109-125 + Total)

### Format Data Khusus
- Angka menggunakan titik sebagai pemisah ribuan
- **SPASI ANEH dalam angka:** `3 .005.022`, `5 3.653.573`, `1 18.794`
- L/F dalam persentase dengan koma: `77,8%`
- Banyak sel kosong/`-` di kolom "JUMLAH POS"

### Anomali
- **Multi-line headers:** Sama seperti File 2
- **Spasi tidak standar dalam angka:** Harus dibersihkan
- Baris "Total" di halaman 3 dengan kolom RUTE = None
- Banyak rute dengan data kosong (tidak beroperasi)

---

## RINGKASAN ANOMALI & SOLUSI

| Anomali | File | Solusi |
|---------|------|--------|
| Header berulang di setiap halaman | 1, 3 | Skip header di halaman genap, merge kolom |
| Multi-line headers | 2, 4 | Join dengan space: `\n` → ` ` |
| Spasi aneh dalam angka | 4 | Hapus semua spasi, lalu parse |
| Titik pemisah ribuan | Semua | Hapus titik, konversi ke int |
| Sel kosong/`-` | Semua | Konversi ke None/NaN |
| Baris Total | Semua | Pertahankan, biarkan route kosong |
| Nomor urut berlanjut | Semua | Concat tanpa reset |

---

**Tanggal Analisa:** April 2026
**Analis:** AI Data Engineer
