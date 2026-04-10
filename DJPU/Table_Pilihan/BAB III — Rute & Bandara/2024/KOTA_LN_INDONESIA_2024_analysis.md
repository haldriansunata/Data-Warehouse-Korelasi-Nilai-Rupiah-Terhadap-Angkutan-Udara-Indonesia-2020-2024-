# Analisis Tabel: KOTA TERHUBUNG OLEH RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI DI INDONESIA TAHUN 2024

## Informasi Umum
| Atribut | Nilai |
|---------|-------|
| **Sumber File** | `KOTA TERHUBUNG OLEH RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI DI INDONESIA TAHUN 2024.csv` |
| **Tahun** | 2024 |
| **Kategori** | Kota Indonesia — Rute Niaga Berjadwal Luar Negeri |
| **Total Baris Data** | 17 |
| **Jumlah Kolom** | 2 |

---

## Struktur Tabel

| No | Nama Kolom | Tipe Data | Deskripsi |
|----|------------|-----------|-----------|
| 1 | `NO` | Integer | Nomor urut kota |
| 2 | `KOTA` | String | Nama kota di Indonesia yang terhubung oleh rute angkutan udara niaga berjadwal luar negeri, dilengkapi kode bandara dalam kurung |

---

## Sample Data (3 Baris Pertama)

| NO | KOTA |
|----|------|
| 1 | Balikpapan(BPN) |
| 2 | Banda Aceh(BTJ) |
| 3 | Batam(BTH) |

---

## Analisis Kualitas Data

### Ringkasan Umum
| Metrik | Nilai |
|--------|-------|
| Total Baris | 17 |
| Kolom dengan Missing Values | 0 |
| Kolom dengan Nilai Null/NaN | 0 |
| Kolom dengan Strip ("-") | 0 |

### Detail Per Kolom

| Kolom | Total Baris | Non-Empty | Empty | Null/NaN | Strip ("-") | Lainnya | Keterangan |
|-------|-------------|-----------|-------|----------|-------------|---------|------------|
| `NO` | 17 | 17 | 0 | 0 | 0 | 0 | Semua terisi (angka 1-17) |
| `KOTA` | 17 | 17 | 0 | 0 | 0 | 0 | Semua terisi, format umum: `Nama Kota(KODE)` — tanpa spasi sebelum kurung |

### Catatan Khusus Kolom `KOTA`

#### Format Penulisan Nama Kota:
| Format | Jumlah | Contoh |
|--------|--------|--------|
| `Nama Kota(KODE)` (tanpa spasi) | 16 | Balikpapan(BPN), Banda Aceh(BTJ), Denpasar(DPS) |
| `"Nama, Lombok(KODE)"` (quoted, tanpa spasi) | 1 | `"Praya, Lombok(LOP)"` |

#### Format Kode Bandara:
| Tipe | Jumlah | Keterangan |
|------|--------|------------|
| 3 huruf (IATA standar) | 17 | Semua kode bandara IATA |
| uppercase penuh | 17 | Semua menggunakan huruf kapital |

#### Anomali Format:
| No | Nilai | Anomali |
|----|-------|---------|
| 6 | `Jakarta(HLP)` | Format tetap tanpa prefix "HLP" — konsisten dengan 2023 |
| 14 | `"Praya, Lombok(LOP)"` | Mengandung koma, di-quote dalam CSV |

#### Perubahan Dibanding 2023 (Catatan Internal):
| Status 2023 | Status 2024 | Kota |
|-------------|-------------|------|
| Ada | Hilang | — (tidak ada yang hilang) |
| Baru | Ada | Labuhan Bajo(LBJ) |
| **Format global** | **Tetap tanpa spasi** | Konsisten dengan 2022-2023 |
| **Judul file** | **Berubah** | "TERHUBUNGI OLEH RUTE" → "TERHUBUNG OLEH RUTE" |

---

## Diagram Distribusi Format Penulisan Kota

```mermaid
pie title Distribusi Format Penulisan Kota (Kota LN Indonesia 2024)
    "Nama Kota(KODE)" : 16
    "Quoted (mengandung koma)" : 1
```

---

## Catatan Tambahan
- ✅ Data bersih tanpa nilai kosong/null/strip
- ✅ Semua entri memiliki kode bandara IATA (3 huruf)
- ⚠️ Jumlah kota bertambah dari 16 (2023) → 17 (2024): `Labuhan Bajo(LBJ)` kota baru
- ⚠️ Terdapat 1 entri dengan format khusus: `"Praya, Lombok(LOP)"` — mengandung koma, di-quote dalam CSV
- ⚠️ `Jakarta(HLP)` — format tetap konsisten dengan 2023 (tanpa prefix "HLP" di nama)
