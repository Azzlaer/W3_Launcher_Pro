from __future__ import annotations
import tkinter as tk
from tkinter import ttk
from core.config_manager import ConfigManager
from core.theme import apply_style, ORC
from core.assets import asset_path, load_image

from tabs.dashboard_tab import DashboardTab
from tabs.registry_tab import RegistryTab
from tabs.video_tab import VideoTab
from tabs.gproxy_tab import GProxyTab
from tabs.integrity_tab import IntegrityTab
from tabs.maps_tab import MapsTab
from tabs.tools_tab import ToolsTab

class WC3LauncherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('WC3 Orc Launcher Pro - Frozen Throne / PvPGN / GProxy')
        self.geometry('980x660')
        self.minsize(900, 600)
        self.config_manager = ConfigManager()
        apply_style(self)
        self._build()

    def _build(self):
        top = ttk.Frame(self, padding=(10, 6))
        top.pack(fill='x')
        self._top_logo = load_image(asset_path('latinbattle_logo.png'), size=(190, 64))
        if self._top_logo:
            tk.Label(top, image=self._top_logo, bg=ORC['bg'], borderwidth=0).pack(side='left', padx=(0, 10))
        else:
            ttk.Label(top, text='⚔️ LATINBATTLE', style='Title.TLabel').pack(side='left', padx=(0, 10))
        title_box = ttk.Frame(top)
        title_box.pack(side='left', fill='x', expand=True)
        ttk.Label(title_box, text='WC3 ORC LAUNCHER PRO', style='Title.TLabel').pack(anchor='w')
        ttk.Label(title_box, text='Frozen Throne • Reign of Chaos • PvPGN • GProxy • WorldOfEditors', style='Muted.TLabel').pack(anchor='w')
        self._top_url = load_image(asset_path('latinbattle_url.png'), size=(230, 48))
        if self._top_url:
            tk.Label(top, image=self._top_url, bg=ORC['bg'], borderwidth=0).pack(side='right')

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=(0, 6))
        self.console = tk.Text(self, height=5, bg=ORC['entry'], fg=ORC['green'], insertbackground=ORC['gold'], relief='flat', font=('Consolas', 9))
        self.console.pack(fill='x', padx=10, pady=(0, 8))
        self.log('Launcher iniciado.')

        tabs = [
            ('🏠 Inicio', DashboardTab, True),
            ('🧩 GProxy', GProxyTab, True),
            ('🛡️ Registro', RegistryTab, True),
            ('🎥 Video', VideoTab, True),
            ('🔎 CRC', IntegrityTab, True),
            # La sección Mapas queda conservada pero oculta por defecto.
            # Actívala desde config.ini: [FEATURES] show_maps_tab = true
            ('🗺️ Mapas', MapsTab, self.config_manager.getbool('FEATURES', 'show_maps_tab', False)),
            ('🧰 Tools', ToolsTab, True),
        ]
        for title, cls, visible in tabs:
            if visible:
                frame = cls(self.notebook, self)
                self.notebook.add(frame, text=title)

    def log(self, message: str):
        self.console.insert('end', f'> {message}\n')
        self.console.see('end')

if __name__ == '__main__':
    app = WC3LauncherApp()
    app.mainloop()
