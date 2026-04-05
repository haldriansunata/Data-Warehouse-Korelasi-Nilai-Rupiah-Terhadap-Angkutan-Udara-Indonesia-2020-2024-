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
    output_path="D:\\Kuliah\\projek_dw\\Table_Pilihan\\BAB VI — Penumpang Per Rute\\JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI JAN-DES 2020.pdf",  # Folder + Nama File
    start_page=130,
    end_page=139
)
extract_pdf_range(
    input_path="D:\\Kuliah\\projek_dw\\DJPU\\Statistik Angkutan Udara\\Statistik Angkutan Udara Tahun 2020.pdf",
    output_path="D:\\Kuliah\\projek_dw\\Table_Pilihan\\BAB VI — Penumpang Per Rute\\JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI BULAN JANUARI S.D DESEMBER TAHUN 2020.pdf",  # Folder + Nama File
    start_page=150,
    end_page=152
)

# 2021
extract_pdf_range(
   input_path="D:\\Kuliah\\projek_dw\\DJPU\\Statistik Angkutan Udara\\Statistik Angkutan Udara Tahun 2021.pdf",
    output_path="D:\\Kuliah\\projek_dw\\Table_Pilihan\\BAB VI — Penumpang Per Rute\\JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI JAN-DES 2021.pdf",  # Folder + Nama File
    start_page=136,
    end_page=142
)
extract_pdf_range(
    input_path="D:\\Kuliah\\projek_dw\\DJPU\\Statistik Angkutan Udara\\Statistik Angkutan Udara Tahun 2021.pdf",
    output_path="D:\\Kuliah\\projek_dw\\Table_Pilihan\\BAB VI — Penumpang Per Rute\\JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI BULAN JANUARI S.D DESEMBER TAHUN 2021.pdf",  # Folder + Nama File
    start_page=152,
    end_page=154
)

# 2022
extract_pdf_range(
   input_path="D:\\Kuliah\\projek_dw\\DJPU\\Statistik Angkutan Udara\\Statistik Angkutan Udara Tahun 2022.pdf",
    output_path="D:\\Kuliah\\projek_dw\\Table_Pilihan\\BAB VI — Penumpang Per Rute\\JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI JAN-DES 2022.pdf",  # Folder + Nama File
    start_page=171,
    end_page=179
)
extract_pdf_range(
    input_path="D:\\Kuliah\\projek_dw\\DJPU\\Statistik Angkutan Udara\\Statistik Angkutan Udara Tahun 2022.pdf",
    output_path="D:\\Kuliah\\projek_dw\\Table_Pilihan\\BAB VI — Penumpang Per Rute\\JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI BULAN JANUARI S.D DESEMBER TAHUN 2022.pdf",  # Folder + Nama File
    start_page=189,
    end_page=191
)

# 2023
extract_pdf_range(
   input_path="D:\\Kuliah\\projek_dw\\DJPU\\Statistik Angkutan Udara\\Statistik Angkutan Udara Tahun 2023.pdf",
    output_path="D:\\Kuliah\\projek_dw\\Table_Pilihan\\BAB VI — Penumpang Per Rute\\JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI JAN-DES 2023.pdf",  # Folder + Nama File
    start_page=111,
    end_page=122
)
extract_pdf_range(
    input_path="D:\\Kuliah\\projek_dw\\DJPU\\Statistik Angkutan Udara\\Statistik Angkutan Udara Tahun 2023.pdf",
    output_path="D:\\Kuliah\\projek_dw\\Table_Pilihan\\BAB VI — Penumpang Per Rute\\JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI BULAN JANUARI S.D DESEMBER TAHUN 2023.pdf",  # Folder + Nama File
    start_page=129,
    end_page=134
)

# 2024
extract_pdf_range(
   input_path="D:\\Kuliah\\projek_dw\\DJPU\\Statistik Angkutan Udara\\Statistik Angkutan Udara Tahun 2024.pdf",
    output_path="D:\\Kuliah\\projek_dw\\Table_Pilihan\\BAB VI — Penumpang Per Rute\\JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI JAN-DES 2024.pdf",  # Folder + Nama File
    start_page=106,
    end_page=111
)
extract_pdf_range(
    input_path="D:\\Kuliah\\projek_dw\\DJPU\\Statistik Angkutan Udara\\Statistik Angkutan Udara Tahun 2024.pdf",
    output_path="D:\\Kuliah\\projek_dw\\Table_Pilihan\\BAB VI — Penumpang Per Rute\\JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI BULAN JANUARI S.D DESEMBER TAHUN 2024.pdf",  # Folder + Nama File
    start_page=118,
    end_page=120
)