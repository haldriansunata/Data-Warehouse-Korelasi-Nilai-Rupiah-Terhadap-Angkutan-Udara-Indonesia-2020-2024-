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
    output_path="D:\\Kuliah\\projek_dw\\Table_Pilihan\\BAB VI — Penumpang Per Rute\\STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2020 BERDASARKAN URUTAN JUMLAH PENUMPANG.pdf",  # Folder + Nama File
    start_page=140,
    end_page=149
)
extract_pdf_range(
    input_path="D:\\Kuliah\\projek_dw\\DJPU\\Statistik Angkutan Udara\\Statistik Angkutan Udara Tahun 2020.pdf",
    output_path="D:\\Kuliah\\projek_dw\\Table_Pilihan\\BAB VI — Penumpang Per Rute\\STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI TAHUN 2020 BERDASARKAN URUTAN JUMLAH PENUMPANG.pdf",  # Folder + Nama File
    start_page=153,
    end_page=155
)

# 2021
extract_pdf_range(
   input_path="D:\\Kuliah\\projek_dw\\DJPU\\Statistik Angkutan Udara\\Statistik Angkutan Udara Tahun 2021.pdf",
    output_path="D:\\Kuliah\\projek_dw\\Table_Pilihan\\BAB VI — Penumpang Per Rute\\STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2021 BERDASARKAN URUTAN JUMLAH PENUMPANG.pdf",  # Folder + Nama File
    start_page=143,
    end_page=151
)
extract_pdf_range(
    input_path="D:\\Kuliah\\projek_dw\\DJPU\\Statistik Angkutan Udara\\Statistik Angkutan Udara Tahun 2021.pdf",
    output_path="D:\\Kuliah\\projek_dw\\Table_Pilihan\\BAB VI — Penumpang Per Rute\\STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI TAHUN 2021 BERDASARKAN URUTAN JUMLAH PENUMPANG.pdf",  # Folder + Nama File
    start_page=155,
    end_page=157
)

# 2022
extract_pdf_range(
   input_path="D:\\Kuliah\\projek_dw\\DJPU\\Statistik Angkutan Udara\\Statistik Angkutan Udara Tahun 2022.pdf",
    output_path="D:\\Kuliah\\projek_dw\\Table_Pilihan\\BAB VI — Penumpang Per Rute\\STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2022 BERDASARKAN URUTAN JUMLAH PENUMPANG.pdf",  # Folder + Nama File
    start_page=180,
    end_page=188
)
extract_pdf_range(
    input_path="D:\\Kuliah\\projek_dw\\DJPU\\Statistik Angkutan Udara\\Statistik Angkutan Udara Tahun 2022.pdf",
    output_path="D:\\Kuliah\\projek_dw\\Table_Pilihan\\BAB VI — Penumpang Per Rute\\STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI TAHUN 2022 BERDASARKAN URUTAN JUMLAH PENUMPANG.pdf",  # Folder + Nama File
    start_page=192,
    end_page=194
)

# 2023
extract_pdf_range(
   input_path="D:\\Kuliah\\projek_dw\\DJPU\\Statistik Angkutan Udara\\Statistik Angkutan Udara Tahun 2023.pdf",
    output_path="D:\\Kuliah\\projek_dw\\Table_Pilihan\\BAB VI — Penumpang Per Rute\\STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2023 BERDASARKAN URUTAN JUMLAH PENUMPANG.pdf",  # Folder + Nama File
    start_page=123,
    end_page=128
)
extract_pdf_range(
    input_path="D:\\Kuliah\\projek_dw\\DJPU\\Statistik Angkutan Udara\\Statistik Angkutan Udara Tahun 2023.pdf",
    output_path="D:\\Kuliah\\projek_dw\\Table_Pilihan\\BAB VI — Penumpang Per Rute\\STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI TAHUN 2023 BERDASARKAN URUTAN JUMLAH PENUMPANG.pdf",  # Folder + Nama File
    start_page=135,
    end_page=137
)

# 2024
extract_pdf_range(
   input_path="D:\\Kuliah\\projek_dw\\DJPU\\Statistik Angkutan Udara\\Statistik Angkutan Udara Tahun 2024.pdf",
    output_path="D:\\Kuliah\\projek_dw\\Table_Pilihan\\BAB VI — Penumpang Per Rute\\STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2024 BERDASARKAN URUTAN JUMLAH PENUMPANG.pdf",  # Folder + Nama File
    start_page=112,
    end_page=117
)
extract_pdf_range(
    input_path="D:\\Kuliah\\projek_dw\\DJPU\\Statistik Angkutan Udara\\Statistik Angkutan Udara Tahun 2024.pdf",
    output_path="D:\\Kuliah\\projek_dw\\Table_Pilihan\\BAB VI — Penumpang Per Rute\\STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI TAHUN 2024 BERDASARKAN URUTAN JUMLAH PENUMPANG.pdf",  # Folder + Nama File
    start_page=121,
    end_page=123
)