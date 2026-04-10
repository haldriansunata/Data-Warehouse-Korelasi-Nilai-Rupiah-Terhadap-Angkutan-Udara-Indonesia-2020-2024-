# TASK PROMPT — Analisis File CSV Perusahaan Angkutan Udara per Tahun

## Deskripsi Umum
Proyek ini memproses file CSV dari data perusahaan angkutan udara yang tersimpan dalam folder per tahun (2020-2024). Setiap folder tahun berisi 4 file CSV yang mewakili kategori perusahaan yang sama.

---

## Scope & Struktur Folder
```
BAB II — Perusahaan Angkutan Udara/
├── 2020/
│   ├── DAFTAR BADAN USAHA ANGKUTAN UDARA NIAGA BERJADWAL YANG BEROPERASI TAHUN 2020.csv
│   ├── DAFTAR PERUSAHAAN ANGKUTAN UDARA ASING YANG BEROPERASI TAHUN 2020.csv
│   ├── DAFTAR PERUSAHAAN ANGKUTAN UDARA BUKAN NIAGA YANG BEROPERASI TAHUN 2020.csv
│   ├── DAFTAR PERUSAHAAN ANGKUTAN UDARA NIAGA TIDAK BERJADWAL YANG BEROPERASI TAHUN 2020.csv
│   └── PDF/ (skip folder ini, tidak ada CSV)
├── 2021/
│   ├── DAFTAR BADAN USAHA ANGKUTAN UDARA NIAGA BERJADWAL TAHUN 2021.csv
│   ├── DAFTAR PERUSAHAAN ANGKUTAN UDARA ASING TAHUN 2021.csv
│   ├── DAFTAR PERUSAHAAN ANGKUTAN UDARA BUKAN NIAGA TAHUN 2021.csv
│   ├── DAFTAR PERUSAHAAN ANGKUTAN UDARA NIAGA TIDAK BERJADWAL TAHUN 2021.csv
│   └── PDF/ (skip folder ini, tidak ada CSV)
├── 2022/
│   ├── DAFTAR BADAN USAHA ANGKUTAN UDARA NIAGA BERJADWAL TAHUN 2022.csv
│   ├── DAFTAR PERUSAHAAN ANGKUTAN UDARA ASING TAHUN 2022.csv
│   ├── DAFTAR PERUSAHAAN ANGKUTAN UDARA BUKAN NIAGA TAHUN 2022.csv
│   ├── DAFTAR PERUSAHAAN ANGKUTAN UDARA NIAGA TIDAK BERJADWAL TAHUN 2022.csv
│   └── PDF/ (skip folder ini, tidak ada CSV)
├── 2023/
├── 2024/
└── py_ekstrak/
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
3. **Skip Subfolder PDF:** Tidak ada CSV di dalamnya
4. **Format Output:** Semua dalam `.md`, gunakan Mermaid jika lebih efektif untuk visualisasi
5. **Sample Data:** 3 baris pertama per file CSV
6. **Bahasa Output:** Indonesia untuk konten `.md`, English untuk komunikasi dengan user

---

## Template Output (Contoh)

### File: `NIAGA_BERJADWAL_2020_analysis.md`
```markdown
# Analisis Tabel: DAFTAR BADAN USAHA ANGKUTAN UDARA NIAGA BERJADWAL YANG BEROPERASI TAHUN 2020

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
- [ ] Proses folder 2020 (4 file CSV → 4 file .md)
- [ ] Review hasil 2020 dengan user
- [ ] Proses folder 2021 (4 file CSV → 4 file .md)
- [ ] Proses folder 2022 (4 file CSV → 4 file .md)
- [ ] Proses folder 2023 (4 file CSV → 4 file .md)
- [ ] Proses folder 2024 (4 file CSV → 4 file .md)
- [ ] Buat file `ANALISIS_PERBANDINGAN_STRUKTUR_CSV.md` di root directory
- [ ] Final review semua output

---

## Catatan Penting
- File CSV menggunakan encoding yang perlu dicek (UTF-8, Latin-1, dll)
- Separator CSV mungkin `,` atau `;` — perlu diverifikasi
- Nama kolom mungkin dalam bahasa Indonesia — pertahankan asli
- Jangan modifikasi file CSV asli, hanya buat file `.md` baru

