from __future__ import annotations

import binascii
from pathlib import Path
from typing import Iterable


def crc32_file(path: str | Path) -> str:
    p = Path(path)
    crc = 0
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            crc = binascii.crc32(chunk, crc)
    return f"{crc & 0xFFFFFFFF:08X}"


def scan_named_files(base: str | Path, files: Iterable[str]) -> list[dict]:
    base_path = Path(base)
    rows: list[dict] = []
    for name in files:
        p = base_path / name
        if p.exists() and p.is_file():
            try:
                crc = crc32_file(p)
                status = "OK"
            except Exception as e:
                crc = "ERROR"
                status = str(e)
        else:
            crc = "NO_EXISTE"
            status = "No encontrado"
        rows.append({"file": name, "path": str(p), "crc": crc, "status": status})
    return rows


def compare_crc(base: str | Path, expected: dict[str, str]) -> list[dict]:
    rows = []
    for item in scan_named_files(base, expected.keys()):
        exp = expected.get(item["file"], "").upper()
        got = item["crc"].upper()
        if got == "NO_EXISTE":
            result = "FALTA"
        elif exp == "SIN_CRC":
            result = "PRESENTE"
        elif got == exp:
            result = "ORIGINAL"
        else:
            result = "MODIFICADO"
        item["expected"] = exp
        item["result"] = result
        rows.append(item)
    return rows
