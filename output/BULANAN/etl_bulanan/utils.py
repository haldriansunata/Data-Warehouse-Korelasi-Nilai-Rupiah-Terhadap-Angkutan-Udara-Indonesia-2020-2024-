"""
Utility kecil untuk ETL Bulanan (versi ringkas, hanya yang dipakai pipeline bulanan).
"""
import re


def parse_angka_indonesia(val):
    """
    Konversi string angka format Indonesia ke numerik Python.
        "1.234.567" → 1234567       (titik ribuan)
        "61,07"     → 61.07         (koma desimal eropa)
        "-"         → 0
        "" / None   → None
    """
    if val is None:
        return None
    val = str(val).strip().strip('"').strip("'").strip()
    if val in ('-', '–', '—'):
        return 0
    if val in ('', 'nan', 'None', 'NaN', 'none'):
        return None
    if ',' in val and '.' not in val:
        try:
            return float(val.replace(',', '.'))
        except ValueError:
            return None
    if '.' in val:
        parts = val.split('.')
        if len(parts) > 1 and all(len(p) == 3 for p in parts[1:]):
            try:
                return int(val.replace('.', ''))
            except ValueError:
                return None
        try:
            f = float(val)
            return int(f) if f == int(f) else f
        except ValueError:
            return None
    try:
        return int(val)
    except ValueError:
        try:
            return int(float(val))
        except (ValueError, TypeError):
            return None


_ROUTE_LONG_PATTERN = re.compile(
    r'(.+?)\s*\(([A-Z]{3}\*?)\)\s*[-–]\s*(.+?)\s*\(([A-Z]{3}\*?)\)\s*$'
)


def extract_iata_from_route(route_str):
    """
    Parse string rute → (iata_asal, iata_tujuan, kota_asal, kota_tujuan).
        "Jakarta (CGK) - Denpasar (DPS)" → ("CGK","DPS","Jakarta","Denpasar")
        "CGK-DPS"                         → ("CGK","DPS","","")
    """
    route_str = str(route_str).strip()
    m = _ROUTE_LONG_PATTERN.match(route_str)
    if m:
        return (m.group(2).strip().rstrip('*'),
                m.group(4).strip().rstrip('*'),
                m.group(1).strip(),
                m.group(3).strip())
    for sep in [' - ', '-', ' – ', '–']:
        if sep in route_str:
            parts = route_str.split(sep, 1)
            a = parts[0].strip().rstrip('*')
            b = parts[1].strip().rstrip('*')
            if (len(a) == 3 and a.isalpha() and a.isupper()
                and len(b) == 3 and b.isalpha() and b.isupper()):
                return (a, b, '', '')
            break
    return ('', '', '', '')
