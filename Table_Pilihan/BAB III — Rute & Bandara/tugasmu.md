# TASK PROMPT — Analisis File CSV Rute & Bandara Angkutan Udara per Tahun

## Deskripsi Umum
Proyek ini memproses file CSV dari data rute dan bandara angkutan udara yang tersimpan dalam folder per tahun (2020-2024). Setiap folder tahun berisi 6 file CSV yang mewakili kategori rute dan kota yang sama, kecuali tahun 2024 yang memiliki 2 file agregat tambahan.

---

## Scope & Struktur Folder
```
BAB III — Rute & Bandara/
├── 2020/
│   ├── BADAN USAHA ANGKUTAN UDARA NASIONAL YANG MELAYANI PENUMPANG RUTE INTERNASIONAL TAHUN 2020.csv
│   ├── KOTA TERHUBUNGI OLEH RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2020.csv
│   ├── KOTA TERHUBUNGI OLEH RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI DI INDONESIA TAHUN 2020.csv
│   ├── KOTA TERHUBUNGI OLEH RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI DI NEGARA TUJUAN TAHUN 2020.csv
│   ├── RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2020.csv
│   ├── RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI TAHUN 2020.csv
│   ├── PDF/ (SKIP - tidak ada CSV)
│   └── TOTAL RUTE/ (SKIP - berisi rekapitulasi tahunan, tidak dipakai)
├── 2021/
│   ├── BADAN USAHA ANGKUTAN UDARA NASIONAL YANG MELAYANI PENUMPANG RUTE INTERNASIONAL TAHUN 2021.csv
│   ├── KOTA TERHUBUNGI OLEH RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2021.csv
│   ├── KOTA TERHUBUNGI OLEH RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI DI INDONESIA TAHUN 2021.csv
│   ├── KOTA TERHUBUNGI OLEH RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI DI NEGARA TUJUAN TAHUN 2021.csv
│   ├── RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2021..csv
│   ├── RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI TAHUN 2021.csv
│   ├── PDF/ (SKIP - tidak ada CSV)
│   └── TOTAL RUTE/ (SKIP - berisi rekapitulasi tahunan, tidak dipakai)
├── 2022/
│   ├── BADAN USAHA ANGKUTAN UDARA NASIONAL YANG MELAYANI PENUMPANG RUTE INTERNASIONAL TAHUN 2022.csv
│   ├── KOTA TERHUBUNGI OLEH RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2022.csv
│   ├── KOTA TERHUBUNGI OLEH RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI DI INDONESIA TAHUN 2022.csv
│   ├── KOTA TERHUBUNGI OLEH RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI DI NEGARA TUJUAN TAHUN 2022.csv
│   ├── RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2022.csv
│   ├── RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI TAHUN 2022.csv
│   ├── PDF/ (SKIP - tidak ada CSV)
│   └── TOTAL RUTE/ (SKIP - berisi rekapitulasi tahunan, tidak dipakai)
├── 2023/
│   ├── BADAN USAHA ANGKUTAN UDARA NASIONAL PENUMPANG YANG MELAYANI RUTE INTERNASIONAL TAHUN 2023.csv
│   ├── KOTA TERHUBUNGI OLEH RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2023.csv
│   ├── KOTA TERHUBUNGI OLEH RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI DI INDONESIA TAHUN 2023.csv
│   ├── KOTA TERHUBUNGI OLEH RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI DI NEGARA TUJUAN TAHUN 2023.csv
│   ├── RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2023.csv
│   ├── RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI TAHUN 2023.csv
│   ├── PDF/ (SKIP - tidak ada CSV)
│   └── TOTAL RUTE/ (SKIP - berisi rekapitulasi tahunan, tidak dipakai)
├── 2024/
│   ├── BADAN USAHA ANGKUTAN UDARA NASIONAL PENUMPANG YANG MELAYANI RUTE INTERNASIONAL.csv
│   ├── KOTA TERHUBUNG OLEH ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2024.csv
│   ├── KOTA TERHUBUNG OLEH RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI DI INDONESIA TAHUN 2024.csv
│   ├── KOTA TERHUBUNG OLEH RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI DI NEGARA TUJUAN TAHUN 2024.csv
│   ├── RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2024.csv
│   ├── RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI TAHUN 2024.csv
│   ├── TOTAL JUMLAH RUTE DOMESTIK ANGKUTAN UDARA NIAGA BERJADWAL TAHUN 2020-2024.csv (AGREGAT - diproses)
│   ├── TOTAL JUMLAH RUTE INTERNATIONAL TAHUN 2020-2024.csv (AGREGAT - diproses)
│   └── PDF/ (SKIP - tidak ada CSV)
├── py_ekstrak/ (SKIP - tidak relevan dengan tugas ini)
└── tugasmu.md
```

---

## Task Detail

### TASK 1: Dokumentasi Per File CSV Per Tahun
**Input:** Semua file `.csv` di setiap folder tahun (skip subfolder `PDF`)

**Output per file CSV:** Satu file `.md` di dalam folder tahun yang bersangkutan

**Nama File Output:**
```
{KATEGORI}_{TAHUN}_analysis.md
```
Contoh: `NIAGA_BERJADWAL_2020_analysis.md`

**Konten File .md:**
1. **Judul Tabel**
   - Judul asli dari file CSV (dibersihkan/diformat)

2. **Struktur Tabel**
   - Tabel berisi: Nama Kolom | Tipe Data | Deskripsi (jika bisa disimpulkan dari nama)

3. **Sample Data (3 Baris)**
   - Tampilkan 3 baris pertama data dari CSV
   - Format: Tabel markdown dengan header kolom

4. **Analisis Kualitas Data Per Kolom**
   - Jumlah baris total
   - Analisis nilai kosong/null/NaN/strip/missing values per kolom
   - Format tabel:
     | Kolom | Total Baris | Non-Empty | Empty | Null/NaN | Strip ("-") | Lainnya | Keterangan |
   - "Lainnya" mencakup: spasi kosong, string "N/A", "n/a", "unknown", dll.

---

### TASK 2: Analisis Perbandingan Antar Tahun
**Scope:** Semua file CSV dari semua tahun (2020-2024)

**Output:** Satu file `.md` di root directory

**Nama File Output:**
```
ANALISIS_PERBANDINGAN_STRUKTUR_CSV.md
```

**Konten File .md:**
1. **Perbandingan Judul Tabel**
   - Tabel perbandingan: Kategori | 2020 | 2021 | 2022 | 2023 | 2024 | Catatan Perubahan
   - Highlight jika ada perubahan penamaan

2. **Perbandingan Struktur Tabel (Kolom)**
   - Perbandingan kolom per kategori:
     - Kolom yang konsisten ada di semua tahun
     - Kolom yang hilang/muncul di tahun tertentu
   - Gunakan Mermaid diagram jika relevan (misal: timeline perubahan struktur)

3. **Perbandingan Tipe Data**
   - Tabel perbandingan tipe data per kolom antar tahun
   - Highlight jika ada kolom yang berubah tipe datanya

4. **Perbandingan Kualitas Data**
   - Pola data kosong/null/NaN/strip per tahun
   - Apakah ada tahun yang lebih "bersih" atau lebih "kotor" datanya?

5. **Kesimpulan & Rekomendasi**
   - Ringkasan temuan utama
   - Ketidakonsistenan yang ditemukan
   - Saran untuk standardisasi data

---

## Aturan Eksekusi
1. **Pendekatan Bertahap:** Mulai dari satu folder tahun (2020) sebagai pilot
2. **Tidak Halusinasi:** Baca file CSV secara aktual, jangan asumsi struktur
3. **Skip Folder/Folder yang Tidak Relevan:**
   - `PDF/` → folder di setiap tahun (2020-2024), tidak ada CSV di dalamnya
   - `TOTAL RUTE/` → folder di setiap tahun (2020-2023), berisi rekapitulasi tahunan yang tidak dipakai
   - `py_ekstrak/` → folder di root directory, tidak relevan dengan tugas ini (hanya hasil ekstrak PDF sebelumnya)
4. **Format Output:** Semua dalam `.md`, gunakan Mermaid jika lebih efektif untuk visualisasi
5. **Sample Data:** Tampilkan 3 baris pertama dari setiap file CSV
6. **Bahasa Output:** Full Indonesia untuk konten `.md` dan komunikasi dengan user di terminal

---

## Template Output (Contoh)

### File: `KOTA_TERHUBUNGI_DALAM_NEGERI_2020_analysis.md`
```markdown
# Analisis Tabel: KOTA TERHUBUNGI OLEH RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2020

## Struktur Tabel
| Nama Kolom | Tipe Data | Deskripsi |
|------------|-----------|-----------|
| ... | ... | ... |

## Sample Data (3 Baris)
| Kolom1 | Kolom2 | Kolom3 | ... |
|--------|--------|--------|-----|
| ... | ... | ... | ... |
| ... | ... | ... | ... |
| ... | ... | ... | ... |

## Analisis Kualitas Data
| Kolom | Total Baris | Non-Empty | Empty | Null/NaN | Strip ("-") | Lainnya | Keterangan |
|-------|-------------|-----------|-------|----------|-------------|---------|------------|
| ... | ... | ... | ... | ... | ... | ... | ... |
```

---

## Checklist Eksekusi
- [ ] Proses folder 2020 (6 file CSV → 6 file .md)
- [ ] Review hasil 2020 dengan user
- [ ] Proses folder 2021 (6 file CSV → 6 file .md)
- [ ] Proses folder 2022 (6 file CSV → 6 file .md)
- [ ] Proses folder 2023 (6 file CSV → 6 file .md)
- [ ] Proses folder 2024 (8 file CSV termasuk 2 agregat → 8 file .md)
- [ ] Buat file `ANALISIS_PERBANDINGAN_STRUKTUR_CSV.md` di root directory
- [ ] Final review semua output

---

## Catatan Penting
- File CSV menggunakan encoding yang perlu dicek (UTF-8, Latin-1, dll)
- Separator CSV mungkin `,` atau `;` — perlu diverifikasi
- Nama kolom mungkin dalam bahasa Indonesia — pertahankan asli
- Jangan modifikasi file CSV asli, hanya buat file `.md` baru

