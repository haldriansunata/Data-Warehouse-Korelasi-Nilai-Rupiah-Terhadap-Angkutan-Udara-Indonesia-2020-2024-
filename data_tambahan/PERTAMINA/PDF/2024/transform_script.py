import csv
import re

# Mapping month names to numbers
month_map = {
    'Januari': '01',
    'Februari': '02',
    'Maret': '03',
    'April': '04',
    'Mei': '05',
    'Juni': '06',
    'Juli': '07',
    'Agustus': '08',
    'September': '09',
    'Oktober': '10',
    'November': '11',
    'Desember': '12'
}

input_file = r'c:\Users\Haldrian\OneDrive\Desktop\data_tambahan\PERTAMINA\PDF\2024\exel2024.csv'
output_file = r'c:\Users\Haldrian\OneDrive\Desktop\data_tambahan\PERTAMINA\PDF\2024\transformed_exel2024.csv'

with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    
    # Write header
    writer.writerow(['Year', 'Month', 'No', 'Location', 'City', 'IATA_Code', 'International_Flight_Price_USCents_Liter', 'Domestic_Flight_Price_Into_Plane_Rp_Liter', 'Domestic_Flight_Price_One_Time_Customer_Rp_Liter'])
    
    current_year = None
    current_month = None
    
    for row in reader:
        if len(row) > 0 and row[0].startswith('2024'):
            # Extract year and month from filename
            match = re.search(r'2024(\d{2})\d+pdf_.* (\w+) 2024\.pdf', row[0])
            if match:
                month_num = match.group(1)
                month_name = match.group(2)
                if month_name in month_map:
                    current_month = month_map[month_name]
                current_year = '2024'
            
            if len(row) > 1 and row[1].isdigit():
                # Data row
                no = row[1]
                location = row[2]
                city = row[3]
                iata_code = row[4]
                intl_price = row[5]
                dom_into_plane = row[6]
                dom_one_time = row[7]
                
                writer.writerow([current_year, current_month, no, location, city, iata_code, intl_price, dom_into_plane, dom_one_time])

print("Transformation complete. Output saved to transformed_exel2024.csv")