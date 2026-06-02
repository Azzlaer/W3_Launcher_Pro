from __future__ import annotations

import configparser
from pathlib import Path


DEFAULT_CONFIG = {
    "GAME": {
        "install_path": r"D:\\Juegos\\Blizzard\\Warcraft III",
        "normal_loader_exe": "w3l.exe",
        "rubattle_loader_exe": "w3l_rubattle.exe",
        "launcher_exe": "w3l.exe",
        "war3_exe": "War3.exe",
        "warcraft_exe": "Warcraft III.exe",
        "frozen_throne_exe": "Frozen Throne.exe",
        "world_editor_exe": "World Editor.exe",
        "default_edition": "Frozen Throne",
        "default_loader": "W3 Loader normal",
    },
    "LAUNCH": {
        "window_mode": "true",
        "opengl": "false",
        "cleanup_registry_before_launch": "false",
        "fix_world_editor_before_launch": "true",
        "add_gateways_before_launch": "true",
        "apply_resolution_before_launch": "false",
        "apply_shadows_before_launch": "false",
        "unit_shadows": "true",
        "selected_resolution": "1280x720",
        "extra_args": "",
    },
    "TOOLS": {
        "warcraft_helper_releases_url": "https://github.com/LoveBeforT/WarcraftHelper/releases",
        "warcraft_helper_api_latest": "https://api.github.com/repos/LoveBeforT/WarcraftHelper/releases/latest",
        "rubattle_loader_url": "http://www.playground.ru/download/?file=142613",
        "w3l_126_128_url": "http://cdn.pvpgn.pro/w3l/w3l_1_5_1_1_by_Keres.zip",
        "w3l_127_url": "http://cdn.pvpgn.pro/w3l/w3l_1_4_2_by_Keres.zip",
        "w3l_zip_password": "pvpgn",
    },
    "MAPS": {
        "download_folder": r"Maps\\Download",
    },
    "GPROXY": {
        "github_url": "https://github.com/dns/GProxy-Warcraft3-disconnect-protection-tool",
        "download_url": "https://github.com/dns/GProxy-Warcraft3-disconnect-protection-tool/releases/download/v2.0/GProxy-2.0.zipx",
        "install_subdir": "GProxy",
        "bnet_hostname": "eurobattle.net",
        "game_port": "6125",
        "game_indicator": "GProxy",
        "bnet_addgateway": "true",
        "debug": "false",
        "log": "gproxy.log",
        "auto_start_before_game": "false",
    },
}


class ConfigManager:
    def __init__(self, path: str | Path = "config.ini"):
        self.path = Path(path)
        self.config = configparser.ConfigParser()
        self.load()

    def load(self) -> None:
        if not self.path.exists():
            self.config.read_dict(DEFAULT_CONFIG)
            self.save()
            return
        self.config.read(self.path, encoding="utf-8")
        changed = False
        for section, values in DEFAULT_CONFIG.items():
            if not self.config.has_section(section):
                self.config.add_section(section)
                changed = True
            for key, value in values.items():
                if not self.config.has_option(section, key):
                    self.config.set(section, key, value)
                    changed = True
        if changed:
            self.save()

    def save(self) -> None:
        with self.path.open("w", encoding="utf-8") as f:
            self.config.write(f)

    def get(self, section: str, key: str, fallback: str = "") -> str:
        return self.config.get(section, key, fallback=fallback)

    def get_bool(self, section: str, key: str, fallback: bool = False) -> bool:
        return self.config.getboolean(section, key, fallback=fallback)

    def set(self, section: str, key: str, value: str | bool | int) -> None:
        if not self.config.has_section(section):
            self.config.add_section(section)
        if isinstance(value, bool):
            value = "true" if value else "false"
        self.config.set(section, key, str(value))
        self.save()
