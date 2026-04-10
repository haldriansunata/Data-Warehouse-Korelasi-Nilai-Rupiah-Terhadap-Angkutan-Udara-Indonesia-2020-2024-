import pdfplumber
import pandas as pd
import os
import re

# Configuration
PDF_FILES = [
    "JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI JAN-DES 2022.pdf",
    "STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2022 BERDASARKAN URUTAN JUMLAH PENUMPANG.pdf",
    "JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI BULAN JANUARI S.D DESEMBER TAHUN 2022.pdf",
    "STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI TAHUN 2022 BERDASARKAN URUTAN JUMLAH PENUMPANG.pdf"
]

WORKING_DIR = r"D:\Kuliah\projek_dw\Table_Pilihan\BAB VI — Penumpang Per Rute\2022"

def clean_number(value):
    """Clean number strings from PDF artifacts"""
    if value is None or value == "" or value == "-":
        return None
    
    value = str(value).strip()
    
    # If it's already a valid number, return as is
    try:
        return int(value)
    except ValueError:
        pass
    
    try:
        return float(value)
    except ValueError:
        pass
    
    # Remove all spaces first (PDF artifacts)
    value = value.replace(" ", "")
    
    # Remove thousand separators (dots)
    value = value.replace(".", "")
    
    # Handle comma as decimal separator
    if "," in value:
        value = value.replace(",", ".")
        try:
            return float(value)
        except ValueError:
            return None
    
    # Try to convert to int
    try:
        return int(value)
    except ValueError:
        return None

def normalize_header(header):
    """Normalize multi-line headers"""
    if header is None:
        return ""
    # Replace newlines with spaces and strip
    return " ".join(str(header).split())

def extract_tables_from_pdf(pdf_path):
    """Extract all tables from PDF with structure analysis"""
    structure_info = {
        "file": os.path.basename(pdf_path),
        "pages": 0,
        "total_rows": 0,
        "headers_per_page": [],
        "has_repetitive_headers": False,
        "has_page_breaks": False,
        "anomalies": []
    }
    
    all_data = []
    first_header = None
    
    with pdfplumber.open(pdf_path) as pdf:
        structure_info["pages"] = len(pdf.pages)
        
        for page_num, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            
            if not tables:
                structure_info["anomalies"].append(f"Page {page_num + 1}: No table found")
                continue
            
            for table in tables:
                if not table:
                    continue
                
                # Extract header (first row)
                raw_header = table[0]
                normalized_header = [normalize_header(h) for h in raw_header]
                structure_info["headers_per_page"].append({
                    "page": page_num + 1,
                    "headers": normalized_header
                })
                
                # Check if headers are repetitive
                if first_header is None:
                    first_header = normalized_header
                elif normalized_header == first_header:
                    structure_info["has_repetitive_headers"] = True
                
                # Extract data rows (skip header)
                for row in table[1:]:
                    # Check if this is a repeated header row
                    row_normalized = [normalize_header(cell) for cell in row]
                    if row_normalized == first_header:
                        structure_info["anomalies"].append(
                            f"Page {page_num + 1}: Found duplicate header row"
                        )
                        continue
                    
                    all_data.append(row)
                    structure_info["total_rows"] += 1
    
    return all_data, first_header, structure_info

def process_dataframe(data, headers, pdf_name):
    """Convert raw data to DataFrame and clean"""
    # Create DataFrame
    df = pd.DataFrame(data, columns=headers)
    
    # Identify which columns should be numbers vs strings
    # Typically: column 0 (No) is number, column 1 (Route) is string, rest are numbers
    numeric_columns = []
    string_columns = []
    
    for i, col in enumerate(df.columns):
        # Check first non-null value to determine type
        for val in df[col]:
            if val is not None and val != "" and val != "-":
                cleaned = clean_number(val)
                if cleaned is not None and isinstance(cleaned, (int, float)):
                    numeric_columns.append(i)
                else:
                    string_columns.append(i)
                break
    
    # Clean numeric columns
    for col_idx in numeric_columns:
        col_name = df.columns[col_idx]
        df[col_name] = df[col_name].apply(clean_number)
    
    # Handle null values
    df = df.replace({None: pd.NA, "": pd.NA, "-": pd.NA})
    
    return df

def verify_output(df, pdf_name):
    """Verify the output DataFrame"""
    print(f"\n{'='*80}")
    print(f"VERIFICATION: {pdf_name}")
    print(f"{'='*80}")
    print(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")
    print(f"\nColumns: {list(df.columns)}")
    print(f"\nFirst 5 rows:")
    print(df.head().to_string())
    print(f"\nLast 5 rows:")
    print(df.tail().to_string())
    print(f"\nData types:")
    print(df.dtypes)
    print(f"\nNull counts:")
    print(df.isnull().sum())
    print(f"{'='*80}\n")

def main():
    for pdf_file in PDF_FILES:
        pdf_path = os.path.join(WORKING_DIR, pdf_file)
        
        if not os.path.exists(pdf_path):
            print(f"❌ File not found: {pdf_file}")
            continue
        
        print(f"\n📄 Processing: {pdf_file}")
        
        # Extract tables
        data, headers, structure_info = extract_tables_from_pdf(pdf_path)
        
        if not data or not headers:
            print(f"❌ No data extracted from {pdf_file}")
            continue
        
        print(f"✅ Extracted {len(data)} rows with {len(headers)} columns")
        
        # Create DataFrame and clean
        df = process_dataframe(data, headers, pdf_file)
        
        # Generate CSV filename (same as PDF, just change extension)
        csv_filename = pdf_file.replace(".pdf", ".csv")
        csv_path = os.path.join(WORKING_DIR, csv_filename)
        
        # Export to CSV with UTF-8 BOM
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")
        print(f"✅ Saved to: {csv_filename}")
        
        # Verify output
        verify_output(df, pdf_file)
        
        # Store structure info for later use
        structure_info["csv_file"] = csv_filename
        structure_info["shape"] = df.shape
        
        # Save structure info
        structure_path = os.path.join(WORKING_DIR, "structure_info.json")
        import json
        if os.path.exists(structure_path):
            with open(structure_path, "r", encoding="utf-8") as f:
                all_structures = json.load(f)
        else:
            all_structures = []
        
        all_structures.append(structure_info)
        with open(structure_path, "w", encoding="utf-8") as f:
            json.dump(all_structures, f, indent=2, ensure_ascii=False)
    
    print("\n✅ All PDFs processed successfully!")

if __name__ == "__main__":
    main()
