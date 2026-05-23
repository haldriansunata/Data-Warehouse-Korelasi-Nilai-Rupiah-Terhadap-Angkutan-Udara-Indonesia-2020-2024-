# Bab 5 / WS5 — Top 15 Provinsi by Total Penumpang Domestik

## Tujuan
Distribusi geografis demand domestik per provinsi origin. Konteks penting untuk pembuat kebijakan: mana provinsi yang flow-nya paling besar.

## Pendekatan
Aggregate total penumpang per `o_provinsi` (provinsi asal), filter `kategori = DOMESTIK`, top 15.

## Hasil

| Rank | Provinsi (origin) | Total Pax (juta) |
|---:|---|---:|
| 1 | **JAKARTA** | **115,15** |
| 2 | EAST KALIMANTAN | 16,62 |
| 3 | RIAU ISLANDS | 14,63 |
| 4 | BALI | 13,17 |
| 5 | KALIMANTAN SELATAN | 10,70 |
| 6 | DKI JAKARTA | 9,63 |
| 7 | PAPUA | 6,97 |
| 8 | EAST JAVA | 5,88 |
| 9 | KALIMANTAN TIMUR | 4,34 |
| 10 | EAST NUSA TENGGARA | 3,74 |
| 11 | WEST PAPUA | 3,43 |
| 12 | MALUKU | 3,33 |
| 13 | SOUTHEAST SULAWESI | 3,11 |
| 14 | WEST NUSA TENGGARA | 2,89 |
| 15 | NORTH SULAWESI | 2,75 |

## Caveat Data — Inkonsistensi Nama Provinsi

Ada **dua entri Jakarta**: `JAKARTA` (115M) dan `DKI JAKARTA` (9,63M). Juga **dua entri Kalimantan Timur**: `EAST KALIMANTAN` (16,6M) dan `KALIMANTAN TIMUR` (4,3M). Ini karena `dim_bandara.csv` punya field `provinsi` yang inkonsisten — sebagian dari `airportsdata` library (Bahasa Inggris) dan sebagian dari override manual (Bahasa Indonesia).

### Implikasi
- **Jakarta + DKI Jakarta = 124,78M** sebenarnya — masih dominan absolut.
- East Kalimantan + Kalimantan Timur = 20,96M.

### Rekomendasi Cleanup (opsional, future)
Tambahkan pemetaan di ETL `03_dim_bandara.py`:
```python
PROVINSI_HARMONIZE = {
    "JAKARTA": "DKI JAKARTA",
    "EAST KALIMANTAN": "KALIMANTAN TIMUR",
    "EAST JAVA": "JAWA TIMUR",
    # ... dst
}
```
Tapi karena kamu sudah set TIDAK mengubah BULANAN, ini bisa di-handle di **Tableau dengan group manual** (klik kanan field → Group → satukan duplikat).

## Makna

### 1. Dominasi Jakarta (~125M ≈ 50% dari semua flow domestik)
Jakarta adalah origin dari hampir setengah total penumpang domestik. Bukan kejutan tapi konfirmasi numerik.

### 2. Kalimantan & Riau Islands tinggi
- Kalimantan (Timur + Selatan) total ~31M — workforce migration ke industri tambang/sawit.
- Riau Islands (Batam, Tanjung Pinang) ~14,6M — gerbang Singapura, cross-border worker.

### 3. Bali (13,2M)
Origin Bali tinggi karena wisman + outbound. Tableau peta akan menyoroti ini.

### 4. Indonesia Timur (Papua, NTT, Maluku, Sulawesi Tenggara)
Kombinasi 4 provinsi ini ~17M — penting untuk konektivitas region, biasanya rute thin & dependen subsidi.

## Output
- `plot.png` — horizontal bar top 15
- `top15_provinsi.csv`

## Target Tableau — Tutorial Step-by-Step

> **Konteks penting sebelum mulai**: field `Provinsi` di `dim_bandara` punya **18 pasangan duplikat** karena campuran Bahasa Indonesia + Bahasa Inggris (mis. "JAKARTA" vs "DKI JAKARTA"). Kita selesaikan ini dengan **Group** di Tableau — tidak ubah CSV, aman untuk 24 sheet lain yang sudah jadi.

### Step 1 — Buat Group `Provinsi (Cleaned)`

> **Catatan dual instance**: field `Provinsi` ada di **2 tempat** di Data pane karena `dim_bandara` di-join 2× (origin dan destination):
> - **`Provinsi`** (tanpa suffix) → dari `dim_bandara_origin`. **INI yang dipakai WS5.**
> - **`Provinsi (Dim Bandara Destination.Csv)`** → dari `dim_bandara_destination`. **TIDAK dipakai** di WS5 (atau di 24 WS lainnya).
>
> WS5 menghitung total penumpang dari sisi **keberangkatan** saja (kalau pakai keduanya = double count). Jadi Group cuma perlu di instance origin.

1. Di **Data pane** (panel kiri), cari field **`Provinsi`** di dalam `dim_bandara_origin` (yang **tanpa suffix** — itu instance origin).
2. Klik kanan field **`Provinsi`** → **Create** → **Group...**.
3. Jendela "Create Group" muncul.
4. Di kotak **Name**: ketik **`Provinsi (Cleaned)`**.
5. Untuk tiap pasangan duplikat di tabel di bawah, lakukan:
   - **Ctrl+click** kedua nilai (mis. "JAKARTA" dan "DKI JAKARTA") di list di kiri.
   - Klik tombol **Group** (di bawah list).
   - Double-click nama group yang baru terbentuk → rename sesuai kolom "Hasil Group" di tabel.
6. Setelah selesai semua 18 pasangan, klik **OK**.

#### Daftar 18 Pasangan untuk di-Group

| # | Pilih (Ctrl+click) | Rename Group jadi |
|---:|---|---|
| 1 | `JAKARTA` + `DKI JAKARTA` | **DKI JAKARTA** |
| 2 | `EAST KALIMANTAN` + `KALIMANTAN TIMUR` | **KALIMANTAN TIMUR** |
| 3 | `EAST JAVA` + `JAWA TIMUR` | **JAWA TIMUR** |
| 4 | `EAST NUSA TENGGARA` + `NUSA TENGGARA TIMUR` | **NUSA TENGGARA TIMUR** |
| 5 | `WEST NUSA TENGGARA` + `NUSA TENGGARA BARAT` | **NUSA TENGGARA BARAT** |
| 6 | `WEST KALIMANTAN` + `KALIMANTAN BARAT` | **KALIMANTAN BARAT** |
| 7 | `SOUTH KALIMANTAN` + `KALIMANTAN SELATAN` | **KALIMANTAN SELATAN** |
| 8 | `NORTH-KALIMANTAN` + `KALIMANTAN UTARA` | **KALIMANTAN UTARA** |
| 9 | `NORTH SULAWESI` + `SULAWESI UTARA` | **SULAWESI UTARA** |
| 10 | `SOUTH SULAWESI` + `SULAWESI SELATAN` | **SULAWESI SELATAN** |
| 11 | `SOUTHEAST SULAWESI` + `SULAWESI TENGGARA` | **SULAWESI TENGGARA** |
| 12 | `CENTRAL JAVA` + `JAWA TENGAH` | **JAWA TENGAH** |
| 13 | `CENTRAL SULAWESI` + `SULAWESI TENGAH` | **SULAWESI TENGAH** |
| 14 | `NORTH SUMATRA` + `SUMATERA UTARA` | **SUMATERA UTARA** |
| 15 | `SOUTH SUMATRA` + `SUMATERA SELATAN` | **SUMATERA SELATAN** |
| 16 | `RIAU ISLANDS` + `KEPULAUAN RIAU` | **KEPULAUAN RIAU** |
| 17 | `WEST PAPUA` + `PAPUA BARAT` | **PAPUA BARAT** |
| 18 | `NORTH MALUKU` + `MALUKU UTARA` | **MALUKU UTARA** |

> **Tips**: kalau capek scroll list, ketik di search box di atas list — Tableau akan filter nama yang mengandung teks tersebut.

> **Hasil**: setelah klik OK, di Data pane akan muncul field baru **`Provinsi (Cleaned)`** dengan icon paperclip (tanda field group). Yang akan kita pakai di WS5 ini, **bukan** field `Provinsi` aslinya.

### Step 2 — Buat worksheet baru
1. Klik **icon worksheet baru** di bar bawah Tableau.
2. Rename tab jadi **`Bab5_WS5_Provinsi`** (double-click tab → ketik nama).

### Step 3 — Filter Domestik
1. **Drag `kategori`** ke area **Filters**.
2. Di dialog yang muncul, **centang HANYA `DOMESTIK`** (uncheck INTERNASIONAL).
3. Klik **OK**.

### Step 4 — Drag field ke Rows dan Columns
1. **Drag `Provinsi (Cleaned)`** (field group yang baru dibuat di Step 1) ke **Rows**. Pil biru muncul.
   - ⚠️ **Pastikan** kamu drag field group `Provinsi (Cleaned)`, **BUKAN** field `Provinsi` original. Yang group ada icon paperclip.
2. **Drag `jumlah_penumpang`** ke **Columns**. Pil hijau `SUM(jumlah_penumpang)` muncul.

### Step 5 — Filter Top 15 Provinsi
1. **Drag `Provinsi (Cleaned)`** lagi ke area **Filters** (dari Data pane, bukan dari Rows).
2. Di dialog "Filter [Provinsi (Cleaned)]":
   - Klik tab **Top**.
   - Pilih radio **By field**.
   - Set: **Top** `15` **by** `SUM(jumlah_penumpang)` **Sum**.
3. Klik **OK**.

### Step 6 — Sort descending
1. Klik kanan pil `Provinsi (Cleaned)` di **Rows** → **Sort**.
2. Sort By: **Field**.
3. Field Name: `Jumlah Penumpang`, Aggregation: `Sum`.
4. Sort Order: **Descending**.
5. Klik **OK**.

Sekarang JAKARTA (cleaned) akan ada di paling atas.

### Step 7 — Marks: Bar (default) + Label
1. Di Marks card, pastikan tipe **Bar** (default kalau pakai SUM di Columns).
2. **Drag `jumlah_penumpang`** ke **Label** di Marks card → pil `SUM(jumlah_penumpang)` muncul.
3. **Format label**:
   - Klik kanan pil di Label → **Format Number** (Tableau Web) atau **Format** (Desktop).
   - Pilih **Custom**.
   - Ketik: **`#,##0.0,,"M"`** (decimal 1, suffix M).
4. Klik di luar dialog.

Sekarang label tampil `125,0M`, `21,0M`, dst.

### Step 8 — Color (opsional)
1. **Drag `jumlah_penumpang`** ke **Color** di Marks card → bar pakai sequential palette berdasarkan magnitude.
2. Atau biarkan warna tunggal default.

---

## Cross-Check ke Python

Setelah Group jadi, top 15 harus tampil seperti ini (DKI JAKARTA dan KALIMANTAN TIMUR sudah merged):

| Rank | Provinsi (Cleaned) | Total Pax (juta) — harus match |
|---:|---|---:|
| 1 | **DKI JAKARTA** (Jakarta + DKI Jakarta) | **124,8** |
| 2 | **KALIMANTAN TIMUR** (East Kalimantan + Kalimantan Timur) | **21,0** |
| 3 | KEPULAUAN RIAU (Riau Islands + Kepulauan Riau) | 14,6 |
| 4 | BALI | 13,2 |
| 5 | KALIMANTAN SELATAN | 10,7 |
| 6 | PAPUA | 7,0 |
| 7 | JAWA TIMUR | 5,9 |
| 8 | NUSA TENGGARA TIMUR | 3,7 |
| 9 | PAPUA BARAT | 3,4 |
| 10 | MALUKU | 3,3 |
| 11 | SULAWESI TENGGARA | 3,1 |
| 12 | NUSA TENGGARA BARAT | 2,9 |
| 13 | SULAWESI UTARA | 2,8 |
| 14 | RIAU | ~2,5 |
| 15 | KALIMANTAN BARAT atau LAINNYA | ~2,3 |

Bar pertama (DKI JAKARTA) harus **3x lipat** dari bar kedua (KALIMANTAN TIMUR). Kalau tampil duplikat (JAKARTA dan DKI JAKARTA terpisah) → Step 1 Group belum berhasil, ulangi.

---

## Bonus: Sheet Pendamping Peta Provinsi (Opsional)

Kalau punya waktu dan mau impressive untuk presentasi:

### Step 9 — Buat worksheet `Bab5_WS5b_PetaProvinsi`
1. Buat worksheet baru, rename `Bab5_WS5b_PetaProvinsi`.
2. **Filter `kategori` = DOMESTIK** (sama seperti Step 3).
3. **Double-click `Provinsi (Cleaned)`** di Data pane — Tableau auto-detect sebagai geographic role.
4. Kalau peta yang muncul **dunia** (bukan Indonesia):
   - Klik kanan `Provinsi (Cleaned)` di Data pane → **Geographic Role** → **State/Province**.
5. Kalau ada provinsi yang **unrecognized** (Tableau tidak kenal):
   - Klik tombol kecil "X unknown" di pojok kanan-bawah peta → **Edit Locations**.
   - Country: **Indonesia**.
   - Untuk tiap unrecognized name, pilih dari dropdown.
6. **Show Me** (kanan atas) → pilih **Symbol Map** atau **Filled Map**.
7. **Drag `jumlah_penumpang`** ke **Size** di Marks card.
8. **(Opsional)** Drag `jumlah_penumpang` ke **Color** juga (sequential palette).

### Catatan Peta
- Tableau geocoding untuk Indonesia kadang tidak lengkap (provinsi baru seperti PAPUA PEGUNUNGAN, PAPUA SELATAN, PAPUA TENGAH bisa unrecognized).
- Kalau peta terlalu repot, **bar chart Step 1-8 sudah cukup** untuk paper. Peta jadi bonus visual untuk dashboard.

---

## Validasi Akhir
✅ Kalau bar paling atas tampil **DKI JAKARTA dengan ~125M**, dan KALIMANTAN TIMUR dengan ~21M, kerjaan WS5 selesai.

❌ Kalau masih tampil JAKARTA + DKI JAKARTA terpisah, atau EAST KALIMANTAN + KALIMANTAN TIMUR terpisah, ulangi Step 1 (Group manual).
