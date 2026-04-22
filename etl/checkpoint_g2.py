"""
checkpoint_g2.py — Validasi hasil Gelombang 2 (Dim Bandara + Dim Rute)
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
    print("CHECKPOINT VALIDASI GELOMBANG 2")
    print("=" * 60)

    # ─── dim_bandara ───
    with open(OUTPUT_DIR / "dim_bandara.csv", 'r', encoding='utf-8') as f:
        bandara = list(csv.DictReader(f))

    total_bandara = len(bandara)
    indo = [r for r in bandara if r['negara'] == 'INDONESIA']
    foreign = [r for r in bandara if r['negara'] != 'INDONESIA']
    with_iata = [r for r in bandara if r['kode_iata']]
    no_provinsi_indo = [r for r in indo if not r['provinsi']]
    dup_ids = len(bandara) - len(set(r['bandara_id'] for r in bandara))

    check(f"dim_bandara total > 200", total_bandara > 200, f"got {total_bandara}")
    check(f"dim_bandara Indonesia > 200", len(indo) > 200, f"got {len(indo)}")
    check(f"dim_bandara foreign > 0", len(foreign) > 0, f"got {len(foreign)}")
    check(f"dim_bandara with IATA > 100", len(with_iata) > 100, f"got {len(with_iata)}")
    check(f"dim_bandara Indo no NULL provinsi", len(no_provinsi_indo) == 0,
          f"{len(no_provinsi_indo)} NULL")
    check(f"dim_bandara no duplicate bandara_id", dup_ids == 0, f"{dup_ids} dupes")

    # IATA uniqueness (among non-empty)
    iata_codes = [r['kode_iata'] for r in bandara if r['kode_iata']]
    dup_iata = len(iata_codes) - len(set(iata_codes))
    check(f"dim_bandara no duplicate IATA", dup_iata == 0, f"{dup_iata} dupes")

    # ─── dim_rute ───
    with open(OUTPUT_DIR / "dim_rute.csv", 'r', encoding='utf-8') as f:
        rute = list(csv.DictReader(f))

    total_rute = len(rute)
    dom_rute = [r for r in rute if r['kategori'] == 'DOMESTIK']
    intl_rute = [r for r in rute if r['kategori'] == 'INTERNASIONAL']
    dup_kode = len(rute) - len(set(r['kode_rute'] for r in rute))

    check(f"dim_rute total > 400", total_rute > 400, f"got {total_rute}")
    check(f"dim_rute domestik > 300", len(dom_rute) > 300, f"got {len(dom_rute)}")
    check(f"dim_rute internasional > 100", len(intl_rute) > 100, f"got {len(intl_rute)}")
    check(f"dim_rute no duplicate kode_rute", dup_kode == 0, f"{dup_kode} dupes")

    # FK integritas: bandara_1_id dan bandara_2_id harus ada di dim_bandara
    bandara_ids = set(r['bandara_id'] for r in bandara)
    invalid_fk1 = sum(1 for r in rute if r['bandara_1_id'] not in bandara_ids)
    invalid_fk2 = sum(1 for r in rute if r['bandara_2_id'] not in bandara_ids)
    check(f"dim_rute FK bandara_1_id valid", invalid_fk1 == 0, f"{invalid_fk1} invalid")
    check(f"dim_rute FK bandara_2_id valid", invalid_fk2 == 0, f"{invalid_fk2} invalid")

    print(f"\n=== CHECKPOINT GELOMBANG 2: ALL PASSED ===")

    # Summary table
    print(f"\n📊 Summary:")
    print(f"  dim_bandara: {total_bandara} total (Indo={len(indo)}, "
          f"Foreign={len(foreign)}, IATA={len(with_iata)})")
    print(f"  dim_rute: {total_rute} total (DOM={len(dom_rute)}, "
          f"INT={len(intl_rute)})")


if __name__ == "__main__":
    main()
