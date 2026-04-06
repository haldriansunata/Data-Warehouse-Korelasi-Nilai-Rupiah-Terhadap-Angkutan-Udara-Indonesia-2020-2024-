# Implementation Plan - Fase 2: Analisis Tabel & Konversi CSV

## Pemahaman Tugas

Saya memahami bahwa tugas saya adalah:

1. **Menganalisis PDF** di folder `Table_Pilihan/` yang berisi 7 subfolder (BAB II - BAB XII)
2. **Mengekstrak tabel** dari setiap PDF dan mengonversinya ke format CSV
3. **Menangani kompleksitas** seperti:
   - Tabel berdampingan (side-by-side)
   - Tabel multi-halaman yang berlanjut
   - Header bertingkat dan sel gabungan
   - Format tidak standar (data pemerintah)
   - Konten campuran (teks, grafik, catatan kaki)

## Pendekatan yang Akan Digunakan

### 1. Eksplorasi Awal
- Menjelajahi setiap folder BAB untuk melihat file PDF yang ada
- Membaca sample PDF untuk memahami struktur dan format
- Mengidentifikasi pola yang konsisten vs anomali

### 2. Strategi Ekstraksi (Hybrid: Script + LLM)

#### A. Script Python untuk:
- Membaca PDF dan mendeteksi tabel secara otomatis
- Ekstraksi struktur tabel dasar
- Konversi ke CSV dengan naming convention yang sesuai
- Handling common patterns (multi-page tables, merged cells)

#### B. LLM untuk:
- Menangani anomali yang tidak bisa diatasi script
- Memahami konteks tabel yang ambigu
- Membersihkan dan memvalidasi data hasil ekstraksi
- Menyesuaikan struktur kompleks menjadi format CSV yang proper

### 3. Output yang Akan Dihasilkan

Untuk **setiap PDF** yang diproses:
- ✅ File CSV dengan nama sesuai judul tabel
- ✅ Laporan analisis struktur tabel (dokumentasi)
- ✅ File CSV disimpan terorganisir (mengikuti struktur BAB atau flat dengan naming jelas)

### 4. Konvensi Penamaan File CSV
```
{judul_tabel}.csv
```
- Karakter khusus (`/`, `,`, `:`, `*`, `?`, `"`, `<`, `>`, `|`) → diganti `_`
- Spasi berlebih dihilangkan
- Judul tetap mendekati aslinya

### 5. Struktur Output (Contoh)
```
Table_Pilihan/
├── BAB II — Perusahaan Angkutan Udara/
│   ├── CSV/
│   │   ├── DAFTAR BADAN USAHA...csv
│   │   └── ...
│   └── analisis_BAB_II.md
├── BAB III — Rute & Bandara/
│   ├── CSV/
│   │   └── ...
│   └── analisis_BAB_III.md
└── ...
```

## Langkah Selanjutnya (Setelah Konfirmasi)

1. ✅ Eksplorasi semua folder BAB dan inventory file PDF
2. ✅ Baca sample PDF dari setiap BAB untuk memahami pola
3. ✅ Buat script Python untuk ekstraksi tabel awal
4. ✅ Proses setiap PDF, gunakan LLM untuk handling edge cases
5. ✅ Validasi hasil CSV (struktur, data integrity)
6. ✅ Buat laporan analisis per BAB

## Prinsip Kerja
- **Data Engineer mindset**: Presisi, integritas data utama, handling edge cases dengan baik
- **Hybrid approach**: Otomatisasi dengan script, kecerdasan kontekstual dengan LLM
- **Traceable**: Dokumentasi setiap keputusan transformasi data
- **Reversible**: Jika ada kesalahan, mudah rollback

---

**Status**: Menunggu konfirmasi sebelum memulai ⏸️
