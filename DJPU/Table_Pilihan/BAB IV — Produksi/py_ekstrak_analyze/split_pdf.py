import os
from pypdf import PdfReader, PdfWriter

def split_pdf(source_path, splits):
    """
    Split PDF into multiple files based on page ranges.
    Supports long paths on Windows using the \\?\ prefix.
    """
    def get_long_path(p):
        p = os.path.abspath(p)
        if not p.startswith("\\\\?\\") and os.name == 'nt':
            return "\\\\?\\" + p
        return p

    source_path_long = get_long_path(source_path)
    if not os.path.exists(source_path_long):
        print(f"Error: Source file not found: {source_path}")
        return

    reader = PdfReader(source_path_long)
    total_pages = len(reader.pages)
    print(f"Source PDF loaded. Total pages: {total_pages}")

    for split in splits:
        output_dir = split['output_dir']
        output_name = split['output_name']
        start_page, end_page = split['pages']
        
        output_dir_long = get_long_path(output_dir)
        
        # Ensure directory exists
        if not os.path.exists(output_dir_long):
            os.makedirs(output_dir_long, exist_ok=True)
            print(f"Created directory: {output_dir}")

        writer = PdfWriter()
        
        # pypdf indexing: 0-indexed
        # range(start, end) goes up to end-1
        for page_num in range(start_page - 1, min(end_page, total_pages)):
            writer.add_page(reader.pages[page_num])

        output_path = os.path.join(output_dir, f"{output_name}.pdf")
        output_path_long = get_long_path(output_path)
        
        try:
            with open(output_path_long, "wb") as output_file:
                writer.write(output_file)
            print(f"Successfully saved pages {start_page}-{end_page} to:\n{output_path}\n")
        except Exception as e:
            print(f"Error saving to {output_path}: {e}")

if __name__ == "__main__":
    # Source PDF path
    SOURCE_PDF = r"D:\Kuliah\projek_dw\DJPU\Statistik Angkutan Udara\PDF\Statistik Angkutan Udara Tahun 2024.pdf"
    
    # Base folder
    BASE_OUTPUT = r"D:\Kuliah\projek_dw\DJPU\Table_Pilihan\BAB IV — Produksi\PDF"
    
    # Configuration for splits
    SPLITS = [
        {
            "output_dir": os.path.join(BASE_OUTPUT, "PRODUKSI ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI 2020 - 2024 BADAN USAHA ANGKUTAN UDARA NASIONAL"),
            "output_name": "PRODUKSI ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI 2020 - 2024 BADAN USAHA ANGKUTAN UDARA NASIONAL",
            "pages": (55, 60)
        },
        {
            "output_dir": os.path.join(BASE_OUTPUT, "PRODUKSI ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI 2020 - 2024 PERUSAHAAN ANGKUTAN UDARA ASING"),
            "output_name": "PRODUKSI ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI 2020 - 2024 PERUSAHAAN ANGKUTAN UDARA ASING",
            "pages": (61, 94)
        }
    ]

    split_pdf(SOURCE_PDF, SPLITS)
