import os
import pandas as pd
import json

base_dir = r"d:\Kuliah\projek_dw"
bps_dir = os.path.join(base_dir, "BPS")
djpu_dir = os.path.join(base_dir, "DJPU", "Table_Pilihan")

result = {"BPS": {}, "DJPU_CSV": {}, "DJPU_MD": {}}

# Analyze BPS
for root, dirs, files in os.walk(bps_dir):
    for f in files:
        if f.endswith('.csv'):
            path = os.path.join(root, f)
            rel_path = os.path.relpath(path, bps_dir)
            try:
                df = pd.read_csv(path, sep=None, engine='python', nrows=5)
                cols = list(df.columns)
                sample = df.head(3).to_dict(orient='records')
                result["BPS"][rel_path] = {"columns": cols, "sample": sample}
            except Exception as e:
                result["BPS"][rel_path] = {"error": str(e)}

# Analyze DJPU CSVs
for root, dirs, files in os.walk(djpu_dir):
    for f in files:
        if f.endswith('.csv'):
            path = os.path.join(root, f)
            rel_path = os.path.relpath(path, djpu_dir)
            try:
                df = pd.read_csv(path, sep=None, engine='python', nrows=5)
                cols = list(df.columns)
                sample = df.head(3).to_dict(orient='records')
                result["DJPU_CSV"][rel_path] = {"columns": cols, "sample": sample}
            except Exception as e:
                result["DJPU_CSV"][rel_path] = {"error": str(e)}

# Read DJPU MDs
for root, dirs, files in os.walk(djpu_dir):
    for f in files:
        if f.endswith('.md'):
            path = os.path.join(root, f)
            rel_path = os.path.relpath(path, djpu_dir)
            try:
                with open(path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    # Truncate MD content to keep output manageable, maybe first 1500 chars
                    result["DJPU_MD"][rel_path] = content[:1500] 
            except Exception as e:
                result["DJPU_MD"][rel_path] = f"Error: {str(e)}"

out_path = os.path.join(base_dir, "analysis_output.json")
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=4)

print(f"Analysis complete. Written to {out_path}")
