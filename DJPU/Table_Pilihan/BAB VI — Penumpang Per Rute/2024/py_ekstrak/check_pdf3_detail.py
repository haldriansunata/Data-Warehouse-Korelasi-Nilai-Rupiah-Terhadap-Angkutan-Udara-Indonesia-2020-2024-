import pdfplumber
import os

BASE_DIR = r"D:\Kuliah\projek_dw\Table_Pilihan\BAB VI — Penumpang Per Rute\2024"
pdf_file = "JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI BULAN JANUARI S.D DESEMBER TAHUN 2024.pdf"
pdf_path = os.path.join(BASE_DIR, pdf_file)

print(f"Detail page 3:")

with pdfplumber.open(pdf_path) as pdf:
    page = pdf.pages[2]  # Page 3 (index 2)
    table = page.extract_tables()[0]
    
    print(f"Total rows: {len(table)}")
    print("\nAll rows (NO, RUTE):")
    for i, row in enumerate(table):
        print(f"  {i}: NO={row[0]}, RUTE={row[1]}")
