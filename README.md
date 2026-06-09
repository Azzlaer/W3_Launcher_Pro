# ⚔️ WC3 Orc Launcher Pro + GProxy

Launcher modular en Python GUI para **Warcraft III Frozen Throne / Reign of Chaos**, pensado para PvPGN, GProxy, WoEProxy, W3 Loader y configuraciones clásicas del juego.

## 🆕 Cambios de esta versión

- Se agregó manejo especial para el archivo antiguo de GProxy publicado como `.zipx`:
  - Descarga desde GitHub Releases.
  - Busca el último release disponible si GitHub responde.
  - Si descarga `GProxy-2.0.zipx`, lo renombra automáticamente a `GProxy-2.0.zip`.
  - Luego intenta descomprimirlo en `tools/GProxy`.
- La pestaña **Mapas** quedó oculta por defecto.
  - El código sigue incluido para activarlo más adelante.
  - Para mostrarla: editar `config.ini` y cambiar:

```ini
[FEATURES]
show_maps_tab = true
```

## ▶️ Ejecutar

```bat
pip install -r requirements.txt
python main.py
```

O usando el BAT:

```bat
run.bat
```

Para registro avanzado, HKCR/HKLM o ejecución elevada:

```bat
ejecutar_admin.bat
```

## 🧩 GProxy / WoEProxy

La pestaña **GProxy** permite:

- Descargar **WoEProxy** desde:
  - `https://proxy.worldofeditors.net/woeproxy.exe`
- Instalarlo en la carpeta de Warcraft III y en `tools/GProxy`.
- Ejecutar `woeproxy.exe`.
- Descargar **GProxy clásico** desde GitHub:
  - `https://github.com/dns/GProxy-Warcraft3-disconnect-protection-tool/releases/download/v2.0/GProxy-2.0.zipx`
- Renombrar automáticamente `.zipx` a `.zip`.
- Descomprimir el archivo en `tools/GProxy`.
- Ejecutar `GPROXY.EXE` o `gproxy.exe`.

> Nota: algunos `.zipx` antiguos pueden necesitar 7-Zip o WinRAR si Python no logra abrirlos como ZIP estándar. El launcher igual deja el archivo descargado y renombrado como `.zip` en `tools/downloads`.

## 🏠 Inicio

Incluye dashboard compacto estilo orco/Frozen Throne con:

- Selector de juego:
  - Frozen Throne
  - Reign of Chaos
- Selector de modo:
  - Directo sin loader
  - W3 Loader normal
  - W3 Loader Rubattle
  - WoEProxy
- Opciones rápidas:
  - `-window`
  - `-opengl`

## 🔎 CRC / Integridad

Incluye base de CRC para detectar:

- W3L 1.26a / 1.27B / 1.28F
- Archivos originales de Warcraft III
- Herramientas permitidas
- Archivos sospechosos conocidos

## 🧱 Estructura modular

```txt
core/
  config_manager.py
  download_tools.py
  registry_tools.py
  crc_database.py
  crc_scanner.py
  theme.py

tabs/
  dashboard_tab.py
  gproxy_tab.py
  registry_tab.py
  video_tab.py
  integrity_tab.py
  maps_tab.py   # Oculta por defecto
  tools_tab.py
```

## ⚙️ Configuración importante

`config.ini`:

```ini
[GENERAL]
warcraft_path = D:\Juegos\Blizzard\Warcraft III

[DOWNLOADS]
github_gproxy_zip = https://github.com/dns/GProxy-Warcraft3-disconnect-protection-tool/releases/download/v2.0/GProxy-2.0.zipx
woe_proxy_exe = https://proxy.worldofeditors.net/woeproxy.exe

[GPROXY]
install_dir = tools\GProxy
server_profile = WorldOfEditors
server_address = worldofeditors.net
username = Azzlaer

[FEATURES]
show_maps_tab = false
```

## 👑 Créditos

Creado para **Azzlaer / LatinBattle.com** con ayuda de **ChatGPT OpenAI**.


## Corrección ZIPX / método de compresión no soportado

El archivo oficial antiguo de GProxy puede venir como `.zipx`. El launcher ahora lo descarga, lo renombra automáticamente a `.zip` y primero intenta extraerlo con Python. Si aparece el error `That compression method is not supported`, el launcher intenta usar 7-Zip o WinRAR automáticamente si están instalados.

Recomendado: instala 7-Zip en `C:\Program Files\7-Zip\7z.exe` para que la extracción sea automática. Si no tienes 7-Zip/WinRAR, el launcher dejará el archivo descargado en `tools/downloads/` para que lo extraigas manualmente.

## 🎨 Versión visual LatinBattle / Orc

Esta versión incorpora assets gráficos en `assets/`:

- `orc_night_camp.jpg`: banner principal del dashboard.
- `orc_day_banner.jpg`: tarjeta visual lateral del inicio.
- `latinbattle_logo.png`: logo superior y del dashboard.
- `latinbattle_url.png`: etiqueta visual con la web.

También se agregó `Pillow` a `requirements.txt` para cargar JPG/PNG, redimensionar y oscurecer fondos automáticamente dentro del GUI.

Si quieres reemplazar imágenes, conserva los mismos nombres de archivo dentro de `assets/` o modifica `core/assets.py` / `tabs/dashboard_tab.py`.
