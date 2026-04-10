import pdfplumber

pdf_path = r"D:\Kuliah\projek_dw\Table_Pilihan\BAB VI — Penumpang Per Rute\2023\STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2023 BERDASARKAN URUTAN JUMLAH PENUMPANG.pdf"

with pdfplumber.open(pdf_path) as pdf:
    print(f"Total halaman: {len(pdf.pages)}")
    
    for i, page in enumerate(pdf.pages):
        print(f"\n{'='*80}")
        print(f"HALAMAN {i+1}")
        print(f"{'='*80}")
        
        tables = page.extract_tables()
        
        if tables:
            table = tables[0]
            print(f"Jumlah baris: {len(table)}")
            print(f"Headers: {table[0]}")
            
            # Show first 5 rows in detail
            print(f"\nDetail 5 baris pertama:")
            for row_idx, row in enumerate(table[:6]):
                print(f"\n  Baris {row_idx}:")
                for col_idx, cell in enumerate(row):
                    print(f"    Kolom {col_idx}: {repr(cell)}")
