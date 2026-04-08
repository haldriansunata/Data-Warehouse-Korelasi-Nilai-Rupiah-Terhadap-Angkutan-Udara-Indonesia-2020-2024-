import pdfplumber
import os

# Directory containing the PDFs
pdf_dir = r"D:\Kuliah\projek_dw\Table_Pilihan\BAB VI — Penumpang Per Rute\2023"

# List all PDF files
pdf_files = [
    "JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI JAN-DES 2023.pdf",
    "STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2023 BERDASARKAN URUTAN JUMLAH PENUMPANG.pdf",
    "JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI BULAN JANUARI S.D DESEMBER TAHUN 2023.pdf",
    "STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI TAHUN 2023 BERDASARKAN URUTAN JUMLAH PENUMPANG.pdf"
]

# Analyze each PDF
for pdf_file in pdf_files:
    pdf_path = os.path.join(pdf_dir, pdf_file)
    print(f"\n{'='*80}")
    print(f"FILE: {pdf_file}")
    print(f"{'='*80}")
    
    with pdfplumber.open(pdf_path) as pdf:
        print(f"Total halaman: {len(pdf.pages)}")
        
        for i, page in enumerate(pdf.pages):
            print(f"\n--- Halaman {i+1} ---")
            
            # Extract tables
            tables = page.extract_tables()
            
            if not tables:
                print("  [!] Tidak ada tabel terdeteksi di halaman ini")
                continue
            
            print(f"  Jumlah tabel ditemukan: {len(tables)}")
            
            for t_idx, table in enumerate(tables):
                print(f"\n  Tabel #{t_idx+1}:")
                print(f"  Jumlah baris: {len(table)}")
                
                if len(table) > 0:
                    # Show headers (first row)
                    headers = table[0]
                    print(f"  Headers: {headers}")
                    print(f"  Jumlah kolom: {len(headers)}")
                    
                    # Show first 3 data rows
                    print(f"  Sample data (3 baris pertama):")
                    for row_idx, row in enumerate(table[1:min(4, len(table))]):
                        print(f"    Baris {row_idx+1}: {row}")
                    
                    # Show last 2 rows
                    if len(table) > 4:
                        print(f"  Sample data (2 baris terakhir):")
                        for row_idx, row in enumerate(table[-2:]):
                            print(f"    Baris {len(table)-2+row_idx+1}: {row}")
                    
                    # Check for anomalies
                    print(f"\n  Anomali terdeteksi:")
                    for row_idx, row in enumerate(table):
                        for col_idx, cell in enumerate(row):
                            if cell is None or cell == "" or cell == "-":
                                print(f"    - Baris {row_idx}, Kolom {col_idx}: Nilai kosong/None/'-'")
                            elif isinstance(cell, str) and "  " in cell:
                                print(f"    - Baris {row_idx}, Kolom {col_idx}: Multi-space ditemukan: '{cell[:30]}...'")
                            elif isinstance(cell, str) and "\n" in cell:
                                print(f"    - Baris {row_idx}, Kolom {col_idx}: Multi-line text: '{cell[:30]}...'")
                    
                    # Check if header repeats
                    if i > 0 and len(tables) > 0:
                        print(f"\n  [NOTE] Periksa apakah header sama dengan halaman sebelumnya")

print("\n" + "="*80)
print("ANALISA SELESAI")
print("="*80)
