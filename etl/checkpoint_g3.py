"""
checkpoint_g3.py — Validasi hasil Gelombang 3 (Fact Tables)
"""

import csv
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from etl.config import OUTPUT_DIR


def check(desc, condition, detail=""):
    status = "PASS" if condition else "FAIL"
    msg = f"  [{status}] {desc}"
    if detail:
        msg += f" -- {detail}"
    print(msg)
    if not condition:
        raise AssertionError(f"CHECKPOINT FAIL: {desc}")


def main():
    print("=" * 60)
    print("CHECKPOINT VALIDASI GELOMBANG 3 (FACT TABLES)")
    print("=" * 60)

    # 1. Kurs
    with open(OUTPUT_DIR / "fact_kurs_bulanan.csv", 'r', encoding='utf-8') as f:
        kurs_b = list(csv.DictReader(f))
    check("fact_kurs_bulanan ada 60 baris", len(kurs_b) == 60, f"got {len(kurs_b)}")
    
    with open(OUTPUT_DIR / "fact_kurs_tahunan.csv", 'r', encoding='utf-8') as f:
        kurs_t = list(csv.DictReader(f))
    check("fact_kurs_tahunan ada 5 baris", len(kurs_t) == 5, f"got {len(kurs_t)}")

    # 2. Penumpang Rute
    with open(OUTPUT_DIR / "fact_penumpang_rute.csv", 'r', encoding='utf-8') as f:
        penumpang = list(csv.DictReader(f))
    check("fact_penumpang_rute > 10000 baris", len(penumpang) > 10000, f"got {len(penumpang)}")

    # 3. Statistik Rute
    with open(OUTPUT_DIR / "fact_statistik_rute.csv", 'r', encoding='utf-8') as f:
        statistik = list(csv.DictReader(f))
    check("fact_statistik_rute > 1000 baris", len(statistik) > 1000, f"got {len(statistik)}")

    # 4. Lalu Lintas
    with open(OUTPUT_DIR / "fact_lalu_lintas_bandara.csv", 'r', encoding='utf-8') as f:
        lalu_lintas = list(csv.DictReader(f))
    check("fact_lalu_lintas_bandara > 1000 baris", len(lalu_lintas) > 1000, f"got {len(lalu_lintas)}")
    check("kolom 'kategori' exists di lalu lintas", 'kategori' in lalu_lintas[0])

    # 5. Produksi
    with open(OUTPUT_DIR / "fact_produksi_maskapai.csv", 'r', encoding='utf-8') as f:
        produksi = list(csv.DictReader(f))
    check("fact_produksi_maskapai > 300 baris", len(produksi) > 300, f"got {len(produksi)}")

    # 6. OTP
    with open(OUTPUT_DIR / "fact_otp_maskapai.csv", 'r', encoding='utf-8') as f:
        otp = list(csv.DictReader(f))
    check("fact_otp_maskapai > 50 baris", len(otp) > 50, f"got {len(otp)}")
    check("kolom 'otp_percentage' exists di otp", 'otp_percentage' in otp[0])

    # FK integrity check example (Sample basis for performance)
    # Check if rute_id in fact_penumpang_rute exists in dim_rute
    with open(OUTPUT_DIR / "dim_rute.csv", 'r', encoding='utf-8') as f:
        dim_rute_ids = set(r['rute_id'] for r in csv.DictReader(f))
    
    missing_rute = sum(1 for r in penumpang if r['rute_id'] not in dim_rute_ids)
    check("fact_penumpang_rute FK rute_id valid", missing_rute == 0, f"{missing_rute} invalid")

    print(f"\n=== CHECKPOINT GELOMBANG 3: ALL PASSED ===")

if __name__ == "__main__":
    main()
