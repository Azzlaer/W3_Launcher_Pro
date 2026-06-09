import tkinter as tk
from tkinter import ttk, messagebox
from core.registry_tools import delete_warcraft_registry, fix_world_editor, set_gateways, set_install_associations

class RegistryTab(ttk.Frame):
    def __init__(self,parent,app):
        super().__init__(parent,padding=10); self.app=app; self.cfg=app.config_manager; self._build()
    def _build(self):
        ttk.Label(self,text='🛡️ Registro Warcraft III',style='Title.TLabel').pack(anchor='w')
        box=ttk.LabelFrame(self,text='Acciones de Registro',padding=8); box.pack(fill='x',pady=8)
        ttk.Button(box,text='Eliminar claves Battle.net / Blizzard / asociaciones',style='Danger.TButton',command=self.clean).pack(fill='x',pady=3)
        ttk.Button(box,text='Fix World Editor',command=self.worldedit).pack(fill='x',pady=3)
        ttk.Button(box,text='Agregar Battle.net Gateways LatinBattle / WoE / Rubattle',command=self.gateways).pack(fill='x',pady=3)
        ttk.Button(box,text='Registrar InstallPath y asociaciones básicas',command=self.installpath).pack(fill='x',pady=3)
        ttk.Label(self,text='Nota: HKLM/HKCR normalmente requiere ejecutar como administrador.',style='Muted.TLabel').pack(anchor='w')
    def _show(self,rows):
        for r in rows: self.app.log(r)
        messagebox.showinfo('Resultado','\n'.join(rows[:12]) + ('\n...' if len(rows)>12 else ''))
    def clean(self):
        if messagebox.askyesno('Confirmar','Esto eliminará claves de registro de Warcraft/Battle.net. ¿Continuar?'):
            self._show(delete_warcraft_registry())
    def worldedit(self): self._show(fix_world_editor())
    def gateways(self): self._show(set_gateways())
    def installpath(self): self._show(set_install_associations(self.cfg.get('GENERAL','warcraft_path','')))
