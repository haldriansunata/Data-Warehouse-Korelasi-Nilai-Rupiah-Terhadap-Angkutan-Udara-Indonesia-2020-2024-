import pandas as pd
import re
import os

def clean_number(s):
    if pd.isna(s) or s == '' or s == '-':
        return 0.0
    s = str(s).strip().replace('"', '')
    if not s or s == '-':
        return 0.0
    
    # Remove spaces
    s = s.replace(' ', '')
    
    # Detect pattern
    # 11,791.07 -> 11791.07
    # 14.934,62 -> 14934.62
    if '.' in s and ',' in s:
        if s.find('.') < s.find(','):
            # Indonesian format: dot for thousand, comma for decimal
            return float(s.replace('.', '').replace(',', '.'))
        else:
            # English format: comma for thousand, dot for decimal
            return float(s.replace(',', ''))
    
    if ',' in s:
        parts = s.split(',')
        if len(parts) == 2 and len(parts[1]) <= 2:
            # Likely decimal comma (Indonesian)
            return float(s.replace(',', '.'))
        else:
            # Likely thousand comma (English)
            return float(s.replace(',', ''))
            
    if '.' in s:
        # For values like 75.80 it's decimal.
        # For values like 11.791 it's ambiguous if no comma is present.
        # But in this dataset, usually large numbers have commas or both.
        # Let's check the number of digits after the dot.
        parts = s.split('.')
        if len(parts) == 2 and len(parts[1]) == 3 and float(s) > 1000:
            # Likely thousand separator if it's like 11.791
            return float(s.replace('.', ''))
        return float(s)
    
    try:
        return float(s)
    except:
        return 0.0

month_map = {
    'januari': 1, 'februari': 2, 'maret': 3, 'april': 4, 'mei': 5, 'juni': 6,
    'juli': 7, 'agustus': 8, 'september': 9, 'oktober': 10, 'november': 11, 'desember': 12
}

days_in_month = {
    1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
    7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
}

def parse_source_name(name):
    # Example: 20220101095002pdf_1-14 Januari 2022.pdf
    # Also handles: 20220414213730pdf_15-30 APRIL 2022.pdf
    match = re.search(r'(\d+)-(\d+)\s+([a-zA-Z]+)\s+(\d{4})', name)
    if match:
        start_day = int(match.group(1))
        end_day = int(match.group(2))
        month_name = match.group(3).lower()
        year = int(match.group(4))
        month = month_map.get(month_name, 0)
        
        period = 1 if start_day == 1 else 2
        return year, month, period
    return None, None, None

def transform():
    input_file = r'd:\Kuliah\projek_dw\data_tambahan\PERTAMINA\PDF\2022\exel_2022.csv'
    output_file = r'd:\Kuliah\projek_dw\data_tambahan\PERTAMINA\PDF\2022\transformed_exel_2022.csv'
    
    print(f"Reading {input_file}...")
    df = pd.read_csv(input_file)
    
    # Basic validation: Source.Name must be present
    if 'Source.Name' not in df.columns:
        print("Error: Source.Name column not found")
        return

    # Extract Year, Month, Period
    parsed = df['Source.Name'].apply(parse_source_name)
    df['Year'] = [p[0] for p in parsed]
    df['Month'] = [p[1] for p in parsed]
    df['Period'] = [p[2] for p in parsed]
    
    # Filter rows that have a valid Year/Month and a numeric NO
    df = df[df['Year'].notna() & (df['Month'] != 0)]
    
    # We only care about rows where Column1 (NO) is a number
    def is_number(s):
        try:
            float(str(s).strip())
            return True
        except:
            return False
            
    df = df[df['Column1'].apply(is_number)]
    
    # Map columns to meaningful names
    # Column1: NO
    # Column2: LOCATION
    # Column3: CITY
    # Column4: IATA CODE
    
    # Convert Column1 to numeric, errors='coerce' will turn non-numeric to NaN
    df['No_Temp'] = pd.to_numeric(df['Column1'], errors='coerce')
    df = df[df['No_Temp'].notna()]
    df['No'] = df['No_Temp'].astype(int)
    
    df['Location'] = df['Column2'].fillna('').str.strip()
    df['City'] = df['Column3'].fillna('').str.strip()
    df['IATA_Code'] = df['Column4'].fillna('').str.strip()
    
    # Clean the price columns
    df['Int_Price'] = df['INTERNATIONAL'].apply(clean_number)
    df['Dom_Price_Into'] = df['Column6'].apply(clean_number)
    df['Dom_Price_OTC'] = df['Column7'].apply(clean_number)
    
    # Group by Year, Month, Location, City, IATA_Code
    results = []
    
    # Grain: Year, Month, Location, City, IATA_Code
    # Some columns might have NaNs, fill them to avoid grouping issues
    df['Location'] = df['Location'].fillna('UNKNOWN')
    df['City'] = df['City'].fillna('UNKNOWN')
    df['IATA_Code'] = df['IATA_Code'].fillna('UNKNOWN')
    
    grouped = df.groupby(['Year', 'Month', 'Location', 'City', 'IATA_Code'])
    
    for (year, month, loc, city, iata), group in grouped:
        no = int(group['No'].iloc[0])
        
        # Period 1 (1-14)
        p1_data = group[group['Period'] == 1]
        # Period 2 (15-end)
        p2_data = group[group['Period'] == 2]
        
        if p1_data.empty and p2_data.empty:
            continue
            
        p1_int = p1_data['Int_Price'].mean() if not p1_data.empty else 0.0
        p1_dom_into = p1_data['Dom_Price_Into'].mean() if not p1_data.empty else 0.0
        p1_dom_otc = p1_data['Dom_Price_OTC'].mean() if not p1_data.empty else 0.0
        
        p2_int = p2_data['Int_Price'].mean() if not p2_data.empty else 0.0
        p2_dom_into = p2_data['Dom_Price_Into'].mean() if not p2_data.empty else 0.0
        p2_dom_otc = p2_data['Dom_Price_OTC'].mean() if not p2_data.empty else 0.0
        
        # Weight 1: 14 days
        # Weight 2: Total days in month - 14
        w1 = 14
        total_days = days_in_month.get(month, 30)
        w2 = total_days - 14
        
        if p1_data.empty:
            final_int = p2_int
            final_dom_into = p2_dom_into
            final_dom_otc = p2_dom_otc
        elif p2_data.empty:
            final_int = p1_int
            final_dom_into = p1_dom_into
            final_dom_otc = p1_dom_otc
        else:
            final_int = (p1_int * w1 + p2_int * w2) / total_days
            final_dom_into = (p1_dom_into * w1 + p2_dom_into * w2) / total_days
            final_dom_otc = (p1_dom_otc * w1 + p2_dom_otc * w2) / total_days
            
        results.append({
            'Year': int(year),
            'Month': int(month),
            'No': no,
            'Location': loc,
            'City': city,
            'IATA_Code': iata,
            'International_Flight_Price_USCents_Liter': round(final_int, 2),
            'Domestic_Flight_Price_Into_Plane_Rp_Liter': round(final_dom_into, 2),
            'Domestic_Flight_Price_One_Time_Customer_Rp_Liter': round(final_dom_otc, 2)
        })
        
    if not results:
        print("No data processed.")
        return

    final_df = pd.DataFrame(results)
    final_df = final_df.sort_values(['Year', 'Month', 'No'])
    final_df.to_csv(output_file, index=False)
    print(f"Successfully saved {len(final_df)} rows to {output_file}")

if __name__ == "__main__":
    transform()
