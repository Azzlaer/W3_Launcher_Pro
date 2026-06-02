from __future__ import annotations

import json
import threading
import urllib.parse
from pathlib import Path
from tkinter import messagebox, ttk

import requests


DEFAULT_MAPS = [
    {"name": "Saint Seiya Legends 4.0", "epicwar_url": "https://www.epicwar.com/maps/349240/", "comment": "Mapa agregado inicialmente", "user": "Azzlaer", "date": "2026-05-04"},
    {"name": "Guns Duel V1.0 Open", "epicwar_url": "https://www.epicwar.com/maps/349238/", "comment": "Ejemplo editable", "user": "Azzlaer", "date": "2026-05-04"},
]


class MapsTab(ttk.Frame):
    def __init__(self, master, app):
        super().__init__(master, padding=8)
        self.app = app
        self.cfg = app.cfg
        self.maps = []
        self.build()
        self.load_maps()

    @property
    def maps_json(self) -> Path:
        return Path("web_maps") / "maps.json"

    def build(self):
        ttk.Label(self, text="Mapas EpicWar", style="Title.TLabel").pack(anchor="w", pady=(0, 5))
        ttk.Label(
            self,
            text="Usa web_maps/maps.json y web_maps/index.php para publicar/agregar mapas desde navegador.",
            style="Muted.TLabel",
            wraplength=760,
        ).pack(anchor="w", pady=(0, 6))
        columns = ("name", "url", "date", "user", "comment")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=9)
        headers = {"name": "Mapa", "url": "EpicWar", "date": "Fecha", "user": "Usuario", "comment": "Comentario"}
        widths = {"name": 160, "url": 220, "date": 80, "user": 90, "comment": 230}
        for col in columns:
            self.tree.heading(col, text=headers[col])
            self.tree.column(col, width=widths[col], minwidth=60)
        self.tree.pack(fill="both", expand=True)
        row = ttk.Frame(self)
        row.pack(fill="x", pady=7)
        ttk.Button(row, text="🔄 Recargar", command=self.load_maps).pack(side="left")
        ttk.Button(row, text="⬇ Descargar seleccionado", style="Accent.TButton", command=self.download_selected).pack(side="left", padx=6)

    def load_maps(self):
        self.maps_json.parent.mkdir(exist_ok=True)
        if not self.maps_json.exists():
            self.maps_json.write_text(json.dumps(DEFAULT_MAPS, indent=2, ensure_ascii=False), encoding="utf-8")
        self.maps = json.loads(self.maps_json.read_text(encoding="utf-8"))
        for i in self.tree.get_children():
            self.tree.delete(i)
        for idx, item in enumerate(self.maps):
            self.tree.insert("", "end", iid=str(idx), values=(item.get("name", ""), item.get("epicwar_url", ""), item.get("date", ""), item.get("user", ""), item.get("comment", "")))
        self.app.logger.log(f"🗺 Mapas cargados: {len(self.maps)}")

    def _extract_download_link(self, html: str, page_url: str) -> str | None:
        import re
        for href in re.findall(r'href=["\']([^"\']+)["\']', html, flags=re.I):
            if "download" in href.lower():
                return urllib.parse.urljoin(page_url, href)
        return None

    def download_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Selecciona un mapa", "Debes seleccionar un mapa de la tabla.")
            return
        item = self.maps[int(sel[0])]
        threading.Thread(target=self._download_map, args=(item,), daemon=True).start()

    def _download_map(self, item: dict):
        try:
            page_url = item["epicwar_url"]
            self.app.logger.log(f"Buscando enlace de descarga: {page_url}")
            html = requests.get(page_url, timeout=30).text
            dl = self._extract_download_link(html, page_url)
            if not dl:
                raise RuntimeError("No se encontró enlace de descarga en la página EpicWar.")
            resp = requests.get(dl, timeout=120)
            resp.raise_for_status()
            folder = Path(self.cfg.get("GAME", "install_path")) / self.cfg.get("MAPS", "download_folder")
            folder.mkdir(parents=True, exist_ok=True)
            map_id = page_url.rstrip("/").split("/")[-1]
            out = folder / f"{map_id}.w3x"
            if out.exists():
                self.app.logger.log(f"⚠ Ya existía, será reemplazado: {out.name}")
            out.write_bytes(resp.content)
            self.app.logger.log(f"✅ Mapa descargado: {out}")
        except Exception as e:
            self.app.logger.log(f"❌ Error descargando mapa: {e}")
            messagebox.showerror("Error", str(e))
