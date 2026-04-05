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
    output_path="D:\\Kuliah\\projek_dw\\Table_Pilihan\\BAB VII — Lalu Lintas Bandara\\DATA LALU LINTAS ANGKUTAN UDARA DI BANDAR UDARA TAHUN 2016 - 2020.pdf",  # Folder + Nama File
    start_page=157,
    end_page=192
)
extract_pdf_range(
    input_path="D:\\Kuliah\\projek_dw\\DJPU\\Statistik Angkutan Udara\\Statistik Angkutan Udara Tahun 2020.pdf",
    output_path="D:\\Kuliah\\projek_dw\\Table_Pilihan\\BAB VII — Lalu Lintas Bandara\\DATA LALU LINTAS ANGKUTAN PENUMPANG DAN KARGO DALAM NEGERI DI BANDAR UDARA INDONESIA TAHUN 2020.pdf",  # Folder + Nama File
    start_page=193,
    end_page=196
)
extract_pdf_range(
    input_path="D:\\Kuliah\\projek_dw\\DJPU\\Statistik Angkutan Udara\\Statistik Angkutan Udara Tahun 2020.pdf",
    output_path="D:\\Kuliah\\projek_dw\\Table_Pilihan\\BAB VII — Lalu Lintas Bandara\\DATA LALU LINTAS ANGKUTAN PENUMPANG DAN KARGO LUAR NEGERI DI BANDAR UDARA INDONESIA TAHUN 2020.pdf",  # Folder + Nama File
    start_page=197,
    end_page=197
)
extract_pdf_range(
    input_path="D:\\Kuliah\\projek_dw\\DJPU\\Statistik Angkutan Udara\\Statistik Angkutan Udara Tahun 2020.pdf",
    output_path="D:\\Kuliah\\projek_dw\\Table_Pilihan\\BAB VII — Lalu Lintas Bandara\\KOMPOSISI PENUMPANG BERDASARKAN PENGELOLA BANDAR UDARA TAHUN 2020.pdf",  # Folder + Nama File
    start_page=198,
    end_page=198
)

# 2021
extract_pdf_range(
   input_path="D:\\Kuliah\\projek_dw\\DJPU\\Statistik Angkutan Udara\\Statistik Angkutan Udara Tahun 2021.pdf",
    output_path="D:\\Kuliah\\projek_dw\\Table_Pilihan\\BAB VII — Lalu Lintas Bandara\\DATA LALU LINTAS ANGKUTAN UDARA DI BANDAR UDARA TAHUN 2017 - 2021.pdf",  # Folder + Nama File
    start_page=159,
    end_page=194
)
extract_pdf_range(
    input_path="D:\\Kuliah\\projek_dw\\DJPU\\Statistik Angkutan Udara\\Statistik Angkutan Udara Tahun 2021.pdf",
    output_path="D:\\Kuliah\\projek_dw\\Table_Pilihan\\BAB VII — Lalu Lintas Bandara\\DATA LALU LINTAS ANGKUTAN PENUMPANG DAN KARGO DALAM NEGERI DI BANDAR UDARA INDONESIA TAHUN 2021.pdf",  # Folder + Nama File
    start_page=195,
    end_page=198
)
extract_pdf_range(
    input_path="D:\\Kuliah\\projek_dw\\DJPU\\Statistik Angkutan Udara\\Statistik Angkutan Udara Tahun 2021.pdf",
    output_path="D:\\Kuliah\\projek_dw\\Table_Pilihan\\BAB VII — Lalu Lintas Bandara\\DATA LALU LINTAS ANGKUTAN PENUMPANG DAN KARGO LUAR NEGERI DI BANDAR UDARA INDONESIA TAHUN 2021.pdf",  # Folder + Nama File
    start_page=199,
    end_page=199
)
extract_pdf_range(
    input_path="D:\\Kuliah\\projek_dw\\DJPU\\Statistik Angkutan Udara\\Statistik Angkutan Udara Tahun 2021.pdf",
    output_path="D:\\Kuliah\\projek_dw\\Table_Pilihan\\BAB VII — Lalu Lintas Bandara\\KOMPOSISI PENUMPANG BERDASARKAN PENGELOLA BANDAR UDARA TAHUN 2021.pdf",  # Folder + Nama File
    start_page=200,
    end_page=200
)

# 2022
extract_pdf_range(
   input_path="D:\\Kuliah\\projek_dw\\DJPU\\Statistik Angkutan Udara\\Statistik Angkutan Udara Tahun 2022.pdf",
    output_path="D:\\Kuliah\\projek_dw\\Table_Pilihan\\BAB VII — Lalu Lintas Bandara\\DATA LALU LINTAS ANGKUTAN UDARA DI BANDAR UDARA TAHUN 2018 - 2022.pdf",  # Folder + Nama File
    start_page=196,
    end_page=233
)
extract_pdf_range(
    input_path="D:\\Kuliah\\projek_dw\\DJPU\\Statistik Angkutan Udara\\Statistik Angkutan Udara Tahun 2022.pdf",
    output_path="D:\\Kuliah\\projek_dw\\Table_Pilihan\\BAB VII — Lalu Lintas Bandara\\DATA LALU LINTAS ANGKUTAN PENUMPANG DAN KARGO DALAM NEGERI DI BANDAR UDARA INDONESIA TAHUN 2022.pdf",  # Folder + Nama File
    start_page=234,
    end_page=237
)
extract_pdf_range(
    input_path="D:\\Kuliah\\projek_dw\\DJPU\\Statistik Angkutan Udara\\Statistik Angkutan Udara Tahun 2022.pdf",
    output_path="D:\\Kuliah\\projek_dw\\Table_Pilihan\\BAB VII — Lalu Lintas Bandara\\DATA LALU LINTAS ANGKUTAN PENUMPANG DAN KARGO LUAR NEGERI DI BANDAR UDARA INDONESIA TAHUN 2022.pdf",  # Folder + Nama File
    start_page=238,
    end_page=238
)
extract_pdf_range(
    input_path="D:\\Kuliah\\projek_dw\\DJPU\\Statistik Angkutan Udara\\Statistik Angkutan Udara Tahun 2022.pdf",
    output_path="D:\\Kuliah\\projek_dw\\Table_Pilihan\\BAB VII — Lalu Lintas Bandara\\KOMPOSISI PENUMPANG BERDASARKAN PENGELOLA BANDAR UDARA TAHUN 2022.pdf",  # Folder + Nama File
    start_page=239,
    end_page=239
)

# 2023
extract_pdf_range(
   input_path="D:\\Kuliah\\projek_dw\\DJPU\\Statistik Angkutan Udara\\Statistik Angkutan Udara Tahun 2023.pdf",
    output_path="D:\\Kuliah\\projek_dw\\Table_Pilihan\\BAB VII — Lalu Lintas Bandara\\DATA LALU LINTAS ANGKUTAN UDARA DI BANDAR UDARA TAHUN 2020 - 2024.pdf",  # Folder + Nama File
    start_page=139,
    end_page=212
)
extract_pdf_range(
    input_path="D:\\Kuliah\\projek_dw\\DJPU\\Statistik Angkutan Udara\\Statistik Angkutan Udara Tahun 2023.pdf",
    output_path="D:\\Kuliah\\projek_dw\\Table_Pilihan\\BAB VII — Lalu Lintas Bandara\\DATA LALU LINTAS ANGKUTAN PENUMPANG DAN KARGO DALAM NEGERI DI BANDAR UDARA INDONESIA TAHUN 2023.pdf",  # Folder + Nama File
    start_page=213,
    end_page=220
)
extract_pdf_range(
    input_path="D:\\Kuliah\\projek_dw\\DJPU\\Statistik Angkutan Udara\\Statistik Angkutan Udara Tahun 2023.pdf",
    output_path="D:\\Kuliah\\projek_dw\\Table_Pilihan\\BAB VII — Lalu Lintas Bandara\\DATA LALU LINTAS ANGKUTAN PENUMPANG DAN KARGO LUAR NEGERI DI BANDAR UDARA INDONESIA TAHUN 2023.pdf",  # Folder + Nama File
    start_page=221,
    end_page=222
)
extract_pdf_range(
    input_path="D:\\Kuliah\\projek_dw\\DJPU\\Statistik Angkutan Udara\\Statistik Angkutan Udara Tahun 2023.pdf",
    output_path="D:\\Kuliah\\projek_dw\\Table_Pilihan\\BAB VII — Lalu Lintas Bandara\\KOMPOSISI PENUMPANG BERDASARKAN PENGELOLA BANDAR UDARA TAHUN 2023.pdf",  # Folder + Nama File
    start_page=223,
    end_page=223
)

# 2024
extract_pdf_range(
   input_path="D:\\Kuliah\\projek_dw\\DJPU\\Statistik Angkutan Udara\\Statistik Angkutan Udara Tahun 2024.pdf",
    output_path="D:\\Kuliah\\projek_dw\\Table_Pilihan\\BAB VII — Lalu Lintas Bandara\\DATA LALU LINTAS ANGKUTAN UDARA DI BANDAR UDARA TAHUN 2020 - 2024.pdf",  # Folder + Nama File
    start_page=125,
    end_page=164
)
extract_pdf_range(
    input_path="D:\\Kuliah\\projek_dw\\DJPU\\Statistik Angkutan Udara\\Statistik Angkutan Udara Tahun 2024.pdf",
    output_path="D:\\Kuliah\\projek_dw\\Table_Pilihan\\BAB VII — Lalu Lintas Bandara\\DATA LALU LINTAS ANGKUTAN PENUMPANG DAN KARGO DALAM NEGERI DI BANDAR UDARA INDONESIA TAHUN 2024.pdf",  # Folder + Nama File
    start_page=165,
    end_page=168
)
extract_pdf_range(
    input_path="D:\\Kuliah\\projek_dw\\DJPU\\Statistik Angkutan Udara\\Statistik Angkutan Udara Tahun 2024.pdf",
    output_path="D:\\Kuliah\\projek_dw\\Table_Pilihan\\BAB VII — Lalu Lintas Bandara\\DATA LALU LINTAS ANGKUTAN PENUMPANG DAN KARGO LUAR NEGERI DI BANDAR UDARA INDONESIA TAHUN 2024.pdf",  # Folder + Nama File
    start_page=169,
    end_page=169
)
extract_pdf_range(
    input_path="D:\\Kuliah\\projek_dw\\DJPU\\Statistik Angkutan Udara\\Statistik Angkutan Udara Tahun 2024.pdf",
    output_path="D:\\Kuliah\\projek_dw\\Table_Pilihan\\BAB VII — Lalu Lintas Bandara\\KOMPOSISI PENUMPANG BERDASARKAN PENGELOLA BANDAR UDARA TAHUN 2024.pdf",  # Folder + Nama File
    start_page=170,
    end_page=170
)