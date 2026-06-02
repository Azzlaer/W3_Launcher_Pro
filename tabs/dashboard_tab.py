from __future__ import annotations

import os
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
import webbrowser

from core.process_launcher import build_launch_command, launch_game
from core.version_info import get_file_version
from core import win_registry
from core.gproxy_manager import gproxy_dir, launch_gproxy, write_gproxy_cfg, GProxyConfig


class DashboardTab(ttk.Frame):
    """Pantalla Inicio: imagen, modo de juego y selección de loader."""

    def __init__(self, master, app):
        super().__init__(master, padding=8)
        self.app = app
        self.cfg = app.cfg
        self.log = app.logger.log
        self.banner_img = None
        self.gproxy_proc = None
        self.build()
        self.refresh_status()

    def build(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.rowconfigure(2, weight=1)

        image_box = ttk.LabelFrame(self, text="Inicio", padding=6)
        image_box.grid(row=0, column=0, rowspan=3, sticky="nsew", padx=(0, 8))
        image_box.columnconfigure(0, weight=1)
        image_box.rowconfigure(0, weight=1)

        banner = Path(__file__).resolve().parent.parent / "assets" / "orc_banner.png"
        if banner.exists():
            try:
                self.banner_img = tk.PhotoImage(file=str(banner))
                ttk.Label(image_box, image=self.banner_img).grid(row=0, column=0, sticky="n", pady=(6, 8))
            except Exception:
                ttk.Label(image_box, text="⚔ WARCRAFT III ORC LAUNCHER PRO", style="Header.TLabel").grid(row=0, column=0, sticky="n", pady=20)
        else:
            ttk.Label(image_box, text="⚔ WARCRAFT III ORC LAUNCHER PRO", style="Header.TLabel").grid(row=0, column=0, sticky="n", pady=20)

        self.install_var = tk.StringVar(value=self.cfg.get("GAME", "install_path"))
        path_row = ttk.Frame(image_box)
        path_row.grid(row=1, column=0, sticky="ew", pady=(6, 0))
        path_row.columnconfigure(1, weight=1)
        ttk.Label(path_row, text="Carpeta:").grid(row=0, column=0, sticky="w")
        ttk.Entry(path_row, textvariable=self.install_var).grid(row=0, column=1, sticky="ew", padx=5)
        ttk.Button(path_row, text="...", width=4, command=self.pick_folder).grid(row=0, column=2)

        controls = ttk.LabelFrame(self, text="Jugar", padding=8)
        controls.grid(row=0, column=1, sticky="nsew")
        controls.columnconfigure(1, weight=1)

        self.edition_var = tk.StringVar(value=self.cfg.get("GAME", "default_edition", "Frozen Throne"))
        self.loader_var = tk.StringVar(value=self.cfg.get("GAME", "default_loader", "W3 Loader normal"))
        self.window_var = tk.BooleanVar(value=self.cfg.get_bool("LAUNCH", "window_mode"))
        self.opengl_var = tk.BooleanVar(value=self.cfg.get_bool("LAUNCH", "opengl"))
        self.gproxy_var = tk.BooleanVar(value=self.cfg.get_bool("GPROXY", "auto_start_before_game", False))

        ttk.Label(controls, text="Modo:").grid(row=0, column=0, sticky="w", pady=2)
        ttk.Radiobutton(controls, text="Frozen Throne", variable=self.edition_var, value="Frozen Throne").grid(row=0, column=1, sticky="w")
        ttk.Radiobutton(controls, text="Reign of Chaos", variable=self.edition_var, value="Reign of Chaos").grid(row=1, column=1, sticky="w")

        ttk.Label(controls, text="Loader:").grid(row=2, column=0, sticky="w", pady=(8, 2))
        self.loader_combo = ttk.Combobox(controls, textvariable=self.loader_var, state="readonly", values=["W3 Loader normal", "W3 Loader Rubattle", "Directo sin loader"], width=24)
        self.loader_combo.grid(row=2, column=1, sticky="ew", pady=(8, 2))

        ttk.Checkbutton(controls, text="Ventana (-window)", variable=self.window_var).grid(row=3, column=1, sticky="w", pady=(8, 0))
        ttk.Checkbutton(controls, text="OpenGL (-opengl)", variable=self.opengl_var).grid(row=4, column=1, sticky="w")
        ttk.Checkbutton(controls, text="Iniciar GProxy antes", variable=self.gproxy_var).grid(row=5, column=1, sticky="w")

        ttk.Button(controls, text="▶ JUGAR AHORA", style="Accent.TButton", command=self.launch).grid(row=6, column=0, columnspan=2, sticky="ew", pady=(12, 4))
        ttk.Button(controls, text="Ver comando", command=self.show_command).grid(row=7, column=0, columnspan=2, sticky="ew")

        tools = ttk.LabelFrame(self, text="Loader / Descargas", padding=8)
        tools.grid(row=1, column=1, sticky="nsew", pady=(8, 0))
        ttk.Button(tools, text="Abrir descarga Rubattle", command=self.open_rubattle).pack(fill="x")
        ttk.Button(tools, text="Abrir carpeta WC3", command=self.open_folder).pack(fill="x", pady=5)

        status = ttk.LabelFrame(self, text="Estado rápido", padding=8)
        status.grid(row=2, column=1, sticky="nsew", pady=(8, 0))
        self.status_var = tk.StringVar(value="...")
        self.version_var = tk.StringVar(value="...")
        ttk.Label(status, textvariable=self.status_var, style="Status.TLabel").pack(anchor="w")
        ttk.Label(status, textvariable=self.version_var, style="Muted.TLabel", wraplength=260).pack(anchor="w", pady=(6, 0))
        ttk.Button(status, text="Actualizar estado", command=self.refresh_status).pack(fill="x", pady=(8, 0))

    def pick_folder(self):
        folder = filedialog.askdirectory(title="Seleccionar carpeta Warcraft III")
        if folder:
            self.install_var.set(folder)
            self.cfg.set("GAME", "install_path", folder)
            self.refresh_status()

    def selected_exe(self) -> str:
        edition = self.edition_var.get()
        loader = self.loader_var.get()
        if loader == "W3 Loader normal":
            return self.cfg.get("GAME", "normal_loader_exe", "w3l.exe")
        if loader == "W3 Loader Rubattle":
            return self.cfg.get("GAME", "rubattle_loader_exe", "w3l_rubattle.exe")
        if edition == "Reign of Chaos":
            return self.cfg.get("GAME", "warcraft_exe", "Warcraft III.exe")
        return self.cfg.get("GAME", "frozen_throne_exe", "Frozen Throne.exe")

    def save_quick(self):
        self.cfg.set("GAME", "install_path", self.install_var.get())
        self.cfg.set("GAME", "default_edition", self.edition_var.get())
        self.cfg.set("GAME", "default_loader", self.loader_var.get())
        self.cfg.set("LAUNCH", "window_mode", self.window_var.get())
        self.cfg.set("LAUNCH", "opengl", self.opengl_var.get())
        self.cfg.set("GPROXY", "auto_start_before_game", self.gproxy_var.get())

    def _prelaunch(self):
        if self.cfg.get_bool("LAUNCH", "cleanup_registry_before_launch"):
            win_registry.cleanup_blizzard_registry(self.app.logger)
        if self.cfg.get_bool("LAUNCH", "fix_world_editor_before_launch"):
            win_registry.apply_world_editor_fix(self.app.logger)
        if self.cfg.get_bool("LAUNCH", "add_gateways_before_launch"):
            win_registry.apply_gateways(self.app.logger)

    def build_cmd(self):
        exe = self.selected_exe()
        extra = self.cfg.get("LAUNCH", "extra_args", "")
        return build_launch_command(self.install_var.get(), exe, self.window_var.get(), self.opengl_var.get(), extra)

    def show_command(self):
        self.save_quick()
        cmd = self.build_cmd()
        text = " ".join([f'"{x}"' if " " in x else x for x in cmd])
        messagebox.showinfo("Comando de lanzamiento", text)

    def start_gproxy_if_needed(self):
        if not self.gproxy_var.get():
            return
        if self.gproxy_proc and self.gproxy_proc.poll() is None:
            self.log("🛡 GProxy ya estaba activo desde el dashboard.")
            return
        folder = gproxy_dir(self.install_var.get(), self.cfg.get("GPROXY", "install_subdir", "GProxy"))
        cfg = GProxyConfig(
            install_path=self.install_var.get(),
            bnet_hostname=self.cfg.get("GPROXY", "bnet_hostname", "eurobattle.net"),
            game_port=int(self.cfg.get("GPROXY", "game_port", "6125")),
            game_indicator=self.cfg.get("GPROXY", "game_indicator", "GProxy"),
            bnet_addgateway=self.cfg.get_bool("GPROXY", "bnet_addgateway", True),
            debug=self.cfg.get_bool("GPROXY", "debug", False),
            log=self.cfg.get("GPROXY", "log", "gproxy.log"),
        )
        write_gproxy_cfg(folder, cfg)
        self.gproxy_proc = launch_gproxy(folder, logger=self.app.logger)
        self.log("🛡 GProxy iniciado antes del juego.")

    def launch(self):
        self.save_quick()
        try:
            self._prelaunch()
            self.start_gproxy_if_needed()
            proc = launch_game(self.install_var.get(), self.selected_exe(), self.window_var.get(), self.opengl_var.get(), self.cfg.get("LAUNCH", "extra_args", ""))
            self.log(f"▶ Iniciado {self.edition_var.get()} con {self.loader_var.get()} | PID: {proc.pid}")
        except Exception as e:
            messagebox.showerror("Error al lanzar", str(e))
            self.log(f"❌ Error al iniciar: {e}")

    def refresh_status(self):
        exe = Path(self.install_var.get()) / self.selected_exe()
        self.status_var.set(f"{'✅ Detectado' if exe.exists() else '❌ No encontrado'}: {self.selected_exe()}")
        info = get_file_version(exe)
        self.version_var.set(f"FileVersion: {info.get('file_version','No disponible')}\nProductVersion: {info.get('product_version','No disponible')}")

    def open_rubattle(self):
        webbrowser.open(self.cfg.get("TOOLS", "rubattle_loader_url"))
        self.log("🌐 Abriendo descarga de W3 Loader Rubattle")

    def open_folder(self):
        p = Path(self.install_var.get())
        if p.exists():
            os.startfile(str(p))
        else:
            messagebox.showwarning("Carpeta no encontrada", str(p))
