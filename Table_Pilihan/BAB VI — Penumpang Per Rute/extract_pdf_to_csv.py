import pdfplumber
import pandas as pd
import os
import re
import glob

def clean_number(value):
    """Clean number values from Indonesian format"""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return value
    
    value = str(value).strip()
    
    # Handle special cases
    if value in ['-', '#DIV/0!', '']:
        return 0
    
    # Remove periods (thousands separator in Indonesian)
    # Remove spaces that might be embedded in numbers
    value = value.replace('.', '').replace(' ', '')
    
    # Remove % symbol for percentages
    value = value.replace('%', '')
    
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value

def clean_route_name(route, year):
    """Clean route name based on year format"""
    if route is None:
        return route
    
    route = str(route).strip()
    
    # For 2020, convert full names to short codes
    # Example: "Jakarta (CGK)-Makassar (UPG)" -> "CGK-UPG"
    if year == 2020:
        # Extract airport codes from parentheses
        matches = re.findall(r'\(([A-Z]{3,4})\)', route)
        if len(matches) >= 2:
            return f"{matches[0]}-{matches[1]}"
    
    # Remove extra spaces
    route = re.sub(r'\s+', ' ', route)
    
    return route

def extract_table_from_pdf(pdf_path, year):
    """Extract table from a single PDF file"""
    all_rows = []
    headers = None
    header_detected = False
    
    with pdfplumber.open(pdf_path) as pdf:
        # Check if this is a "JUMLAH PENUMPANG" file (monthly data)
        pdf_name = os.path.basename(pdf_path).upper()
        is_monthly = 'JUMLAH PENUMPANG' in pdf_name and 'JAN-DES' in pdf_name
        
        if is_monthly and year == 2023:
            # Special handling for 2023 monthly files - columns are split across pages
            return extract_2023_monthly(pdf)
        
        for page_num, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            
            for table in tables:
                if not table:
                    continue
                
                # Check if first row looks like headers
                first_row = table[0]
                if first_row and not header_detected:
                    # Check if any cell contains month names or year indicators
                    first_row_text = ' '.join([str(cell) for cell in first_row if cell])
                    if any(keyword in first_row_text.upper() for keyword in ['RUTE', 'NO', 'JAN', 'PENUMPANG', 'STATISTIK', 'JUMLAH']):
                        raw_headers = [h for h in table[0] if h is not None]
                        # Clean headers
                        headers = []
                        for h in raw_headers:
                            # Handle multi-line headers
                            h_clean = str(h).replace('\n', ' ').strip()
                            # Normalize whitespace
                            h_clean = re.sub(r'\s+', ' ', h_clean)
                            headers.append(h_clean)
                        header_detected = True
                        continue
                
                # If headers not detected yet, keep looking
                if not header_detected:
                    continue
                
                # Process data rows
                for row in table[1:]:
                    # Skip rows that look like headers (page repeats)
                    if row[0] and str(row[0]).upper() in ['NO', 'RUTE']:
                        continue
                    
                    # Clean and process row
                    cleaned_row = []
                    for i, cell in enumerate(row):
                        cell_str = str(cell).strip() if cell is not None else None
                        
                        # Skip empty rows
                        if not cell_str or cell_str == '':
                            continue
                        
                        # First column is NO (row number)
                        if i == 0:
                            cleaned_row.append(cell_str)
                        # Second column is RUTE
                        elif i == 1:
                            cleaned_row.append(clean_route_name(cell_str, year))
                        # Other columns are numeric
                        else:
                            cleaned_row.append(clean_number(cell_str))
                    
                    # Skip if all values are None or empty
                    if all(v is None or v == '' for v in cleaned_row):
                        continue
                    
                    # Skip if row doesn't have enough columns
                    if len(cleaned_row) < 3:
                        continue
                    
                    # Pad row if it has fewer columns than headers
                    while len(cleaned_row) < len(headers):
                        cleaned_row.append(None)
                    
                    # Truncate if it has more columns than headers
                    cleaned_row = cleaned_row[:len(headers)]
                    
                    all_rows.append(cleaned_row)
    
    if not headers:
        return None
    
    # Create DataFrame
    df = pd.DataFrame(all_rows, columns=headers)
    
    # Convert numeric columns
    for col in df.columns[2:]:  # Skip NO and RUTE columns
        if df[col].dtype == object:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df

def extract_2023_monthly(pdf):
    """Special extraction for 2023 monthly files where columns are split across pages"""
    # Page 0 has NO, RUTE, Jan-Jun (8 columns)
    # Page 1 has Jul-Dec + TOTAL (7 columns) - NO RUTE, data aligns by row index
    # This pattern repeats for continuation pages
    
    all_rows = []  # List of dicts with merged data
    current_headers = []
    
    for page_num, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        if not tables:
            continue
            
        table = tables[0]
        if not table:
            continue
        
        # First row is headers
        page_headers = [str(h).replace('\n', ' ').strip() for h in table[0] if h is not None]
        
        if page_num % 2 == 0:
            # Even page (0, 2, 4...) - has NO and RUTE
            current_headers = page_headers
        else:
            # Odd page (1, 3, 5...) - only has month columns, append to previous
            current_headers.extend(page_headers)
        
        # Process data rows
        for row_idx, row in enumerate(table[1:]):
            if not row or len(row) < 2:
                continue
                
            # Skip header rows
            if row[0] and str(row[0]).upper() in ['NO', 'RUTE']:
                continue
            
            if page_num % 2 == 0:
                # Even page - create new row entry
                route = clean_route_name(str(row[1]).strip(), 2023)
                if not route or route == '':
                    continue
                
                no = str(row[0]).strip() if row[0] else None
                
                row_dict = {
                    'NO': no,
                    'RUTE ( PP)': route
                }
                
                # Add values for this page's columns
                for i, val in enumerate(row[2:]):
                    if i < len(page_headers) - 2:
                        col_name = page_headers[i + 2]
                        row_dict[col_name] = clean_number(val)
                
                all_rows.append(row_dict)
            else:
                # Odd page - append to existing row
                if row_idx < len(all_rows):
                    # Add values for this page's columns
                    for i, val in enumerate(row):
                        if i < len(page_headers):
                            col_name = page_headers[i]
                            all_rows[row_idx][col_name] = clean_number(val)
    
    if not all_rows:
        return None
    
    # Convert to DataFrame
    df = pd.DataFrame(all_rows)
    
    # Reorder columns properly
    base_cols = ['NO', 'RUTE ( PP)']
    month_cols = [col for col in df.columns if col not in base_cols]
    final_cols = base_cols + month_cols
    
    df = df[final_cols]
    
    # Convert numeric columns
    for col in df.columns[2:]:
        try:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        except:
            pass
    
    # Reset index
    df = df.reset_index(drop=True)
    
    return df

def process_year(year_folder, year):
    """Process all PDFs in a year folder"""
    print(f"\n{'='*60}")
    print(f"Processing year: {year}")
    print(f"{'='*60}")
    
    # Find all PDF files in the year folder
    pdf_files = glob.glob(os.path.join(year_folder, '*.pdf'))
    
    if not pdf_files:
        print(f"  No PDF files found in {year_folder}")
        return
    
    print(f"  Found {len(pdf_files)} PDF files")
    
    for pdf_path in pdf_files:
        pdf_filename = os.path.basename(pdf_path)
        csv_filename = pdf_filename.replace('.pdf', '.csv')
        csv_path = os.path.join(year_folder, csv_filename)
        
        print(f"\n  Processing: {pdf_filename}")
        
        try:
            df = extract_table_from_pdf(pdf_path, year)
            
            if df is not None:
                # Save to CSV
                df.to_csv(csv_path, index=False, encoding='utf-8-sig')
                print(f"    [OK] Extracted {len(df)} rows, {len(df.columns)} columns")
                print(f"    [OK] Saved to: {csv_filename}")
                
                # Show sample
                print(f"    Headers: {list(df.columns)}")
            else:
                print(f"    [FAIL] Failed to extract table from {pdf_filename}")
        
        except Exception as e:
            print(f"    [FAIL] Error processing {pdf_filename}: {str(e)}")
            import traceback
            traceback.print_exc()

def main():
    """Main function to process all years"""
    base_dir = r"D:\Kuliah\projek_dw\Table_Pilihan\BAB VI — Penumpang Per Rute"
    
    years = [
        (os.path.join(base_dir, '2020'), 2020),
        (os.path.join(base_dir, '2021'), 2021),
        (os.path.join(base_dir, '2022'), 2022),
        (os.path.join(base_dir, '2023'), 2023),
        (os.path.join(base_dir, '2024'), 2024),
    ]
    
    print("PDF to CSV Extraction Script")
    print("="*60)
    
    for year_folder, year in years:
        if os.path.exists(year_folder):
            process_year(year_folder, year)
        else:
            print(f"\n  ⚠ Folder not found: {year_folder}")
    
    print("\n" + "="*60)
    print("Extraction complete!")
    print("="*60)

if __name__ == "__main__":
    main()
