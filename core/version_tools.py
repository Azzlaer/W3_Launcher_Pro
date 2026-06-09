from __future__ import annotations
import ctypes
from pathlib import Path

def file_version(path):
    path = str(Path(path))
    try:
        size = ctypes.windll.version.GetFileVersionInfoSizeW(path, None)
        if not size:
            return 'No disponible'
        res = ctypes.create_string_buffer(size)
        ctypes.windll.version.GetFileVersionInfoW(path, 0, size, res)
        r = ctypes.c_void_p()
        l = ctypes.c_uint()
        ctypes.windll.version.VerQueryValueW(res, '\\', ctypes.byref(r), ctypes.byref(l))
        class VS_FIXEDFILEINFO(ctypes.Structure):
            _fields_ = [('dwSignature', ctypes.c_uint32),('dwStrucVersion', ctypes.c_uint32),('dwFileVersionMS', ctypes.c_uint32),('dwFileVersionLS', ctypes.c_uint32),('dwProductVersionMS', ctypes.c_uint32),('dwProductVersionLS', ctypes.c_uint32),('dwFileFlagsMask', ctypes.c_uint32),('dwFileFlags', ctypes.c_uint32),('dwFileOS', ctypes.c_uint32),('dwFileType', ctypes.c_uint32),('dwFileSubtype', ctypes.c_uint32),('dwFileDateMS', ctypes.c_uint32),('dwFileDateLS', ctypes.c_uint32)]
        ffi = ctypes.cast(r, ctypes.POINTER(VS_FIXEDFILEINFO)).contents
        return f"{ffi.dwFileVersionMS >> 16}.{ffi.dwFileVersionMS & 0xffff}.{ffi.dwFileVersionLS >> 16}.{ffi.dwFileVersionLS & 0xffff}"
    except Exception as e:
        return f'No disponible ({e})'
