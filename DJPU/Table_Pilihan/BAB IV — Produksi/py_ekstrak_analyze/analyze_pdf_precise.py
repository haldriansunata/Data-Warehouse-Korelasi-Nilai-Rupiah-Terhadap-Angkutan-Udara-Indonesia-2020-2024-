import pdfplumber
import os

pdf_path = r"D:\Kuliah\projek_dw\DJPU\Table_Pilihan\BAB IV — Produksi\PDF\PRODUKSI ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI 2020 - 2024 PERUSAHAAN ANGKUTAN UDARA ASING\PRODUKSI ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI 2020 - 2024 PERUSAHAAN ANGKUTAN UDARA ASING.pdf"

def get_long_path(p):
    p = os.path.abspath(p)
    if not p.startswith("\\\\?\\") and os.name == 'nt':
        return "\\\\?\\" + p
    return p

pdf_path_long = get_long_path(pdf_path)

with pdfplumber.open(pdf_path_long) as pdf:
    for i, page in enumerate(pdf.pages):
        text = page.extract_text()
        if not text:
            continue
            
        print(f"--- Halaman {i + 1} ---")
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        table_titles = []
        for j, line in enumerate(lines):
            if "NO DISCRIPTION" in line or "NO DESCRIPTION" in line:
                if j > 0:
                    title = lines[j-1]
                    # Fallback check if the title just grabbed was the category name
                    if title == "PERUSAHAAN ANGKUTAN UDARA ASING" and j > 1:
                         title = lines[j-2]
                    table_titles.append(title)
        
        print(f"Jumlah Tabel: {len(table_titles)}")
        if table_titles:
            for idx, title in enumerate(table_titles):
                print(f"  Judul Tabel {idx + 1}: {title}")
