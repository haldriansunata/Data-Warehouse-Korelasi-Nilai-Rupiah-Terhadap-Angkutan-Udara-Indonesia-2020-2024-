from pypdf import PdfReader, PdfWriter

def extract_pdf_range(input_path, output_path, start_page, end_page):
    reader = PdfReader(input_path)
    writer = PdfWriter()
    
    total_pages = len(reader.pages)
    if start_page < 1 or end_page > total_pages or start_page > end_page:
        raise ValueError(f"Range tidak valid. PDF memiliki {total_pages} halaman.")
        
    for i in range(start_page - 1, end_page):
        writer.add_page(reader.pages[i])
        
    with open(output_path, "wb") as f:
        writer.write(f)
    print(f"✅ Berhasil: {output_path} ({end_page - start_page + 1} halaman)")

# 👇 GANTI SESUAI KEBUTUHANMU:

# 2020
extract_pdf_range(
   input_path="D:\\Kuliah\\projek_dw\\DJPU\\Statistik Angkutan Udara\\Statistik Angkutan Udara Tahun 2020.pdf",
    output_path="D:\\Kuliah\\projek_dw\\Table_Pilihan\\BAB III — Rute & Bandara\\kota_rute_dan_total_domestik_2020.pdf",  # Folder + Nama File
    start_page=27,
    end_page=31
)
extract_pdf_range(
    input_path="D:\\Kuliah\\projek_dw\\DJPU\\Statistik Angkutan Udara\\Statistik Angkutan Udara Tahun 2020.pdf",
    output_path="D:\\Kuliah\\projek_dw\\Table_Pilihan\\BAB III — Rute & Bandara\\kota_rute_dan_total_inter_2020.pdf",  # Folder + Nama File
    start_page=33,
    end_page=35
)

# 2021
extract_pdf_range(
    input_path="D:\\Kuliah\\projek_dw\\DJPU\\Statistik Angkutan Udara\\Statistik Angkutan Udara Tahun 2021.pdf",
    output_path="D:\\Kuliah\\projek_dw\\Table_Pilihan\\BAB III — Rute & Bandara\\kota_rute_dan_total_domestik_2021.pdf",  # Folder + Nama File
    start_page=29,
    end_page=33
)
extract_pdf_range(
    input_path="D:\\Kuliah\\projek_dw\\DJPU\\Statistik Angkutan Udara\\Statistik Angkutan Udara Tahun 2021.pdf",
    output_path="D:\\Kuliah\\projek_dw\\Table_Pilihan\\BAB III — Rute & Bandara\\kota_rute_dan_total_inter_2021.pdf",  # Folder + Nama File
    start_page=35,
    end_page=37
)

# 2022
extract_pdf_range(
    input_path="D:\\Kuliah\\projek_dw\\DJPU\\Statistik Angkutan Udara\\Statistik Angkutan Udara Tahun 2022.pdf",
    output_path="D:\\Kuliah\\projek_dw\\Table_Pilihan\\BAB III — Rute & Bandara\\kota_rute_dan_total_domestik_2022.pdf",  # Folder + Nama File
    start_page=60,
    end_page=64
)
extract_pdf_range(
    input_path="D:\\Kuliah\\projek_dw\\DJPU\\Statistik Angkutan Udara\\Statistik Angkutan Udara Tahun 2022.pdf",
    output_path="D:\\Kuliah\\projek_dw\\Table_Pilihan\\BAB III — Rute & Bandara\\kota_rute_dan_total_inter_2022.pdf",  # Folder + Nama File
    start_page=65,
    end_page=67
)

# 2023
extract_pdf_range(
   input_path="D:\\Kuliah\\projek_dw\\DJPU\\Statistik Angkutan Udara\\Statistik Angkutan Udara Tahun 2023.pdf",
    output_path="D:\\Kuliah\\projek_dw\\Table_Pilihan\\BAB III — Rute & Bandara\\rute_kota_rekapitulasi_domestik_2023.pdf",  # Folder + Nama File
    start_page=34,
    end_page=40
)
extract_pdf_range(
    input_path="D:\\Kuliah\\projek_dw\\DJPU\\Statistik Angkutan Udara\\Statistik Angkutan Udara Tahun 2023.pdf",
    output_path="D:\\Kuliah\\projek_dw\\Table_Pilihan\\BAB III — Rute & Bandara\\rute_kota_rekapitulasi_inter_2023.pdf",  # Folder + Nama File
    start_page=41,
    end_page=45
)

# 2024
extract_pdf_range(
    input_path="D:\\Kuliah\\projek_dw\\DJPU\\Statistik Angkutan Udara\\Statistik Angkutan Udara Tahun 2024.pdf",
    output_path="D:\\Kuliah\\projek_dw\\Table_Pilihan\\BAB III — Rute & Bandara\\kota_rute_dan_total_domestik_2024.pdf",  # Folder + Nama File
    start_page=34,
    end_page=39
)
extract_pdf_range(
    input_path="D:\\Kuliah\\projek_dw\\DJPU\\Statistik Angkutan Udara\\Statistik Angkutan Udara Tahun 2024.pdf",
    output_path="D:\\Kuliah\\projek_dw\\Table_Pilihan\\BAB III — Rute & Bandara\\kota_rute_dan_total_inter_2024.pdf",  # Folder + Nama File
    start_page=40,
    end_page=43
)