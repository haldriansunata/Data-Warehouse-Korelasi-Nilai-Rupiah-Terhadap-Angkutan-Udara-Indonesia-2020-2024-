# Analisis Tabel: KOTA TERHUBUNGI OLEH RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2020

## Informasi Umum
| Atribut | Nilai |
|---------|-------|
| **Sumber File** | `KOTA TERHUBUNGI OLEH RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2020.csv` |
| **Tahun** | 2020 |
| **Kategori** | Kota Domestik — Rute Niaga Berjadwal Dalam Negeri |
| **Total Baris Data** | 138 |
| **Jumlah Kolom** | 2 |

---

## Struktur Tabel

| No | Nama Kolom | Tipe Data | Deskripsi |
|----|------------|-----------|-----------|
| 1 | `NO` | Integer | Nomor urut kota |
| 2 | `KOTA` | String | Nama kota yang terhubung oleh rute angkutan udara niaga berjadwal dalam negeri, dilengkapi kode bandara dalam kurung |

---

## Sample Data (3 Baris Pertama)

| NO | KOTA |
|----|------|
| 1 | Alor (ARD) |
| 2 | Ambon (AMQ) |
| 3 | Ampana (OJU) |

---

## Analisis Kualitas Data

### Ringkasan Umum
| Metrik | Nilai |
|--------|-------|
| Total Baris | 138 |
| Kolom dengan Missing Values | 0 |
| Kolom dengan Nilai Null/NaN | 0 |
| Kolom dengan Strip ("-") | 0 |

### Detail Per Kolom

| Kolom | Total Baris | Non-Empty | Empty | Null/NaN | Strip ("-") | Lainnya | Keterangan |
|-------|-------------|-----------|-------|----------|-------------|---------|------------|
| `NO` | 138 | 138 | 0 | 0 | 0 | 0 | Semua terisi (angka 1-138) |
| `KOTA` | 138 | 138 | 0 | 0 | 0 | 0 | Semua terisi, format umum: `Nama Kota (KODE)` |

### Catatan Khusus Kolom `KOTA`

#### Format Penulisan Nama Kota:
| Format | Jumlah | Contoh |
|--------|--------|--------|
| `Nama Kota (KODE)` | 135 | Alor (ARD), Ambon (AMQ), Balikpapan (BPN) |
| `Nama Kota-KODE (KODE)` | 2 | Jakarta-HLP (HLP), Siborongborong -(DTB) |
| `"Nama, Keterangan (KODE)"` (quoted) | 1 | `"Praya, Lombok (LOP)"` |

#### Format Kode Bandara:
| Tipe | Jumlah | Keterangan |
|------|--------|------------|
| 3 huruf (IATA standar) | 138 | Semua kode bandara IATA |
| uppercase penuh | 138 | Semua menggunakan huruf kapital |

#### Anomali Format:
| No | Nilai | Anomali |
|----|-------|---------|
| 32 | `Jakarta-HLP (HLP)` | Menggunakan format `Nama-KODE` sebelum kurung |
| 109 | `Siborongborong -(DTB)` | Strip sebelum kurung: `-(DTB)` |
| 95 | `"Praya, Lombok (LOP)"` | Mengandung koma, di-quote dalam CSV |

---

## Diagram Distribusi Format Penulisan Kota

```mermaid
pie title Distribusi Format Penulisan Kota (Kota Domestik 2020)
    "Nama Kota (KODE)" : 135
    "Nama Kota-KODE (KODE)" : 2
    "Quoted (mengandung koma)" : 1
```

---

## Catatan Tambahan
- ✅ Data bersih tanpa nilai kosong/null/strip
- ✅ Semua entri memiliki kode bandara IATA (3 huruf)
- ⚠️ Terdapat 3 anomali format penulisan:
  - `Jakarta-HLP (HLP)` — penulisan ganda kode
  - `Siborongborong -(DTB)` — strip sebelum kurung
  - `"Praya, Lombok (LOP)"` — mengandung koma, di-quote dalam CSV
