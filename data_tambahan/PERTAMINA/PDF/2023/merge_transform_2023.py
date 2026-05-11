import csv
import re
from collections import defaultdict
from pathlib import Path

# Mapping month names to numbers and days in month
month_map = {
    'Januari': ('01', 31),
    'Februari': ('02', 28),  # Non-leap year
    'Maret': ('03', 31),
    'April': ('04', 30),
    'Mei': ('05', 31),
    'Juni': ('06', 30),
    'Juli': ('07', 31),
    'Agustus': ('08', 31),
    'September': ('09', 30),
    'Oktober': ('10', 31),
    'November': ('11', 30),
    'Desember': ('12', 31)
}

# Define paths
base_path = r'c:\Users\Haldrian\OneDrive\Desktop\data_tambahan\PERTAMINA\PDF\2023'
existing_file = Path(base_path) / 'exel2023.csv'
new_files = [
    Path(base_path) / 'kampret' / '20230201082329pdf_1-14 Februari 2023.csv',
    Path(base_path) / 'kampret' / '20230215022333pdf_15-28 Februari 2023.csv',
    Path(base_path) / 'kampret' / '20230301022720pdf_1-14 Maret 2023.csv'
]
output_file = Path(base_path) / 'merged_transformed_exel2023.csv'

# Storage for all data
all_data = []

# Function to extract year, month, and date range from filename
def extract_date_info(filename):
    """Extract year, month, and date range from filename"""
    # Pattern: 20230201082329pdf_1-14 Februari 2023.pdf or 20230201082329pdf_1-14 Februari 2023.csv
    match = re.search(r'(\d{4})(\d{2})\d+pdf_(\d+-\d+) (\w+) (\d{4})\.(pdf|csv)', filename)
    if match:
        file_year = match.group(5)  # Year from filename (2023)
        file_month_name = match.group(4)  # Month name
        date_range = match.group(3)  # Date range like "1-14" or "15-28"
        
        if file_month_name in month_map:
            month_num, days_in_month = month_map[file_month_name]
            
            # Parse date range
            date_parts = date_range.split('-')
            start_day = int(date_parts[0])
            end_day = int(date_parts[1])
            num_days = end_day - start_day + 1
            
            return {
                'year': file_year,
                'month': month_num,
                'month_name': file_month_name,
                'date_range': date_range,
                'start_day': start_day,
                'end_day': end_day,
                'num_days': num_days,
                'days_in_month': days_in_month
            }
    return None

# Function to clean numeric value
def clean_numeric(value):
    """Clean numeric value - remove commas and convert"""
    if value and value.strip() and value != '#VALUE!':
        try:
            return float(str(value).replace(',', '').strip())
        except:
            return None
    return None

# Read existing exel2023.csv
print("Reading existing exel2023.csv...")
with open(existing_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    current_source = None
    current_date_info = None
    
    for row in reader:
        if len(row) > 0:
            # Check if this is a source name row
            if row[0].endswith('.pdf'):
                current_source = row[0]
                current_date_info = extract_date_info(current_source)
            
            # Check if this is a data row (NO is a number)
            if len(row) > 1 and current_date_info:
                try:
                    no = int(row[1])
                    if len(row) >= 8:
                        location = row[2]
                        city = row[3]
                        iata_code = row[4]
                        intl_price = clean_numeric(row[5])
                        dom_into_plane = clean_numeric(row[6])
                        dom_one_time = clean_numeric(row[7])
                        
                        if intl_price is not None:
                            all_data.append({
                                'source': current_source,
                                'year': current_date_info['year'],
                                'month': current_date_info['month'],
                                'month_name': current_date_info['month_name'],
                                'date_range': current_date_info['date_range'],
                                'start_day': current_date_info['start_day'],
                                'end_day': current_date_info['end_day'],
                                'num_days': current_date_info['num_days'],
                                'no': no,
                                'location': location,
                                'city': city,
                                'iata_code': iata_code,
                                'intl_price': intl_price,
                                'dom_into_plane': dom_into_plane,
                                'dom_one_time': dom_one_time
                            })
                except ValueError:
                    pass

# Read new files
print("Reading new files...")
for new_file in new_files:
    if new_file.exists():
        print(f"  Processing {new_file.name}...")
        filename = new_file.name
        date_info = extract_date_info(filename)
        
        if date_info:
            with open(new_file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) >= 8:
                        try:
                            no = int(row[0])
                            location = row[1]
                            city = row[2]
                            iata_code = row[3]
                            intl_price = clean_numeric(row[4])
                            dom_into_plane = clean_numeric(row[5])
                            dom_one_time = clean_numeric(row[6])
                            
                            if intl_price is not None:
                                all_data.append({
                                    'source': filename,
                                    'year': date_info['year'],
                                    'month': date_info['month'],
                                    'month_name': date_info['month_name'],
                                    'date_range': date_info['date_range'],
                                    'start_day': date_info['start_day'],
                                    'end_day': date_info['end_day'],
                                    'num_days': date_info['num_days'],
                                    'no': no,
                                    'location': location,
                                    'city': city,
                                    'iata_code': iata_code,
                                    'intl_price': intl_price,
                                    'dom_into_plane': dom_into_plane,
                                    'dom_one_time': dom_one_time
                                })
                        except (ValueError, IndexError):
                            pass

print(f"Total records loaded: {len(all_data)}")

# Group by year, month, and location to find and merge split entries
print("Calculating weighted averages for split entries...")
grouped = defaultdict(list)

for entry in all_data:
    key = (entry['year'], entry['month'], entry['no'], entry['location'], entry['city'], entry['iata_code'])
    grouped[key].append(entry)

# Process grouped entries
final_data = []
for key, entries in grouped.items():
    if len(entries) == 1:
        # Single entry, use as is
        entry = entries[0]
        final_data.append({
            'year': entry['year'],
            'month': entry['month'],
            'no': entry['no'],
            'location': entry['location'],
            'city': entry['city'],
            'iata_code': entry['iata_code'],
            'intl_price': entry['intl_price'],
            'dom_into_plane': entry['dom_into_plane'],
            'dom_one_time': entry['dom_one_time'],
            'source': entry['source']
        })
    elif len(entries) == 2:
        # Two entries - calculate weighted average
        # Sort by start_day to get first half and second half
        entries.sort(key=lambda x: x['start_day'])
        
        # Calculate weighted average (skip None values)
        total_days = entries[0]['num_days'] + entries[1]['num_days']
        
        # Handle None values in weighted average calculation
        if entries[0]['intl_price'] is not None and entries[1]['intl_price'] is not None:
            intl_price_avg = (entries[0]['intl_price'] * entries[0]['num_days'] + 
                             entries[1]['intl_price'] * entries[1]['num_days']) / total_days
        else:
            intl_price_avg = entries[0]['intl_price'] or entries[1]['intl_price']
        
        if entries[0]['dom_into_plane'] is not None and entries[1]['dom_into_plane'] is not None:
            dom_into_plane_avg = (entries[0]['dom_into_plane'] * entries[0]['num_days'] + 
                                 entries[1]['dom_into_plane'] * entries[1]['num_days']) / total_days
        else:
            dom_into_plane_avg = entries[0]['dom_into_plane'] or entries[1]['dom_into_plane']
        
        if entries[0]['dom_one_time'] is not None and entries[1]['dom_one_time'] is not None:
            dom_one_time_avg = (entries[0]['dom_one_time'] * entries[0]['num_days'] + 
                               entries[1]['dom_one_time'] * entries[1]['num_days']) / total_days
        else:
            dom_one_time_avg = entries[0]['dom_one_time'] or entries[1]['dom_one_time']
        
        final_data.append({
            'year': entries[0]['year'],
            'month': entries[0]['month'],
            'no': entries[0]['no'],
            'location': entries[0]['location'],
            'city': entries[0]['city'],
            'iata_code': entries[0]['iata_code'],
            'intl_price': intl_price_avg,
            'dom_into_plane': dom_into_plane_avg,
            'dom_one_time': dom_one_time_avg,
            'source': f"{entries[0]['source']} + {entries[1]['source']}"
        })
    else:
        # More than 2 entries - use simple average
        intl_prices = [e['intl_price'] for e in entries if e['intl_price'] is not None]
        dom_into_planes = [e['dom_into_plane'] for e in entries if e['dom_into_plane'] is not None]
        dom_one_times = [e['dom_one_time'] for e in entries if e['dom_one_time'] is not None]
        
        intl_price_avg = sum(intl_prices) / len(intl_prices) if intl_prices else None
        dom_into_plane_avg = sum(dom_into_planes) / len(dom_into_planes) if dom_into_planes else None
        dom_one_time_avg = sum(dom_one_times) / len(dom_one_times) if dom_one_times else None
        
        sources = ', '.join(e['source'] for e in entries)
        
        final_data.append({
            'year': entries[0]['year'],
            'month': entries[0]['month'],
            'no': entries[0]['no'],
            'location': entries[0]['location'],
            'city': entries[0]['city'],
            'iata_code': entries[0]['iata_code'],
            'intl_price': intl_price_avg,
            'dom_into_plane': dom_into_plane_avg,
            'dom_one_time': dom_one_time_avg,
            'source': sources
        })

# Sort by year, month, no
final_data.sort(key=lambda x: (x['year'], x['month'], x['no']))

# Write output file
print(f"Writing output file: {output_file}")
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    
    # Write header
    writer.writerow(['Year', 'Month', 'No', 'Location', 'City', 'IATA_Code', 
                     'International_Flight_Price_USCents_Liter', 
                     'Domestic_Flight_Price_Into_Plane_Rp_Liter', 
                     'Domestic_Flight_Price_One_Time_Customer_Rp_Liter',
                     'Source'])
    
    # Write data rows
    for entry in final_data:
        intl_price_str = f"{entry['intl_price']:.2f}" if entry['intl_price'] is not None else ""
        dom_into_plane_str = f"{entry['dom_into_plane']:.2f}" if entry['dom_into_plane'] is not None else ""
        dom_one_time_str = f"{entry['dom_one_time']:.2f}" if entry['dom_one_time'] is not None else ""
        
        writer.writerow([
            entry['year'],
            entry['month'],
            entry['no'],
            entry['location'],
            entry['city'],
            entry['iata_code'],
            intl_price_str,
            dom_into_plane_str,
            dom_one_time_str,
            entry['source']
        ])

print(f"Transformation complete! Output saved to {output_file}")
print(f"Total records in output: {len(final_data)}")
