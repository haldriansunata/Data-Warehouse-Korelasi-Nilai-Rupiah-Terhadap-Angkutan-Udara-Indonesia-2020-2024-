import pdfplumber
import pandas as pd
import os
import re

# Configuration
BASE_DIR = r"D:\Kuliah\projek_dw\Table_Pilihan\BAB VI — Penumpang Per Rute\2024"

PDF_FILES = [
    "JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI JAN-DES 2024.pdf",
    "STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2024 BERDASARKAN URUTAN JUMLAH PENUMPANG.pdf",
    "JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI BULAN JANUARI S.D DESEMBER TAHUN 2024.pdf",
    "STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI TAHUN 2024 BERDASARKAN URUTAN JUMLAH PENUMPANG.pdf"
]


def clean_number(value):
    """Clean number string by removing thousand separators (dots) and converting to int"""
    if value is None or value == '' or value == '-':
        return None
    
    # Convert to string and strip whitespace
    val_str = str(value).strip()
    
    # If it's empty or dash, return None
    if val_str == '' or val_str == '-':
        return None
    
    # Remove dots (thousand separators)
    val_clean = val_str.replace('.', '')
    
    # Try to convert to int
    try:
        return int(val_clean)
    except ValueError:
        # If fails, return original (might be text like "TOTAL")
        return val_str


def clean_percentage(value):
    """Keep percentage as string with % sign"""
    if value is None or value == '' or value == '-':
        return None
    
    val_str = str(value).strip()
    
    if val_str == '' or val_str == '-':
        return None
    
    # If already has %, keep as is
    if '%' in val_str:
        return val_str
    
    return val_str


def normalize_header(header):
    """Normalize header by joining multi-line headers and trimming"""
    if header is None:
        return None
    # Replace newlines with space and trim
    return str(header).replace('\n', ' ').strip()


def extract_pdf_to_csv(pdf_path, csv_path):
    """Extract table from PDF to CSV with cleaning"""
    
    print(f"\n{'='*80}")
    print(f"Processing: {os.path.basename(pdf_path)}")
    print(f"{'='*80}")
    
    all_data = []
    headers = None
    
    with pdfplumber.open(pdf_path) as pdf:
        print(f"Total halaman: {len(pdf.pages)}")
        
        for page_idx, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            
            if not tables:
                print(f"  ⚠️ Halaman {page_idx+1}: Tidak ada tabel")
                continue
            
            # Assuming one table per page
            table = tables[0]
            
            if not table:
                continue
            
            # First page: extract header
            if page_idx == 0:
                raw_header = table[0]
                headers = [normalize_header(h) for h in raw_header]
                print(f"  Header: {headers}")
                
                # Data rows start from index 1
                data_rows = table[1:]
            else:
                # Subsequent pages: all rows are data (no header repetition)
                data_rows = table
            
            # Process data rows
            for row in data_rows:
                # Check if this is a TOTAL row (first column contains 'TOTAL', 'OTAL', etc.)
                first_col = str(row[0]).strip() if row[0] else ''
                
                # Fix typo: 'OTAL' -> 'TOTAL'
                if first_col == 'OTAL':
                    row[0] = 'TOTAL'
                
                all_data.append(row)
        
        # Create DataFrame
        df = pd.DataFrame(all_data, columns=headers)
        
        # Clean columns
        # Column 'NO' - keep as is (has numbers and 'TOTAL')
        # Column 'RUTE PP' - keep as is (route codes)
        
        # For monthly data files (15 columns)
        if len(headers) == 15:
            # Clean monthly columns (Jan-24 to Dec-24) and TOTAL 2024
            for col in headers[2:]:  # Skip NO and RUTE PP
                df[col] = df[col].apply(clean_number)
        
        # For statistics files (8 columns)
        elif len(headers) == 8:
            # Clean: JUMLAH PENERBANGAN, JUMLAH PENUMPANG, KAPASITAS SEAT,
            #        JUMLAH BARANG KG, JUMLAH POS KG
            for col in headers[2:7]:  # Skip NO, RUTE PP, and LF %
                df[col] = df[col].apply(clean_number)
            
            # Clean LF % (keep as string with %)
            df['LF %'] = df['LF %'].apply(clean_percentage)
        
        # Strip whitespace from all string columns
        for col in df.columns:
            df[col] = df[col].apply(
                lambda x: x.strip() if isinstance(x, str) else x
            )
        
        # Export to CSV with UTF-8-sig
        df.to_csv(csv_path, index=False, encoding='utf-8-sig')
        
        # Verification
        print(f"\n  ✅ CSV saved: {os.path.basename(csv_path)}")
        print(f"  Shape: {df.shape[0]} rows × {df.shape[1]} columns")
        print(f"\n  First 5 rows:")
        print(df.head().to_string(index=False))
        print(f"\n  Last 5 rows:")
        print(df.tail().to_string(index=False))
        
        # Check for duplicate headers in data
        if headers:
            header_str = headers[0] if headers[0] else ''
            duplicates = df[df['NO'] == header_str].shape[0]
            if duplicates > 0:
                print(f"\n  ⚠️ Warning: Found {duplicates} duplicate header rows in data")
        
        return df


def main():
    print("Starting PDF to CSV extraction...")
    
    for pdf_file in PDF_FILES:
        pdf_path = os.path.join(BASE_DIR, pdf_file)
        
        # Generate CSV name (same as PDF, just change extension)
        csv_file = pdf_file.replace('.pdf', '.csv')
        csv_path = os.path.join(BASE_DIR, csv_file)
        
        if not os.path.exists(pdf_path):
            print(f"\n❌ File not found: {pdf_file}")
            continue
        
        try:
            extract_pdf_to_csv(pdf_path, csv_path)
        except Exception as e:
            print(f"\n❌ Error processing {pdf_file}: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print(f"\n{'='*80}")
    print("✅ All PDF files processed!")
    print(f"{'='*80}")


if __name__ == "__main__":
    main()
