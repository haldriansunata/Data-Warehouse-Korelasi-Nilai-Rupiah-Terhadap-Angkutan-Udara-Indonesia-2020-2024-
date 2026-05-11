"""
Orchestrator: Run semua script ETL secara berurutan.
Usage: python etl/run_all.py
"""

import subprocess
import sys
import os

SCRIPTS = [
    ("Fase 1 — dim_waktu", "etl/01_dim_waktu.py"),
    ("Fase 1 — fact_kurs", "etl/03_fact_kurs.py"),
    ("Fase 1 — fact_penumpang", "etl/04_fact_penumpang.py"),
    ("Fase 2 — dim_maskapai", "etl/02_dim_maskapai.py"),
    ("Fase 2 — fact_enrichment", "etl/05_fact_enrichment.py"),
]


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8'
    
    print("=" * 60)
    print("ETL PIPELINE — Run All Scripts")
    print("=" * 60)
    
    for label, script in SCRIPTS:
        print(f"\n{'─' * 60}")
        print(f"▶ {label}")
        print(f"{'─' * 60}")
        
        result = subprocess.run(
            [sys.executable, script],
            cwd=base_dir,
            env=env,
            capture_output=False,
        )
        
        if result.returncode != 0:
            print(f"\n❌ FAILED: {label} (exit code {result.returncode})")
            sys.exit(1)
    
    print(f"\n{'=' * 60}")
    print("✅ ALL SCRIPTS COMPLETED SUCCESSFULLY")
    print(f"{'=' * 60}")
    
    print("\nOutput files:")
    for folder in ['output/fase1_core', 'output/fase2_enrichment']:
        full = os.path.join(base_dir, folder)
        if os.path.isdir(full):
            for f in sorted(os.listdir(full)):
                size = os.path.getsize(os.path.join(full, f))
                print(f"  {folder}/{f} ({size:,} bytes)")


if __name__ == "__main__":
    main()
