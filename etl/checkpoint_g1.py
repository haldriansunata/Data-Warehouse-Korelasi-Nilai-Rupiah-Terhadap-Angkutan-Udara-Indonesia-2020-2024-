"""Checkpoint Validasi Gelombang 1"""
import csv, os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from etl.config import OUTPUT_DIR

def check(label, condition, msg=""):
    status = "PASS" if condition else "FAIL"
    print(f"  [{status}] {label}" + (f" -- {msg}" if msg else ""))
    if not condition:
        raise AssertionError(f"CHECKPOINT FAILED: {label} {msg}")

def main():
    print("=" * 60)
    print("CHECKPOINT VALIDASI GELOMBANG 1")
    print("=" * 60)

    # dim_waktu_bulanan
    with open(OUTPUT_DIR / "dim_waktu_bulanan.csv", "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    check("dim_waktu_bulanan rows == 60", len(rows) == 60, f"got {len(rows)}")
    check("first waktu_id == 202001", rows[0]["waktu_id"] == "202001", rows[0]["waktu_id"])
    check("last waktu_id == 202412", rows[-1]["waktu_id"] == "202412", rows[-1]["waktu_id"])

    # dim_waktu_tahunan
    with open(OUTPUT_DIR / "dim_waktu_tahunan.csv", "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    check("dim_waktu_tahunan rows == 5", len(rows) == 5, f"got {len(rows)}")
    check("range 2020..2024", rows[0]["waktu_id"] == "2020" and rows[-1]["waktu_id"] == "2024")

    # dim_maskapai
    with open(OUTPUT_DIR / "dim_maskapai.csv", "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    names = [r["nama_maskapai"] for r in rows]
    dupes = len(names) - len(set(names))
    null_kat = sum(1 for r in rows if not r["kategori_maskapai"])
    null_jenis = sum(1 for r in rows if not r["jenis_kegiatan"])
    nasional = sum(1 for r in rows if r["kategori_maskapai"] == "NASIONAL")
    asing = sum(1 for r in rows if r["kategori_maskapai"] == "ASING")

    check("dim_maskapai no NULL kategori", null_kat == 0, f"{null_kat} NULL")
    check("dim_maskapai no NULL jenis", null_jenis == 0, f"{null_jenis} NULL")
    check("dim_maskapai no duplicate nama", dupes == 0, f"{dupes} dupes")
    check(f"dim_maskapai total = {len(rows)}", len(rows) > 0, f"Nasional={nasional}, Asing={asing}")

    print()
    print("=== CHECKPOINT GELOMBANG 1: ALL PASSED ===")

if __name__ == "__main__":
    main()
