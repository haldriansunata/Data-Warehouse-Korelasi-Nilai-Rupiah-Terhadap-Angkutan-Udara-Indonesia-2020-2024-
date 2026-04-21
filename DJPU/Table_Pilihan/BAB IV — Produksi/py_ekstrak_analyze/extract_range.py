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
    output_path="D:\\Kuliah\\projek_dw\\Table_Pilihan\\BAB IV — Produksi\\Produksi Angkutan Udara Niaga Berjadwal Dalam Negeri 2016-2020.pdf",  # Folder + Nama File
    start_page=37,
    end_page=53
)

# 2021
extract_pdf_range(
    input_path="D:\\Kuliah\\projek_dw\\DJPU\\Statistik Angkutan Udara\\Statistik Angkutan Udara Tahun 2021.pdf",
    output_path="D:\\Kuliah\\projek_dw\\Table_Pilihan\\BAB IV — Produksi\\Produksi Angkutan Udara Niaga Berjadwal Dalam Negeri 2017-2021.pdf",  # Folder + Nama File
    start_page=39,
    end_page=56
)

# 2022
extract_pdf_range(
    input_path="D:\\Kuliah\\projek_dw\\DJPU\\Statistik Angkutan Udara\\Statistik Angkutan Udara Tahun 2022.pdf",
    output_path="D:\\Kuliah\\projek_dw\\Table_Pilihan\\BAB IV — Produksi\\Produksi Angkutan Udara Niaga Berjadwal Dalam Negeri 2018-2022.pdf",  # Folder + Nama File
    start_page=69,
    end_page=86
)

# 2023
extract_pdf_range(
    input_path="D:\\Kuliah\\projek_dw\\DJPU\\Statistik Angkutan Udara\\Statistik Angkutan Udara Tahun 2023.pdf",
    output_path="D:\\Kuliah\\projek_dw\\Table_Pilihan\\BAB IV — Produksi\\Produksi Angkutan Udara Niaga Berjadwal Dalam Negeri 2019-2023.pdf",  # Folder + Nama File
    start_page=47,
    end_page=55
)

# 2024
extract_pdf_range(
    input_path="D:\\Kuliah\\projek_dw\\DJPU\\Statistik Angkutan Udara\\Statistik Angkutan Udara Tahun 2024.pdf",
    output_path="D:\\Kuliah\\projek_dw\\Table_Pilihan\\BAB IV — Produksi\\Produksi Angkutan Udara Niaga Berjadwal Dalam Negeri 2020 - 2024.pdf",  # Folder + Nama File
    start_page=45,
    end_page=54
)