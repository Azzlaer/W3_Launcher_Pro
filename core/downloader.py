from __future__ import annotations

import io
import zipfile
from pathlib import Path

import requests


def _best_asset(assets: list[dict]) -> dict | None:
    preferred_ext = (".zip", ".7z", ".rar", ".exe")
    for ext in preferred_ext:
        for asset in assets:
            name = asset.get("name", "").lower()
            if name.endswith(ext):
                return asset
    return assets[0] if assets else None


def download_latest_warcraft_helper(api_url: str, install_path: str, logger=None) -> Path:
    if logger:
        logger.log("Buscando última release de WarcraftHelper...")
    resp = requests.get(api_url, timeout=30)
    resp.raise_for_status()
    release = resp.json()
    asset = _best_asset(release.get("assets", []))
    if not asset:
        raise RuntimeError("La release no contiene assets descargables.")

    url = asset.get("browser_download_url")
    name = asset.get("name", "WarcraftHelper.zip")
    target_dir = Path(install_path)
    target_dir.mkdir(parents=True, exist_ok=True)
    download_path = target_dir / name

    if logger:
        logger.log(f"Descargando: {name}")
    with requests.get(url, stream=True, timeout=120) as r:
        r.raise_for_status()
        with download_path.open("wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 256):
                if chunk:
                    f.write(chunk)

    if name.lower().endswith(".zip"):
        if logger:
            logger.log("Descomprimiendo ZIP en la carpeta de Warcraft III...")
        with zipfile.ZipFile(download_path, "r") as zf:
            zf.extractall(target_dir)
        if logger:
            logger.log(f"✅ Fix Tools instalado desde: {download_path.name}")
    else:
        if logger:
            logger.log(f"✅ Descargado en carpeta del juego: {download_path.name}")
    return download_path
