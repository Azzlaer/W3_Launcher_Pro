from __future__ import annotations

import threading
import webbrowser
from pathlib import Path
from tkinter import BooleanVar, StringVar, Text, messagebox, ttk

from core.gproxy_manager import (
    GProxyConfig,
    download_and_install_gproxy,
    find_gproxy_exe,
    gproxy_dir,
    launch_gproxy,
    read_gproxy_cfg,
    write_gproxy_cfg,
)


class GProxyTab(ttk.Frame):
    """Pestaña modular para descargar, instalar, configurar y ejecutar GProxy++."""

    SERVERS = [
        "eurobattle.net",
        "rubattle.net",
        "server.tsgamerz.com",
        "pvpgn.onligamez.ru",
        "uswest.battle.net",
        "useast.battle.net",
        "asia.battle.net",
        "europe.battle.net",
        "localhost",
    ]

    def __init__(self, master, app):
        super().__init__(master, padding=8)
        self.app = app
        self.cfg = app.cfg
        self.proc = None

        self.install_path = StringVar(value=self.cfg.get("GAME", "install_path"))
        self.subdir = StringVar(value=self.cfg.get("GPROXY", "install_subdir", "GProxy"))
        self.download_url = StringVar(value=self.cfg.get("GPROXY", "download_url"))
        self.server = StringVar(value=self.cfg.get("GPROXY", "bnet_hostname", "eurobattle.net"))
        self.port = StringVar(value=self.cfg.get("GPROXY", "game_port", "6125"))
        self.indicator = StringVar(value=self.cfg.get("GPROXY", "game_indicator", "GProxy"))
        self.add_gateway = BooleanVar(value=self.cfg.get_bool("GPROXY", "bnet_addgateway", True))
        self.debug = BooleanVar(value=self.cfg.get_bool("GPROXY", "debug", False))
        self.auto_start = BooleanVar(value=self.cfg.get_bool("GPROXY", "auto_start_before_game", False))
        self.log_name = StringVar(value=self.cfg.get("GPROXY", "log", "gproxy.log"))

        self.build()
        self.refresh_status()

    def folder(self) -> Path:
        return gproxy_dir(self.install_path.get(), self.subdir.get())

    def build(self):
        ttk.Label(self, text="🛡 GProxy++ Protección de desconexión", style="Title.TLabel").pack(anchor="w", pady=(0, 6))

        info = ttk.LabelFrame(self, text="¿Qué hace?", padding=8)
        info.pack(fill="x", pady=(0, 7))
        ttk.Label(
            info,
            text=(
                "GProxy++ se ejecuta antes del juego, agrega un gateway local llamado GProxy y permite reconectar "
                "si hay una caída temporal en partidas alojadas en servidores GHost++ compatibles."
            ),
            style="Muted.TLabel",
            wraplength=820,
        ).pack(anchor="w")

        top = ttk.Frame(self)
        top.pack(fill="x", pady=(0, 7))
        left = ttk.LabelFrame(top, text="Instalación", padding=8)
        left.pack(side="left", fill="both", expand=True, padx=(0, 5))
        right = ttk.LabelFrame(top, text="Estado", padding=8)
        right.pack(side="right", fill="both", expand=True, padx=(5, 0))

        self._row_entry(left, "Carpeta WC3", self.install_path)
        self._row_entry(left, "Subcarpeta", self.subdir)
        self._row_entry(left, "URL descarga", self.download_url)
        btns = ttk.Frame(left)
        btns.pack(fill="x", pady=(7, 0))
        ttk.Button(btns, text="🌐 Abrir GitHub", command=self.open_github).pack(side="left")
        ttk.Button(btns, text="⬇ Descargar / instalar", style="Accent.TButton", command=self.download_install).pack(side="left", padx=5)
        ttk.Button(btns, text="📁 Abrir carpeta", command=self.open_folder).pack(side="left")

        self.status_text = Text(right, height=7, bg="#050B06", fg="#80FF68", relief="flat", font=("Consolas", 9), padx=6, pady=5)
        self.status_text.pack(fill="both", expand=True)
        ttk.Button(right, text="🔍 Actualizar estado", command=self.refresh_status).pack(anchor="e", pady=(6, 0))

        cfgbox = ttk.LabelFrame(self, text="Configuración gproxy.cfg", padding=8)
        cfgbox.pack(fill="x", pady=(0, 7))
        row1 = ttk.Frame(cfgbox)
        row1.pack(fill="x", pady=2)
        ttk.Label(row1, text="Servidor destino", width=16).pack(side="left")
        server_combo = ttk.Combobox(row1, values=self.SERVERS, textvariable=self.server, width=32)
        server_combo.pack(side="left", padx=(0, 8))
        ttk.Label(row1, text="Puerto", width=8).pack(side="left")
        ttk.Entry(row1, textvariable=self.port, width=10).pack(side="left", padx=(0, 8))
        ttk.Label(row1, text="Indicador", width=10).pack(side="left")
        ttk.Entry(row1, textvariable=self.indicator, width=18).pack(side="left")

        row2 = ttk.Frame(cfgbox)
        row2.pack(fill="x", pady=4)
        ttk.Checkbutton(row2, text="Agregar gateway local GProxy", variable=self.add_gateway).pack(side="left")
        ttk.Checkbutton(row2, text="Debug", variable=self.debug).pack(side="left", padx=8)
        ttk.Checkbutton(row2, text="Iniciar GProxy antes del juego", variable=self.auto_start).pack(side="left", padx=8)
        ttk.Label(row2, text="Log", width=5).pack(side="left")
        ttk.Entry(row2, textvariable=self.log_name, width=18).pack(side="left")

        actions = ttk.Frame(cfgbox)
        actions.pack(fill="x", pady=(6, 0))
        ttk.Button(actions, text="💾 Guardar config", style="Accent.TButton", command=self.save_config).pack(side="left")
        ttk.Button(actions, text="📖 Leer config actual", command=self.load_existing_cfg).pack(side="left", padx=5)
        ttk.Button(actions, text="🚀 Iniciar GProxy", style="Accent.TButton", command=self.start_gproxy).pack(side="left", padx=5)
        ttk.Button(actions, text="🛑 Detener", style="Danger.TButton", command=self.stop_gproxy).pack(side="left")

        notes = ttk.LabelFrame(self, text="Notas importantes", padding=8)
        notes.pack(fill="both", expand=True)
        ttk.Label(
            notes,
            text=(
                "1) Primero inicia GProxy y luego abre Warcraft III.  2) En Battle.net elige el gateway GProxy.  "
                "3) Esta protección solo funciona bien si el host/servidor usa GHost++ con soporte GPS/GProxy.  "
                "4) Si cambias el servidor destino, guarda gproxy.cfg antes de iniciar."
            ),
            style="Muted.TLabel",
            wraplength=820,
        ).pack(anchor="w")

    def _row_entry(self, parent, label, variable):
        row = ttk.Frame(parent)
        row.pack(fill="x", pady=2)
        ttk.Label(row, text=label, width=13).pack(side="left")
        ttk.Entry(row, textvariable=variable).pack(side="left", fill="x", expand=True)

    def open_github(self):
        webbrowser.open(self.cfg.get("GPROXY", "github_url", "https://github.com/dns/GProxy-Warcraft3-disconnect-protection-tool"))

    def open_folder(self):
        folder = self.folder()
        folder.mkdir(parents=True, exist_ok=True)
        webbrowser.open(str(folder))

    def refresh_status(self):
        folder = self.folder()
        exe = find_gproxy_exe(folder)
        cfg_path = folder / "gproxy.cfg"
        lines = [
            f"Carpeta: {folder}",
            f"GProxy.exe: {'OK' if exe else 'NO ENCONTRADO'}",
            f"gproxy.cfg: {'OK' if cfg_path.exists() else 'NO ENCONTRADO'}",
            f"Proceso GUI: {'ACTIVO' if self.proc and self.proc.poll() is None else 'DETENIDO / no iniciado desde GUI'}",
        ]
        if exe:
            lines.append(f"EXE: {exe.name}")
        self.status_text.configure(state="normal")
        self.status_text.delete("1.0", "end")
        self.status_text.insert("end", "\n".join(lines))
        self.status_text.configure(state="disabled")

    def persist_fields(self):
        self.cfg.set("GAME", "install_path", self.install_path.get())
        self.cfg.set("GPROXY", "install_subdir", self.subdir.get())
        self.cfg.set("GPROXY", "download_url", self.download_url.get())
        self.cfg.set("GPROXY", "bnet_hostname", self.server.get())
        self.cfg.set("GPROXY", "game_port", self.port.get())
        self.cfg.set("GPROXY", "game_indicator", self.indicator.get())
        self.cfg.set("GPROXY", "bnet_addgateway", self.add_gateway.get())
        self.cfg.set("GPROXY", "debug", self.debug.get())
        self.cfg.set("GPROXY", "auto_start_before_game", self.auto_start.get())
        self.cfg.set("GPROXY", "log", self.log_name.get())

    def save_config(self):
        try:
            port = int(self.port.get())
            if port <= 0 or port > 65535:
                raise ValueError("El puerto debe estar entre 1 y 65535.")
            self.persist_fields()
            cfg = GProxyConfig(
                install_path=self.install_path.get(),
                bnet_hostname=self.server.get().strip(),
                game_port=port,
                game_indicator=self.indicator.get().strip(),
                bnet_addgateway=self.add_gateway.get(),
                debug=self.debug.get(),
                log=self.log_name.get().strip() or "gproxy.log",
            )
            path = write_gproxy_cfg(self.folder(), cfg)
            self.app.logger.log(f"✅ Configuración GProxy guardada: {path}")
            self.refresh_status()
        except Exception as e:
            self.app.logger.log(f"❌ Error guardando GProxy: {e}")
            messagebox.showerror("GProxy", str(e))

    def load_existing_cfg(self):
        data = read_gproxy_cfg(self.folder())
        if not data:
            messagebox.showinfo("GProxy", "No encontré gproxy.cfg en la carpeta configurada.")
            return
        self.server.set(data.get("bnet_hostname", self.server.get()))
        self.port.set(data.get("game_port", self.port.get()))
        self.indicator.set(data.get("game_indicator", self.indicator.get()))
        self.add_gateway.set(data.get("bnet_addgateway", "1") not in ("0", "false", "False"))
        self.debug.set(data.get("debug", "0") in ("1", "true", "True"))
        self.log_name.set(data.get("log", self.log_name.get()))
        self.app.logger.log("📖 gproxy.cfg cargado en el formulario.")

    def download_install(self):
        self.persist_fields()
        def worker():
            try:
                folder = download_and_install_gproxy(
                    self.download_url.get(),
                    self.install_path.get(),
                    self.subdir.get(),
                    logger=self.app.logger,
                )
                self.app.logger.log(f"✅ Instalación GProxy terminada en: {folder}")
                self.save_config()
            except Exception as e:
                self.app.logger.log(f"❌ Error instalando GProxy: {e}")
                messagebox.showerror("GProxy", str(e))
            finally:
                self.refresh_status()
        threading.Thread(target=worker, daemon=True).start()

    def start_gproxy(self):
        try:
            self.save_config()
            if self.proc and self.proc.poll() is None:
                messagebox.showinfo("GProxy", "GProxy ya está iniciado desde esta ventana.")
                return
            self.proc = launch_gproxy(self.folder(), logger=self.app.logger)
            self.refresh_status()
        except Exception as e:
            self.app.logger.log(f"❌ Error iniciando GProxy: {e}")
            messagebox.showerror("GProxy", str(e))

    def stop_gproxy(self):
        if self.proc and self.proc.poll() is None:
            self.proc.terminate()
            self.app.logger.log("🛑 GProxy detenido desde el launcher.")
        else:
            self.app.logger.log("ℹ No hay proceso GProxy activo iniciado por esta GUI.")
        self.refresh_status()
