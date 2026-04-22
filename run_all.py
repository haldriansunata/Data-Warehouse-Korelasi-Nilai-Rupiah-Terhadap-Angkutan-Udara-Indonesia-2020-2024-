"""
run_all.py — Orchestrator for DJPU Data Warehouse ETL Pipeline
ETL Pipeline v3.2 (Clean Rewrite)

Menjalankan Gelombang 1, 2, dan 3 secara berurutan.
"""

import subprocess
import sys
import time
import os

# Ensure we are in the root directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

GELOMBANG_1 = [
    "etl/01_dim_waktu.py",
    "etl/02_dim_maskapai.py",
    "etl/checkpoint_g1.py"
]

GELOMBANG_2 = [
    "etl/03_dim_bandara.py",
    "etl/04_dim_rute.py",
    "etl/checkpoint_g2.py"
]

GELOMBANG_3 = [
    "etl/05_fact_kurs.py",
    "etl/06_fact_penumpang_rute.py",
    "etl/07_fact_statistik_rute.py",
    "etl/08_fact_lalu_lintas.py",
    "etl/09_fact_produksi.py",
    "etl/10_fact_otp.py",
    "etl/checkpoint_g3.py"
]

def run_script(script_path):
    print(f"\n🚀 Running: {script_path}...")
    start_time = time.time()
    
    # Use the same interpreter
    # Handle Windows encoding
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    
    result = subprocess.run([sys.executable, script_path], env=env)
    
    end_time = time.time()
    if result.returncode == 0:
        print(f"✅ Success! ({end_time - start_time:.2f}s)")
        return True
    else:
        print(f"❌ Failed with exit code {result.returncode}")
        return False

def main():
    print("="*60)
    print("  DJPU DATA WAREHOUSE ETL PIPELINE v3.2")
    print("  Correlation Analysis: IDR/USD vs Air Transport")
    print("="*60)
    
    pipeline_start = time.time()
    
    waves = [
        ("GELOMBANG 1: Dimensi Independen", GELOMBANG_1),
        ("GELOMBANG 2: Dimensi Integrasi", GELOMBANG_2),
        ("GELOMBANG 3: Tabel Fakta", GELOMBANG_3)
    ]
    
    for wave_name, scripts in waves:
        print(f"\n\n>>> {wave_name}")
        print("-" * len(wave_name))
        for script in scripts:
            if not run_script(script):
                print(f"\n🛑 Pipeline stopped due to error in {script}")
                sys.exit(1)
                
    pipeline_end = time.time()
    
    print("\n" + "="*60)
    print("🎉 PIPELINE COMPLETED SUCCESSFULLY!")
    print(f"Total duration: {pipeline_end - pipeline_start:.2f} seconds")
    print(f"Output files are in: {os.path.abspath('output')}")
    print("="*60)

if __name__ == "__main__":
    main()
