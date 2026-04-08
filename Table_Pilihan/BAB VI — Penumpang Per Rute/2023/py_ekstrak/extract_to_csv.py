import pdfplumber
import pandas as pd
import os
import re

# Directory containing the PDFs
pdf_dir = r"D:\Kuliah\projek_dw\Table_Pilihan\BAB VI — Penumpang Per Rute\2023"

# Define PDF files and their configurations
pdf_configs = [
    {
        "file": "JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI JAN-DES 2023.pdf",
        "type": "domestik_monthly",
        "odd_cols": ['NO', 'RUTE ( PP)', 'Jan-23', 'Feb-23', 'Mar-23', 'Apr-23', 'Mei-23', 'Jun-23'],
        "even_cols": ['Jul-23', 'Agu-23', 'Sep-23', 'Okt-23', 'Nov-23', 'Des-23', 'TOTAL 2023'],
        "final_cols": ['NO', 'RUTE', 'Jan-23', 'Feb-23', 'Mar-23', 'Apr-23', 'Mei-23', 'Jun-23', 
                       'Jul-23', 'Agu-23', 'Sep-23', 'Okt-23', 'Nov-23', 'Des-23', 'TOTAL 2023']
    },
    {
        "file": "STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2023 BERDASARKAN URUTAN JUMLAH PENUMPANG.pdf",
        "type": "domestik_statistik",
        "cols": ['NO', 'RUTE', 'JUMLAH PENERBANGAN', 'JUMLAH PENUMPANG', 'KAPASITAS SEAT', 'JUMLAH BARANG', 'JUMLAH POS', 'L/F']
    },
    {
        "file": "JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI BULAN JANUARI S.D DESEMBER TAHUN 2023.pdf",
        "type": "luar_negeri_monthly",
        "odd_cols": ['NO', 'RUTE ( PP)', 'Jan-23', 'Feb-23', 'Mar-23', 'Apr-23', 'Mei-23', 'Jun-23'],
        "even_cols": ['Jul-23', 'Agu-23', 'Sep-23', 'Okt-23', 'Nov-23', 'Des-23', 'TOTAL 2023'],
        "final_cols": ['NO', 'RUTE', 'Jan-23', 'Feb-23', 'Mar-23', 'Apr-23', 'Mei-23', 'Jun-23', 
                       'Jul-23', 'Agu-23', 'Sep-23', 'Okt-23', 'Nov-23', 'Des-23', 'TOTAL 2023']
    },
    {
        "file": "STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI TAHUN 2023 BERDASARKAN URUTAN JUMLAH PENUMPANG.pdf",
        "type": "luar_negeri_statistik",
        "cols": ['NO', 'RUTE', 'JUMLAH PENERBANGAN', 'JUMLAH PENUMPANG', 'KAPASITAS SEAT', 'JUMLAH BARANG', 'JUMLAH POS', 'L/F']
    }
]


def clean_number(value):
    """
    Clean number string from PDF artifacts:
    - Remove all spaces
    - Remove dots (thousand separators)
    - Convert to integer
    - Handle '-', '', None as NaN
    """
    if value is None or value == '' or value == '-':
        return None
    
    # Convert to string
    val_str = str(value).strip()
    
    # Remove all spaces first (handles PDF artifacts like "3 .005.022")
    val_str = val_str.replace(' ', '')
    
    # Remove dots (thousand separators)
    val_str = val_str.replace('.', '')
    
    # Remove commas (decimal separators) - for percentages
    val_str = val_str.replace(',', '.')
    
    # Try to convert to number
    try:
        # Check if it has decimal point
        if '.' in val_str:
            return float(val_str)
        return int(val_str)
    except ValueError:
        return None


def clean_percentage(value):
    """
    Clean percentage values like "77,8%" -> "77.8%"
    """
    if value is None or value == '' or value == '-':
        return None
    
    val_str = str(value).strip()
    
    # Replace comma with dot for decimal
    val_str = val_str.replace(',', '.')
    
    return val_str


def normalize_header(header):
    """
    Normalize header by joining multi-line headers
    """
    if header is None:
        return ''
    return str(header).replace('\n', ' ').strip()


def process_domestik_monthly(pdf_path, config):
    """
    Process domestic monthly passenger data PDF.
    Structure: Odd pages have NO, RUTE, Jan-Jun; Even pages have Jul-Des + Total
    """
    all_data = []
    
    with pdfplumber.open(pdf_path) as pdf:
        print(f"  Total halaman: {len(pdf.pages)}")
        
        # Process pairs of pages (odd + even)
        for page_idx in range(0, len(pdf.pages), 2):
            # Odd page (Jan-Jun)
            odd_page = pdf.pages[page_idx]
            odd_tables = odd_page.extract_tables()
            
            if not odd_tables:
                print(f"  [WARNING] Tidak ada tabel di halaman {page_idx + 1}")
                continue
            
            odd_table = odd_tables[0]
            
            # Even page (Jul-Des + Total)
            if page_idx + 1 < len(pdf.pages):
                even_page = pdf.pages[page_idx + 1]
                even_tables = even_page.extract_tables()
                
                if not even_tables:
                    print(f"  [WARNING] Tidak ada tabel di halaman {page_idx + 2}")
                    continue
                
                even_table = even_tables[0]
            else:
                print(f"  [WARNING] Halaman genap tidak ada")
                continue
            
            # Skip headers (first row)
            odd_data_rows = odd_table[1:]
            even_data_rows = even_table[1:]
            
            # Merge odd and even data
            for i, (odd_row, even_row) in enumerate(zip(odd_data_rows, even_data_rows)):
                # odd_row: [NO, RUTE, Jan, Feb, Mar, Apr, Mei, Jun]
                # even_row: [Jul, Agu, Sep, Okt, Nov, Des, Total]
                
                no = odd_row[0]
                rute = odd_row[1]
                
                # Skip if NO is empty or route data is completely empty
                if no is None and rute is None:
                    continue
                
                merged_row = {
                    'NO': no,
                    'RUTE': rute if rute else None,
                    'Jan-23': odd_row[2],
                    'Feb-23': odd_row[3],
                    'Mar-23': odd_row[4],
                    'Apr-23': odd_row[5],
                    'Mei-23': odd_row[6],
                    'Jun-23': odd_row[7],
                    'Jul-23': even_row[0],
                    'Agu-23': even_row[1],
                    'Sep-23': even_row[2],
                    'Okt-23': even_row[3],
                    'Nov-23': even_row[4],
                    'Des-23': even_row[5],
                    'TOTAL 2023': even_row[6]
                }
                
                all_data.append(merged_row)
    
    # Create DataFrame
    df = pd.DataFrame(all_data, columns=config['final_cols'])
    
    # Clean number columns (skip NO and RUTE)
    number_cols = ['Jan-23', 'Feb-23', 'Mar-23', 'Apr-23', 'Mei-23', 'Jun-23', 
                   'Jul-23', 'Agu-23', 'Sep-23', 'Okt-23', 'Nov-23', 'Des-23', 'TOTAL 2023']
    
    for col in number_cols:
        df[col] = df[col].apply(clean_number)
    
    return df


def process_statistik(pdf_path, config):
    """
    Process statistics PDF with columns: NO, RUTE, JUMLAH PENERBANGAN, etc.
    Handles multi-line headers (2 or 3 lines) and various header name formats.
    """
    all_data = []
    
    with pdfplumber.open(pdf_path) as pdf:
        print(f"  Total halaman: {len(pdf.pages)}")
        
        for page_idx, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            
            if not tables:
                print(f"  [WARNING] Tidak ada tabel di halaman {page_idx + 1}")
                continue
            
            table = tables[0]
            
            # Normalize headers
            raw_headers = table[0]
            headers = [normalize_header(h) for h in raw_headers]
            
            # Map headers to standard names based on content
            standard_headers_map = {
                'NO': 'NO',
                'RUTE': 'RUTE',
                'RUTE ( PP)': 'RUTE',
                'JUMLAH PENERBANGAN': 'JUMLAH PENERBANGAN',
                'JUMLAH PENERBA NGAN': 'JUMLAH PENERBANGAN',
                'JUMLAH PENUMPANG': 'JUMLAH PENUMPANG',
                'KAPASITAS SEAT': 'KAPASITAS SEAT',
                'JUMLAH BARANG': 'JUMLAH BARANG',
                'JUMLAH BARANG (Kg)': 'JUMLAH BARANG',
                'JUMLAH POS': 'JUMLAH POS',
                'JUMLAH POS (Kg)': 'JUMLAH POS',
                'L/F': 'L/F'
            }
            
            # Create mapping from actual headers to standard headers
            header_mapping = {}
            for i, h in enumerate(headers):
                if h in standard_headers_map:
                    header_mapping[i] = standard_headers_map[h]
                else:
                    # Fallback: use the header as-is
                    header_mapping[i] = h
                    print(f"  [WARNING] Header tidak dikenal: '{h}', menggunakan as-is")
            
            # Process data rows (skip header)
            for row_idx, row in enumerate(table[1:]):
                # Check if all cells are empty
                if all(cell is None or cell == '' for cell in row):
                    continue
                
                # Build row dict with standard header names
                merged_row = {}
                for col_idx, cell in enumerate(row):
                    if col_idx in header_mapping:
                        merged_row[header_mapping[col_idx]] = cell
                
                all_data.append(merged_row)
    
    # Create DataFrame with proper column order
    final_cols = config['cols']
    df = pd.DataFrame(all_data, columns=final_cols)
    
    # Clean number columns (skip NO, RUTE, L/F)
    number_cols = ['JUMLAH PENERBANGAN', 'JUMLAH PENUMPANG', 'KAPASITAS SEAT', 'JUMLAH BARANG', 'JUMLAH POS']
    
    for col in number_cols:
        df[col] = df[col].apply(clean_number)
    
    # Clean percentage column
    df['L/F'] = df['L/F'].apply(clean_percentage)
    
    return df


def process_luar_negeri_monthly(pdf_path, config):
    """
    Process international monthly passenger data PDF.
    Similar structure to domestik_monthly.
    """
    return process_domestik_monthly(pdf_path, config)


def process_luar_negeri_statistik(pdf_path, config):
    """
    Process international statistics PDF.
    Similar structure to domestik_statistik, but with weird spaces in numbers.
    """
    return process_statistik(pdf_path, config)


def verify_output(df, pdf_file):
    """
    Verify the output DataFrame
    """
    print(f"\n  {'='*60}")
    print(f"  VERIFIKASI OUTPUT: {pdf_file}")
    print(f"  {'='*60}")
    print(f"  Shape: {df.shape[0]} rows × {df.shape[1]} columns")
    print(f"\n  5 baris pertama:")
    print(df.head().to_string(index=False))
    print(f"\n  5 baris terakhir:")
    print(df.tail().to_string(index=False))
    
    # Check for duplicate headers
    print(f"\n  Memeriksa duplikasi header...")
    # Check if any data row contains header values
    for col in df.columns:
        if df[col].astype(str).str.contains(col, case=False, na=False).any():
            print(f"    [WARNING] Kolom '{col}' mungkin mengandung header terduplikasi")
    
    # Check number format
    print(f"\n  Memeriksa format angka...")
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    print(f"  Kolom numerik: {numeric_cols}")
    
    # Check for NaN values
    print(f"\n  Jumlah NaN per kolom:")
    print(df.isnull().sum().to_string())
    
    print(f"\n  {'='*60}")


# Process each PDF
for config in pdf_configs:
    pdf_file = config['file']
    pdf_path = os.path.join(pdf_dir, pdf_file)
    csv_file = pdf_file.replace('.pdf', '.csv')
    csv_path = os.path.join(pdf_dir, csv_file)
    
    print(f"\n{'='*80}")
    print(f"MEMPROSES: {pdf_file}")
    print(f"{'='*80}")
    
    if not os.path.exists(pdf_path):
        print(f"  [ERROR] File tidak ditemukan: {pdf_path}")
        continue
    
    try:
        # Process based on type
        if config['type'] == 'domestik_monthly':
            df = process_domestik_monthly(pdf_path, config)
        elif config['type'] == 'domestik_statistik':
            df = process_statistik(pdf_path, config)
        elif config['type'] == 'luar_negeri_monthly':
            df = process_luar_negeri_monthly(pdf_path, config)
        elif config['type'] == 'luar_negeri_statistik':
            df = process_luar_negeri_statistik(pdf_path, config)
        
        # Verify output
        verify_output(df, pdf_file)
        
        # Export to CSV with UTF-8 BOM
        df.to_csv(csv_path, index=False, encoding='utf-8-sig')
        print(f"\n  ✅ CSV berhasil dibuat: {csv_file}")
        print(f"  Location: {csv_path}")
        
    except Exception as e:
        print(f"  [ERROR] Gagal memproses {pdf_file}: {str(e)}")
        import traceback
        traceback.print_exc()

print("\n" + "="*80)
print("EKSTRAKSI SELESAI")
print("="*80)
