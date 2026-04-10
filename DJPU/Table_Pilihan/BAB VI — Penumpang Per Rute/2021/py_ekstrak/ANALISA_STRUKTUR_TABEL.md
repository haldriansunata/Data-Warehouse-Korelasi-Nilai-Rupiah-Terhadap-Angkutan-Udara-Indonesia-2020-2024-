# Analisa Struktur Tabel - PDF Penumpang Per Rute 2021

## Ringkasan

| No | Nama File PDF | Halaman | Total Baris Data | Jumlah Kolom |
|----|---------------|---------|------------------|--------------|
| 1 | JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI JAN-DES 2021.pdf | 7 | 361 (360 routes + 1 Total) | 17 |
| 2 | JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI BULAN JANUARI S.D DESEMBER TAHUN 2021.pdf | 3 | 147 (146 routes + 1 Total) | 17 |
| 3 | STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2021 BERDASARKAN URUTAN JUMLAH PENUMPANG.pdf | 9 | 379 (378 routes + 1 Total) | 8 |
| 4 | STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI TAHUN 2021 BERDASARKAN URUTAN JUMLAH PENUMPANG.pdf | 3 | 147 (146 routes + 1 Total) | 8 |

---

## Detail Per File PDF

### 1. DALAM NEGERI - Bulanan (Jan-Des 2021)

**File:** `JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI JAN-DES 2021.pdf`

- **Halaman:** 7
- **Baris per halaman:** 1-6: 60 baris, 7: 19 baris + 1 Total
- **Header kolom (17):** `NO`, `RUTE ( PP)`, `Jan-21`, `Feb-21`, `Mar-21`, `Apr-21`, `Mei-21`, `Jun-21`, `Jul-21`, `Agu-21`, `Sep-21`, `Okt-21`, `Nov-21`, `Des-21`, `TOTAL 2021`, `TOTAL 2020`, `TOTAL 2019`
- **Multi-line headers:** Tidak ada
- **Header berulang:** Ya, sama persis di setiap halaman
- **Nomor urut:** Berlanjut antar halaman (1-378)

**Sample data (3 baris pertama):**
```
1  Jakarta (CGK) - Denpasar (DPS)      107.991  76.081  129.566  ...  2.002.789  1.549.163  4.384.437
2  Jakarta (CGK) - Makassar (UPG)      132.428  117.623 158.762  ...  1.750.282  1.579.052  2.886.112
3  Jakarta (CGK) - Medan (KNO)         167.440  110.650 138.147  ...  1.735.789  1.544.801  2.646.246
```

**Sample data (3 baris terakhir):**
```
377  Solo (SOC) - Balikpapan (BPN)      -  -  -  ...  -  -  352
378  Bandar Lampung (TKG) - Bengkulu (BKS)  -  -  -  ...  -  4.529  16.198
Total  (route=None)                     2.570.979  2.118.600  ...  33.336.639  34.263.751  73.790.516
```

---

### 2. LUAR NEGERI - Bulanan (Jan-Des 2021)

**File:** `JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI BULAN JANUARI S.D DESEMBER TAHUN 2021.pdf`

- **Halaman:** 3
- **Baris per halaman:** 1-2: 52 baris, 3: 42 baris + 1 Total
- **Header kolom (17):** `NO`, `RUTE`, `Jan-21`, `Feb-21`, `Mar-21`, `Apr-21`, `Mei-21`, `Jun-21`, `Jul-21`, `Agu-21`, `Sep-21`, `Okt-21`, `Nov-21`, `Des-21`, `TOTAL 2021`, `TOTAL 2020`, `TOTAL 2019`
- **Multi-line headers:** Tidak ada
- **Header berulang:** Ya, sama persis di setiap halaman
- **Nomor urut:** Berlanjut antar halaman (1-145)

**Catatan:** Kolom rute bernama `RUTE` (bukan `RUTE ( PP)`) karena rute internasional satu arah.

**Sample data (3 baris pertama):**
```
1  Jakarta (CGK) - Singapura (SIN)   7.734  7.238  10.246  ...  199.358  618.117  4.077.673
2  Jakarta (CGK) - Doha (DOH)        9.923  10.021 11.620  ...  194.624  129.366  400.515
3  Jakarta (CGK) - Dubai (DXB)       11.400 9.138  10.688  ...  173.989  153.952  459.159
```

**Sample data (3 baris terakhir):**
```
144  Semarang (SRG) - Haikou (HAK)          -  -  -  ...  -  -  -
145  Bandar Lampung (TKG) - Kuala Lumpur (KUL)  -  -  -  ...  -  -  -
Total  (route=None)                          93.297  73.959  ...  1.362.755  7.002.158  35.683.914
```

---

### 3. DALAM NEGERI - Statistik (Urut Jumlah Penumpang)

**File:** `STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2021 BERDASARKAN URUTAN JUMLAH PENUMPANG.pdf`

- **Halaman:** 9
- **Baris per halaman:** 1-8: 43 baris, 9: 35 baris + 1 Total
- **Header kolom (8):** `NO`, `RUTE ( PP)`, `JUMLAH\nPENERBANGAN`, `JUMLAH\nPENUMPANG`, `KAPASITAS\nSEAT`, `JUMLAH\nBARANG\n(Kg)`, `JUMLAH POS`, `L/F`
- **Multi-line headers:** **Ya** - header mengandung newline (`\n`)
- **Header berulang:** Ya, sama persis di setiap halaman (termasuk `\n`)
- **Nomor urut:** Berlanjut antar halaman (1-378)

**Header setelah normalisasi:**
`NO`, `RUTE ( PP)`, `JUMLAH PENERBANGAN`, `JUMLAH PENUMPANG`, `KAPASITAS SEAT`, `JUMLAH BARANG (Kg)`, `JUMLAH POS`, `L/F`

**Sample data (3 baris pertama):**
```
1  Jakarta (CGK) - Denpasar (DPS)   14.974   2.002.789   2.977.867   21.365.798   196.771   67,3%
2  Jakarta (CGK) - Makassar (UPG)   15.789   1.750.282   2.679.920   28.754.522   789.774   65,3%
3  Jakarta (CGK) - Medan (KNO)      14.397   1.735.789   2.540.826   26.521.622   335.986   68,3%
```

**Sample data (3 baris terakhir):**
```
377  Solo (SOC) - Balikpapan (BPN)       -    -    -    -    -    0,0%
378  Bandar Lampung (TKG) - Bengkulu (BKS)  -    -    -    -    -    0,0%
Total  (route=None)                       339.638  33.336.639  50.123.416  417.048.368  5.278.756  66,5%
```

---

### 4. LUAR NEGERI - Statistik (Urut Jumlah Penumpang)

**File:** `STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI TAHUN 2021 BERDASARKAN URUTAN JUMLAH PENUMPANG.pdf`

- **Halaman:** 3
- **Baris per halaman:** 1-2: 52 baris, 3: 42 baris + 1 Total
- **Header kolom (8):** `NO`, `RUTE`, `JUMLAH\nPENERBANGAN`, `JUMLAH\nPENUMPANG`, `KAPASITAS\nSEAT`, `JUMLAH\nBARANG`, `JUMLAH\nPOS`, `L/F`
- **Multi-line headers:** **Ya** - header mengandung newline (`\n`)
- **Header berulang:** Ya, sama persis di setiap halaman (termasuk `\n`)
- **Nomor urut:** Berlanjut antar halaman (1-145)

**Header setelah normalisasi:**
`NO`, `RUTE`, `JUMLAH PENERBANGAN`, `JUMLAH PENUMPANG`, `KAPASITAS SEAT`, `JUMLAH BARANG`, `JUMLAH POS`, `L/F`

**Catatan:** `JUMLAH BARANG` tanpa suffix `(Kg)` berbeda dengan versi domestik.

**Sample data (3 baris pertama):**
```
1  Jakarta (CGK) - Singapura (SIN)   6.190    199.358    960.938    77.876.539    118.699    20,7%
2  Jakarta (CGK) - Doha (DOH)        1.418    194.624    382.972    15.993.771    77.839     50,8%
3  Jakarta (CGK) - Dubai (DXB)       999      173.989    387.632    19.813.415    206.404    44,9%
```

**Sample data (3 baris terakhir):**
```
144  Semarang (SRG) - Haikou (HAK)          -    -    -    -    -    0,0%
145  Bandar Lampung (TKG) - Kuala Lumpur (KUL)  -    -    -    -    -    0,0%
Total  (route=None)                          25.854  1.362.755  5.194.806  370.483.101  3.650.276  26,2%
```

---

## Perilaku Tabel Antar Halaman

| Aspek | Keterangan |
|-------|------------|
| **Konsistensi header** | ✅ Header sama persis di semua halaman (keempat PDF) |
| **Nomor urut** | ✅ Berlanjut secara berurutan antar halaman |
| **Tabel terputus** | ✅ Tidak ada tabel yang terputus di tengah baris |
| **Duplikasi data** | ✅ Tidak ada duplikasi antar halaman |

---

## Format Data Khusus yang Perlu Dibersihkan

### 1. Angka dengan Spasi Errant
- **Masalah:** Spasi di tengah angka, contoh: `"7 6.081"` seharusnya `"76.081"`
- **Solusi:** Hapus semua spasi dalam string angka sebelum konversi ke integer

### 2. Pemisah Ribuan (Titik)
- **Format:** `"1.579.052"` → seharusnya `1579052` (integer)
- **Solusi:** Hapus titik setelah spasi errant dihapus

### 3. Desimal Koma (Load Factor)
- **Format:** `"67,3%"` → format Indonesia
- **Solusi:** Biarkan sebagai string, atau ganti `,` dengan `.` dan konversi ke float jika perlu

### 4. Nilai Kosong / Null
- **Format:** `"-"` (dash)
- **Solusi:** Konversi ke `None`/`NaN` di CSV

### 5. Multi-line Headers (PDF Statistik)
- **Masalah:** `"JUMLAH\nPENERBANGAN"` terpecah jadi 2 baris
- **Solusi:** Replace `\n` dengan space → `"JUMLAH PENERBANGAN"`

### 6. Header Berulang
- **Masalah:** Header muncul di setiap halaman
- **Solusi:** Gunakan header dari halaman pertama, skip header di halaman selanjutnya

### 7. Baris Total
- **Posisi:** Baris terakhir di setiap PDF
- **Kolom route:** `None` (kosong)
- **Solusi:** Pertahankan baris Total, biarkan kolom route kosong

---

## Perbedaan Struktur Antar File

| Aspek | JUMLAH PENUMPANG | STATISTIK |
|-------|------------------|-----------|
| **Jumlah kolom** | 17 | 8 |
| **Kolom rute** | `RUTE ( PP)` (domestik) / `RUTE` (internasional) | `RUTE ( PP)` (domestik) / `RUTE` (internasional) |
| **Multi-line headers** | Tidak | Ya |
| **Data** | Breakdown bulanan (Jan-Des) + Total per tahun | Agregat: Penerbangan, Penumpang, Kapasitas, Barang, Pos, Load Factor |

---

## Ringkasan Anomali

| No | Anomali | File Terkena | Penanganan |
|----|---------|--------------|------------|
| 1 | Spasi errant dalam angka | Semua PDF | Hapus spasi, lalu hapus titik ribuan |
| 2 | Multi-line headers | PDF STATISTIK (2 file) | Replace `\n` dengan space |
| 3 | Header berulang | Semua PDF | Skip header di halaman 2+ |
| 4 | Nilai `"-"` sebagai null | Semua PDF | Konversi ke empty/NaN |
| 5 | Baris Total dengan route None | Semua PDF | Pertahankan, biarkan route kosong |
| 6 | Load factor format koma (`67,3%`) | PDF STATISTIK (2 file) | Keep as string |
| 7 | Rute tidak aktif (semua nilai `-`) | Semua PDF | Pertahankan sebagai data valid |
