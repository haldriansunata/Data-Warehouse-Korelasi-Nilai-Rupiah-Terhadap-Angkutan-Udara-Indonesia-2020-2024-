import pdfplumber
import os

def analyze_pdf(pdf_path):
    # Fix for Long Path and Em Dash
    def get_long_path(p):
        p = os.path.abspath(p)
        if not p.startswith("\\\\?\\") and os.name == 'nt':
            return "\\\\?\\" + p
        return p
        
    pdf_path_long = get_long_path(pdf_path)
    
    print(f"Analyzing PDF: {pdf_path}")
    try:
        if not os.path.exists(pdf_path_long):
            print(f"Error: Path does not exist. {pdf_path_long}")
            return
            
        with pdfplumber.open(pdf_path_long) as pdf:
            total_pages = len(pdf.pages)
            print(f"Total Pages: {total_pages}\n")
            
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                
                # Extract first a few non-empty lines for Title
                lines = [line.strip() for line in (text or "").split('\n') if line.strip()]
                
                title = ""
                # Title on these reports are usually the first few lines 
                # Let's extract the first 3 lines
                if len(lines) > 0:
                    title = " | ".join(lines[:3])
                
                tables = page.find_tables()
                print(f"--- Page {i + 1} ---")
                print(f"Possible Title: {title}")
                print(f"Tables found: {len(tables)}")
                if len(tables) > 0:
                    for t_idx, table in enumerate(tables):
                        parsed_table = table.extract()
                        print(f"  Table {t_idx + 1}: {len(parsed_table)} rows, {len(parsed_table[0]) if len(parsed_table) > 0 else 0} cols")
                print("-" * 20)
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    pdf_path = r"D:\Kuliah\projek_dw\DJPU\Table_Pilihan\BAB IV — Produksi\PDF\PRODUKSI ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI 2020 - 2024 BADAN USAHA ANGKUTAN UDARA NASIONAL\PRODUKSI ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI 2020 - 2024 BADAN USAHA ANGKUTAN UDARA NASIONAL.pdf"
    analyze_pdf(pdf_path)
