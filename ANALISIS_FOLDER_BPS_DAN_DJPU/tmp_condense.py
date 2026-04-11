import os

base_dir = r"d:\Kuliah\projek_dw"
bps_dir = os.path.join(base_dir, "BPS")
djpu_dir = os.path.join(base_dir, "DJPU", "Table_Pilihan")

output = []

output.append("=== BPS DATA ===")
for root, dirs, files in os.walk(bps_dir):
    for f in files:
        if f.endswith('.csv'):
            rel_path = os.path.relpath(os.path.join(root, f), base_dir)
            output.append(f"\nFILE: {rel_path}")
            try:
                with open(os.path.join(root, f), 'r', encoding='utf-8') as file:
                    lines = [file.readline().strip() for _ in range(3)]
                    output.append("HEAD: " + " | ".join(lines))
            except Exception as e:
                output.append(f"ERR: {e}")

output.append("\n\n=== DJPU DATA ===")
for root, dirs, files in os.walk(djpu_dir):
    for f in files:
        if f.endswith('.csv'):
            rel_path = os.path.relpath(os.path.join(root, f), base_dir)
            output.append(f"\nFILE: {rel_path}")
            try:
                with open(os.path.join(root, f), 'r', encoding='utf-8') as file:
                    lines = [file.readline().strip() for _ in range(3)]
                    output.append("HEAD: " + " | ".join(lines))
            except Exception as e:
                output.append(f"ERR: {e}")

output.append("\n\n=== DJPU MD SUMMARIES ===")
for root, dirs, files in os.walk(djpu_dir):
    for f in files:
        if f.endswith('.md'):
            rel_path = os.path.relpath(os.path.join(root, f), base_dir)
            output.append(f"\nMD FILE: {rel_path}")
            try:
                with open(os.path.join(root, f), 'r', encoding='utf-8') as file:
                    output.append(file.read()[:500].replace('\n', ' '))
            except Exception as e:
                output.append(f"ERR: {e}")

with open(os.path.join(base_dir, "condensed.txt"), 'w', encoding='utf-8') as f:
    f.write("\n".join(output))

print("Condensed text generated.")
