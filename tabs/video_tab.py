from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from core.resolution import list_display_resolutions
from core import win_registry


class VideoTab(ttk.Frame):
    def __init__(self, master, app):
        super().__init__(master, padding=8)
        self.app = app
        self.cfg = app.cfg
        self.build()

    def build(self):
        ttk.Label(self, text="Video / Resolución", style="Title.TLabel").pack(anchor="w", pady=(0, 6))
        form = ttk.LabelFrame(self, text="Configuración gráfica", padding=8)
        form.pack(fill="x")
        self.res_var = tk.StringVar(value=self.cfg.get("LAUNCH", "selected_resolution", "1280x720"))
        self.combo = ttk.Combobox(form, textvariable=self.res_var, values=list_display_resolutions(), state="readonly", width=22)
        ttk.Label(form, text="Resolución:").grid(row=0, column=0, sticky="w")
        self.combo.grid(row=0, column=1, sticky="w", padx=6)
        self.shadows_var = tk.BooleanVar(value=self.cfg.get_bool("LAUNCH", "unit_shadows", True))
        ttk.Checkbutton(form, text="Sombras de unidades", variable=self.shadows_var).grid(row=1, column=1, sticky="w", padx=6, pady=5)
        ttk.Button(form, text="💾 Aplicar al registro", style="Accent.TButton", command=self.apply).grid(row=2, column=1, sticky="w", padx=6, pady=(2, 0))
        ttk.Label(
            self,
            text="WC3 clásico usa DWORD: reswidth/resheight. Ejemplo 640=0x280 y 400=0x190.",
            style="Muted.TLabel",
            wraplength=760,
        ).pack(anchor="w", pady=8)

    def apply(self):
        w, h = self.res_var.get().lower().split("x")
        win_registry.apply_resolution(int(w), int(h), self.app.logger)
        win_registry.apply_unit_shadows(self.shadows_var.get(), self.app.logger)
        self.cfg.set("LAUNCH", "selected_resolution", self.res_var.get())
        self.cfg.set("LAUNCH", "unit_shadows", self.shadows_var.get())
