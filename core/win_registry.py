from __future__ import annotations

import subprocess
import winreg
from pathlib import Path
from typing import Any

ROOTS = {
    "HKCU": winreg.HKEY_CURRENT_USER,
    "HKEY_CURRENT_USER": winreg.HKEY_CURRENT_USER,
    "HKLM": winreg.HKEY_LOCAL_MACHINE,
    "HKEY_LOCAL_MACHINE": winreg.HKEY_LOCAL_MACHINE,
    "HKCR": winreg.HKEY_CLASSES_ROOT,
    "HKEY_CLASSES_ROOT": winreg.HKEY_CLASSES_ROOT,
}

DELETE_KEYS = [
    ("HKCU", r"SOFTWARE\Battle.net"),
    ("HKCU", r"SOFTWARE\Blizzard Entertainment"),
    ("HKLM", r"SOFTWARE\WOW6432Node\Blizzard Entertainment"),
    ("HKCR", r"Warcraft3.Replay"),
    ("HKCR", r"WorldEdit.Scenario"),
    ("HKCR", r"WorldEdit.Campaign"),
    ("HKCR", r"WorldEdit.AIData"),
]

WC3_KEY = r"Software\Blizzard Entertainment\Warcraft III"
WC3_VIDEO_KEY = WC3_KEY + r"\Video"
WORLDEDIT_KEY = r"Software\Blizzard Entertainment\WorldEdit"

GATEWAYS = [
    "1001", "01",
    "47.180.222.51", "-3", "LatinBattle",
    "26.79.212.213", "-4", "LatinBattle.Radmin",
    "worldofeditors.net", "-4", "WorldEditors",
    "olds.ar", "-4", "OldServers",
    "rubattle.net", "-4", "Rubattle",
    "server.tsgamerz.com", "-3", "TSGamerZ",
    "war3.nightbot.ru", "-4", "NightBot",
    "ingame.go.ro", "-4", "ICCup",
    "europe.warcraft3.eu", "-4", "EuropeBattle",
    "pvpgn.onligamez.ru", "-4", "OZBNet",
    "116.203.95.137", "-4", "eurobattle.net",
    "185.231.245.32", "-4", "NightBot",
]


def _create_key(root_name: str, sub_key: str):
    return winreg.CreateKeyEx(ROOTS[root_name], sub_key, 0, winreg.KEY_SET_VALUE | winreg.KEY_CREATE_SUB_KEY)


def set_value(root_name: str, sub_key: str, name: str, value: Any, reg_type: int) -> None:
    with _create_key(root_name, sub_key) as key:
        winreg.SetValueEx(key, name, 0, reg_type, value)


def set_dword(root_name: str, sub_key: str, name: str, value: int) -> None:
    set_value(root_name, sub_key, name, int(value), winreg.REG_DWORD)


def set_string(root_name: str, sub_key: str, name: str, value: str) -> None:
    set_value(root_name, sub_key, name, value, winreg.REG_SZ)


def set_default(root_name: str, sub_key: str, value: str) -> None:
    set_string(root_name, sub_key, "", value)


def delete_tree(root_name: str, sub_key: str) -> tuple[bool, str]:
    try:
        subprocess.run(["reg", "delete", f"{root_name}\\{sub_key}", "/f"], check=True, capture_output=True, text=True)
        return True, f"Eliminado: {root_name}\\{sub_key}"
    except subprocess.CalledProcessError as e:
        msg = (e.stderr or e.stdout or "").strip()
        if "no se encuentra" in msg.lower() or "unable to find" in msg.lower() or "cannot find" in msg.lower():
            return True, f"No existía: {root_name}\\{sub_key}"
        return False, f"Error eliminando {root_name}\\{sub_key}: {msg}"


def cleanup_blizzard_registry(logger=None) -> None:
    for root, sub in DELETE_KEYS:
        ok, msg = delete_tree(root, sub)
        if logger:
            logger.log(("✅ " if ok else "❌ ") + msg)


def apply_world_editor_fix(logger=None) -> None:
    values = {
        "Has Been Run": 1,
        "Minimap - Show Creep Camps": 1,
        "Minimap - Show Game Area Only": 1,
        "Minimap - Show Icons": 1,
        "Allow Local Files": 1,
    }
    for name, value in values.items():
        set_dword("HKCU", WORLDEDIT_KEY, name, value)
        if logger:
            logger.log(f"✅ WorldEdit: {name} = {value}")


def apply_gateways(logger=None) -> None:
    # REG_MULTI_SZ equivalente al hex(7) que compartiste.
    set_value("HKCU", WC3_KEY, "Battle.net Gateways", GATEWAYS, winreg.REG_MULTI_SZ)
    if logger:
        logger.log(f"✅ Gateways Battle.net instalados: {len(GATEWAYS)//3} servidores aproximados")


def apply_resolution(width: int, height: int, logger=None) -> None:
    set_dword("HKCU", WC3_VIDEO_KEY, "reswidth", width)
    set_dword("HKCU", WC3_VIDEO_KEY, "resheight", height)
    if logger:
        logger.log(f"✅ Resolución aplicada en registro: {width}x{height}")


def apply_unit_shadows(enabled: bool, logger=None) -> None:
    set_dword("HKCU", WC3_VIDEO_KEY, "unitshadows", 1 if enabled else 0)
    if logger:
        logger.log(f"✅ Sombras de unidades: {'activadas' if enabled else 'desactivadas'}")


def apply_base_install_registry(install_path: str, logger=None) -> None:
    p = Path(install_path)
    set_string("HKCU", WC3_KEY, "InstallPath", str(p))
    set_string("HKCU", WC3_KEY, "InstallPathX", str(p))
    set_string("HKCU", WC3_KEY, "Program", str(p / "Warcraft III.exe"))
    set_string("HKCU", WC3_KEY, "ProgramX", str(p / "Frozen Throne.exe"))
    set_string("HKCU", WC3_KEY, "War3CD", "")
    set_string("HKCU", WC3_KEY, "War3XCD", "")
    set_dword("HKCU", WC3_KEY, "Allow Local Files", 1)
    set_dword("HKCU", WC3_KEY, "Preferred Game Version", 1)
    set_dword("HKCU", WC3_KEY, "Migration Complete", 1)
    if logger:
        logger.log("✅ Registro base de Warcraft III aplicado")


def apply_file_associations(install_path: str, logger=None) -> None:
    p = Path(install_path)
    associations = [
        (".w3g", "Warcraft3.Replay", "Warcraft III Replay File", str(p / "Replays.ico"), f'"{p / "War3.exe"}" -loadfile "%1"'),
        (".w3m", "WorldEdit.Scenario", "Warcraft III Scenario File", f'{p / "WorldEdit.exe"},2', f'"{p / "World Editor.exe"}" -loadfile "%1"'),
        (".w3n", "WorldEdit.Campaign", "Warcraft III Campaign File", f'{p / "WorldEdit.exe"},4', f'"{p / "World Editor.exe"}" -loadfile "%1"'),
        (".w3x", "WorldEdit.ScenarioEx", "Warcraft III Expansion Scenario File", f'{p / "WorldEdit.exe"},3', f'"{p / "World Editor.exe"}" -loadfile "%1"'),
        (".wai", "WorldEdit.AIData", "Warcraft III AI Data File", f'{p / "WorldEdit.exe"},5', f'"{p / "World Editor.exe"}" -loadfile "%1"'),
    ]
    for ext, cls, desc, icon, command in associations:
        set_default("HKCR", ext, cls)
        set_default("HKCR", cls, desc)
        set_default("HKCR", cls + r"\DefaultIcon", icon)
        set_default("HKCR", cls + r"\shell\open\command", command)
        if logger:
            logger.log(f"✅ Asociación aplicada: {ext} -> {cls}")


def apply_gameplay_defaults(logger=None) -> None:
    gameplay = WC3_KEY + r"\Gameplay"
    values = {
        "gamespeed": 3, "mousescroll": 50, "mousescrolldisable": 0, "keyscroll": 50,
        "tooltips": 1, "healthbars": 1, "formations": 1, "formationtoggle": 1,
        "herobar": 1, "netgameport": 0x17ED, "inputsprocket": 0, "ammtype": 0,
        "ammrace": 0x20, "customfilter": 0, "custommask": 0, "allyFilter": 0,
        "creepFilter": 1, "terrainFilter": 1, "subgrouporder": 0, "multiboardon": 0,
        "customkeys": 1, "schedrace": 0x20, "autosaveReplay": 1,
    }
    for k, v in values.items():
        set_dword("HKCU", gameplay, k, v)
    set_string("HKCU", gameplay, "ammstyles", "0;")
    set_string("HKCU", gameplay, "ammmapprefs", "1;")
    set_string("HKCU", gameplay, "ammmaphashes", "B7B031FA;")
    if logger:
        logger.log("✅ Gameplay defaults aplicados")


def apply_video_quality_defaults(logger=None) -> None:
    values = {
        "colordepth": 32, "adapter": 0, "refreshrate": 60, "gamma": 25,
        "modeldetail": 2, "animquality": 2, "texquality": 2, "miplevel": 0,
        "texcolordepth": 32, "particles": 2, "lights": 2, "lockfb": 1,
        "unitshadows": 1, "occlusion": 1, "cinematicoverrides": 0, "cinematicrefresh": 75,
        "cinematicbpp": 32, "cinematicwidth": 800, "cinematicheight": 600,
        "spellfilter": 2, "maxfps": 200, "fixedaspect": 0,
    }
    for k, v in values.items():
        set_dword("HKCU", WC3_VIDEO_KEY, k, v)
    if logger:
        logger.log("✅ Video quality defaults aplicados")


def apply_misc_sound_string_defaults(username: str = "Azzlaer", logger=None) -> None:
    misc = WC3_KEY + r"\Misc"
    sound = WC3_KEY + r"\Sound"
    string = WC3_KEY + r"\String"
    for k, v in {"seenintromovie": 1, "clickedtourn": 0, "clickedclan": 0, "clickedladder": 0, "clickedad": 0, "chatsupport": 0}.items():
        set_dword("HKCU", misc, k, v)
    set_string("HKCU", misc, "campaignprofile", username)
    for k, v in {
        "provider": 1, "positional": 1, "environmental": 1, "music": 1, "musicvolume": 16,
        "sfx": 1, "sfxvolume": 56, "ambient": 1, "movement": 1, "unit": 1,
        "subtitles": 1, "nomidi": 0, "softwaremidi": 1, "nosoundwarn": 1, "donotusewaveout": 0,
    }.items():
        set_dword("HKCU", sound, k, v)
    set_string("HKCU", string, "userbnet", username)
    set_string("HKCU", string, "userlocal", username)
    if logger:
        logger.log("✅ Misc/Sound/String defaults aplicados")
