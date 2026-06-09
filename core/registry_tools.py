from __future__ import annotations
import sys

IS_WINDOWS = sys.platform.startswith('win')
if IS_WINDOWS:
    import winreg

DELETE_KEYS = [
    ('HKCU', r'SOFTWARE\Battle.net'),
    ('HKCU', r'SOFTWARE\Blizzard Entertainment'),
    ('HKLM', r'SOFTWARE\WOW6432Node\Blizzard Entertainment'),
    ('HKCR', r'Warcraft3.Replay'),
    ('HKCR', r'WorldEdit.Scenario'),
    ('HKCR', r'WorldEdit.Campaign'),
    ('HKCR', r'WorldEdit.AIData'),
]

ROOTS = {}
if IS_WINDOWS:
    ROOTS = {'HKCU': winreg.HKEY_CURRENT_USER, 'HKLM': winreg.HKEY_LOCAL_MACHINE, 'HKCR': winreg.HKEY_CLASSES_ROOT}

def _delete_tree(root, subkey):
    with winreg.OpenKey(root, subkey, 0, winreg.KEY_READ | winreg.KEY_WRITE) as key:
        while True:
            try:
                child = winreg.EnumKey(key, 0)
                _delete_tree(root, subkey + '\\' + child)
            except OSError:
                break
    winreg.DeleteKey(root, subkey)

def delete_warcraft_registry():
    if not IS_WINDOWS:
        return ['Registro solo disponible en Windows.']
    out=[]
    for hive, path in DELETE_KEYS:
        try:
            _delete_tree(ROOTS[hive], path)
            out.append(f'Eliminado: {hive}\\{path}')
        except FileNotFoundError:
            out.append(f'No existe: {hive}\\{path}')
        except PermissionError:
            out.append(f'Permiso denegado: {hive}\\{path} - ejecuta como administrador')
        except Exception as e:
            out.append(f'Error {hive}\\{path}: {e}')
    return out

def set_dword(hive, path, name, value):
    if not IS_WINDOWS: return 'Registro solo disponible en Windows.'
    with winreg.CreateKeyEx(ROOTS[hive], path, 0, winreg.KEY_WRITE) as key:
        winreg.SetValueEx(key, name, 0, winreg.REG_DWORD, int(value))
    return f'{hive}\\{path} {name}={value}'

def set_string(hive, path, name, value):
    if not IS_WINDOWS: return 'Registro solo disponible en Windows.'
    with winreg.CreateKeyEx(ROOTS[hive], path, 0, winreg.KEY_WRITE) as key:
        winreg.SetValueEx(key, name, 0, winreg.REG_SZ, str(value))
    return f'{hive}\\{path} {name}={value}'

def fix_world_editor():
    base = r'Software\Blizzard Entertainment\WorldEdit'
    vals = {
        'Has Been Run': 1,
        'Minimap - Show Creep Camps': 1,
        'Minimap - Show Game Area Only': 1,
        'Minimap - Show Icons': 1,
        'Allow Local Files': 1,
    }
    return [set_dword('HKCU', base, k, v) for k, v in vals.items()]

def set_video(width, height, shadows=True):
    base = r'Software\Blizzard Entertainment\Warcraft III\Video'
    out = [set_dword('HKCU', base, 'reswidth', int(width)), set_dword('HKCU', base, 'resheight', int(height))]
    out.append(set_dword('HKCU', base, 'unitshadows', 1 if shadows else 0))
    return out

def set_install_associations(wc3_path):
    from pathlib import Path
    p = Path(wc3_path)
    out=[]
    base = r'Software\Blizzard Entertainment\Warcraft III'
    out.append(set_string('HKCU', base, 'InstallPath', str(p)))
    out.append(set_string('HKCU', base, 'InstallPathX', str(p)))
    out.append(set_string('HKCU', base, 'Program', str(p / 'Warcraft III.exe')))
    out.append(set_string('HKCU', base, 'ProgramX', str(p / 'Frozen Throne.exe')))
    out.append(set_dword('HKCU', base, 'Allow Local Files', 1))
    return out

# REG_MULTI_SZ Battle.net gateway list, built from the data supplied by Azzlaer.
def set_gateways():
    if not IS_WINDOWS: return ['Registro solo disponible en Windows.']
    gateways = [
        '1001','01','47.180.222.51','-3','LatinBattle',
        '26.79.212.213','-4','LatinBattle.Radmin',
        'worldofeditors.net','-4','WorldEditors',
        'olds.ar','-4','OldServers',
        'rubattle.net','-4','Rubattle',
        'server.tsgamerz.com','-3','TSGamerZ',
        'war3.nightbot.ru','-4','NightBot',
        'ingame.go.ro','-4','ICCup',
        'europe.warcraft3.eu','-4','EuropeBattle',
        'pvpgn.onligamez.ru','-4','OZBNet',
        '116.203.95.137','-4','eurobattle.net',
        '185.231.245.32','-4','NightBot',
    ]
    path = r'Software\Blizzard Entertainment\Warcraft III'
    with winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, path, 0, winreg.KEY_WRITE) as key:
        winreg.SetValueEx(key, 'Battle.net Gateways', 0, winreg.REG_MULTI_SZ, gateways)
    return ['Battle.net Gateways agregado/actualizado.']
