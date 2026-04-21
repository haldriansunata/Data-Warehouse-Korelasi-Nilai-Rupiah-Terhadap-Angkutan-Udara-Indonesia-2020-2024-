import pandas as pd
import json

file_path = r"D:\Kuliah\projek_dw\KURS\BI.csv"

def get_long_path(p):
    p = p.replace('\\', '/')
    if not p.startswith("\\\\?\\"):
        return "\\\\?\\" + p.replace('/', '\\')
    return p

def analyze_kurs_bi():
    print("=== Analysis for KURS BI ===")
    analysis = {}
    try:
        df = pd.read_csv(get_long_path(file_path), encoding='utf-8')
        
        raw_columns = list(df.columns)
        dtypes = {col: str(dt) for col, dt in df.dtypes.items()}
        
        distinct_examples = {}
        for col in raw_columns:
            if df[col].dtype == 'object' or len(df[col].dropna().unique()) < 20:
                unique_vals = [str(x) for x in df[col].dropna().unique()][:5]
                if unique_vals:
                    distinct_examples[col] = unique_vals
                    
        analysis = {
            "num_rows": int(len(df)),
            "num_cols": int(len(raw_columns)),
            "columns": raw_columns,
            "dtypes": dtypes,
            "distinct_value_examples": distinct_examples,
            "has_nulls": bool(df.isnull().values.any())
        }
    except Exception as e:
        print(f"Error reading file: {e}")
        
    return analysis

if __name__ == "__main__":
    report_data = analyze_kurs_bi()
    with open('kurs_bi_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=4)
    print("Done")
