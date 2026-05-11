# Merge & Transformation Summary - 2023 PERTAMINA Data

## Overview
Script berhasil merge dan transform data 2023 dari 4 sumber file menjadi 1 file output yang terstruktur.

## Input Files

### Existing File
- **exel2023.csv** - File utama yang sudah ada dengan data dari berbagai bulan

### New Files Added
- **20230201082329pdf_1-14 Februari 2023.csv** - Data Februari 1-14
- **20230215022333pdf_15-28 Februari 2023.csv** - Data Februari 15-28
- **20230301022720pdf_1-14 Maret 2023.csv** - Data Maret 1-14

## Output File
- **merged_transformed_exel2023.csv** - File hasil merge dan transformasi

## Processing Details

### Data Loaded
- Total records loaded: 1,725 rows
- Data sources: 22 file PDF/CSV dari berbagai periode bulan

### Data Transformation
- Total records in output: 865 rows (dengan weighted average untuk split entries)

### Columns in Output
1. **Year** - Tahun (2023)
2. **Month** - Bulan (01-12)
3. **No** - Nomor urut lokasi (1-72)
4. **Location** - Nama bandara
5. **City** - Kota
6. **IATA_Code** - Kode IATA bandara
7. **International_Flight_Price_USCents_Liter** - Harga internasional (USCents/Liter)
8. **Domestic_Flight_Price_Into_Plane_Rp_Liter** - Harga domestik ke pesawat (Rp/Liter)
9. **Domestic_Flight_Price_One_Time_Customer_Rp_Liter** - Harga domestik one-time customer (Rp/Liter)
10. **Source** - Sumber file data

## Data Aggregation by Month

| Month | Records | Notes |
|-------|---------|-------|
| 01 (Januari) | 72 | Merged dari 2 file (1-14 & 15-31) |
| 02 (Februari) | 71 | **NEWLY ADDED** - Merged dari 2 file (1-14 & 15-28) |
| 03 (Maret) | 72 | Merged dengan 1-14 baru + existing 15-31 |
| 04-12 (April-Desember) | 72-73 | Data existing dari exel2023.csv |

## Weighted Average Calculation

Untuk data yang terbagi menjadi 2 periode (misalnya 1-14 dan 15-31), script menghitung weighted average berdasarkan jumlah hari:

**Formula:**
```
Weighted_Average = (Value_Half1 × Days_Half1 + Value_Half2 × Days_Half2) / Total_Days
```

**Contoh (Februari):**
- PATTIMURA (AMQ):
  - 1-14 Februari: 105.40 (14 hari)
  - 15-28 Februari: 106.20 (14 hari)
  - Weighted Average: (105.40×14 + 106.20×14) / 28 = **105.80**

## Verification

- ✅ Semua 3 file baru berhasil di-merge
- ✅ Data Februari (02) sekarang ada dalam output
- ✅ Data Maret (03) sudah merged dengan data baru
- ✅ Weighted average sudah dihitung dengan benar
- ✅ Source information mencatat kombinasi file untuk setiap merged entry
- ✅ Format kolom sesuai dengan spesifikasi yang diminta

## File Location
- Script: `c:\Users\Haldrian\OneDrive\Desktop\data_tambahan\PERTAMINA\PDF\2023\merge_transform_2023.py`
- Output: `c:\Users\Haldrian\OneDrive\Desktop\data_tambahan\PERTAMINA\PDF\2023\merged_transformed_exel2023.csv`

---
*Generated on: May 11, 2026*
