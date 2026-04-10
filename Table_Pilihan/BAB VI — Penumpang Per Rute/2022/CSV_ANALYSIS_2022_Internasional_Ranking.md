# CSV Analysis: Statistik Per Rute — Internasional Ranking 2022

## 📊 Informasi Umum

| Properti | Nilai |
|----------|-------|
| **Nama File** | `STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI TAHUN 2022 BERDASARKAN URUTAN JUMLAH PENUMPANG.csv` |
| **Jumlah Baris** | 136 (1 header + 133 rute + 1 Total + 1 empty) |
| **Jumlah Kolom** | 8 |
| **Format Rute** | Hanya IATA code |
| **Format Angka** | Float dengan titik sebagai pemisah ribuan |

---

## ⚠️ PERBEDAAN SANGAT SIGNIFIKAN vs 2020-2021

| Aspek | 2020-2021 | **2022** |
|-------|-----------|----------|
| **Format Rute** | Nama + IATA | **Hanya IATA** ⚠️ |
| **Format Angka** | Float (.0) | **Titik = ribuan** ⚠️ |
| **Jumlah Rute** | ~147 | **133** |

---

## 🗂️ Struktur Tabel

```
NO (float)
RUTE (string - IATA only)
JUMLAH PENERBANGAN (float - titik = ribuan)
JUMLAH PENUMPANG (float - titik = ribuan)
KAPASITAS SEAT (float - titik = ribuan)
JUMLAH BARANG (float - titik = ribuan)
JUMLAH POS (float - titik = ribuan)
L/F (string - "XX,X%")
```

### Top Routes 2022

| Rank | Rute | Penumpang | Penerbangan | LF |
|------|------|-----------|-------------|-----|
| 1 | CGK-SIN | 1,705,435 | 12,360 | 80.5% |
| 2 | SIN-DPS | 1,205,738 | 5,665 | 83.9% |
| 3 | CGK-KUL | 816,674 | 5,985 | 75.1% |
| 4 | CGK-JED | 637,181 | 1,840 | 85.2% |
| 5 | KUL-DPS | 541,398 | 3,594 | 75.3% |

### Total Row
- **JUMLAH PENERBANGAN:** 74,438
- **JUMLAH PENUMPANG:** 12,298,746
- **KAPASITAS SEAT:** 15,795,936
- **JUMLAH BARANG:** 304,944,484 kg
- **JUMLAH POS:** 3,502,685 kg
- **L/F Rata-rata:** 77.9%

---

## ⚠️ Potensi Masalah & Saran

### 1. Format Angka dengan Titik sebagai Pemisah Ribuan (KRUSIAL!)
- **Contoh:** `12.360` = 12,360 penerbangan
- **Saran:** Parse string → hapus titik → integer

### 2. Format Rute Hanya IATA Code
- **Saran:** Mapping table

### 3. Load Factor Koma Desimal
- **Saran:** Replace `,` → `.`

### 4. Baris Total Tanpa Label
- **Saran:** Flag `is_total_row`

---

## 🎯 Kesimpulan

### Masalah Kritikal
1. ✅ Format angka titik = ribuan
2. ✅ Format rute hanya IATA
3. ✅ Load Factor koma desimal
4. ✅ Baris Total

### Metadata

| Properti | Nilai |
|----------|-------|
| **Jumlah Rute** | 133 |
| **Total Penumpang** | 12,298,746 |
| **Average LF** | 77.9% |

---

> **Catatan:** Dokumen ini hanya fokus pada file Internasional Ranking 2022.
