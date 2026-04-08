import pdfplumber
import pandas as pd
import os

# Directory containing the PDFs
pdf_dir = r"D:\Kuliah\projek_dw\Table_Pilihan\BAB VI — Penumpang Per Rute\2020"

# List of PDF files to analyze
pdf_files = [
    "JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI JAN-DES 2020.pdf",
    "JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI BULAN JANUARI S.D DESEMBER TAHUN 2020.pdf",
    "STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2020 BERDASARKAN URUTAN JUMLAH PENUMPANG.pdf",
    "STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI TAHUN 2020 BERDASARKAN URUTAN JUMLAH PENUMPANG.pdf"
]

# Analyze each PDF
for pdf_file in pdf_files:
    pdf_path = os.path.join(pdf_dir, pdf_file)
    print(f"\n{'='*100}")
    print(f"ANALYZING: {pdf_file}")
    print(f"{'='*100}")
    
    with pdfplumber.open(pdf_path) as pdf:
        print(f"Total pages: {len(pdf.pages)}")
        
        for page_num, page in enumerate(pdf.pages, 1):
            print(f"\n--- Page {page_num} ---")
            
            # Extract text to see titles/headers
            text = page.extract_text()
            if text:
                # Print first 500 chars of text to see titles
                print(f"Text preview (first 500 chars):\n{text[:500]}")
            
            # Extract tables
            tables = page.extract_tables()
            print(f"\nNumber of tables found: {len(tables)}")
            
            for table_idx, table in enumerate(tables):
                print(f"\nTable {table_idx + 1}:")
                print(f"  Rows: {len(table)}")
                if table:
                    print(f"  Columns: {len(table[0])}")
                    # Print first 5 rows to see structure
                    print(f"  First 5 rows:")
                    for row_idx, row in enumerate(table[:5]):
                        print(f"    Row {row_idx}: {row}")

print("\n\nAnalysis complete!")
