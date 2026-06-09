from tkinter import ttk
from core.download_tools import open_url

class MapsTab(ttk.Frame):
    def __init__(self,parent,app):
        super().__init__(parent,padding=10); self.app=app; self._build()
    def _build(self):
        ttk.Label(self,text='🗺️ Mapas EpicWar / Web PHP',style='Title.TLabel').pack(anchor='w')
        ttk.Label(self,text='Incluye web_maps/index.php para publicar/agregar listado de mapas con enlace, comentario, usuario y fecha.',style='Muted.TLabel').pack(anchor='w',pady=4)
        ttk.Button(self,text='Abrir EpicWar',command=lambda:open_url('https://www.epicwar.com/maps/')).pack(anchor='w',pady=8)
