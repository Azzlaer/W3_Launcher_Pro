from __future__ import annotations

import subprocess
from pathlib import Path


def build_launch_command(install_path: str, exe_name: str, window_mode: bool, opengl: bool, extra_args: str = "") -> list[str]:
    exe = Path(install_path) / exe_name
    args = [str(exe)]
    if window_mode:
        args.append("-window")
    if opengl:
        args.append("-opengl")
    if extra_args.strip():
        args.extend(extra_args.strip().split())
    return args


def launch_game(install_path: str, exe_name: str, window_mode: bool, opengl: bool, extra_args: str = "") -> subprocess.Popen:
    cmd = build_launch_command(install_path, exe_name, window_mode, opengl, extra_args)
    exe = Path(cmd[0])
    if not exe.exists():
        raise FileNotFoundError(f"No existe el ejecutable: {exe}")
    return subprocess.Popen(cmd, cwd=str(exe.parent))
