from __future__ import annotations

import threading
import webbrowser
from tkinter import messagebox, ttk

from core.downloader import download_latest_warcraft_helper


class ToolsTab(ttk.Frame):
    def __init__(self, master, app):
        super().__init__(master, padding=8)
        self.app = app
        self.cfg = app.cfg
        self.build()

    def build(self):
        ttk.Label(self, text="Fix Tools / WarcraftHelper", style="Title.TLabel").pack(anchor="w", pady=(0, 6))
        box = ttk.LabelFrame(self, text="GitHub Releases", padding=8)
        box.pack(fill="x")
        ttk.Label(
            box,
            text="Descarga la última release y si viene en ZIP la descomprime en la carpeta de Warcraft III.",
            style="Muted.TLabel",
            wraplength=720,
        ).pack(anchor="w", pady=(0, 8))
        row = ttk.Frame(box)
        row.pack(fill="x")
        ttk.Button(row, text="🌐 Abrir releases", command=self.open_releases).pack(side="left")
        ttk.Button(row, text="⬇ Descargar e instalar", style="Accent.TButton", command=self.download).pack(side="left", padx=6)

    def open_releases(self):
        webbrowser.open(self.cfg.get("TOOLS", "warcraft_helper_releases_url"))

    def download(self):
        def worker():
            try:
                download_latest_warcraft_helper(
                    self.cfg.get("TOOLS", "warcraft_helper_api_latest"),
                    self.cfg.get("GAME", "install_path"),
                    self.app.logger,
                )
            except Exception as e:
                self.app.logger.log(f"❌ Error descargando Fix Tools: {e}")
                messagebox.showerror("Error", str(e))
        threading.Thread(target=worker, daemon=True).start()
