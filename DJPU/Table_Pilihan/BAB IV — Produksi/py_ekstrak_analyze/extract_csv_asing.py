import pdfplumber
import os

pdf_path = r"D:\Kuliah\projek_dw\DJPU\Table_Pilihan\BAB IV — Produksi\PDF\PRODUKSI ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI 2020 - 2024 PERUSAHAAN ANGKUTAN UDARA ASING\PRODUKSI ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI 2020 - 2024 PERUSAHAAN ANGKUTAN UDARA ASING.pdf"
out_dir = r"D:\Kuliah\projek_dw\DJPU\Table_Pilihan\BAB IV — Produksi\hasil_ekstrak"

def get_long_path(p):
    p = os.path.abspath(p)
    if not p.startswith("\\\\?\\") and os.name == 'nt':
        return "\\\\?\\" + p
    return p

rules = [
    ("1 Aircraft KM", "1", "Aircraft KM", "(000)"),
    ("2 Aircraft Dep", "2", "Aircraft Departure", "number"),
    ("3 Aircraft Hou", "3", "Aircraft Hours", "number"),
    ("4 Passenger", "4", "Passenger Carried", "number"),
    ("5 Freight", "5", "Freight Carried", "ton"),
    ("6 Passenger KM", "6", "Passenger KM", "(000)"),
    ("7 Available", "7", "Available Seat KM", "(000)"),
    ("8 Passenger L/F", "8", "Passenger L/F", "(%)"),
    ("a. Passeng", "9a", "Ton KM Performed - Passenger", "(000)"),
    ("b. Freight", "9b", "Ton KM Performed - Freight", "(000)"),
    ("c. Mail", "9c", "Ton KM Performed - Mail", "(000)"),
    ("d. Total", "9d", "Ton KM Performed - Total", "(000)"),
    ("10 Available", "10", "Available Ton KM", "(000)"),
    ("11 Weight", "11", "Weight L/F", "(%)")
]

os.makedirs(get_long_path(out_dir), exist_ok=True)

with pdfplumber.open(get_long_path(pdf_path)) as pdf:
    for i, page in enumerate(pdf.pages):
        text = page.extract_text()
        if not text: continue
        
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        for j, line in enumerate(lines):
            if "NO DISCRIPTION" in line or "NO DESCRIPTION" in line:
                title = ""
                if j > 0:
                    title = lines[j-1].strip()
                    if title == "PERUSAHAAN ANGKUTAN UDARA ASING" and j > 1:
                        title = lines[j-2].strip()
                
                # Replace invalid characters in title for filename if any
                safe_title = "".join([c for c in title if c.isalpha() or c.isdigit() or c in (' ', '-', '_', '&')]).strip()

                csv_filename = f"PRODUKSI ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI 2020 - 2024 PERUSAHAAN ANGKUTAN UDARA ASING {safe_title}.csv"
                csv_path = os.path.join(out_dir, csv_filename)
                
                print(f"Menyimpan ke: {csv_filename}")
                with open(get_long_path(csv_path), "w", encoding="utf-8") as f:
                    f.write("NO,DESCRIPTION,Unit,2020,2021,2022,2023,2024\n")
                    
                    found_rules = set()
                    for k in range(j+1, len(lines)):
                        l = lines[k].strip()
                        if "Sumber Data" in l or "NO DISCRIPTION" in l:
                            break
                            
                        for prefix, row_id, desc, unit in rules:
                            if l.startswith(prefix) and row_id not in found_rules:
                                tokens = l.split()
                                if len(tokens) >= 5:
                                    # Ensure quotes for values
                                    y2020, y2021, y2022, y2023, y2024 = tokens[-5:]
                                    f.write(f'{row_id},{desc},{unit},"{y2020}","{y2021}","{y2022}","{y2023}","{y2024}"\n')
                                    found_rules.add(row_id)
                                break
