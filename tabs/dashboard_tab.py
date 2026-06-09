from __future__ import annotations
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from core.theme import ORC
from core.assets import asset_path, load_image
from core.version_tools import file_version
from core.download_tools import start_process

class DashboardTab(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, padding=8)
        self.app = app
        self.cfg = app.config_manager
        self.game_mode = tk.StringVar(value=self.cfg.get('GENERAL','last_game_mode','frozen_throne'))
        self.loader = tk.StringVar(value=self.cfg.get('GENERAL','last_loader','normal'))
        self.window = tk.BooleanVar(value=self.cfg.getbool('LAUNCH','window_mode',True))
        self.opengl = tk.BooleanVar(value=self.cfg.getbool('LAUNCH','opengl',False))
        self.path = tk.StringVar(value=self.cfg.get('GENERAL','warcraft_path',''))
        self.info = tk.StringVar(value='')
        self._images = []
        self._build()
        self.refresh_info()

    def _build(self):
        # HERO VISUAL
        hero = tk.Canvas(self, height=190, highlightthickness=2, highlightbackground=ORC['gold'], bg=ORC['panel'])
        hero.pack(fill='x', pady=(0,8))
        hero.bind('<Configure>', self._draw_hero)

        # Barra rápida de ruta
        route = ttk.LabelFrame(self, text='📁 Carpeta Warcraft III', padding=7)
        route.pack(fill='x', pady=(0,8))
        ttk.Entry(route, textvariable=self.path).pack(side='left', fill='x', expand=True, padx=(0,6))
        ttk.Button(route, text='Buscar', command=self.choose_path).pack(side='left')
        ttk.Button(route, text='Guardar', command=self.save_path).pack(side='left', padx=(6,0))

        grid = ttk.Frame(self)
        grid.pack(fill='both', expand=True)

        left_col = ttk.Frame(grid)
        left_col.pack(side='left', fill='both', expand=True, padx=(0,6))
        right_col = ttk.Frame(grid)
        right_col.pack(side='left', fill='both', expand=True, padx=(6,0))

        modes = ttk.LabelFrame(left_col, text='⚔️ Modo de juego', padding=8)
        modes.pack(fill='x', pady=(0,8))
        ttk.Radiobutton(modes, text='Frozen Throne', variable=self.game_mode, value='frozen_throne').pack(anchor='w')
        ttk.Radiobutton(modes, text='Reign of Chaos', variable=self.game_mode, value='reign_of_chaos').pack(anchor='w')

        launch_box = ttk.LabelFrame(left_col, text='🚀 Launcher / Loader', padding=8)
        launch_box.pack(fill='x')
        ttk.Radiobutton(launch_box, text='W3 Loader normal', variable=self.loader, value='normal').pack(anchor='w')
        ttk.Radiobutton(launch_box, text='W3 Loader Rubattle', variable=self.loader, value='rubattle').pack(anchor='w')
        ttk.Radiobutton(launch_box, text='WoEProxy / WorldOfEditors', variable=self.loader, value='woe').pack(anchor='w')
        ttk.Radiobutton(launch_box, text='Directo sin loader', variable=self.loader, value='direct').pack(anchor='w')

        params = ttk.LabelFrame(right_col, text='⚙️ Parámetros rápidos', padding=8)
        params.pack(fill='x', pady=(0,8))
        ttk.Checkbutton(params, text='Modo ventana (-window)', variable=self.window).pack(anchor='w')
        ttk.Checkbutton(params, text='Mejora OpenGL (-opengl)', variable=self.opengl).pack(anchor='w')

        preview = tk.Canvas(right_col, height=112, highlightthickness=1, highlightbackground=ORC['green2'], bg=ORC['panel2'])
        preview.pack(fill='x', pady=(0,8))
        preview.bind('<Configure>', self._draw_preview)

        actions = ttk.Frame(right_col)
        actions.pack(fill='x')
        ttk.Button(actions, text='⚔️ JUGAR AHORA', style='Gold.TButton', command=self.launch_game).pack(side='left', fill='x', expand=True, ipady=10)
        ttk.Button(actions, text='Actualizar', command=self.refresh_info).pack(side='left', padx=(8,0), ipady=10)

        status = ttk.LabelFrame(self, text='📌 Estado del launcher', padding=7)
        status.pack(fill='x', pady=(8,0))
        ttk.Label(status, textvariable=self.info, style='Muted.TLabel').pack(anchor='w')

    def _draw_hero(self, event):
        canvas = event.widget
        w, h = event.width, event.height
        canvas.delete('all')
        self._hero_img = load_image(asset_path('orc_night_camp.jpg'), size=(w, h), cover=True, darken=0.55)
        if self._hero_img:
            canvas.create_image(0, 0, image=self._hero_img, anchor='nw')
        canvas.create_rectangle(10, 10, w-10, h-10, outline=ORC['gold'], width=1)
        self._hero_logo = load_image(asset_path('latinbattle_logo.png'), size=(260, 90))
        if self._hero_logo:
            canvas.create_image(24, 18, image=self._hero_logo, anchor='nw')
        canvas.create_text(w-26, 42, text='WC3 ORC LAUNCHER PRO', fill=ORC['gold'], font=('Segoe UI Black', 22), anchor='ne')
        canvas.create_text(w-26, 75, text='Frozen Throne • PvPGN • GProxy • WoEProxy', fill=ORC['green'], font=('Segoe UI Semibold', 11), anchor='ne')
        canvas.create_text(w-26, 104, text='Lok\'tar Ogar — preparado para LatinBattle y servidores clásicos', fill='#e8f4df', font=('Segoe UI', 10), anchor='ne')
        canvas.create_text(24, h-28, text='Selecciona modo, loader y presiona JUGAR AHORA', fill='#ffffff', font=('Segoe UI Semibold', 10), anchor='sw')

    def _draw_preview(self, event):
        canvas = event.widget
        w, h = event.width, event.height
        canvas.delete('all')
        self._preview_img = load_image(asset_path('orc_day_banner.jpg'), size=(w, h), cover=True, darken=0.72)
        if self._preview_img:
            canvas.create_image(0, 0, image=self._preview_img, anchor='nw')
        canvas.create_text(14, 18, text='Modo recomendado', fill=ORC['gold'], font=('Segoe UI Black', 11), anchor='nw')
        canvas.create_text(14, 45, text='Frozen Throne + W3L normal + GProxy opcional', fill='#ffffff', font=('Segoe UI Semibold', 9), anchor='nw')
        canvas.create_text(14, 72, text='Usa la pestaña GProxy para WoEProxy o GProxy clásico.', fill=ORC['muted'], font=('Segoe UI', 9), anchor='nw')

    def choose_path(self):
        p = filedialog.askdirectory(title='Selecciona carpeta Warcraft III')
        if p:
            self.path.set(p)
            self.refresh_info()

    def save_path(self):
        self.cfg.set('GENERAL','warcraft_path', self.path.get())
        self.app.log(f'Carpeta guardada: {self.path.get()}')

    def _exe(self):
        folder = Path(self.path.get())
        loader = self.loader.get()
        if loader == 'normal':
            return folder / self.cfg.get('EXECUTABLES','normal_loader_exe','w3l.exe')
        if loader == 'rubattle':
            return folder / self.cfg.get('EXECUTABLES','rubattle_loader_exe','w3l_rubattle.exe')
        if loader == 'woe':
            return folder / self.cfg.get('EXECUTABLES','woe_loader_exe','woeproxy.exe')
        if self.game_mode.get() == 'reign_of_chaos':
            return folder / self.cfg.get('EXECUTABLES','reign_of_chaos_exe','Warcraft III.exe')
        return folder / self.cfg.get('EXECUTABLES','frozen_throne_exe','Frozen Throne.exe')

    def launch_game(self):
        self.save_path()
        self.cfg.set('GENERAL','last_game_mode', self.game_mode.get())
        self.cfg.set('GENERAL','last_loader', self.loader.get())
        self.cfg.set('LAUNCH','window_mode', str(self.window.get()).lower())
        self.cfg.set('LAUNCH','opengl', str(self.opengl.get()).lower())
        exe = self._exe()
        args=[]
        if self.window.get(): args.append('-window')
        if self.opengl.get(): args.append('-opengl')
        extra = self.cfg.get('LAUNCH','extra_args','').strip()
        if extra: args += extra.split()
        if not exe.exists():
            messagebox.showerror('No encontrado', f'No existe:\n{exe}')
            return
        start_process(exe, args=args, cwd=exe.parent)
        self.app.log(f'Ejecutado: {exe.name} {" ".join(args)}')

    def refresh_info(self):
        folder = Path(self.path.get())
        w3l = folder / 'w3l.exe'
        ft = folder / self.cfg.get('EXECUTABLES','frozen_throne_exe','Frozen Throne.exe')
        roc = folder / self.cfg.get('EXECUTABLES','reign_of_chaos_exe','Warcraft III.exe')
        parts = []
        parts.append(f'w3l.exe: {"OK" if w3l.exists() else "NO encontrado"}')
        if w3l.exists():
            parts.append(f'versión: {file_version(w3l)}')
        parts.append(f'Frozen Throne: {"OK" if ft.exists() else "NO"}')
        parts.append(f'Reign of Chaos: {"OK" if roc.exists() else "NO"}')
        self.info.set(' | '.join(parts))
