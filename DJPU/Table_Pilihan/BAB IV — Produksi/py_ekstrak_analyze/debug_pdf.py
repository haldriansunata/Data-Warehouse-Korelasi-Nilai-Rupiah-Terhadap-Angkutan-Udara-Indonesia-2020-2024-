import pdfplumber
import os

pdf_path = r"D:\Kuliah\projek_dw\DJPU\Table_Pilihan\BAB IV — Produksi\PDF\PRODUKSI ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI 2020 - 2024 BADAN USAHA ANGKUTAN UDARA NASIONAL\PRODUKSI ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI 2020 - 2024 BADAN USAHA ANGKUTAN UDARA NASIONAL.pdf"
    
def get_long_path(p):
    p = os.path.abspath(p)
    if not p.startswith("\\\\?\\") and os.name == 'nt':
        return "\\\\?\\" + p
    return p
    
with pdfplumber.open(get_long_path(pdf_path)) as pdf:
    text = pdf.pages[0].extract_text()
    print(text)
    print("="*40)
    tables = pdf.pages[0].extract_tables(table_settings={"vertical_strategy": "text", "horizontal_strategy": "text"})
    for table in tables:
        print(table)
