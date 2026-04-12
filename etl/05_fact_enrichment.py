"""
Script 5 (Fase 2): Process BAB IV + BAB VII + BAB XII → Enrichment Facts
Output:
  - output/fase2_enrichment/fact_produksi_maskapai.csv
  - output/fase2_enrichment/fact_lalu_lintas_bandara.csv
  - output/fase2_enrichment/fact_otp_maskapai.csv
"""

import os
import sys
import re
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import BAB_IV_DIR, BAB_VII_DIR, BAB_XII_DIR, OUTPUT_ENRICHMENT, TAHUN_RANGE
from utils import (
    parse_indonesian_number,
    parse_angka_bandara,
    standardize_maskapai,
    maskapai_to_id,
)


# ============================================================
# BAB IV — PRODUKSI MASKAPAI
# ============================================================

def parse_hours_to_minutes(val):
    """
    Convert format waktu ke total menit.
    
    Formats:
        "1221:26"       → 1221*60 + 26 = 73286
        "167383:21:00"  → 167383*60 + 21 = 10043001
        "0:00"          → None (tidak beroperasi)
        "0"             → None
        "-"             → None
    """
    if val is None:
        return None
    
    val = str(val).strip().strip('"')
    
    if val in ('-', '', '0', 'nan', 'None'):
        return None
    
    # Split on ':'
    parts = val.split(':')
    
    try:
        if len(parts) == 2:
            # "1221:26" → hours:minutes
            hours = int(parts[0])
            minutes = int(parts[1])
            total = hours * 60 + minutes
            return total if total > 0 else None
        elif len(parts) == 3:
            # "167383:21:00" → hours:minutes:seconds (ignore seconds)
            hours = int(parts[0])
            minutes = int(parts[1])
            total = hours * 60 + minutes
            return total if total > 0 else None
        else:
            # Try as integer (for "0" case)
            v = int(float(val))
            return v if v > 0 else None
    except (ValueError, TypeError):
        return None


def process_bab_iv():
    """Process 19 CSV files dari BAB IV → fact_produksi_maskapai."""
    
    print("\n--- BAB IV: Produksi Maskapai ---")
    
    prefix = "PRODUKSI ANGKUTAN UDARA NIAGA BERJADWAL DALAM NEGERI 2020-2024 "
    all_rows = []
    
    csv_files = sorted([f for f in os.listdir(BAB_IV_DIR) if f.endswith('.csv')])
    
    for fname in csv_files:
        fpath = os.path.join(BAB_IV_DIR, fname)
        
        # Extract airline name from filename
        airline_raw = fname.replace(prefix, '').replace('.csv', '').strip()
        airline_std = standardize_maskapai(airline_raw)
        mid = maskapai_to_id(airline_raw)
        
        # Read CSV: 14 rows × 7 cols (NO, DESCRIPTION, Unit, 2020-2024)
        df = pd.read_csv(fpath, encoding='utf-8', dtype=str)
        
        # Build a dict of metric → {year: value}
        metrics = {}
        for _, row in df.iterrows():
            desc = str(row.get('DESCRIPTION', '')).strip()
            no = str(row.get('NO', '')).strip()
            
            for year in TAHUN_RANGE:
                year_str = str(year)
                val = str(row.get(year_str, '')).strip()
                
                if year not in metrics:
                    metrics[year] = {}
                
                # Map metric names to output column names
                if no == '1':
                    metrics[year]['aircraft_km_ribuan'] = parse_indonesian_number(val)
                elif no == '2':
                    metrics[year]['aircraft_departures'] = parse_indonesian_number(val)
                elif no == '3':
                    metrics[year]['aircraft_hours_minutes'] = parse_hours_to_minutes(val)
                elif no == '4':
                    metrics[year]['passengers_carried'] = parse_indonesian_number(val)
                elif no == '5':
                    metrics[year]['freight_carried_ton'] = parse_indonesian_number(val)
                elif no == '6':
                    metrics[year]['passenger_km_ribuan'] = parse_indonesian_number(val)
                elif no == '7':
                    metrics[year]['available_seat_km_ribuan'] = parse_indonesian_number(val)
                elif no == '8':
                    metrics[year]['passenger_load_factor'] = parse_indonesian_number(val)
                elif no == '9d':
                    metrics[year]['ton_km_total_ribuan'] = parse_indonesian_number(val)
                elif no == '10':
                    metrics[year]['available_ton_km_ribuan'] = parse_indonesian_number(val)
                elif no == '11':
                    metrics[year]['weight_load_factor'] = parse_indonesian_number(val)
        
        # Convert to rows
        for year in TAHUN_RANGE:
            if year in metrics:
                m = metrics[year]
                # Skip if ALL values are None (airline not active that year)
                values = [v for v in m.values() if v is not None]
                if not values:
                    continue
                
                row_data = {
                    'maskapai_id': mid,
                    'tahun': year,
                }
                row_data.update(m)
                all_rows.append(row_data)
        
        print(f"  {airline_std}: {sum(1 for y in TAHUN_RANGE if y in metrics and any(v is not None for v in metrics[y].values()))} tahun aktif")
    
    df_out = pd.DataFrame(all_rows)
    
    # Ensure correct column order
    col_order = ['maskapai_id', 'tahun', 'aircraft_km_ribuan', 'aircraft_departures',
                 'aircraft_hours_minutes', 'passengers_carried', 'freight_carried_ton',
                 'passenger_km_ribuan', 'available_seat_km_ribuan', 'passenger_load_factor',
                 'ton_km_total_ribuan', 'available_ton_km_ribuan', 'weight_load_factor']
    
    for col in col_order:
        if col not in df_out.columns:
            df_out[col] = None
    
    df_out = df_out[col_order]
    
    # Convert numeric columns to appropriate types
    int_cols = ['aircraft_departures', 'aircraft_hours_minutes', 'passengers_carried']
    for col in int_cols:
        df_out[col] = pd.to_numeric(df_out[col], errors='coerce')
        # Keep as float to handle NaN (int can't have NaN in pandas)
    
    float_cols = ['aircraft_km_ribuan', 'freight_carried_ton', 'passenger_km_ribuan',
                  'available_seat_km_ribuan', 'passenger_load_factor',
                  'ton_km_total_ribuan', 'available_ton_km_ribuan', 'weight_load_factor']
    for col in float_cols:
        df_out[col] = pd.to_numeric(df_out[col], errors='coerce')
    
    return df_out


# ============================================================
# BAB VII — LALU LINTAS BANDARA
# ============================================================

def process_bab_vii():
    """Process 1 CSV file BAB VII → fact_lalu_lintas_bandara."""
    
    print("\n--- BAB VII: Lalu Lintas Bandara ---")
    
    fname = "DATA LALU LINTAS ANGKUTAN UDARA DI BANDAR UDARA TAHUN 2020 - 2024.csv"
    fpath = os.path.join(BAB_VII_DIR, fname)
    
    df = pd.read_csv(fpath, encoding='utf-8', dtype=str)
    print(f"  Raw rows: {len(df)}, Columns: {list(df.columns)}")
    
    rows = []
    for _, row in df.iterrows():
        airport_raw = str(row.get('airport_name', '')).strip()
        
        # Extract: "SULTAN ISKANDAR MUDA - BANDA ACEH (DOM)"
        # → nama_bandara, kota, tipe_penerbangan
        nama_bandara = ''
        kota = ''
        tipe_penerbangan = ''
        
        # Pattern: NAME - CITY (DOM/INT)
        m = re.match(r'^(.+?)\s*-\s*(.+?)\s*\((DOM|INT|DOMESTIK|INTERNASIONAL)\)\s*$', airport_raw)
        if m:
            nama_bandara = m.group(1).strip()
            kota = m.group(2).strip()
            tipe_raw = m.group(3).strip().upper()
            tipe_penerbangan = 'DOMESTIK' if tipe_raw in ('DOM', 'DOMESTIK') else 'INTERNASIONAL'
        else:
            # Fallback: no DOM/INT tag (bandara tanpa international)
            m2 = re.match(r'^(.+?)\s*-\s*(.+)$', airport_raw)
            if m2:
                nama_bandara = m2.group(1).strip()
                kota = m2.group(2).strip()
                tipe_penerbangan = 'DOMESTIK'  # default
            else:
                # Bandara kecil tanpa format "NAMA - KOTA" (e.g., "MUARO BUNGO", "BUDIARTO")
                # Default: domestik (bandara kecil hanya melayani domestik)
                nama_bandara = airport_raw
                kota = ''
                tipe_penerbangan = 'DOMESTIK'
        
        # Parse numeric columns
        tahun = parse_angka_bandara(row.get('year', ''))
        if tahun is None:
            continue
        tahun = int(tahun)
        
        rows.append({
            'tahun': tahun,
            'propinsi': str(row.get('propinsi_name', '')).strip(),
            'nama_bandara': nama_bandara,
            'kota': kota,
            'tipe_penerbangan': tipe_penerbangan,
            'pesawat_datang': parse_angka_bandara(row.get('pesawat_dtg', '')),
            'pesawat_berangkat': parse_angka_bandara(row.get('pesawat_brk', '')),
            'penumpang_datang': parse_angka_bandara(row.get('penumpang_dtg', '')),
            'penumpang_berangkat': parse_angka_bandara(row.get('penumpang_brk', '')),
            'penumpang_total': parse_angka_bandara(row.get('penumpang_total', '')),
            'penumpang_transit': parse_angka_bandara(row.get('penumpang_tra', '')),
            'barang_total_kg': parse_angka_bandara(row.get('barang_total', '')),
            'bagasi_total_kg': parse_angka_bandara(row.get('bagasi_total', '')),
        })
    
    df_out = pd.DataFrame(rows)
    print(f"  Parsed rows: {len(df_out)}")
    
    return df_out


# ============================================================
# BAB XII — OTP MASKAPAI
# ============================================================

def process_bab_xii():
    """Process 1 CSV file BAB XII → fact_otp_maskapai."""
    
    print("\n--- BAB XII: OTP Maskapai ---")
    
    csv_files = [f for f in os.listdir(BAB_XII_DIR) if f.endswith('.csv')]
    if not csv_files:
        print("  WARNING: No CSV found in BAB XII")
        return pd.DataFrame()
    
    fpath = os.path.join(BAB_XII_DIR, csv_files[0])
    df = pd.read_csv(fpath, encoding='utf-8', dtype=str)
    
    print(f"  File: {csv_files[0]}")
    print(f"  Raw rows: {len(df)}")
    
    rows = []
    for _, row in df.iterrows():
        no = str(row.get('NO', '')).strip()
        nama = str(row.get('BADAN USAHA', '')).strip()
        
        # Skip Total/Rata-rata row
        if no == '-' or 'Total' in nama or 'Rata' in nama:
            continue
        
        mid = maskapai_to_id(nama)
        
        # Unpivot year columns (skip 2018, 2019)
        for year in TAHUN_RANGE:
            year_str = str(year)
            val = str(row.get(year_str, '')).strip().strip('"')
            
            if val in ('-', '', 'nan', 'None'):
                otp = None
            else:
                # Parse "61,07%" → 61.07
                val_clean = val.replace('%', '').replace(',', '.').strip()
                try:
                    otp = round(float(val_clean), 2)
                except (ValueError, TypeError):
                    otp = None
            
            rows.append({
                'maskapai_id': mid,
                'tahun': year,
                'otp_persen': otp,
            })
    
    df_out = pd.DataFrame(rows)
    
    # Remove rows where otp is None (not active that year)
    df_filled = df_out.dropna(subset=['otp_persen'])
    
    print(f"  Maskapai: {df_out['maskapai_id'].nunique()}")
    print(f"  Rows with data: {len(df_filled)} / {len(df_out)}")
    
    return df_filled


# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 60)
    print("SCRIPT 5 (Fase 2): Enrichment Facts")
    print("=" * 60)
    
    # --- BAB IV ---
    df_produksi = process_bab_iv()
    prod_path = os.path.join(OUTPUT_ENRICHMENT, "fact_produksi_maskapai.csv")
    df_produksi.to_csv(prod_path, index=False)
    print(f"\n  Output: {prod_path}")
    print(f"  Baris: {len(df_produksi)} (expected <= 95)")
    
    # --- BAB VII ---
    df_bandara = process_bab_vii()
    bandara_path = os.path.join(OUTPUT_ENRICHMENT, "fact_lalu_lintas_bandara.csv")
    df_bandara.to_csv(bandara_path, index=False)
    print(f"\n  Output: {bandara_path}")
    print(f"  Baris: {len(df_bandara)} (expected ~1280)")
    
    # --- BAB XII ---
    df_otp = process_bab_xii()
    otp_path = os.path.join(OUTPUT_ENRICHMENT, "fact_otp_maskapai.csv")
    df_otp.to_csv(otp_path, index=False)
    print(f"\n  Output: {otp_path}")
    print(f"  Baris: {len(df_otp)} (expected <= 70)")
    
    # --- VERIFIKASI ---
    print(f"\n{'=' * 60}")
    print("VERIFIKASI")
    print(f"{'=' * 60}")
    
    # Produksi spot-check
    print(f"\n[Produksi] Top 5 maskapai by passengers_carried (2024):")
    if not df_produksi.empty:
        top = df_produksi[df_produksi['tahun'] == 2024].nlargest(5, 'passengers_carried', 'all')
        for _, r in top.iterrows():
            pax = r['passengers_carried']
            pax_str = f"{pax:,.0f}" if pd.notna(pax) else "N/A"
            print(f"  {r['maskapai_id']:35s} | {pax_str} penumpang")
    
    # Bandara spot-check
    print(f"\n[Bandara] Tipe penerbangan distribution:")
    if not df_bandara.empty:
        print(df_bandara['tipe_penerbangan'].value_counts().to_string())
    
    # OTP spot-check
    print(f"\n[OTP] Top 5 by OTP 2024:")
    if not df_otp.empty:
        top_otp = df_otp[df_otp['tahun'] == 2024].nlargest(5, 'otp_persen')
        for _, r in top_otp.iterrows():
            print(f"  {r['maskapai_id']:35s} | {r['otp_persen']}%")
    
    print(f"\n[DONE] Semua output Fase 2 selesai!")


if __name__ == "__main__":
    main()
