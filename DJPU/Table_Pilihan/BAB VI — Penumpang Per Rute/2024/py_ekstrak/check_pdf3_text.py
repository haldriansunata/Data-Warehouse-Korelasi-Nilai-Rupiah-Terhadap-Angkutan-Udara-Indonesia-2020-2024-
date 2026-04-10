import pdfplumber
import os

BASE_DIR = r"D:\Kuliah\projek_dw\Table_Pilihan\BAB VI — Penumpang Per Rute\2024"
pdf_file = "JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI BULAN JANUARI S.D DESEMBER TAHUN 2024.pdf"
pdf_path = os.path.join(BASE_DIR, pdf_file)

print("Extracting all text from page 3 to understand structure:")

with pdfplumber.open(pdf_path) as pdf:
    page = pdf.pages[2]
    
    # Get text
    text = page.extract_text()
    print("\n--- FULL TEXT ---")
    print(text[:2000])
