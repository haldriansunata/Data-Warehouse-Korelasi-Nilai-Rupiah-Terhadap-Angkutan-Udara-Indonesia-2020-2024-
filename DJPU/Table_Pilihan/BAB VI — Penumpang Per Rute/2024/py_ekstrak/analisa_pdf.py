import pdfplumber
import os

# Daftar file PDF
pdf_files = [
    "JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI JAN-DES 2024.pdf",
    "STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2024 BERDASARKAN URUTAN JUMLAH PENUMPANG.pdf",
    "JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI BULAN JANUARI S.D DESEMBER TAHUN 2024.pdf",
    "STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI TAHUN 2024 BERDASARKAN URUTAN JUMLAH PENUMPANG.pdf"
]

base_dir = r"D:\Kuliah\projek_dw\Table_Pilihan\BAB VI — Penumpang Per Rute\2024"

for pdf_file in pdf_files:
    pdf_path = os.path.join(base_dir, pdf_file)
    print(f"\n{'='*80}")
    print(f"FILE: {pdf_file}")
    print(f"{'='*80}")
    
    with pdfplumber.open(pdf_path) as pdf:
        print(f"Jumlah halaman: {len(pdf.pages)}")
        
        for i, page in enumerate(pdf.pages):
            print(f"\n--- Halaman {i+1} ---")
            tables = page.extract_tables()
            print(f"Jumlah tabel di halaman ini: {len(tables)}")
            
            for j, table in enumerate(tables):
                print(f"\nTabel {j+1}:")
                print(f"  Jumlah baris: {len(table)}")
                if table:
                    print(f"  Jumlah kolom: {len(table[0])}")
                    # Print header rows
                    print(f"  Header (3 baris pertama):")
                    for row_idx, row in enumerate(table[:3]):
                        print(f"    Row {row_idx}: {row}")
                    
                    # Print last row
                    if len(table) > 3:
                        print(f"  Last row: {table[-1]}")
                    
                    # Check for repeated headers
                    if len(table) > 1:
                        header = table[0]
                        repeats = sum(1 for row in table[1:] if row == header)
                        if repeats > 0:
                            print(f"  ⚠️ Header diulang {repeats} kali")
