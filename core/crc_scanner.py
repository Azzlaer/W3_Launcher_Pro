from __future__ import annotations
from pathlib import Path
import zlib, csv, datetime
from .crc_database import ORIGINALS, SUSPECT, ALLOWED_TOOLS, W3L_CRC

def crc32_file(path: Path) -> str:
    c = 0
    with Path(path).open('rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            c = zlib.crc32(chunk, c)
    return f'{c & 0xffffffff:08X}'

def scan_version(folder: Path, version: str):
    rows=[]
    for name, expected in ORIGINALS.get(version, {}).items():
        p = Path(folder) / name
        if not p.exists():
            rows.append((name, expected, '', 'NO EXISTE'))
        else:
            got = crc32_file(p)
            rows.append((name, expected, got, 'OK' if got.upper()==expected.upper() else 'MODIFICADO'))
    return rows

def scan_known(folder: Path):
    rows=[]
    for dbname, db, status in [('Sospechoso', SUSPECT, 'ALERTA'), ('Permitido', ALLOWED_TOOLS, 'PERMITIDO')]:
        for name, expected in db.items():
            p=Path(folder)/name
            if p.exists():
                got=crc32_file(p)
                rows.append((dbname, name, expected, got, status if got.upper()==expected.upper() else 'CRC DIFERENTE'))
    return rows

def identify_w3l(folder: Path):
    p = Path(folder) / 'w3l.exe'
    if not p.exists():
        return [('w3l.exe', '', '', 'NO EXISTE')]
    got = crc32_file(p)
    hits=[]
    for ver, items in W3L_CRC.items():
        for label, crc in items.items():
            if got.upper()==crc.upper():
                hits.append((label, ver, got, 'IDENTIFICADO'))
    return hits or [('w3l.exe', 'Desconocido', got, 'NO RECONOCIDO')]

def export_csv(rows, dest):
    dest=Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open('w', newline='', encoding='utf-8-sig') as f:
        w=csv.writer(f); w.writerows(rows)
    return dest
