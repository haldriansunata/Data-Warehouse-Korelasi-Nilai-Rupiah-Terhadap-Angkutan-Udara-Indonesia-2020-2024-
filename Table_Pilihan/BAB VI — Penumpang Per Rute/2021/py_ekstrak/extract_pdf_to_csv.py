import pdfplumber
import pandas as pd
import os
import re

# Directory containing the PDFs
BASE_DIR = r"D:\Kuliah\projek_dw\Table_Pilihan\BAB VI — Penumpang Per Rute\2021"

# PDF files to process
PDF_FILES = [
    "JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI JAN-DES 2021.pdf",
    "JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI BULAN JANUARI S.D DESEMBER TAHUN 2021.pdf",
    "STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2021 BERDASARKAN URUTAN JUMLAH PENUMPANG.pdf",
    "STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI TAHUN 2021 BERDASARKAN URUTAN JUMLAH PENUMPANG.pdf",
]


def clean_number(value):
    """
    Clean numeric values from PDF tables.
    - Remove errant spaces within numbers: "7 6.081" -> "76081"
    - Remove thousand separators (dots): "1.579.052" -> "1579052"
    - Handle dash "-" as None
    - Keep percentages with comma decimals as-is: "67,3%"
    """
    if value is None or str(value).strip() == "" or str(value).strip() == "-":
        return None
    
    val_str = str(value).strip()
    
    # Check if it's a percentage (keep as-is but normalize comma to dot if needed)
    if "%" in val_str:
        return val_str  # Keep percentage as string
    
    # Remove all spaces (handles errant spaces like "7 6.081" -> "76.081")
    val_str = val_str.replace(" ", "")
    
    # Remove dots (thousand separators): "1.579.052" -> "1579052"
    val_str = val_str.replace(".", "")
    
    # Try to convert to integer
    try:
        return int(val_str)
    except ValueError:
        # If it has comma as decimal separator, convert to dot
        if "," in val_str:
            val_str = val_str.replace(",", ".")
            try:
                return float(val_str)
            except ValueError:
                return None
        return None


def clean_header(header):
    """
    Clean header names.
    - Join multi-line headers: "JUMLAH\nPENERBANGAN" -> "JUMLAH PENERBANGAN"
    - Trim whitespace
    """
    if header is None:
        return None
    return str(header).replace("\n", " ").strip()


def extract_pdf_to_csv(pdf_path, csv_path):
    """
    Extract table from PDF and save to CSV.
    """
    print(f"\n{'='*80}")
    print(f"Processing: {os.path.basename(pdf_path)}")
    print(f"{'='*80}")
    
    all_data = []
    headers = None
    
    with pdfplumber.open(pdf_path) as pdf:
        print(f"Total pages: {len(pdf.pages)}")
        
        for page_num, page in enumerate(pdf.pages, start=1):
            tables = page.extract_tables()
            
            if not tables:
                print(f"  Page {page_num}: No table found")
                continue
            
            # Each page has exactly 1 table
            table = tables[0]
            
            if not table:
                print(f"  Page {page_num}: Empty table")
                continue
            
            # First row is header (only process on first page)
            if headers is None:
                raw_headers = table[0]
                headers = [clean_header(h) for h in raw_headers]
                print(f"  Headers ({len(headers)}): {headers}")
            
            # Debug: Print first row structure on page 1
            if page_num == 1 and len(table) > 1:
                print(f"  Debug - First data row structure: {table[1]}")
            
            # Data rows (skip header row on all pages)
            data_rows = table[1:]
            
            for row in data_rows:
                # Check if this is a "Total" row
                if row[0] and str(row[0]).strip().lower() == "total":
                    # Keep Total row but normalize
                    cleaned_row = ["Total"]
                    for val in row[1:]:
                        cleaned_row.append(clean_number(val))
                    all_data.append(cleaned_row)
                else:
                    # Regular data row
                    cleaned_row = []
                    for i, val in enumerate(row):
                        # First column (NO) - keep as integer if possible
                        if i == 0:
                            if val is not None:
                                try:
                                    cleaned_row.append(int(str(val).strip()))
                                except ValueError:
                                    cleaned_row.append(val)
                            else:
                                cleaned_row.append(None)
                        # Second column (RUTE) - keep as string, don't clean as number
                        elif i == 1:
                            if val is None or str(val).strip() == "" or str(val).strip() == "-":
                                cleaned_row.append(None)
                            else:
                                cleaned_row.append(str(val).strip())
                        else:
                            cleaned_row.append(clean_number(val))
                    all_data.append(cleaned_row)
            
            print(f"  Page {page_num}: {len(data_rows)} rows extracted")
    
    # Create DataFrame
    df = pd.DataFrame(all_data, columns=headers)
    
    print(f"\n  Total rows: {len(df)}")
    print(f"  Shape: {df.shape}")
    
    # Save to CSV with UTF-8 BOM encoding
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    print(f"  Saved to: {csv_path}")
    
    # Verification
    print(f"\n  --- Verification ---")
    print(f"  First 3 rows:")
    print(df.head(3).to_string(index=False))
    print(f"\n  Last 3 rows:")
    print(df.tail(3).to_string(index=False))
    
    # Check for duplicate headers in data
    if headers:
        header_str = str(headers[1])  # Second column header (RUTE or RUTE ( PP))
        duplicates = df[df.iloc[:, 1] == header_str] if len(df) > 0 else pd.DataFrame()
        if len(duplicates) > 0:
            print(f"\n  ⚠️  Warning: Found {len(duplicates)} rows with header-like values in data")
        else:
            print(f"\n  ✅ No duplicate headers found in data")
    
    return df


def main():
    print("PDF to CSV Extractor")
    print(f"Base directory: {BASE_DIR}")
    
    for pdf_file in PDF_FILES:
        pdf_path = os.path.join(BASE_DIR, pdf_file)
        
        if not os.path.exists(pdf_path):
            print(f"\n❌ File not found: {pdf_file}")
            continue
        
        # Generate CSV filename (same as PDF, just change extension)
        csv_file = pdf_file.replace(".pdf", ".csv")
        csv_path = os.path.join(BASE_DIR, csv_file)
        
        try:
            extract_pdf_to_csv(pdf_path, csv_path)
        except Exception as e:
            print(f"\n❌ Error processing {pdf_file}: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*80)
    print("Extraction complete!")
    print("="*80)


if __name__ == "__main__":
    main()
