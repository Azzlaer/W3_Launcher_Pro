from tkinter import ttk, messagebox
from pathlib import Path
from core.download_tools import open_url, download_file

class ToolsTab(ttk.Frame):
    def __init__(self,parent,app):
        super().__init__(parent,padding=10); self.app=app; self.cfg=app.config_manager; self._build()
    def _build(self):
        ttk.Label(self,text='🧰 Fix Tools / W3L',style='Title.TLabel').pack(anchor='w')
        box=ttk.LabelFrame(self,text='Enlaces útiles',padding=8); box.pack(fill='x',pady=8)
        ttk.Button(box,text='Abrir WarcraftHelper Releases',command=lambda:open_url(self.cfg.get('DOWNLOADS','fix_tools_url',''))).pack(fill='x',pady=3)
        ttk.Button(box,text='Abrir W3L 1.26/1.28 PvPGN',command=lambda:open_url(self.cfg.get('DOWNLOADS','w3l_126_128',''))).pack(fill='x',pady=3)
        ttk.Button(box,text='Abrir W3L 1.27 PvPGN',command=lambda:open_url(self.cfg.get('DOWNLOADS','w3l_127',''))).pack(fill='x',pady=3)
        ttk.Label(self,text='Contraseña ZIP PvPGN: pvpgn',style='Muted.TLabel').pack(anchor='w')
