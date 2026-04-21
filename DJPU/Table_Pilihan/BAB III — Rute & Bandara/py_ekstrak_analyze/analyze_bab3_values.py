import os
import pandas as pd
import json
import re

base_dir = r"D:\Kuliah\projek_dw\DJPU\Table_Pilihan\BAB III — Rute & Bandara"

target_files = {
    "dalam_negeri": [
        os.path.join(base_dir, "2024", "RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2024.csv"),
        os.path.join(base_dir, "2021", "RUTE ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI TAHUN 2021.csv"),
    ],
    "luar_negeri": [
        os.path.join(base_dir, "2024", "RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI TAHUN 2024.csv"),
        os.path.join(base_dir, "2021", "RUTE ANGKUTAN UDARA NIAGA BERJADWAL LUAR NEGERI TAHUN 2021.csv"),
    ]
}

def analyze_rute_patterns(files):
    results = []
    for filepath in files:
        if not os.path.exists(filepath): continue
        year = os.path.basename(os.path.dirname(filepath))
        df = pd.read_csv(filepath, on_bad_lines='skip')
        cols = list(df.columns)
        
        # Determine format
        if len(cols) == 3: # Asal, Tujuan
            asal_col = cols[1]
            tuj_col = cols[2]
            sample_asal = df[asal_col].dropna().head(5).tolist()
            sample_tuj = df[tuj_col].dropna().head(5).tolist()
            results.append({
                "year": year,
                "type": "Terpisah",
                "sample_asal": sample_asal,
                "sample_tuj": sample_tuj,
                "anomalies_asal": df[df[asal_col].str.contains(r'[^a-zA-Z\s\-]', na=False, regex=True)][asal_col].head(3).tolist(),
                "anomalies_tuj": df[df[tuj_col].str.contains(r'[^a-zA-Z\s\-]', na=False, regex=True)][tuj_col].head(3).tolist()
            })
        else: # Gabungan
            rute_col = cols[1]
            sample = df[rute_col].dropna().head(5).tolist()
            # find delimiters
            delimiters = df[rute_col].str.extract(r'([-\–\—\~/;]+)', expand=False).value_counts().to_dict()
            results.append({
                "year": year,
                "type": "Gabungan",
                "sample": sample,
                "delimiters_found": delimiters,
                "anomalies": df[df[rute_col].str.contains(r'[^a-zA-Z\s\-\–\—]', na=False, regex=True)][rute_col].head(3).tolist()
            })
    return results

if __name__ == "__main__":
    report = {
        "dalam_negeri": analyze_rute_patterns(target_files["dalam_negeri"]),
        "luar_negeri": analyze_rute_patterns(target_files["luar_negeri"])
    }
    with open('bab3_rute_analysis.json', 'w') as f:
        json.dump(report, f, indent=4)
    print("Done")
