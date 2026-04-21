import os
import pandas as pd
import json

base_dir = r"D:\Kuliah\projek_dw\DJPU\Table_Pilihan\BAB III — Rute & Bandara"

target_files = {
    "dalam_negeri": [
        os.path.join(base_dir, "2024", "RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2024.csv"),
        os.path.join(base_dir, "2023", "RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2023.csv"),
        os.path.join(base_dir, "2022", "RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2022.csv"),
        os.path.join(base_dir, "2021", "RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2021.csv"),
        os.path.join(base_dir, "2020", "RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2020.csv"),
    ],
    "luar_negeri": [
        os.path.join(base_dir, "2024", "RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI TAHUN 2024.csv"),
        os.path.join(base_dir, "2023", "RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI TAHUN 2023.csv"),
        os.path.join(base_dir, "2022", "RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI TAHUN 2022.csv"),
        os.path.join(base_dir, "2021", "RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI TAHUN 2021.csv"),
        os.path.join(base_dir, "2020", "RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI TAHUN 2020.csv"),
    ]
}

def analyze_csv_structure(files, category_name):
    print(f"=== Analysis for Category: {category_name} ===")
    analysis = []
    for filepath in files:
        if not os.path.exists(filepath):
            print(f"File not found: {filepath}")
            continue
            
        year = os.path.basename(os.path.dirname(filepath))
        filename = os.path.basename(filepath)
        try:
            df = pd.read_csv(filepath, encoding='utf-8', on_bad_lines='skip')
            
            raw_columns = list(df.columns)
            std_columns = [str(c).strip().lower() for c in df.columns]
            
            dtypes = {col: str(dt) for col, dt in df.dtypes.items()}
            
            distinct_examples = {}
            for col in raw_columns:
                # Get a few distinct values for non-numeric columns or columns that might be categorical
                if df[col].dtype == 'object' or len(df[col].dropna().unique()) < 20:
                    unique_vals = [str(x) for x in df[col].dropna().unique()][:5]
                    if unique_vals:
                        distinct_examples[col] = unique_vals
            
            analysis.append({
                "year": year,
                "filename": filename,
                "num_rows": int(len(df)),
                "num_cols": int(len(raw_columns)),
                "raw_columns": raw_columns,
                "standardized_columns": std_columns,
                "dtypes": dtypes,
                "distinct_value_examples": distinct_examples,
                "has_nulls": bool(df.isnull().values.any())
            })
            
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            
    return analysis

if __name__ == "__main__":
    report_data = {}
    for category, files in target_files.items():
        report_data[category] = analyze_csv_structure(files, category)
        
    with open('bab3_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=4)
        
    print("Analysis saved to bab3_analysis.json")
