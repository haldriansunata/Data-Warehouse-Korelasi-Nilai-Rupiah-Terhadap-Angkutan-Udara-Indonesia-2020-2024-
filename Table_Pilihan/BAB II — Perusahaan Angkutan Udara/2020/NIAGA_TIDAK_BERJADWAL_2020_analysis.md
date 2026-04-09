# Analisis Tabel: DAFTAR PERUSAHAAN ANGKUTAN UDARA NIAGA TIDAK BERJADWAL YANG BEROPERASI TAHUN 2020

## Informasi Umum
| Atribut | Nilai |
|---------|-------|
| **Sumber File** | `DAFTAR PERUSAHAAN ANGKUTAN UDARA NIAGA TIDAK BERJADWAL YANG BEROPERASI TAHUN 2020.csv` |
| **Tahun** | 2020 |
| **Kategori** | Angkutan Udara Niaga Tidak Berjadwal |
| **Total Baris Data** | 50 |
| **Jumlah Kolom** | 3 |

---

## Struktur Tabel

| No | Nama Kolom | Tipe Data | Deskripsi |
|----|------------|-----------|-----------|
| 1 | `NO` | Integer | Nomor urut badan usaha |
| 2 | `NAMA BADAN USAHA` | String | Nama resmi badan usaha/perusahaan |
| 3 | `JENIS KEGIATAN` | String | Jenis layanan operasional (Penumpang/Cargo) |

---

## Sample Data (3 Baris Pertama)

| NO | NAMA BADAN USAHA | JENIS KEGIATAN |
|----|------------------|----------------|
| 1 | PT. AIR PASIFIK UTAMA | Penumpang |
| 2 | PT. AIRFAST INDONESIA | Penumpang |
| 3 | PT. ALDA TRANS PAPUA | Penumpang |

---

## Analisis Kualitas Data

### Ringkasan Umum
| Metrik | Nilai |
|--------|-------|
| Total Baris | 50 |
| Kolom dengan Missing Values | 0 |
| Kolom dengan Nilai Null/NaN | 0 |
| Kolom dengan Strip ("-") | 0 |

### Detail Per Kolom

| Kolom | Total Baris | Non-Empty | Empty | Null/NaN | Strip ("-") | Lainnya | Keterangan |
|-------|-------------|-----------|-------|----------|-------------|---------|------------|
| `NO` | 50 | 50 | 0 | 0 | 0 | 0 | Semua terisi (angka 1-50) |
| `NAMA BADAN USAHA` | 50 | 50 | 0 | 0 | 0 | 0 | Semua terisi, format konsisten "PT. ..." |
| `JENIS KEGIATAN` | 50 | 50 | 0 | 0 | 0 | 0 | Semua terisi, nilai unik: "Penumpang", "Cargo", "Penumpang & Cargo" |

### Distribusi Nilai Kolom `JENIS KEGIATAN`
| Nilai | Jumlah | Persentase |
|-------|--------|------------|
| Penumpang | 35 | 70% |
| Penumpang & Cargo | 14 | 28% |
| Cargo | 1 | 2% |

---

## Diagram Distribusi Jenis Kegiatan

```mermaid
pie title Distribusi Jenis Kegiatan (Niaga Tidak Berjadwal 2020)
    "Penumpang" : 35
    "Penumpang & Cargo" : 14
    "Cargo" : 1
```

---

## Catatan Tambahan
- ✅ Data bersih tanpa nilai kosong/null/strip
- ✅ Format penamaan perusahaan konsisten menggunakan awalan "PT."
- ⚠️ Terdapat 1 entitas dengan catatan kaki: `PT. DERAYA*)` (ada tanda `*)` yang kemungkinan merujuk ke catatan tambahan)
- ⚠️ Terdapat 1 perusahaan yang hanya melayani `Cargo`: `PT. DERAYA*)`
- ⚠️ Nama `PT. GARUDA INDONESIA (PERSERO) Tbk` muncul juga di file Niaga Berjadwal (potensi duplikasi antar kategori)
