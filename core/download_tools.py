from __future__ import annotations
import json
import os
import re
import subprocess
import webbrowser
import zipfile
from pathlib import Path
from urllib.parse import urlparse

import requests

ROOT = Path(__file__).resolve().parents[1]


def download_file(url: str, dest: Path, progress=None):
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    with requests.get(url, stream=True, timeout=90, headers={"User-Agent": "WC3-Orc-Launcher-Pro"}) as r:
        r.raise_for_status()
        total = int(r.headers.get('content-length', 0) or 0)
        done = 0
        with dest.open('wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 64):
                if chunk:
                    f.write(chunk)
                    done += len(chunk)
                    if progress:
                        progress(done, total)
    return dest


def filename_from_url(url: str, fallback: str = "download.bin") -> str:
    name = Path(urlparse(url).path).name.strip()
    return name or fallback


def normalize_zipx_to_zip(path: Path) -> Path:
    """Rename .zipx downloads to .zip so Python/7-Zip/WinRAR recognize them easier.

    The old GProxy release is published as GProxy-2.0.zipx, but the file is intended
    to be handled as a compressed archive. This launcher keeps the same base name and
    changes only the final extension: GProxy-2.0.zipx -> GProxy-2.0.zip.
    """
    path = Path(path)
    if path.suffix.lower() != ".zipx":
        return path
    zip_path = path.with_suffix(".zip")
    if zip_path.exists():
        zip_path.unlink()
    path.rename(zip_path)
    return zip_path


def extract_zip(src: Path, dest: Path, password: str | None = None):
    dest.mkdir(parents=True, exist_ok=True)
    pwd = password.encode() if password else None
    with zipfile.ZipFile(src, 'r') as z:
        z.extractall(dest, pwd=pwd)
    return dest



def _find_external_extractor() -> tuple[str, list[str]] | tuple[None, None]:
    """Find 7-Zip or WinRAR on Windows/Linux. Returns executable and base args.

    Python's zipfile cannot read some ZIPX compression methods. 7-Zip and
    WinRAR usually can, so we use them as an automatic fallback when available.
    """
    import shutil
    candidates = [
        (shutil.which("7z"), ["x", "-y"]),
        (shutil.which("7za"), ["x", "-y"]),
        (shutil.which("7zr"), ["x", "-y"]),
        (shutil.which("WinRAR"), ["x", "-y"]),
        (shutil.which("UnRAR"), ["x", "-y"]),
    ]
    common_paths = [
        (r"C:\Program Files\7-Zip\7z.exe", ["x", "-y"]),
        (r"C:\Program Files (x86)\7-Zip\7z.exe", ["x", "-y"]),
        (r"C:\Program Files\WinRAR\WinRAR.exe", ["x", "-y"]),
        (r"C:\Program Files (x86)\WinRAR\WinRAR.exe", ["x", "-y"]),
        (r"C:\Program Files\WinRAR\UnRAR.exe", ["x", "-y"]),
        (r"C:\Program Files (x86)\WinRAR\UnRAR.exe", ["x", "-y"]),
    ]
    candidates.extend([(str(Path(x)), args) for x, args in common_paths if Path(x).exists()])
    for exe, args in candidates:
        if exe:
            return exe, args
    return None, None


def extract_archive_robust(src: Path, dest: Path, password: str | None = None, log=None):
    """Extract an archive with Python first, then 7-Zip/WinRAR fallback.

    Returns a tuple: (success: bool, message: str). This avoids crashing the GUI
    on ZIPX files that use compression methods not supported by Python zipfile.
    """
    src = Path(src)
    dest = Path(dest)
    dest.mkdir(parents=True, exist_ok=True)

    try:
        extract_zip(src, dest, password=password)
        return True, f"Archivo descomprimido con Python en: {dest}"
    except Exception as py_error:
        if log:
            log(f"Python no pudo descomprimir el archivo: {py_error}")
            log("Intentando con extractor externo: 7-Zip / WinRAR...")

    exe, args = _find_external_extractor()
    if not exe:
        return False, (
            "El archivo fue descargado correctamente, pero usa un método de compresión "
            "que Python no soporta. Instala 7-Zip o WinRAR y vuelve a pulsar el botón, "
            f"o extrae manualmente: {src}"
        )

    cmd = [exe, *args]
    if password and "7z" in Path(exe).name.lower():
        cmd.append(f"-p{password}")
    cmd += [str(src), f"-o{dest}"]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        if result.returncode == 0:
            return True, f"Archivo descomprimido con {Path(exe).name} en: {dest}"
        return False, (
            f"{Path(exe).name} no pudo descomprimir el archivo. Código: {result.returncode}\n"
            f"STDOUT: {result.stdout[-800:]}\nSTDERR: {result.stderr[-800:]}"
        )
    except Exception as ext_error:
        return False, f"Error usando extractor externo {exe}: {ext_error}"


def get_latest_github_release_asset(repo: str, asset_regex: str, fallback_url: str = "") -> str:
    """Return the latest GitHub release asset URL matching asset_regex.

    If GitHub is unavailable or there is no matching asset, returns fallback_url.
    Example repo: dns/GProxy-Warcraft3-disconnect-protection-tool
    """
    api = f"https://api.github.com/repos/{repo}/releases/latest"
    try:
        r = requests.get(api, timeout=15, headers={"User-Agent": "WC3-Orc-Launcher-Pro"})
        r.raise_for_status()
        data = r.json()
        pattern = re.compile(asset_regex, re.I)
        for asset in data.get("assets", []):
            name = asset.get("name", "")
            if pattern.search(name):
                return asset.get("browser_download_url") or fallback_url
    except Exception:
        pass
    return fallback_url


def open_url(url: str):
    webbrowser.open(url)


def start_process(path: Path, args=None, cwd=None):
    args = args or []
    return subprocess.Popen([str(path), *args], cwd=str(cwd or path.parent))
