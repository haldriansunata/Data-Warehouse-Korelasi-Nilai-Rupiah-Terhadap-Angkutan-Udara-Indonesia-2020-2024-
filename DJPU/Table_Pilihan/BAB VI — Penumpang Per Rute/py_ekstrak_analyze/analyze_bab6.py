import os
import pandas as pd
import json

base_dir = r"D:\Kuliah\projek_dw\DJPU\Table_Pilihan\BAB VI — Penumpang Per Rute"

def get_long_path(p):
    p = os.path.abspath(p)
    if not p.startswith("\\\\?\\") and os.name == 'nt':
        return "\\\\?\\" + p
    return p

def analyze_bab6_structure():
    print("=== Analysis for BAB VI ===")
    
    jumlah_files = []
    statistik_files = []
    
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.csv'):
                filepath = os.path.join(root, file)
                if file.startswith("JUMLAH"):
                    jumlah_files.append(filepath)
                elif file.startswith("STATISTIK"):
                    statistik_files.append(filepath)
                    
    def profile_files(file_list):
        analysis = []
        for filepath in file_list:
            filename = os.path.basename(filepath)
            year = os.path.basename(os.path.dirname(filepath))
            tipe_cakupan = "Luar Negeri" if "LUAR NEGERI" in filename else "Dalam Negeri"
            
            try:
                df = pd.read_csv(get_long_path(filepath), encoding='utf-8')
                raw_columns = list(df.columns)
                
                # We need to know the schema variance and any potential unique column patterns
                columns_list = raw_columns
                
                analysis.append({
                    "filename": filename,
                    "year": year,
                    "tipe_cakupan": tipe_cakupan,
                    "num_rows": int(len(df)),
                    "num_cols": int(len(raw_columns)),
                    "columns": columns_list,
                    "has_nulls": bool(df.isnull().values.any())
                })
            except Exception as e:
                print(f"Error reading {filename}: {e}")
        return analysis

    report_data = {
        "jumlah": profile_files(jumlah_files),
        "statistik": profile_files(statistik_files)
    }
    
    return report_data

if __name__ == "__main__":
    report_data = analyze_bab6_structure()
    with open('bab6_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=4)
    print("Done")
