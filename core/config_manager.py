from __future__ import annotations
import configparser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_FILE = ROOT / 'config.ini'

class ConfigManager:
    def __init__(self, path: Path = CONFIG_FILE):
        self.path = Path(path)
        self.config = configparser.ConfigParser()
        self.load()

    def load(self):
        self.config.read(self.path, encoding='utf-8')
        return self.config

    def save(self):
        with self.path.open('w', encoding='utf-8') as f:
            self.config.write(f)

    def get(self, section: str, key: str, fallback: str = '') -> str:
        return self.config.get(section, key, fallback=fallback)

    def getbool(self, section: str, key: str, fallback: bool = False) -> bool:
        return self.config.getboolean(section, key, fallback=fallback)

    def set(self, section: str, key: str, value):
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, str(value))
        self.save()

    @property
    def warcraft_path(self) -> Path:
        return Path(self.get('GENERAL', 'warcraft_path', '.'))
