import os
import pandas as pd
import json

base_dir = r"D:\Kuliah\projek_dw\DJPU\Table_Pilihan\BAB IV — Produksi"

# Focus on the folders containing 'CSV_'
csv_folders = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f)) and f.startswith("CSV_")]

def get_long_path(p):
    p = os.path.abspath(p)
    if not p.startswith("\\\\?\\") and os.name == 'nt':
        return "\\\\?\\" + p
    return p

def analyze_bab4_structure():
    analysis = {}
    
    for folder in csv_folders:
        folder_path = get_long_path(os.path.join(base_dir, folder))
        print(f"Scanning folder: {folder}")
        
        files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
        
        if not files:
            continue
            
        sample_files = files[:min(3, len(files))] # Take up to 3 files to represent schema
        
        folder_analysis = {
            "total_files": len(files),
            "schema_samples": [],
            "metric_descriptions": set()
        }
        
        # Analyze all files to get standard list of descriptors, check missing cols
        inconsistent_schemas = []
        standard_cols = set()
        
        for file in files:
            filepath = os.path.join(folder_path, file)
            df = pd.read_csv(filepath, encoding='utf-8')
            cols = [str(c).strip().lower() for c in df.columns]
            
            if len(standard_cols) == 0:
                standard_cols = set(cols)
            elif set(cols) != standard_cols:
                inconsistent_schemas.append(file)
            
            if 'DESCRIPTION' in df.columns:
                folder_analysis["metric_descriptions"].update(df['DESCRIPTION'].dropna().tolist())
            elif 'description' in [c.lower() for c in df.columns]:
                desc_col = [c for c in df.columns if c.lower() == 'description'][0]
                folder_analysis["metric_descriptions"].update(df[desc_col].dropna().tolist())
                
        # Fill schema samples from the first 2
        for s_file in sample_files:
            sf_path = os.path.join(folder_path, s_file)
            df = pd.read_csv(sf_path, encoding='utf-8')
            folder_analysis["schema_samples"].append({
                "filename": s_file,
                "columns": list(df.columns),
                "num_rows": len(df)
            })
            
        folder_analysis["metric_descriptions"] = sorted(list(folder_analysis["metric_descriptions"]))
        folder_analysis["inconsistent_schemas_found"] = len(inconsistent_schemas) > 0
        
        analysis[folder] = folder_analysis
        
    return analysis

if __name__ == "__main__":
    report_data = analyze_bab4_structure()
    with open(os.path.join(base_dir, 'bab4_analysis.json'), 'w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=4)
    print("Done")
