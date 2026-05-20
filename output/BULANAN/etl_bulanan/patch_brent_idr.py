"""
Patch fact_makro_bulanan.csv: tambahkan kolom brent_idr_per_bbl di akhir
tanpa mengubah byte lama (preserve LF line ending dan exact float formatting).

  brent_idr_per_bbl = brent_usd_bbl × avg_kurs_tengah  (dibulatkan 2 desimal)

Cara pakai:
    python output/BULANAN/etl_bulanan/patch_brent_idr.py
"""
from pathlib import Path
import shutil

CSV_PATH    = Path(__file__).resolve().parents[1] / "fact_makro_bulanan.csv"
BACKUP_PATH = CSV_PATH.with_suffix(".csv.bak")

# 1. Backup
shutil.copy(CSV_PATH, BACKUP_PATH)
print(f"[backup] {BACKUP_PATH.name}")

# 2. Baca raw bytes (preserve line ending asli)
with open(CSV_PATH, "rb") as f:
    raw = f.read()

eol = b"\r\n" if b"\r\n" in raw else b"\n"
lines = raw.split(eol)
# Drop empty trailing line jika ada
if lines and lines[-1] == b"":
    lines = lines[:-1]

print(f"[read] {len(lines)} baris (header + {len(lines)-1} data), EOL = {'CRLF' if eol == b'\\r\\n' else 'LF'}")

# 3. Cek header sudah punya kolom atau belum
header_str = lines[0].decode("utf-8")
if "brent_idr_per_bbl" in header_str:
    print("[skip] Kolom brent_idr_per_bbl sudah ada — tidak ada perubahan.")
    raise SystemExit(0)

# 4. Patch header
new_header = header_str + ",brent_idr_per_bbl"

# 5. Patch tiap baris data
new_lines = [new_header.encode("utf-8")]
for i, line in enumerate(lines[1:], start=2):
    s = line.decode("utf-8")
    parts = s.split(",")
    # Index kolom (0-based): waktu_id=0, avg_jual=1, avg_beli=2, avg_tengah=3, min=4, max=5,
    # hari_trading=6, tarif=7, infl_yoy=8, infl_mtm=9, bi_rate=10, brent_usd=11, brent_high=12, brent_low=13
    try:
        avg_kurs_tengah = float(parts[3])
        brent_usd_bbl   = float(parts[11])
    except (IndexError, ValueError) as e:
        print(f"[err] baris {i}: {e}")
        raise

    brent_idr = avg_kurs_tengah * brent_usd_bbl
    # Round 2 decimals + format konsisten
    new_value = f"{brent_idr:.2f}"
    new_line  = s + "," + new_value
    new_lines.append(new_line.encode("utf-8"))

# 6. Tulis kembali dengan EOL yang sama
output = eol.join(new_lines) + eol
with open(CSV_PATH, "wb") as f:
    f.write(output)

print(f"[write] {CSV_PATH.name}: {len(raw)} bytes → {len(output)} bytes (+{len(output)-len(raw)} bytes)")
print(f"[ok] Kolom 'brent_idr_per_bbl' ditambahkan. Backup tersedia di {BACKUP_PATH.name}")

# 7. Verifikasi: baca ulang dan tunjukkan 3 baris pertama
with open(CSV_PATH, "r", encoding="utf-8") as f:
    print("\n=== Preview hasil ===")
    for i, line in enumerate(f):
        if i >= 3:
            break
        print(f"  {line.rstrip()}")
