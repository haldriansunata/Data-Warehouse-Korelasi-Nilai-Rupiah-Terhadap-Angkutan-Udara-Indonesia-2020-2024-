import pdfplumber

pdf_path = r"D:\Kuliah\projek_dw\Table_Pilihan\BAB VI — Penumpang Per Rute\2023\STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2023 BERDASARKAN URUTAN JUMLAH PENUMPANG.pdf"

with pdfplumber.open(pdf_path) as pdf:
    # Check last page for Total row
    last_page = pdf.pages[-1]
    tables = last_page.extract_tables()
    
    if tables:
        table = tables[0]
        print(f"Halaman terakhir - Jumlah baris: {len(table)}")
        print(f"\n5 baris terakhir:")
        for row_idx, row in enumerate(table[-5:]):
            print(f"\n  Baris {len(table)-5+row_idx}:")
            for col_idx, cell in enumerate(row):
                print(f"    Kolom {col_idx}: {repr(cell)}")
