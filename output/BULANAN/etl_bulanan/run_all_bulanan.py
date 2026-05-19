"""
run_all_bulanan.py — Orchestrator pipeline BULANAN.

Urutan eksekusi:
  1. 01_dim_waktu.py            → _tmp/dim_waktu_bulanan.csv (basic)
  2. 05_fact_kurs.py            → _tmp/fact_kurs_bulanan.csv
  3. 03_dim_bandara.py          → BULANAN/dim_bandara.csv
  4. 04_dim_rute.py             → BULANAN/dim_rute.csv             (butuh dim_bandara)
  5. 06_fact_penumpang_rute.py  → BULANAN/fact_penumpang_rute.csv  (butuh dim_rute)
  6. build_makro_warehouse.py   → BULANAN/fact_makro_bulanan.csv +
                                  BULANAN/dim_waktu_bulanan.csv (enriched, menimpa basic)

Override lokasi output via env var:  BULANAN_OUTPUT=<path>
"""
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)

PIPELINE = [
    "01_dim_waktu.py",
    "05_fact_kurs.py",
    "03_dim_bandara.py",
    "04_dim_rute.py",
    "06_fact_penumpang_rute.py",
    "build_makro_warehouse.py",
]


def run(script):
    print(f"\n>>> {script}")
    t0 = time.time()
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    r = subprocess.run([sys.executable, script], env=env, cwd=HERE)
    dt = time.time() - t0
    if r.returncode != 0:
        print(f"[FAIL] {script}  ({dt:.1f}s)  exit={r.returncode}")
        sys.exit(1)
    print(f"[DONE] {script}  ({dt:.1f}s)")


def main():
    print("=" * 60)
    print("  PIPELINE BULANAN — Korelasi Kurs vs Angkutan Udara")
    print("=" * 60)
    t0 = time.time()
    for s in PIPELINE:
        run(s)
    print(f"\nSELESAI dalam {time.time() - t0:.1f}s.")
    sys.path.insert(0, HERE)
    from config import OUTPUT_DIR
    print(f"Output final: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
