import pdfplumber
import os

BASE_DIR = r"D:\Kuliah\projek_dw\Table_Pilihan\BAB VI — Penumpang Per Rute\2024"
pdf_file = "JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI BULAN JANUARI S.D DESEMBER TAHUN 2024.pdf"
pdf_path = os.path.join(BASE_DIR, pdf_file)

print(f"Checking: {pdf_file}")

with pdfplumber.open(pdf_path) as pdf:
    print(f"Total pages: {len(pdf.pages)}")
    
    for i, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        print(f"\n--- Page {i+1} ---")
        print(f"Tables: {len(tables)}")
        
        if tables:
            table = tables[0]
            print(f"Rows in table: {len(table)}")
            
            # Print first 3 rows
            print(f"First 3 rows:")
            for j, row in enumerate(table[:3]):
                print(f"  {j}: {row}")
            
            # Print last 2 rows
            if len(table) > 2:
                print(f"Last 2 rows:")
                for j, row in enumerate(table[-2:]):
                    print(f"  {len(table)-2+j}: {row}")
