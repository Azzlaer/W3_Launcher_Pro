from __future__ import annotations

import os
import shutil
import subprocess
import zipfile
from dataclasses import dataclass
from pathlib import Path

import requests


@dataclass
class GProxyConfig:
    install_path: str
    bnet_hostname: str = "eurobattle.net"
    game_port: int = 6125
    game_indicator: str = "GProxy"
    bnet_addgateway: bool = True
    debug: bool = False
    log: str = "gproxy.log"


def gproxy_dir(wc3_path: str | Path, subdir: str = "GProxy") -> Path:
    return Path(wc3_path) / subdir


def find_gproxy_exe(folder: str | Path) -> Path | None:
    folder = Path(folder)
    candidates = [
        folder / "GProxy.exe",
        folder / "GPROXY.EXE",
        folder / "gproxy.exe",
    ]
    for c in candidates:
        if c.exists():
            return c
    for c in folder.rglob("*.exe"):
        if c.name.lower() == "gproxy.exe":
            return c
    return None


def write_gproxy_cfg(folder: str | Path, cfg: GProxyConfig) -> Path:
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / "gproxy.cfg"
    addgateway = 1 if cfg.bnet_addgateway else 0
    debug = 1 if cfg.debug else 0
    text = f"""# Generado por WC3 Orc Launcher Pro
# GProxy++ protege contra desconexiones temporales al usar servidores GHost++ compatibles.
# El gateway local se agrega como localhost:6112 cuando bnet_addgateway = 1.

bnet_hostname = {cfg.bnet_hostname}
game_port = {int(cfg.game_port)}
game_indicator = {cfg.game_indicator}
bnet_addgateway = {addgateway}
debug = {debug}
log = {cfg.log}
"""
    path.write_text(text, encoding="utf-8")
    return path


def read_gproxy_cfg(folder: str | Path) -> dict[str, str]:
    path = Path(folder) / "gproxy.cfg"
    data: dict[str, str] = {}
    if not path.exists():
        return data
    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        data[k.strip()] = v.strip()
    return data


def download_gproxy_zip(url: str, target_folder: str | Path, logger=None) -> Path:
    target_folder = Path(target_folder)
    target_folder.mkdir(parents=True, exist_ok=True)
    download_path = target_folder / "GProxy-2.0.zipx"
    if logger:
        logger.log("⬇ Descargando GProxy++...")
    with requests.get(url, stream=True, timeout=120) as r:
        r.raise_for_status()
        with download_path.open("wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 256):
                if chunk:
                    f.write(chunk)
    if logger:
        logger.log(f"✅ Descargado: {download_path}")
    return download_path


def extract_gproxy_archive(archive_path: str | Path, target_folder: str | Path, logger=None) -> Path:
    archive_path = Path(archive_path)
    target_folder = Path(target_folder)
    target_folder.mkdir(parents=True, exist_ok=True)

    if zipfile.is_zipfile(archive_path):
        if logger:
            logger.log("📦 Descomprimiendo GProxy++ en carpeta del juego...")
        with zipfile.ZipFile(archive_path, "r") as zf:
            zf.extractall(target_folder)
    else:
        # Algunos mirrors usan .zipx; si no es ZIP válido se conserva para extracción manual.
        manual = target_folder / archive_path.name
        if archive_path.resolve() != manual.resolve():
            shutil.copy2(archive_path, manual)
        if logger:
            logger.log("⚠ El archivo no parece ZIP estándar. Se guardó para extracción manual.")
    return target_folder


def download_and_install_gproxy(url: str, wc3_path: str | Path, subdir: str = "GProxy", logger=None) -> Path:
    folder = gproxy_dir(wc3_path, subdir)
    archive = download_gproxy_zip(url, folder, logger=logger)
    extract_gproxy_archive(archive, folder, logger=logger)
    if logger:
        exe = find_gproxy_exe(folder)
        if exe:
            logger.log(f"✅ GProxy.exe detectado: {exe}")
        else:
            logger.log("⚠ No se encontró GProxy.exe después de extraer. Revisa el ZIP descargado.")
    return folder


def launch_gproxy(folder: str | Path, cfg_name: str = "gproxy.cfg", logger=None) -> subprocess.Popen:
    folder = Path(folder)
    exe = find_gproxy_exe(folder)
    if not exe:
        raise FileNotFoundError("No se encontró GProxy.exe. Descarga o instala GProxy primero.")
    cfg_path = folder / cfg_name
    if not cfg_path.exists():
        raise FileNotFoundError("No existe gproxy.cfg. Guarda la configuración antes de iniciar.")
    if logger:
        logger.log(f"🚀 Iniciando GProxy++ con {cfg_path.name}...")
    return subprocess.Popen(
        [str(exe), str(cfg_path.name)],
        cwd=str(folder),
        creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == "nt" else 0,
    )
