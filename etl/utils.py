"""
Shared utility functions untuk ETL Pipeline v3.2
Data Warehouse: Korelasi Nilai Rupiah terhadap Angkutan Udara Indonesia (2020-2024)
Sumber kebenaran: Master_DWH_Blueprint_dan_Strategi_ETL.md
"""

import re


# ============================================================================
# FUNGSI 1: parse_angka_indonesia
# ============================================================================

def parse_angka_indonesia(val) -> int | float | None:
    """
    Konversi string angka format Indonesia ke numerik Python.

    Examples:
        "1.234.567"  → 1234567  (titik = ribuan)
        "363789"     → 363789
        "1549163.0"  → 1549163
        "-"          → 0
        ""           → None
        "61,07"      → 61.07    (koma = desimal eropa)
        '"43,76"'    → 43.76
    """
    if val is None:
        return None

    val = str(val).strip().strip('"').strip("'").strip()

    if val in ('-', '–', '—'):
        return 0
    if val in ('', 'nan', 'None', 'NaN', 'none'):
        return None

    # Koma tanpa titik → desimal eropa
    if ',' in val and '.' not in val:
        try:
            return float(val.replace(',', '.'))
        except ValueError:
            return None

    # Ada titik → cek apakah ribuan atau desimal
    if '.' in val:
        parts = val.split('.')
        # Semua segmen setelah pertama panjang 3 → titik = ribuan
        if len(parts) > 1 and all(len(p) == 3 for p in parts[1:]):
            try:
                return int(val.replace('.', ''))
            except ValueError:
                return None
        else:
            # Titik = desimal biasa
            try:
                f = float(val)
                return int(f) if f == int(f) else f
            except ValueError:
                return None

    # Tidak ada titik atau koma → integer langsung
    try:
        return int(val)
    except ValueError:
        try:
            return int(float(val))
        except (ValueError, TypeError):
            return None


# ============================================================================
# FUNGSI 2: parse_airport_name
# ============================================================================

_TAG_PATTERN = re.compile(
    r'\s*\((DOM|INT|DOMESTIK|INTERNASIONAL)\)\s*$', re.IGNORECASE
)

_TAG_MAP = {
    'DOM': 'DOMESTIK',
    'DOMESTIK': 'DOMESTIK',
    'INT': 'INTERNASIONAL',
    'INTERNASIONAL': 'INTERNASIONAL',
}


def parse_airport_name(raw: str) -> tuple[str, str, str]:
    """
    Parse kolom airport_name dari BAB VII CSV.

    Returns: (nama_bandara, kota, kategori)

    Examples:
        "SULTAN ISKANDAR MUDA - BANDA ACEH (DOM)"
        → ("SULTAN ISKANDAR MUDA", "BANDA ACEH", "DOMESTIK")

        "KUALANAMU - MEDAN (INT)"
        → ("KUALANAMU", "MEDAN", "INTERNASIONAL")

        "CUT NYAK DHIEN - NAGAN RAYA"
        → ("CUT NYAK DHIEN", "NAGAN RAYA", "DOMESTIK")

        "HALIM PERDANAKUSUMA"
        → ("HALIM PERDANAKUSUMA", "", "DOMESTIK")
    """
    raw = str(raw).strip()

    # Extract tag kategori
    match = _TAG_PATTERN.search(raw)
    if match:
        tag = match.group(1).upper()
        kategori = _TAG_MAP.get(tag, 'DOMESTIK')
        raw = raw[:match.start()].strip()
    else:
        kategori = 'DOMESTIK'

    # Split nama bandara dan kota via ' - '
    if ' - ' in raw:
        parts = raw.split(' - ', 1)
        nama_bandara = parts[0].strip()
        kota = parts[1].strip()
    else:
        nama_bandara = raw.strip()
        kota = ''

    return (nama_bandara, kota, kategori)


# ============================================================================
# FUNGSI 3: extract_iata_from_route
# ============================================================================

# Format panjang: "Jakarta (CGK) - Denpasar (DPS)" atau "Praya, Lombok (LOP) - Jakarta (CGK)"
_ROUTE_LONG_PATTERN = re.compile(
    r'(.+?)\s*\(([A-Z]{3}\*?)\)\s*[-–]\s*(.+?)\s*\(([A-Z]{3}\*?)\)\s*$'
)


def extract_iata_from_route(route_str: str) -> tuple[str, str, str, str]:
    """
    Parse string rute dari BAB III/VI CSV.

    Returns: (iata_asal, iata_tujuan, kota_asal, kota_tujuan)

    Examples:
        "Jakarta (CGK) - Denpasar (DPS)"    → ("CGK", "DPS", "Jakarta", "Denpasar")
        "CGK-DPS"                            → ("CGK", "DPS", "", "")
        "CGK - DPS"                          → ("CGK", "DPS", "", "")
    """
    route_str = str(route_str).strip()

    # Coba pattern panjang dulu
    match = _ROUTE_LONG_PATTERN.match(route_str)
    if match:
        kota_asal = match.group(1).strip()
        iata_asal = match.group(2).strip().rstrip('*')
        kota_tujuan = match.group(3).strip()
        iata_tujuan = match.group(4).strip().rstrip('*')
        return (iata_asal, iata_tujuan, kota_asal, kota_tujuan)

    # Format pendek: "CGK-DPS" atau "CGK - DPS"
    for sep in [' - ', '-', ' – ', '–']:
        if sep in route_str:
            parts = route_str.split(sep, 1)
            a = parts[0].strip().rstrip('*')
            b = parts[1].strip().rstrip('*')
            if len(a) == 3 and a.isalpha() and a.isupper() and \
               len(b) == 3 and b.isalpha() and b.isupper():
                return (a, b, '', '')
            break

    # Fallback: tidak bisa parse → return raw
    return ('', '', '', '')


# ============================================================================
# FUNGSI 4: standardize_maskapai
# ============================================================================

# Karakter Yunani → Latin (ditemukan di data asing 2023-2024)
_GREEK_TO_LATIN = str.maketrans({
    '\u039f': 'O',   # Ο → O
    '\u039c': 'M',   # Μ → M
    '\u0391': 'A',   # Α → A
    '\u039d': 'N',   # Ν → N
    '\u03a7': 'X',   # Χ → X
    '\u0399': 'I',   # Ι → I
    '\u0395': 'E',   # Ε → E
})

# Legal suffixes yang harus di-strip (case-insensitive, setelah uppercase)
_LEGAL_SUFFIXES = [
    ' (PERSERO) TBK', ' (PERSERO)', ' TBK',
    ' PTY LIMITED', ' PTY. LTD', ' PTY LTD',
    ' PTE LTD', ' PTE. LTD',
    ' SDN. BHD.', ' SDN BHD.', ' SDN. BHD', ' SDN BHD', ' SBN. BHD.',
    ' CO. LTD.', ' CO. LTD', ' CO.,LTD.', ' CO.,LTD', ' CO.LTD.',
    ' COMPANY LIMITED',
    ' S.A.O.C', ' S.A.',
    ' LIMITED', ' LTD.',  ' LTD',
    ' INC.', ' INC',
    ' BERHAD', ' BERHARD',
    ' GROUP Q.C.S.C.',
    ' JOIN STOCK COMPANY',
    ' PUBLIC COMPANY LTD',
]

# Canonical name mapping: semua varian → 1 nama standar
# Dibangun dari analisis 166 baris output awal
MASKAPAI_CANONICAL_MAP = {
    # --- ASING: AirAsia group ---
    'AIR ASIA': 'AIRASIA',
    'AIR ASIA X': 'AIRASIA X',
    'AIRASIA X': 'AIRASIA X',

    # --- ASING: All Nippon ---
    'ALL NIPPON AIRLINES': 'ALL NIPPON AIRWAYS',
    'ALL NIPPONAIRWAYS': 'ALL NIPPON AIRWAYS',

    # --- ASING: Cargolux ---
    'CARGOLUX AIRLINES INT': 'CARGOLUX AIRLINES INTERNATIONAL',

    # --- ASING: Cathay Pacific ---
    'CATHAY PACIFIC': 'CATHAY PACIFIC AIRWAYS',
    'CATHAY PACIFIC AIRLINES': 'CATHAY PACIFIC AIRWAYS',

    # --- ASING: Cebu Pacific ---
    'CEBU PACIFIC': 'CEBU PACIFIC AIR',
    'CEBU PACIFIC AIRLINES': 'CEBU PACIFIC AIR',

    # --- ASING: China Airlines ---
    'CHINA AIRLINES': 'CHINA AIRLINES',

    # --- ASING: China Eastern ---
    'CHINA EASTERN': 'CHINA EASTERN AIRLINES',

    # --- ASING: China Southern ---
    'CHINA SOUTHERN': 'CHINA SOUTHERN AIRLINES',

    # --- ASING: Egypt Air ---
    'EGYPT AIR': 'EGYPTAIR',
    'EGYPT AIRLINES': 'EGYPTAIR',

    # --- ASING: Emirates ---
    'EMIRATE': 'EMIRATES',
    'EMIRATES AIRLINE': 'EMIRATES',
    'EMIRATES AIRLINES': 'EMIRATES',

    # --- ASING: Federal Express ---
    'FEDERAL EXPRESS CORPORATION': 'FEDERAL EXPRESS',

    # --- ASING: Firefly ---
    'FIRE FLY': 'FIREFLY',
    'FLY FIRE': 'FIREFLY',
    'FLY FIREFLY': 'FIREFLY',

    # --- ASING: Jetstar ---
    'JETSTAR AIRWAYS PTY': 'JETSTAR AIRWAYS',

    # --- ASING: Jetstar Asia ---
    'JETSTAR ASIA AIRWAYS PTY': 'JETSTAR ASIA AIRWAYS',

    # --- ASING: K-Mile ---
    'K-MILE': 'K-MILE AIR',
    'K-MILE AIR COMPANY': 'K-MILE AIR',

    # --- ASING: KLM ---
    'KLM ROYAL DUTCH': 'KLM ROYAL DUTCH AIRLINES',

    # --- ASING: Korean Air ---
    'KOREAN AIRLINES': 'KOREAN AIR',

    # --- ASING: Malaysia Airlines ---
    'MALAYSIA AIRLINES': 'MALAYSIA AIRLINES',

    # --- ASING: Oman Air ---
    'OMAN AIR': 'OMAN AIR',

    # --- ASING: Philippine AirAsia ---
    'PHILIPINE AIR ASIA': 'PHILIPPINES AIRASIA',
    'PHILIPPINE AIR ASIA': 'PHILIPPINES AIRASIA',

    # --- ASING: Philippine Airlines ---
    'PHILIPINE AIRLINES': 'PHILIPPINE AIRLINES',
    'PHILIPINES AIRLINES': 'PHILIPPINE AIRLINES',

    # --- ASING: Qantas ---
    'QANTAS AIRWAYS': 'QANTAS AIRWAYS',

    # --- ASING: Qatar ---
    'QATAR AIRWAYS GROUP': 'QATAR AIRWAYS',

    # --- ASING: Raya Airways ---
    'RAYA AIRWAYS': 'RAYA AIRWAYS',

    # --- ASING: Scoot ---
    'SCOOT TIGER': 'SCOOT',
    'SCOOT TIGERAIR': 'SCOOT',
    'SCOOT': 'SCOOT',

    # --- ASING: Shenzhen ---
    'SHENZEN AIRLINES': 'SHENZHEN AIRLINES',  # typo fix

    # --- ASING: Sichuan ---
    'SICHUAN AIRLINES': 'SICHUAN AIRLINES',

    # --- ASING: Singapore Airlines ---
    'SINGAPORE AIRLINE': 'SINGAPORE AIRLINES',

    # --- ASING: Thai AirAsia ---
    'THAI AIR ASIA': 'THAI AIRASIA',

    # --- ASING: Thai Airways ---
    'THAI AIRWAYS INTL': 'THAI AIRWAYS INTERNATIONAL',
    'THAI AIRWAYS INTERNATIONAL PUBLIC': 'THAI AIRWAYS INTERNATIONAL',

    # --- ASING: Maswings ---
    'MASWINGS': 'MASWINGS',

    # --- ASING: Thai Smile ---
    'THAI SMILE AIRWAYS COMPANY': 'THAI SMILE AIRWAYS',

    # --- ASING: Turkish ---
    'TURKISH AIRLINES': 'TURKISH AIRLINES',

    # --- ASING: Vietjet ---
    'VIETJET AIR': 'VIETJET AIR',
    'VIETJET AVIATION': 'VIETJET AIR',
    'VIETJET AVIATION JOIN': 'VIETJET AIR',

    # --- ASING: Virgin Australia ---
    'VIRGIN AUSTRALIA INTL AIRLINES': 'VIRGIN AUSTRALIA',
    'VIRGIN AUSTRALIA INTERNATIONAL AIRLINES': 'VIRGIN AUSTRALIA',

    # --- ASING: Xiamen ---
    'XIAMEN AIRLINES': 'XIAMEN AIRLINES',
    'XIAMEN AIRLINES COMPANY': 'XIAMEN AIRLINES',

    # --- ASING: Word/World Cargo ---
    'WORD CARGO AIRLINES': 'WORLD CARGO AIRLINES',  # typo fix

    # --- ASING: Zhejiang ---
    'ZHEJIANG LOONG AIRLINES': 'ZHEJIANG LOONG AIRLINES',

    # --- ASING: Hongkong Dragon → Cathay Dragon (rebranded 2016) ---
    'HONGKONG DRAGON': 'CATHAY DRAGON',

    # --- ASING: Silk Air → merged into Singapore Airlines 2021 ---
    'SILK AIR': 'SILKAIR',

    # --- ASING: Valuair → subsidiary of Jetstar Asia ---
    'VALUAIR': 'VALUAIR',

    # --- NASIONAL: TRI-MG ---
    'PT TRI - M.G. INTRA ASIA AIRLINES': 'PT TRI-MG INTRA ASIA AIRLINES',
    'PT TRI-M.G. INTRA ASIA AIRLINES': 'PT TRI-MG INTRA ASIA AIRLINES',
    'PT TRI MG AIRLINES': 'PT TRI-MG INTRA ASIA AIRLINES',

    # --- NASIONAL: Rusky Aero ---
    'PT RUSKY AERO INDONESIA': 'PT RUSKY AERO INTERNASIONAL',
    'PT RUSKY AERO INTERNATIONAL': 'PT RUSKY AERO INTERNASIONAL',

    # --- NASIONAL: Susi Air ---
    'PT ASI PUJIASTUTI': 'PT ASI PUDJIASTUTI AVIATION',
    'PT ASI PUDJIASTUTI': 'PT ASI PUDJIASTUTI AVIATION',

    # --- NASIONAL: Wings ---
    'PT WINGS ABADI AIRLINES': 'PT WINGS ABADI',
    'WINGS ABADI AIRLINES': 'PT WINGS ABADI',

    # --- NASIONAL: Garuda ---
    'PT GARUDA INDONESIA (PERSERO) TBK': 'PT GARUDA INDONESIA',
    'GARUDA INDONESIA (PERSERO) TBK': 'PT GARUDA INDONESIA',

    # --- NASIONAL: others ---
    'PT TRAVEL EXPRESS AVIATION SERVICE': 'PT TRAVEL EXPRESS AVIATION SERVICES',
    'PT INDONESIA AIR ASIA': 'PT INDONESIA AIRASIA',
    'PT TRI M G INTRA ASIA AIRLINES': 'PT TRI-MG INTRA ASIA AIRLINES',
    'PT BATIK INDONESIA AIR': 'PT BATIK AIR INDONESIA',
    'PT PELITA AIR INDONESIA': 'PT PELITA AIR SERVICE',

    # --- ASING: extra ---
    'HONG KONG AIRLINES': 'HONGKONG AIRLINES',
    'INDIGO AIRLINES': 'INDIGO',
    'TATA SIA AIRLINES LTD DBA VISTARA': 'VISTARA AIRLINES',

    # --- NASIONAL: typo fix ---
    'SEVICE': 'SERVICE',
}

# Negara yang hilang (dari asing 2020 yang tidak punya kolom NEGARA)
MASKAPAI_NEGARA_FILL = {
    'EMIRATES': 'UNI EMIRAT ARAB',
    'CATHAY DRAGON': 'HONGKONG',
    'PHILIPPINE AIRLINES': 'FILIPINA',
    'PHILIPPINES AIRASIA': 'FILIPINA',
    'SHENZHEN AIRLINES': 'REPUBLIK RAKYAT TIONGKOK',
    'SILKAIR': 'SINGAPURA',
    'SCOOT': 'SINGAPURA',
}


def standardize_maskapai(nama: str) -> str:
    """
    Standardisasi nama maskapai ke format konsisten.

    Pipeline:
      1. Uppercase + strip
      2. Fix Greek characters (Ο→O, Χ→X, dll)
      3. Strip 'PT.' → 'PT'
      4. Strip asterisks
      5. Strip legal suffixes (PTY LTD, SDN BHD, INC, etc)
      6. Apply canonical mapping (merge varian ke 1 nama)
      7. Collapse whitespace

    Examples:
        "PT. Garuda Indonesia (Persero) Tbk" → "PT GARUDA INDONESIA"
        "CATHAY PACIFIC AIRWAYS LTD"         → "CATHAY PACIFIC AIRWAYS"
        "ΟΜΑΝ AIR"                           → "OMAN AIR"  (Greek → Latin)
        "ΧΙΑΜΕN AIRLINES"                    → "XIAMEN AIRLINES"
        "AIR ASIA BERHARD**"                 → "AIRASIA"
    """
    nama = str(nama).strip()
    nama = nama.upper()

    # Step 1: Fix Greek characters
    nama = nama.translate(_GREEK_TO_LATIN)

    # Step 2: Strip PT. → PT
    nama = nama.replace('PT.', 'PT')

    # Step 3: Strip asterisks
    nama = nama.replace('**', '').replace('*', '').strip()

    # Step 4: Strip legal suffixes (longest first to avoid partial matches)
    for suffix in _LEGAL_SUFFIXES:
        if nama.endswith(suffix):
            nama = nama[:-len(suffix)].strip()
            break  # Only strip one suffix per pass

    # Step 5: Collapse whitespace
    nama = re.sub(r'\s+', ' ', nama).strip()

    # Step 6: Apply canonical mapping (try longest match first)
    # First exact match
    if nama in MASKAPAI_CANONICAL_MAP:
        nama = MASKAPAI_CANONICAL_MAP[nama]
    else:
        # Try startswith for partial matches (e.g. "QATAR AIRWAYS GROUP Q.C.S.C." after suffix strip)
        for variant, canonical in sorted(MASKAPAI_CANONICAL_MAP.items(), key=lambda x: -len(x[0])):
            if nama.startswith(variant) and nama != canonical:
                nama = canonical
                break

    return nama


# ============================================================================
# FUNGSI 5: normalize_jenis_kegiatan
# ============================================================================

def normalize_jenis_kegiatan(val: str) -> str:
    """
    Standardisasi jenis_kegiatan dari BAB II ke ENUM.

    Returns: 'PENUMPANG' | 'KARGO' | 'PENUMPANG & KARGO'

    Examples:
        "Penumparig"          → "PENUMPANG"
        "Perumpang"           → "PENUMPANG"
        "Cargo"               → "KARGO"
        "Khusus Kargo"        → "KARGO"
        "Penumpang dan Kargo" → "PENUMPANG & KARGO"
        "Penumpang & Cargo"   → "PENUMPANG & KARGO"
        "Penumpang."          → "PENUMPANG"
    """
    val = str(val).strip().strip('.').strip().upper()

    # Fix typos
    val = val.replace('PENUMPARIG', 'PENUMPANG')
    val = val.replace('PERUMPANG', 'PENUMPANG')
    val = val.replace('CARGO', 'KARGO')

    # Determine category
    has_penumpang = 'PENUMPANG' in val
    has_kargo = 'KARGO' in val

    if has_penumpang and has_kargo:
        return 'PENUMPANG & KARGO'
    elif has_kargo:
        # Termasuk "KHUSUS KARGO"
        return 'KARGO'
    elif has_penumpang:
        return 'PENUMPANG'
    else:
        # Fallback — log warning
        print(f"  ⚠️ jenis_kegiatan tidak dikenali: '{val}' → default 'PENUMPANG'")
        return 'PENUMPANG'


# ============================================================================
# KONSTANTA 6: BANDARA_IATA_MAP (Placeholder — diisi saat Phase B dim_bandara)
# ============================================================================

# Format: nama_bandara (dari BAB VII, setelah strip tag) → kode IATA
# Akan diisi ~200-300 entri setelah Phase A extract + fuzzy match + manual review
BANDARA_IATA_MAP: dict[str, str] = {
    # === Placeholder — akan dikembangkan di Gelombang 2 ===
    "SOEKARNO-HATTA": "CGK",
    "HALIM PERDANAKUSUMA": "HLP",
    "HALIM PERDANAKUSUMAH": "HLP",
    "NGURAH RAI": "DPS",
    "JUANDA": "SUB",
    "SULTAN HASANUDDIN": "UPG",
    "KUALANAMU": "KNO",
    "HANG NADIM": "BTH",
    "MINANGKABAU": "PDG",
    "HUSEIN SASTRANEGARA": "BDO",
    "SULTAN AJI MUHAMMAD SULAIMAN SEPINGGAN": "BPN",
    "ADIAN SUCIPTO": "JOG",
}

# Reverse lookup: IATA → nama kota (auto-populated dari extract_iata_from_route)
IATA_KOTA_MAP: dict[str, str] = {
    "CGK": "Jakarta",
    "DPS": "Denpasar",
    "SUB": "Surabaya",
    "UPG": "Makassar",
    "KNO": "Medan",
    "BTH": "Batam",
    "PDG": "Padang",
    "BDO": "Bandung",
    "BPN": "Balikpapan",
    "JOG": "Yogyakarta",
}
