from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from core.process_launcher import build_launch_command, launch_game
from core.version_info import get_file_version
from core import win_registry


class LauncherTab(ttk.Frame):
    def __init__(self, master, app):
        super().__init__(master, padding=8)
        self.app = app
        self.cfg = app.cfg
        self.log = app.logger.log
        self.build()
        self.refresh_version()

    def build(self):
        self.columnconfigure(1, weight=1)
        ttk.Label(self, text="▶ Lanzador principal", style="Title.TLabel").grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 6))

        ttk.Label(self, text="Carpeta WC3:").grid(row=1, column=0, sticky="w")
        self.install_var = tk.StringVar(value=self.cfg.get("GAME", "install_path"))
        ttk.Entry(self, textvariable=self.install_var).grid(row=1, column=1, sticky="ew", padx=6)
        ttk.Button(self, text="Examinar", command=self.pick_folder).grid(row=1, column=2, sticky="ew")

        ttk.Label(self, text="Loader normal:").grid(row=2, column=0, sticky="w", pady=(5, 0))
        self.exe_var = tk.StringVar(value=self.cfg.get("GAME", "normal_loader_exe"))
        ttk.Entry(self, textvariable=self.exe_var).grid(row=2, column=1, sticky="ew", padx=6, pady=(5, 0))
        ttk.Button(self, text="Comprobar", command=self.refresh_version).grid(row=2, column=2, sticky="ew", pady=(5, 0))

        ttk.Label(self, text="Loader Rubattle:").grid(row=3, column=0, sticky="w", pady=(5, 0))
        self.rubattle_var = tk.StringVar(value=self.cfg.get("GAME", "rubattle_loader_exe"))
        ttk.Entry(self, textvariable=self.rubattle_var).grid(row=3, column=1, sticky="ew", padx=6, pady=(5, 0))

        middle = ttk.Frame(self)
        middle.grid(row=4, column=0, columnspan=3, sticky="nsew", pady=7)
        middle.columnconfigure(0, weight=1)
        middle.columnconfigure(1, weight=1)

        opts = ttk.LabelFrame(middle, text="Pre-lanzamiento", padding=7)
        opts.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        self.cleanup_var = tk.BooleanVar(value=self.cfg.get_bool("LAUNCH", "cleanup_registry_before_launch"))
        self.wefix_var = tk.BooleanVar(value=self.cfg.get_bool("LAUNCH", "fix_world_editor_before_launch"))
        self.gateways_var = tk.BooleanVar(value=self.cfg.get_bool("LAUNCH", "add_gateways_before_launch"))
        self.window_var = tk.BooleanVar(value=self.cfg.get_bool("LAUNCH", "window_mode"))
        self.opengl_var = tk.BooleanVar(value=self.cfg.get_bool("LAUNCH", "opengl"))
        ttk.Checkbutton(opts, text="Limpiar claves Blizzard/Battle.net", variable=self.cleanup_var).pack(anchor="w")
        ttk.Checkbutton(opts, text="Fix World Editor", variable=self.wefix_var).pack(anchor="w")
        ttk.Checkbutton(opts, text="Agregar Gateways Battle.net", variable=self.gateways_var).pack(anchor="w")
        ttk.Checkbutton(opts, text="Modo ventana (-window)", variable=self.window_var).pack(anchor="w")
        ttk.Checkbutton(opts, text="OpenGL (-opengl)", variable=self.opengl_var).pack(anchor="w")

        info = ttk.LabelFrame(middle, text="Estado w3l.exe", padding=7)
        info.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        info.columnconfigure(1, weight=1)
        self.exists_var = tk.StringVar(value="...")
        self.filever_var = tk.StringVar(value="...")
        self.prodver_var = tk.StringVar(value="...")
        labels = [("Existe:", self.exists_var), ("FileVersion:", self.filever_var), ("ProductVersion:", self.prodver_var)]
        for r, (name, var) in enumerate(labels):
            ttk.Label(info, text=name).grid(row=r, column=0, sticky="w", pady=1)
            ttk.Label(info, textvariable=var, style="Muted.TLabel").grid(row=r, column=1, sticky="w", padx=6, pady=1)

        ttk.Label(self, text="Args extra:").grid(row=5, column=0, sticky="w")
        self.extra_var = tk.StringVar(value=self.cfg.get("LAUNCH", "extra_args"))
        ttk.Entry(self, textvariable=self.extra_var).grid(row=5, column=1, columnspan=2, sticky="ew", padx=6)

        btns = ttk.Frame(self)
        btns.grid(row=6, column=0, columnspan=3, sticky="ew", pady=(8, 0))
        ttk.Button(btns, text="Guardar", command=self.save).pack(side="left")
        ttk.Button(btns, text="Ver comando", command=self.show_command).pack(side="left", padx=6)
        ttk.Button(btns, text="▶ LANZAR WC3", style="Accent.TButton", command=self.launch).pack(side="right")

    def pick_folder(self):
        folder = filedialog.askdirectory(title="Seleccionar carpeta de Warcraft III")
        if folder:
            self.install_var.set(folder)
            self.save()
            self.refresh_version()

    def save(self):
        self.cfg.set("GAME", "install_path", self.install_var.get())
        self.cfg.set("GAME", "launcher_exe", self.exe_var.get())
        self.cfg.set("GAME", "normal_loader_exe", self.exe_var.get())
        self.cfg.set("GAME", "rubattle_loader_exe", self.rubattle_var.get())
        self.cfg.set("LAUNCH", "cleanup_registry_before_launch", self.cleanup_var.get())
        self.cfg.set("LAUNCH", "fix_world_editor_before_launch", self.wefix_var.get())
        self.cfg.set("LAUNCH", "add_gateways_before_launch", self.gateways_var.get())
        self.cfg.set("LAUNCH", "window_mode", self.window_var.get())
        self.cfg.set("LAUNCH", "opengl", self.opengl_var.get())
        self.cfg.set("LAUNCH", "extra_args", self.extra_var.get())
        self.log("💾 Configuración guardada")

    def refresh_version(self):
        exe = Path(self.install_var.get()) / self.exe_var.get()
        self.exists_var.set("✅ Sí" if exe.exists() else "❌ No encontrado")
        info = get_file_version(exe)
        self.filever_var.set(info.get("file_version", "No disponible"))
        self.prodver_var.set(info.get("product_version", "No disponible"))
        self.log(f"{'✅ w3l detectado' if exe.exists() else '❌ No se encontró w3l'}: {exe}")

    def _prelaunch(self):
        if self.cleanup_var.get():
            win_registry.cleanup_blizzard_registry(self.app.logger)
        if self.wefix_var.get():
            win_registry.apply_world_editor_fix(self.app.logger)
        if self.gateways_var.get():
            win_registry.apply_gateways(self.app.logger)

    def show_command(self):
        cmd = build_launch_command(self.install_var.get(), self.exe_var.get(), self.window_var.get(), self.opengl_var.get(), self.extra_var.get())
        messagebox.showinfo("Comando de lanzamiento", " ".join([f'"{x}"' if " " in x else x for x in cmd]))

    def launch(self):
        self.save()
        try:
            self._prelaunch()
            proc = launch_game(self.install_var.get(), self.exe_var.get(), self.window_var.get(), self.opengl_var.get(), self.extra_var.get())
            self.log(f"▶ Warcraft III iniciado. PID: {proc.pid}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.log(f"❌ Error al iniciar: {e}")
