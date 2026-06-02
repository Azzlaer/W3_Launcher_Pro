from __future__ import annotations

from tkinter import ttk

from core import win_registry


class WorldEditTab(ttk.Frame):
    def __init__(self, master, app):
        super().__init__(master, padding=8)
        self.app = app
        self.build()

    def build(self):
        ttk.Label(self, text="Fix World Editor", style="Title.TLabel").pack(anchor="w", pady=(0, 6))
        box = ttk.LabelFrame(self, text="Reparación del editor", padding=8)
        box.pack(fill="x")
        ttk.Label(
            box,
            text="Activa Has Been Run, opciones del minimapa y Allow Local Files para evitar fallos clásicos del editor.",
            style="Muted.TLabel",
            wraplength=720,
        ).pack(anchor="w", pady=(0, 8))
        ttk.Button(box, text="✅ Aplicar Fix World Editor", style="Accent.TButton", command=self.apply).pack(anchor="w")

    def apply(self):
        win_registry.apply_world_editor_fix(self.app.logger)
