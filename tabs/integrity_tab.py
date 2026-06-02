from __future__ import annotations

import csv
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from core.crc_database import ORIGINAL_FILES, SUSPICIOUS_FILES, ALLOWED_TOOLS, W3L_CRC, W3L_DOWNLOADS
from core.crc_scanner import compare_crc


class IntegrityTab(ttk.Frame):
    """CRC / Integridad / detección básica."""

    def __init__(self, master, app):
        super().__init__(master, padding=8)
        self.app = app
        self.cfg = app.cfg
        self.log = app.logger.log
        self.rows: list[dict] = []
        self.build()

    def build(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        ttk.Label(self, text="🛡 CRC / Integridad de Warcraft III", style="Title.TLabel").grid(row=0, column=0, sticky="w")

        top = ttk.Frame(self)
        top.grid(row=1, column=0, sticky="ew", pady=(6, 6))
        top.columnconfigure(1, weight=1)
        self.path_var = tk.StringVar(value=self.cfg.get("GAME", "install_path"))
        self.version_var = tk.StringVar(value="1.27B")
        self.mode_var = tk.StringVar(value="Originales")
        ttk.Label(top, text="Carpeta:").grid(row=0, column=0, sticky="w")
        ttk.Entry(top, textvariable=self.path_var).grid(row=0, column=1, sticky="ew", padx=5)
        ttk.Button(top, text="...", width=4, command=self.pick_folder).grid(row=0, column=2)
        ttk.Label(top, text="Versión:").grid(row=0, column=3, sticky="e", padx=(10, 3))
        ttk.Combobox(top, textvariable=self.version_var, state="readonly", width=8, values=list(ORIGINAL_FILES.keys())).grid(row=0, column=4)
        ttk.Label(top, text="Tipo:").grid(row=0, column=5, sticky="e", padx=(10, 3))
        ttk.Combobox(top, textvariable=self.mode_var, state="readonly", width=16, values=["Originales", "W3L", "Permitidas", "Sospechosas"]).grid(row=0, column=6)
        ttk.Button(top, text="Escanear", style="Accent.TButton", command=self.scan).grid(row=0, column=7, padx=(6,0))

        cols = ("file", "expected", "crc", "result")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=13)
        for col, text, width in [("file", "Archivo", 190), ("expected", "CRC esperado", 105), ("crc", "CRC actual", 105), ("result", "Resultado", 110)]:
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width, anchor="w")
        self.tree.grid(row=2, column=0, sticky="nsew")
        sb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        sb.grid(row=2, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=sb.set)

        bottom = ttk.Frame(self)
        bottom.grid(row=3, column=0, sticky="ew", pady=(6, 0))
        ttk.Button(bottom, text="Exportar CSV", command=self.export_csv).pack(side="left")
        ttk.Button(bottom, text="Ver lista W3L", command=self.show_w3l_info).pack(side="left", padx=5)
        ttk.Button(bottom, text="Info descargas", command=self.show_downloads).pack(side="left")

    def pick_folder(self):
        folder = filedialog.askdirectory(title="Seleccionar carpeta Warcraft III")
        if folder:
            self.path_var.set(folder)
            self.cfg.set("GAME", "install_path", folder)

    def expected_set(self):
        mode = self.mode_var.get()
        if mode == "Originales":
            return ORIGINAL_FILES[self.version_var.get()]
        if mode == "W3L":
            # compara el archivo w3l.exe contra los CRC conocidos, usando el primer CRC como esperado visual.
            return {"w3l.exe": next(iter(W3L_CRC.get(self.version_var.get(), {"w3l.exe":""}).values()))}
        if mode == "Permitidas":
            return ALLOWED_TOOLS
        return SUSPICIOUS_FILES

    def scan(self):
        self.cfg.set("GAME", "install_path", self.path_var.get())
        self.tree.delete(*self.tree.get_children())
        expected = self.expected_set()
        self.rows = compare_crc(self.path_var.get(), expected)
        for row in self.rows:
            tag = row["result"]
            self.tree.insert("", "end", values=(row["file"], row["expected"], row["crc"], row["result"]), tags=(tag,))
        self.tree.tag_configure("ORIGINAL", foreground="#80FF68")
        self.tree.tag_configure("PRESENTE", foreground="#80FF68")
        self.tree.tag_configure("MODIFICADO", foreground="#FFD35A")
        self.tree.tag_configure("FALTA", foreground="#A9B98E")
        self.tree.tag_configure("OK", foreground="#80FF68")
        if self.mode_var.get() == "Sospechosas":
            found = [r for r in self.rows if r["crc"] != "NO_EXISTE"]
            if found:
                self.log(f"⚠ Se detectaron {len(found)} archivo(s) sospechoso(s) por nombre/CRC")
            else:
                self.log("✅ No se detectaron archivos sospechosos de la lista local")
        else:
            self.log(f"🛡 Escaneo CRC completado: {self.mode_var.get()} / {self.version_var.get()}")

    def export_csv(self):
        if not self.rows:
            messagebox.showinfo("Exportar", "Primero ejecuta un escaneo.")
            return
        out = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")], title="Guardar reporte CRC")
        if not out:
            return
        with open(out, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["file", "expected", "crc", "result", "path", "status"])
            writer.writeheader()
            writer.writerows(self.rows)
        self.log(f"📄 Reporte exportado: {out}")

    def show_w3l_info(self):
        lines = []
        for ver, items in W3L_CRC.items():
            lines.append(f"[{ver}]")
            for name, crc in items.items():
                lines.append(f"{name}: {crc}")
            lines.append("")
        messagebox.showinfo("Listado W3L", "\n".join(lines))

    def show_downloads(self):
        text = "\n".join([f"{k}: {v}" for k, v in W3L_DOWNLOADS.items()])
        messagebox.showinfo("Descargas W3L", text)
