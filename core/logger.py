from datetime import datetime
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
LOG_FILE = ROOT / 'logs' / 'launcher.log'

def log(message: str):
    LOG_FILE.parent.mkdir(exist_ok=True)
    line = f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {message}"
    with LOG_FILE.open('a', encoding='utf-8') as f:
        f.write(line + '\n')
    print(line)
