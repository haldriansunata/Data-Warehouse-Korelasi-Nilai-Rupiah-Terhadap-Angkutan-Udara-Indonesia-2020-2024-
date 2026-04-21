import os
import pandas as pd
import json

base_dir = r"D:\Kuliah\projek_dw\DJPU\Table_Pilihan\BAB II — Perusahaan Angkutan Udara"

target_files = {
    "niaga_berjadwal": [
        os.path.join(base_dir, "2024", "DAFTAR BADAN USAHA ANGKUTAN UDARA NIAGA BERJADWAL TAHUN 2024.csv"),
        os.path.join(base_dir, "2023", "DAFTAR BADAN USAHA ANGKUTAN UDARA NIAGA BERJADWAL TAHUN 2023.csv"),
        os.path.join(base_dir, "2022", "DAFTAR BADAN USAHA ANGKUTAN UDARA NIAGA BERJADWAL TAHUN 2022.csv"),
        os.path.join(base_dir, "2021", "DAFTAR BADAN USAHA ANGKUTAN UDARA NIAGA BERJADWAL TAHUN 2021.csv"),
        os.path.join(base_dir, "2020", "DAFTAR BADAN USAHA ANGKUTAN UDARA NIAGA BERJADWAL YANG BEROPERASI TAHUN 2020.csv"),
    ],
    "asing": [
        os.path.join(base_dir, "2024", "DAFTAR PERWAKILAN PERUSAHAAN ANGKUTAN UDARA ASING TAHUN 2024.csv"),
        os.path.join(base_dir, "2023", "DAFTAR PERUSAHAAN ANGKUTAN UDARA ASING TAHUN 2023.csv"),
        os.path.join(base_dir, "2022", "DAFTAR PERUSAHAAN ANGKUTAN UDARA ASING TAHUN 2022.csv"),
        os.path.join(base_dir, "2021", "DAFTAR PERUSAHAAN ANGKUTAN UDARA ASING TAHUN 2021.csv"),
        os.path.join(base_dir, "2020", "DAFTAR PERUSAHAAN ANGKUTAN UDARA ASING YANG BEROPERASI TAHUN 2020.csv"),
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
                if len(df[col].unique()) < 10 or 'status' in str(col).lower() or 'keter' in str(col).lower():
                    distinct_examples[col] = [str(x) for x in df[col].dropna().unique()][:5]
            
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
        
    with open('bab2_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=4)
        
    print("Analysis saved to bab2_analysis.json")
