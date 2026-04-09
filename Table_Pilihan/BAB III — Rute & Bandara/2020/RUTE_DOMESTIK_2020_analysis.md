# Analisis Tabel: RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2020

## Informasi Umum
| Atribut | Nilai |
|---------|-------|
| **Sumber File** | `RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2020.csv` |
| **Tahun** | 2020 |
| **Kategori** | Rute Domestik — Niaga Berjadwal Dalam Negeri |
| **Total Baris Data** | 410 |
| **Jumlah Kolom** | 3 |

---

## Struktur Tabel

| No | Nama Kolom | Tipe Data | Deskripsi |
|----|------------|-----------|-----------|
| 1 | `NO` | Integer | Nomor urut rute |
| 2 | `RUTE (ASAL)` | String | Kota asal penerbangan, dilengkapi kode bandara dalam kurung |
| 3 | `RUTE (TUJUAN)` | String | Kota tujuan penerbangan, dilengkapi kode bandara dalam kurung |

---

## Sample Data (3 Baris Pertama)

| NO | RUTE (ASAL) | RUTE (TUJUAN) |
|----|-------------|---------------|
| 1 | Pontianak (PNK) | Palangkaraya (PKY) |
| 2 | Timika (TIM) | Manado (MDC) |
| 3 | Balikpapan (BPN) | Bandung (BDO) |

---

## Analisis Kualitas Data

### Ringkasan Umum
| Metrik | Nilai |
|--------|-------|
| Total Baris | 410 |
| Kolom dengan Missing Values | 0 |
| Kolom dengan Nilai Null/NaN | 0 |
| Kolom dengan Strip ("-") | 0 |

### Detail Per Kolom

| Kolom | Total Baris | Non-Empty | Empty | Null/NaN | Strip ("-") | Lainnya | Keterangan |
|-------|-------------|-----------|-------|----------|-------------|---------|------------|
| `NO` | 410 | 410 | 0 | 0 | 0 | 0 | Semua terisi (angka 1-410) |
| `RUTE (ASAL)` | 410 | 410 | 0 | 0 | 0 | 0 | Semua terisi, format umum: `Nama Kota (KODE)` |
| `RUTE (TUJUAN)` | 410 | 408 | 0 | 0 | 2 | 0 | 2 baris hanya berisi kode tanpa nama kota |

### Catatan Khusus Kolom `RUTE (ASAL)`

#### Format Penulisan Rute Asal:
| Format | Jumlah | Contoh |
|--------|--------|--------|
| `Nama Kota (KODE)` | 407 | Pontianak (PNK), Jakarta (CGK), Denpasar (DPS) |
| `Nama Kota-KODE (KODE)` | 2 | Jakarta-HLP (HLP) |
| `"Nama, Keterangan (KODE)"` (quoted) | 1 | `"Praya, Lombok (LOP)"` |

#### Distribusi Kota Asal (Top 10):
| Kota Asal | Jumlah Rute | Persentase |
|-----------|-------------|------------|
| Jakarta (CGK) | 52 | 12.7% |
| Makassar (UPG) | 46 | 11.2% |
| Surabaya (SUB) | 32 | 7.8% |
| Yogyakarta (YIA) | 24 | 5.9% |
| Semarang (SRG) | 20 | 4.9% |
| Medan (KNO) | 18 | 4.4% |
| Palembang (PLM) | 15 | 3.7% |
| Manado (MDC) | 14 | 3.4% |
| Pekanbaru (PKU) | 14 | 3.4% |
| Padang Pariaman (PDG) | 13 | 3.2% |

### Catatan Khusus Kolom `RUTE (TUJUAN)`

#### Format Penulisan Rute Tujuan:
| Format | Jumlah | Contoh |
|--------|--------|--------|
| `Nama Kota (KODE)` | 405 | Palangkaraya (PKY), Manado (MDC), Bandung (BDO) |
| `KODE` (tanpa nama kota) | 2 | `TRT`, `KXB` |
| `"Nama, Keterangan (KODE)"` (quoted) | 3 | `"Praya, Lombok (LOP)"` |

#### Anomali pada `RUTE (TUJUAN)`:
| No | Nilai | Anomali |
|----|-------|---------|
| 9 | `TRT` | Hanya kode bandara, tanpa nama kota (kemungkinan Tana Toraja) |
| 29 | `KXB` | Hanya kode bandara, tanpa nama kota (kemungkinan Kolaka) |

---

## Diagram Distribusi Top 10 Kota Asal

```mermaid
pie title Top 10 Kota Asal Rute Domestik 2020
    "Jakarta (CGK)" : 52
    "Makassar (UPG)" : 46
    "Surabaya (SUB)" : 32
    "Yogyakarta (YIA)" : 24
    "Semarang (SRG)" : 20
    "Medan (KNO)" : 18
    "Palembang (PLM)" : 15
    "Manado (MDC)" : 14
    "Pekanbaru (PKU)" : 14
    "Padang Pariaman (PDG)" : 13
    "Lainnya" : 142
```

---

## Catatan Tambahan
- ✅ Mayoritas data bersih tanpa nilai kosong/null/strip
- ⚠️ Terdapat **2 anomali** pada kolom `RUTE (TUJUAN)`:
  - Baris 9: `TRT` — hanya kode bandara (kemungkinan Tana Toraja)
  - Baris 29: `KXB` — hanya kode bandara (kemungkinan Kolaka)
- ⚠️ Terdapat 1 entri `"Praya, Lombok (LOP)"` yang muncul di beberapa baris (mengandung koma, di-quote dalam CSV)
- ⚠️ Terdapat 2 entri `Jakarta-HLP (HLP)` dengan format penulisan ganda kode
