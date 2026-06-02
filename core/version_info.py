from __future__ import annotations

import ctypes
from ctypes import wintypes
from pathlib import Path


def get_file_version(path: str | Path) -> dict[str, str]:
    """Obtiene FileVersion y ProductVersion desde recursos VERSIONINFO de un EXE/DLL."""
    path = str(Path(path))
    result = {"file_version": "No disponible", "product_version": "No disponible"}
    if not Path(path).exists():
        result["error"] = "Archivo no encontrado"
        return result

    size = ctypes.windll.version.GetFileVersionInfoSizeW(path, None)
    if not size:
        result["error"] = "El archivo no contiene VERSIONINFO legible"
        return result

    buffer = ctypes.create_string_buffer(size)
    if not ctypes.windll.version.GetFileVersionInfoW(path, 0, size, buffer):
        result["error"] = "No se pudo leer VERSIONINFO"
        return result

    trans_ptr = ctypes.c_void_p()
    trans_len = wintypes.UINT()
    if ctypes.windll.version.VerQueryValueW(buffer, r"\VarFileInfo\Translation", ctypes.byref(trans_ptr), ctypes.byref(trans_len)):
        lang_codepage = ctypes.cast(trans_ptr, ctypes.POINTER(wintypes.WORD * 2)).contents
        lang = f"{lang_codepage[0]:04x}{lang_codepage[1]:04x}"
    else:
        lang = "040904b0"

    def query(name: str) -> str:
        value_ptr = ctypes.c_wchar_p()
        value_len = wintypes.UINT()
        sub_block = f"\\StringFileInfo\\{lang}\\{name}"
        ok = ctypes.windll.version.VerQueryValueW(buffer, sub_block, ctypes.byref(value_ptr), ctypes.byref(value_len))
        return value_ptr.value if ok and value_ptr.value else "No disponible"

    result["file_version"] = query("FileVersion")
    result["product_version"] = query("ProductVersion")
    return result
