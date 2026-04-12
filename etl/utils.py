"""
Shared utility functions for ETL pipeline.
"""

import re
import math


def parse_indonesian_number(val):
    """
    Parse angka format Indonesia (titik = ribuan, koma = desimal).
    
    Examples:
        "1.661"     → 1661
        "6.123.017" → 6123017
        "20,28"     → 20.28
        '"20,28"'   → 20.28
        "-"         → None
        ""          → None
    """
    if val is None:
        return None
    
    val = str(val).strip().strip('"').strip("'")
    
    if val in ('-', '', 'nan', 'None', '-,00'):
        return None
    
    # Ganti koma desimal dengan titik (setelah hapus titik ribuan)
    if '.' in val and ',' in val:
        # Format: "1.234,56" → hapus titik, ganti koma
        val = val.replace('.', '').replace(',', '.')
    elif ',' in val:
        # Format: "20,28" → ganti koma
        val = val.replace(',', '.')
    elif '.' in val:
        # Bisa titik ribuan atau titik desimal — cek pattern
        parts = val.split('.')
        if len(parts) >= 2 and all(len(p) == 3 for p in parts[1:]):
            # Titik = ribuan: "1.661" atau "6.123.017"
            val = val.replace('.', '')
        # Else: titik = desimal biasa (e.g., "1549163.0")
    
    try:
        result = float(val)
        return result
    except (ValueError, TypeError):
        return None


def parse_angka_bandara(val):
    """
    Parse angka dari BAB VII — deteksi per-value apakah titik = ribuan.
    
    Examples:
        "1.809"     → 1809  (titik = ribuan)
        "323.529"   → 323529
        "1809"      → 1809  (integer biasa)
        "0"         → 0
        "-"         → None
    """
    if val is None:
        return None
    
    val = str(val).strip()
    
    if val in ('-', '', 'nan', 'None'):
        return None
    
    # Fast path: tidak ada titik → langsung parse
    if '.' not in val:
        try:
            return int(float(val))
        except (ValueError, TypeError):
            return None
    
    # Jika ada titik: cek apakah pemisah ribuan
    parts = val.split('.')
    if all(len(p) == 3 for p in parts[1:]):
        # Titik = pemisah ribuan
        return int(val.replace('.', ''))
    
    # Fallback: mungkin float biasa
    try:
        return int(float(val))
    except (ValueError, TypeError):
        return None


def normalize_route_pp(kode_origin, kode_dest):
    """
    Normalisasi rute PP ke alphabetical order.
    
    Returns: (kode_a, kode_b) dimana kode_a < kode_b secara alfabet.
    
    Examples:
        ("DPS", "CGK") → ("CGK", "DPS")
        ("CGK", "DPS") → ("CGK", "DPS")
    """
    kode_a, kode_b = sorted([kode_origin.strip(), kode_dest.strip()])
    return kode_a, kode_b


def extract_iata_from_route_2020(route_str):
    """
    Parse rute format 2020: "Jakarta (CGK)-Denpasar (DPS)"
    
    Returns: (kode_origin, kode_dest, kota_origin, kota_dest)
    
    Edge cases handled:
        "Praya, Lombok (LOP)-Denpasar (DPS)"
        "Jakarta-HLP (HLP)-Surabaya (SUB)"  
        "Surabaya (SUB)-Jakarta-HLP (HLP)"
    """
    # Strip trailing asterisk (codeshare marker, e.g., "...Taipei (TPE)*")
    route_str = route_str.strip().rstrip('*').strip()
    
    # Pattern: kota (KODE)-kota (KODE)
    # Kota bisa mengandung koma dan dash (Jakarta-HLP)
    pattern = r'^(.+?)\s*\((\w{3})\)\s*-\s*(.+?)\s*\((\w{3})\)\s*$'
    match = re.match(pattern, route_str)
    
    if match:
        kota_origin = match.group(1).strip()
        kode_origin = match.group(2).strip()
        kota_dest = match.group(3).strip()
        kode_dest = match.group(4).strip()
        return kode_origin, kode_dest, kota_origin, kota_dest
    
    # Fallback: "Kota (KODE)-KODE" (destination tanpa kurung)
    pattern2 = r'^(.+?)\s*\((\w{3})\)\s*-\s*(\w{2,4})\s*$'
    match2 = re.match(pattern2, route_str)
    if match2:
        kota_origin = match2.group(1).strip()
        kode_origin = match2.group(2).strip()
        kode_dest = match2.group(3).strip()
        return kode_origin, kode_dest, kota_origin, None
    
    return None, None, None, None


def extract_iata_from_route_2021(route_str):
    """
    Parse rute format 2021: "Jakarta (CGK) - Denpasar (DPS)"
    (sama seperti 2020 tapi spasi sebelum/sesudah dash)
    """
    # Gunakan fungsi yang sama — regex sudah handle spasi fleksibel
    return extract_iata_from_route_2020(route_str)


def extract_iata_from_route_code(route_str):
    """
    Parse rute format 2022-2024: "CGK-DPS"
    
    Returns: (kode_origin, kode_dest, None, None)
    """
    route_str = str(route_str).strip()
    
    # Handle edge case: trailing backslash (e.g., "DEL-DPS\\")
    route_str = route_str.rstrip('\\')
    
    parts = route_str.split('-')
    if len(parts) == 2:
        return parts[0].strip(), parts[1].strip(), None, None
    
    return None, None, None, None


def parse_penumpang_value(val, year):
    """
    Parse nilai penumpang sesuai format per tahun.
    
    2020: Integer/float langsung — "363789" atau "1549163.0"
    2021: Float dengan .0 — "234567.0"
    2022: Titik = ribuan — "1.234.567"
    2023: Float .0 — "234567.0"  
    2024: Integer — "234567", 0 = keep as 0 (conservative)
    """
    if val is None:
        return None
    
    val = str(val).strip().strip('"')
    
    if val in ('', ' '):
        return None
    
    try:
        if year in (2020, 2021, 2023):
            # Float format — bisa "234567.0" atau "234567"
            return int(float(val))
        elif year == 2022:
            # Titik = ribuan: "1.234.567" → 1234567
            # Tapi bisa juga float: "1549163.0"
            if '.' in val:
                parts = val.split('.')
                if all(len(p) == 3 for p in parts[1:]):
                    return int(val.replace('.', ''))
                else:
                    return int(float(val))
            return int(val)
        elif year == 2024:
            # Integer langsung, 0 = keep as 0 (conservative)
            return int(float(val))
    except (ValueError, TypeError):
        return None
    
    return None


# Mapping standardisasi nama maskapai
# Key = raw name dari CSV, Value = standar
MASKAPAI_MAPPING = {
    # BAB XII variants (pakai PT.)
    "PT. Asi Pudjiastuti": "PT Asi Pujiastuti Aviation",
    "PT. Batik Indonesia Air": "PT Batik Air Indonesia",
    "PT. Citilink Indonesia": "PT Citilink Indonesia",
    "PT. Garuda Indonesia": "PT Garuda Indonesia",
    "PT. Indonesia Airasia": "PT Indonesia AirAsia",
    "PT. Lion Mentari Airlines": "PT Lion Mentari Airlines",
    "PT. Nam Air": "PT Nam Air",
    "PT. Sriwijaya Air": "PT Sriwijaya Air",
    "PT. Transnusa Aviation Mandiri": "PT Transnusa Aviation Mandiri",
    "PT. Trigana Air Service": "PT Trigana Air Service",
    "PT. Wings Abadi Airlines": "PT Wings Abadi Airlines",
    "PT. Super Air Jet": "PT Super Air Jet",
    "PT. Pelita Air Indonesia": "PT Pelita Air Service",
    "PT. BBN Airlines Indonesia": "PT BBN Airlines Indonesia",
    
    # BAB IV variants (dari filename, uppercase)
    "PT ASI PUJIASTUTI": "PT Asi Pujiastuti Aviation",
    "PT BATIK AIR": "PT Batik Air Indonesia",
    "PT BBN AIRLINES INDONESIA": "PT BBN Airlines Indonesia",
    "PT CARDIG AIR": "PT Cardig Air",
    "PT CITILINK INDONESIA": "PT Citilink Indonesia",
    "PT GARUDA INDONESIA (Persero) Tbk.": "PT Garuda Indonesia",
    "PT INDONESIA AIRASIA": "PT Indonesia AirAsia",
    "PT LION MENTARI AIRLINES": "PT Lion Mentari Airlines",
    "PT MY INDO AIRLINES": "PT My Indo Airlines",
    "PT NAM AIR": "PT Nam Air",
    "PT PELITA AIR SERVICE": "PT Pelita Air Service",
    "PT RUSKY AERO INTERNATIONAL": "PT Rusky Aero International",
    "PT SRIWIJAYA AIR": "PT Sriwijaya Air",
    "PT SUPER AIR JET": "PT Super Air Jet",
    "PT TRANSNUSA AVIATION MANDIRI": "PT Transnusa Aviation Mandiri",
    "PT TRAVEL EXPRESS AVIATION SERVICE": "PT Travel Express Aviation Service",
    "PT TRI MG AIRLINES": "PT Tri MG Airlines",
    "PT TRIGANA AIR SERVICE": "PT Trigana Air Service",
    "WINGS ABADI AIRLINES": "PT Wings Abadi Airlines",
    
    # Typo fixes
    "PT Pelita Air Sevice": "PT Pelita Air Service",
}


def standardize_maskapai(name):
    """Standardisasi nama maskapai ke bentuk baku."""
    if name is None:
        return None
    name = str(name).strip()
    # Apply mapping
    if name in MASKAPAI_MAPPING:
        return MASKAPAI_MAPPING[name]
    # Normalize PT. → PT (tanpa titik)
    if name.startswith("PT."):
        name = "PT" + name[3:]
    return name


def maskapai_to_id(name):
    """Convert nama maskapai ke maskapai_id format."""
    name = standardize_maskapai(name)
    if name is None:
        return None
    # Strip "PT " prefix, uppercase, replace spaces with underscore
    clean = name
    if clean.upper().startswith("PT "):
        clean = clean[3:]
    return clean.upper().replace(" ", "_").replace(".", "")
