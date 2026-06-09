from __future__ import annotations
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
import shutil, zipfile, subprocess, os
from core.download_tools import download_file, extract_archive_robust, open_url, start_process, filename_from_url, normalize_zipx_to_zip, get_latest_github_release_asset
from core.theme import ORC

class GProxyTab(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, padding=10)
        self.app=app; self.cfg=app.config_manager
        self.wc3_path=tk.StringVar(value=self.cfg.get('GENERAL','warcraft_path',''))
        self.install_dir=tk.StringVar(value=self.cfg.get('GPROXY','install_dir','tools\\GProxy'))
        self.profile=tk.StringVar(value=self.cfg.get('GPROXY','server_profile','WorldOfEditors'))
        self.server=tk.StringVar(value=self.cfg.get('GPROXY','server_address','worldofeditors.net'))
        self.username=tk.StringVar(value=self.cfg.get('GPROXY','username','Azzlaer'))
        self.auto_start=tk.BooleanVar(value=self.cfg.getbool('GPROXY','auto_start_before_game',False))
        self.status=tk.StringVar(value='')
        self._build(); self.refresh()

    def _build(self):
        head=ttk.Frame(self); head.pack(fill='x')
        ttk.Label(head,text='🧩 GProxy / WoEProxy',style='Title.TLabel').pack(side='left')
        ttk.Label(head,text='Protección contra desconexiones para servidores compatibles GHost++/GPS',style='Muted.TLabel').pack(side='right')

        box=ttk.LabelFrame(self,text='Configuración',padding=8); box.pack(fill='x',pady=8)
        r=ttk.Frame(box); r.pack(fill='x',pady=2)
        ttk.Label(r,text='Carpeta Warcraft III:',width=18).pack(side='left')
        ttk.Entry(r,textvariable=self.wc3_path).pack(side='left',fill='x',expand=True,padx=4)
        ttk.Button(r,text='Buscar',command=self.choose_wc3).pack(side='left')
        r=ttk.Frame(box); r.pack(fill='x',pady=2)
        ttk.Label(r,text='Instalar GProxy en:',width=18).pack(side='left')
        ttk.Entry(r,textvariable=self.install_dir).pack(side='left',fill='x',expand=True,padx=4)
        r=ttk.Frame(box); r.pack(fill='x',pady=2)
        ttk.Label(r,text='Perfil:',width=18).pack(side='left')
        cb=ttk.Combobox(r,textvariable=self.profile,values=['WorldOfEditors','Rubattle','GProxy Genérico','Personalizado'],state='readonly',width=22)
        cb.pack(side='left',padx=4); cb.bind('<<ComboboxSelected>>',lambda e:self.apply_profile())
        ttk.Label(r,text='Servidor:').pack(side='left',padx=(10,2))
        ttk.Entry(r,textvariable=self.server,width=28).pack(side='left')
        ttk.Label(r,text='Usuario:').pack(side='left',padx=(10,2))
        ttk.Entry(r,textvariable=self.username,width=18).pack(side='left')
        ttk.Checkbutton(box,text='Iniciar GProxy antes del juego',variable=self.auto_start).pack(anchor='w',pady=(4,0))

        downloads=ttk.LabelFrame(self,text='Descargas / Instalación',padding=8); downloads.pack(fill='x',pady=8)
        ttk.Button(downloads,text='⬇️ Descargar WoEProxy oficial',command=self.download_woe).pack(side='left',padx=3)
        ttk.Button(downloads,text='🌐 Abrir WorldOfEditors',command=lambda:open_url(self.cfg.get('WORLD_OF_EDITORS','website','https://worldofeditors.net/'))).pack(side='left',padx=3)
        ttk.Button(downloads,text='⬇️ Descargar GProxy GitHub',command=self.download_github_gproxy).pack(side='left',padx=3)
        ttk.Button(downloads,text='🌐 Info Rubattle GProxy',command=lambda:open_url(self.cfg.get('RUBATTLE','info_url',''))).pack(side='left',padx=3)
        ttk.Button(downloads,text='🌐 W3 Loader Rubattle',command=lambda:open_url(self.cfg.get('DOWNLOADS','rubattle_w3loader',''))).pack(side='left',padx=3)

        actions=ttk.LabelFrame(self,text='Acciones',padding=8); actions.pack(fill='x',pady=8)
        ttk.Button(actions,text='Guardar configuración',command=self.save).pack(side='left',padx=3)
        ttk.Button(actions,text='▶ Ejecutar GPROXY.EXE',command=self.run_gproxy).pack(side='left',padx=3)
        ttk.Button(actions,text='▶ Ejecutar WoEProxy',command=self.run_woe).pack(side='left',padx=3)
        ttk.Button(actions,text='📁 Abrir carpeta GProxy',command=self.open_install_folder).pack(side='left',padx=3)
        ttk.Button(actions,text='🔄 Comprobar',command=self.refresh).pack(side='left',padx=3)

        note=tk.Text(self,height=7,bg=ORC['entry'],fg=ORC['text'],relief='flat',font=('Consolas',9))
        note.pack(fill='both',expand=True,pady=(6,0))
        note.insert('end','''Notas importantes:\n- WoEProxy oficial se descarga desde https://proxy.worldofeditors.net/woeproxy.exe\n- WorldOfEditors indica ejecutar WoEProxy como administrador.\n- GProxy clásico requiere servidor compatible GHost++/GPS.\n- Si Windows Firewall pregunta, permite conexión privada/pública según tu servidor.\n- Para Rubattle, se deja el botón de información porque algunas descargas cambian con el tiempo.\n''')
        note.config(state='disabled')
        ttk.Label(self,textvariable=self.status,style='Muted.TLabel').pack(anchor='w',pady=(5,0))

    def choose_wc3(self):
        p=filedialog.askdirectory(title='Carpeta Warcraft III')
        if p: self.wc3_path.set(p)

    def install_path(self):
        p=Path(self.install_dir.get())
        if not p.is_absolute(): p=Path(__file__).resolve().parents[1]/p
        return p

    def apply_profile(self):
        if self.profile.get()=='WorldOfEditors': self.server.set('worldofeditors.net')
        elif self.profile.get()=='Rubattle': self.server.set('rubattle.net')
        elif self.profile.get()=='GProxy Genérico': self.server.set('PUBLIC.INDOGAMERS.US')

    def save(self):
        for s,k,v in [('GENERAL','warcraft_path',self.wc3_path.get()),('GPROXY','install_dir',self.install_dir.get()),('GPROXY','server_profile',self.profile.get()),('GPROXY','server_address',self.server.get()),('GPROXY','username',self.username.get()),('GPROXY','auto_start_before_game',str(self.auto_start.get()).lower())]:
            self.cfg.set(s,k,v)
        self.app.log('Configuración GProxy guardada.')

    def download_woe(self):
        self.save(); url=self.cfg.get('WORLD_OF_EDITORS','proxy_url','https://proxy.worldofeditors.net/woeproxy.exe')
        dest_wc3=Path(self.wc3_path.get())/'woeproxy.exe'
        try:
            download_file(url,dest_wc3,lambda d,t:self.app.log(f'Descargando WoEProxy {d}/{t or "?"} bytes'))
            also=self.install_path()/ 'woeproxy.exe'; also.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(dest_wc3,also)
            self.app.log(f'WoEProxy instalado en Warcraft III y tools: {dest_wc3}')
            self.refresh()
        except Exception as e:
            messagebox.showerror('Error',str(e))

    def download_github_gproxy(self):
        self.save()
        fallback = self.cfg.get('DOWNLOADS','github_gproxy_zip','')
        url = get_latest_github_release_asset(
            'dns/GProxy-Warcraft3-disconnect-protection-tool',
            r'GProxy.*\.(zipx|zip)$',
            fallback
        )
        original_name = filename_from_url(url, 'GProxy-2.0.zipx')
        dest = Path(__file__).resolve().parents[1] / 'tools' / 'downloads' / original_name
        try:
            self.app.log(f'URL GProxy seleccionada: {url}')
            download_file(url, dest, lambda d,t:self.app.log(f'Descargando GProxy {d}/{t or "?"} bytes'))

            final_archive = normalize_zipx_to_zip(dest)
            if final_archive != dest:
                self.app.log(f'Archivo .zipx renombrado automáticamente a: {final_archive.name}')

            ok, msg = extract_archive_robust(final_archive, self.install_path(), log=self.app.log)
            self.app.log(msg)
            if not ok:
                messagebox.showwarning('GProxy descargado, extracción pendiente', msg)
            self.refresh()
        except Exception as e:
            messagebox.showerror('Error',str(e))

    def run_gproxy(self):
        exe=self.install_path()/'GPROXY.EXE'
        if not exe.exists(): exe=self.install_path()/'gproxy.exe'
        if not exe.exists():
            messagebox.showwarning('No encontrado','No encontré GPROXY.EXE en la carpeta de instalación.')
            return
        start_process(exe,cwd=exe.parent)
        self.app.log(f'GProxy ejecutado: {exe}')

    def run_woe(self):
        p1=Path(self.wc3_path.get())/'woeproxy.exe'; p2=self.install_path()/'woeproxy.exe'
        exe=p1 if p1.exists() else p2
        if not exe.exists():
            messagebox.showwarning('No encontrado','No encontré woeproxy.exe. Usa Descargar WoEProxy oficial.')
            return
        start_process(exe,cwd=exe.parent)
        self.app.log(f'WoEProxy ejecutado: {exe}')

    def open_install_folder(self):
        p=self.install_path(); p.mkdir(parents=True,exist_ok=True)
        os.startfile(str(p)) if os.name=='nt' else subprocess.Popen(['xdg-open',str(p)])

    def refresh(self):
        wc3=Path(self.wc3_path.get())
        items=[]
        for p in [wc3/'woeproxy.exe', self.install_path()/'GPROXY.EXE', self.install_path()/'gproxy.exe']:
            items.append(f'{p.name}: {"OK" if p.exists() else "NO"}')
        self.status.set(' | '.join(items))
