from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from core import admin, win_registry


class RegistryTab(ttk.Frame):
    def __init__(self, master, app):
        super().__init__(master, padding=8)
        self.app = app
        self.cfg = app.cfg
        self.log = app.logger.log
        self.build()

    def build(self):
        ttk.Label(self, text="Registro Warcraft III", style="Title.TLabel").pack(anchor="w", pady=(0, 6))
        ttk.Label(
            self,
            text="HKLM/HKCR pueden requerir Administrador. Usa esta sección para limpiar, registrar rutas y reparar asociaciones.",
            style="Muted.TLabel",
            wraplength=760,
        ).pack(anchor="w", pady=(0, 6))

        box = ttk.LabelFrame(self, text="Acciones rápidas", padding=7)
        box.pack(fill="x")
        for i in range(2):
            box.columnconfigure(i, weight=1)
        ttk.Button(box, text="🛡 Reiniciar como Admin", command=admin.relaunch_as_admin).grid(row=0, column=0, sticky="ew", padx=3, pady=3)
        ttk.Button(box, text="🧹 Eliminar claves antiguas", style="Danger.TButton", command=self.cleanup).grid(row=0, column=1, sticky="ew", padx=3, pady=3)
        ttk.Button(box, text="📌 Registro base InstallPath", command=self.base_registry).grid(row=1, column=0, sticky="ew", padx=3, pady=3)
        ttk.Button(box, text="🔗 Asociaciones .w3g/.w3x/etc", command=self.associations).grid(row=1, column=1, sticky="ew", padx=3, pady=3)
        ttk.Button(box, text="⚙ Defaults gameplay/video/sound", style="Accent.TButton", command=self.defaults).grid(row=2, column=0, columnspan=2, sticky="ew", padx=3, pady=3)

        row = ttk.LabelFrame(self, text="Perfil", padding=7)
        row.pack(fill="x", pady=7)
        self.user_var = tk.StringVar(value="Azzlaer")
        ttk.Label(row, text="Usuario WC3:").pack(side="left")
        ttk.Entry(row, textvariable=self.user_var, width=28).pack(side="left", padx=6)

    def cleanup(self):
        if not messagebox.askyesno("Confirmar", "¿Eliminar las claves de registro indicadas?"):
            return
        win_registry.cleanup_blizzard_registry(self.app.logger)

    def base_registry(self):
        win_registry.apply_base_install_registry(self.cfg.get("GAME", "install_path"), self.app.logger)

    def associations(self):
        win_registry.apply_file_associations(self.cfg.get("GAME", "install_path"), self.app.logger)

    def defaults(self):
        win_registry.apply_gameplay_defaults(self.app.logger)
        win_registry.apply_video_quality_defaults(self.app.logger)
        win_registry.apply_misc_sound_string_defaults(self.user_var.get().strip() or "Azzlaer", self.app.logger)
