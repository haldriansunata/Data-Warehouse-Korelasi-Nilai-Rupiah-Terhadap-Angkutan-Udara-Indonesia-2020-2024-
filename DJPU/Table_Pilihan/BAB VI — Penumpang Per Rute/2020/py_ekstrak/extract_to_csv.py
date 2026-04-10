import pdfplumber
import pandas as pd
import os
import re

# Directory containing the PDFs
pdf_dir = r"D:\Kuliah\projek_dw\Table_Pilihan\BAB VI — Penumpang Per Rute\2020"

def clean_number(value):
    """Clean and convert number strings with spaces and dots"""
    if value is None or value == '-':
        return None
    # Convert to string and remove spaces
    cleaned = str(value).replace(' ', '')
    # Handle percentage
    if cleaned.endswith('%'):
        return cleaned
    # Remove dots (thousand separators in Indonesian format)
    cleaned = cleaned.replace('.', '')
    # Try to convert to int or float
    try:
        if ',' in cleaned:
            # Handle decimal comma (Indonesian format)
            cleaned = cleaned.replace(',', '.')
            return float(cleaned)
        return int(cleaned) if cleaned else None
    except ValueError:
        return cleaned

def clean_route_number(value):
    """Clean route number which may have spaces"""
    if value is None:
        return None
    cleaned = str(value).replace(' ', '')
    try:
        return int(cleaned)
    except ValueError:
        return value

def extract_domestic_monthly(pdf_path):
    """Extract domestic passenger data by month"""
    all_data = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            if tables:
                table = tables[0]  # First table
                # Skip header row (index 0)
                for row in table[1:]:
                    if len(row) >= 17:
                        cleaned_row = {
                            'NO': clean_route_number(row[0]),
                            'RUTE (PP)': row[1],
                            'Jan-20': clean_number(row[2]),
                            'Feb-20': clean_number(row[3]),
                            'Mar-20': clean_number(row[4]),
                            'Apr-20': clean_number(row[5]),
                            'May-20': clean_number(row[6]),
                            'Jun-20': clean_number(row[7]),
                            'Jul-20': clean_number(row[8]),
                            'Aug-20': clean_number(row[9]),
                            'Sep-20': clean_number(row[10]),
                            'Oct-20': clean_number(row[11]),
                            'Nov-20': clean_number(row[12]),
                            'Dec-20': clean_number(row[13]),
                            'TOTAL 2020': clean_number(row[14]),
                            'TOTAL 2019': clean_number(row[15]),
                            'TOTAL 2018': clean_number(row[16])
                        }
                        all_data.append(cleaned_row)
    
    return pd.DataFrame(all_data)

def extract_international_monthly(pdf_path):
    """Extract international passenger data by month"""
    all_data = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            if tables:
                table = tables[0]
                # Skip header row
                for row in table[1:]:
                    if len(row) >= 17:
                        cleaned_row = {
                            'NO': clean_route_number(row[0]),
                            'RUTE': row[1],
                            'Jan-20': clean_number(row[2]),
                            'Feb-20': clean_number(row[3]),
                            'Mar-20': clean_number(row[4]),
                            'Apr-20': clean_number(row[5]),
                            'May-20': clean_number(row[6]),
                            'Jun-20': clean_number(row[7]),
                            'Jul-20': clean_number(row[8]),
                            'Aug-20': clean_number(row[9]),
                            'Sep-20': clean_number(row[10]),
                            'Oct-20': clean_number(row[11]),
                            'Nov-20': clean_number(row[12]),
                            'Dec-20': clean_number(row[13]),
                            'TOTAL 2020': clean_number(row[14]),
                            'TOTAL 2019': clean_number(row[15]),
                            'TOTAL 2018': clean_number(row[16])
                        }
                        all_data.append(cleaned_row)
    
    return pd.DataFrame(all_data)

def extract_domestic_statistics(pdf_path):
    """Extract domestic route statistics"""
    all_data = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            if tables:
                table = tables[0]
                # Skip header row
                for row in table[1:]:
                    if len(row) >= 8:
                        cleaned_row = {
                            'NO': clean_route_number(row[0]),
                            'RUTE (PP)': row[1],
                            'JUMLAH PENERBANGAN': clean_number(row[2]),
                            'JUMLAH PENUMPANG': clean_number(row[3]),
                            'KAPASITAS SEAT': clean_number(row[4]),
                            'JUMLAH BARANG (Kg)': clean_number(row[5]),
                            'JUMLAH POS': clean_number(row[6]),
                            'L/F': row[7]  # Keep as string (percentage)
                        }
                        all_data.append(cleaned_row)
    
    return pd.DataFrame(all_data)

def extract_international_statistics(pdf_path):
    """Extract international route statistics"""
    all_data = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            if tables:
                table = tables[0]
                # Skip header row
                for row in table[1:]:
                    if len(row) >= 8:
                        cleaned_row = {
                            'NO': clean_route_number(row[0]),
                            'RUTE': row[1],
                            'JUMLAH PENERBANGAN': clean_number(row[2]),
                            'JUMLAH PENUMPANG': clean_number(row[3]),
                            'KAPASITAS SEAT': clean_number(row[4]),
                            'JUMLAH BARANG': clean_number(row[5]),
                            'JUMLAH POS': clean_number(row[6]),
                            'L/F': row[7]  # Keep as string (percentage)
                        }
                        all_data.append(cleaned_row)
    
    return pd.DataFrame(all_data)

# Process each PDF
print("Processing PDF files...\n")

# 1. Domestic Monthly
pdf1 = os.path.join(pdf_dir, "JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI JAN-DES 2020.pdf")
print(f"Processing: Domestic Monthly")
df1 = extract_domestic_monthly(pdf1)
output1 = os.path.join(pdf_dir, "JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI JAN-DES 2020.csv")
df1.to_csv(output1, index=False, encoding='utf-8-sig')
print(f"✓ Saved {len(df1)} rows to: {output1}\n")

# 2. International Monthly
pdf2 = os.path.join(pdf_dir, "JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI BULAN JANUARI S.D DESEMBER TAHUN 2020.pdf")
print(f"Processing: International Monthly")
df2 = extract_international_monthly(pdf2)
output2 = os.path.join(pdf_dir, "JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI BULAN JANUARI S.D DESEMBER TAHUN 2020.csv")
df2.to_csv(output2, index=False, encoding='utf-8-sig')
print(f"✓ Saved {len(df2)} rows to: {output2}\n")

# 3. Domestic Statistics
pdf3 = os.path.join(pdf_dir, "STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2020 BERDASARKAN URUTAN JUMLAH PENUMPANG.pdf")
print(f"Processing: Domestic Statistics")
df3 = extract_domestic_statistics(pdf3)
output3 = os.path.join(pdf_dir, "STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2020 BERDASARKAN URUTAN JUMLAH PENUMPANG.csv")
df3.to_csv(output3, index=False, encoding='utf-8-sig')
print(f"✓ Saved {len(df3)} rows to: {output3}\n")

# 4. International Statistics
pdf4 = os.path.join(pdf_dir, "STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI TAHUN 2020 BERDASARKAN URUTAN JUMLAH PENUMPANG.pdf")
print(f"Processing: International Statistics")
df4 = extract_international_statistics(pdf4)
output4 = os.path.join(pdf_dir, "STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI TAHUN 2020 BERDASARKAN URUTAN JUMLAH PENUMPANG.csv")
df4.to_csv(output4, index=False, encoding='utf-8-sig')
print(f"✓ Saved {len(df4)} rows to: {output4}\n")

print("\n" + "="*100)
print("EXTRACTION SUMMARY")
print("="*100)
print(f"1. Domestic Monthly: {len(df1)} routes extracted")
print(f"   → JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI JAN-DES 2020.csv")
print(f"2. International Monthly: {len(df2)} routes extracted")
print(f"   → JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI BULAN JANUARI S.D DESEMBER TAHUN 2020.csv")
print(f"3. Domestic Statistics: {len(df3)} routes extracted")
print(f"   → STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2020 BERDASARKAN URUTAN JUMLAH PENUMPANG.csv")
print(f"4. International Statistics: {len(df4)} routes extracted")
print(f"   → STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI TAHUN 2020 BERDASARKAN URUTAN JUMLAH PENUMPANG.csv")
print("\nAll CSV files saved successfully!")
