import pandas as pd
import os

BASE_DIR = r"D:\Kuliah\projek_dw\Table_Pilihan\BAB VI — Penumpang Per Rute\2024"

CSV_FILES = [
    "JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI JAN-DES 2024.csv",
    "STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2024 BERDASARKAN URUTAN JUMLAH PENUMPANG.csv",
    "JUMLAH PENUMPANG PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI BULAN JANUARI S.D DESEMBER TAHUN 2024.csv",
    "STATISTIK PER RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI TAHUN 2024 BERDASARKAN URUTAN JUMLAH PENUMPANG.csv"
]

for csv_file in CSV_FILES:
    csv_path = os.path.join(BASE_DIR, csv_file)
    
    print(f"\n{'='*80}")
    print(f"VERIFYING: {csv_file}")
    print(f"{'='*80}")
    
    df = pd.read_csv(csv_path)
    
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print(f"\nData types:\n{df.dtypes}")
    
    # Check for duplicate NO values
    dupes = df[df.duplicated(subset=['NO'], keep=False)]
    if len(dupes) > 0:
        print(f"\n⚠️ Found {len(dupes)} duplicate NO values:")
        print(dupes.head(10))
    
    # Check NO column unique values
    print(f"\nUnique NO values: {df['NO'].nunique()}")
    print(f"NO range: {df['NO'].min()} - {df['NO'].max()}")
    
    # Check for header rows in data
    header_in_data = df[df['NO'] == 'NO']
    if len(header_in_data) > 0:
        print(f"\n❌ Found {len(header_in_data)} header rows in data!")
        print(header_in_data)
    
    # Check for TOTAL row
    total_rows = df[df['NO'] == 'TOTAL']
    print(f"\nTOTAL rows found: {len(total_rows)}")
    
    # Sample data
    print(f"\n--- First 3 rows ---")
    print(df.head(3).to_string(index=False))
    print(f"\n--- Last 3 rows ---")
    print(df.tail(3).to_string(index=False))
