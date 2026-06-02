# WC3 Orc Launcher Pro

Launcher modular en Python GUI para **Warcraft III Frozen Throne / Reign of Chaos**, con estética compacta tipo Orcos / Frozen Throne.

Proyecto creado por **ChatGPT OpenAI y Azzlaer para LatinBattle.com**.

## Novedades de esta versión

- Dashboard **Inicio** con imagen estilo Warcraft III / Orcos.
- Selector para jugar en:
  - Frozen Throne
  - Reign of Chaos
- Selector de método de ejecución:
  - W3 Loader normal
  - W3 Loader Rubattle
  - Directo sin loader
- Pestaña **CRC** para revisar integridad de archivos.
- Listado local de CRC para:
  - W3L 1.26a, 1.27B y 1.28F
  - Archivos originales Warcraft III 1.26a, 1.27B y 1.28
  - Herramientas permitidas
  - Archivos sospechosos conocidos por nombre/CRC
- Botón para abrir descarga de W3 Loader Rubattle.
- Configuración separada por pestañas.
- Estructura modular en `core/` y `tabs/`.

## Instalación

```bat
pip install -r requirements.txt
python main.py
```

Para funciones de registro que tocan `HKLM` o `HKCR`, ejecutar como administrador:

```bat
ejecutar_admin.bat
```

## Estructura

```txt
wc3_launcher_pro/
├─ main.py
├─ config.ini
├─ ejecutar_admin.bat
├─ assets/
│  └─ orc_banner.png
├─ core/
│  ├─ config_manager.py
│  ├─ process_launcher.py
│  ├─ win_registry.py
│  ├─ version_info.py
│  ├─ resolution.py
│  ├─ downloader.py
│  ├─ crc_database.py
│  └─ crc_scanner.py
├─ tabs/
│  ├─ dashboard_tab.py
│  ├─ launcher_tab.py
│  ├─ registry_tab.py
│  ├─ worldedit_tab.py
│  ├─ video_tab.py
│  ├─ tools_tab.py
│  ├─ integrity_tab.py
│  └─ maps_tab.py
└─ web_maps/
   ├─ index.php
   └─ maps.json
```

## Pestañas

### Inicio

Pantalla principal compacta con imagen, selección de juego y loader.

Permite elegir:

- Frozen Throne
- Reign of Chaos
- W3 Loader normal
- W3 Loader Rubattle
- Directo sin loader
- Modo ventana `-window`
- OpenGL `-opengl`

### Opciones

Configuración avanzada del ejecutable, parámetros extra y acciones de pre-lanzamiento.

### Registro

Funciones para borrar o restaurar claves principales de Warcraft III / Blizzard / Battle.net.

### WorldEdit

Fix automático para World Editor:

- `Has Been Run`
- `Minimap - Show Creep Camps`
- `Minimap - Show Game Area Only`
- `Minimap - Show Icons`
- `Allow Local Files`

### Video

Permite modificar resolución, sombras y configuraciones de video mediante registro.

### Fix Tools

Sección para abrir/descargar herramientas como WarcraftHelper.

### CRC

Permite escanear la carpeta de Warcraft III contra listas locales de CRC.

Tipos de escaneo:

- Originales
- W3L
- Permitidas
- Sospechosas

También permite exportar reporte CSV.

## Datos CRC cargados

### W3L

```txt
1.28F  CRC 6B949789
1.27B  CRC 0A5F13E2
1.26a  CRC 9C1648D5
```

### Detección sospechosa local

```txt
Neon.ini        CRC 3B1262F8
NeoN.mix        CRC 119E3C04
yHack.ini       CRC DF65CFE3
yHack.mixtape   CRC 78AF56A9
```

### Herramientas permitidas

```txt
d3d9.dll                    CRC A776A9A6
WarcraftHelper.dll           CRC ECBE70BA
WarcraftHelper.ini           CRC 2F7F2D37
WarcraftHelperLoader.mix     CRC 010CFCFA
msvcr120.dll                 CRC AE33CA0B
msvcp120.dll                 CRC 53C86B80
```

## Configuración de loaders

En `config.ini`:

```ini
[GAME]
normal_loader_exe = w3l.exe
rubattle_loader_exe = w3l_rubattle.exe
```

El launcher no asume que Rubattle ya existe en tu carpeta. Puedes descargarlo desde el botón del dashboard y luego renombrar o configurar el nombre del ejecutable en `config.ini`.

## Nota importante

La sección CRC es una ayuda local de diagnóstico. Si el usuario usa parches gráficos, archivos modificados, traducciones, loaders personalizados o mejoras visuales, algunos CRC pueden aparecer como `MODIFICADO` aunque no necesariamente sean maliciosos.

### GProxy

Nueva pestaña para **GProxy++**:

- Abre el repositorio oficial.
- Descarga `GProxy-2.0.zipx`.
- Instala/descomprime en una subcarpeta dentro de Warcraft III.
- Genera y modifica `gproxy.cfg` desde el launcher.
- Permite configurar:
  - servidor destino `bnet_hostname`
  - puerto local `game_port`, por defecto `6125`
  - indicador `game_indicator`
  - `bnet_addgateway`
  - modo debug
  - archivo de log
- Permite iniciar/detener GProxy desde la GUI.
- El dashboard puede iniciar GProxy automáticamente antes de abrir el juego.

Flujo recomendado:

```txt
1. Entrar a la pestaña GProxy.
2. Descargar / instalar.
3. Elegir servidor destino.
4. Guardar gproxy.cfg.
5. Iniciar GProxy.
6. Abrir Warcraft III.
7. Elegir gateway GProxy dentro del juego.
```

GProxy++ funciona como protección contra desconexiones temporales en partidas de Warcraft III cuando el servidor/host está preparado con soporte GHost++/GPS.
