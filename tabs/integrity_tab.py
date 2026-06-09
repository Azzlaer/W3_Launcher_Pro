import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from core.crc_scanner import scan_version, scan_known, identify_w3l, export_csv

class IntegrityTab(ttk.Frame):
    def __init__(self,parent,app):
        super().__init__(parent,padding=10); self.app=app; self.cfg=app.config_manager
        self.folder=tk.StringVar(value=self.cfg.get('GENERAL','warcraft_path',''))
        self.version=tk.StringVar(value='1.27B'); self.rows=[]; self._build()
    def _build(self):
        ttk.Label(self,text='🔎 CRC / Integridad',style='Title.TLabel').pack(anchor='w')
        top=ttk.Frame(self); top.pack(fill='x',pady=6)
        ttk.Entry(top,textvariable=self.folder).pack(side='left',fill='x',expand=True)
        ttk.Button(top,text='Buscar',command=self.choose).pack(side='left',padx=4)
        ttk.Combobox(top,textvariable=self.version,values=['1.26a','1.27B','1.28'],state='readonly',width=10).pack(side='left',padx=4)
        ttk.Button(top,text='Escanear versión',command=self.scan).pack(side='left',padx=4)
        ttk.Button(top,text='Detectar W3L/Tools',command=self.scan_tools).pack(side='left',padx=4)
        ttk.Button(top,text='Exportar CSV',command=self.export).pack(side='left',padx=4)
        self.tree=ttk.Treeview(self,columns=('a','b','c','d'),show='headings')
        for col,name in zip(('a','b','c','d'),('Archivo/Tipo','Esperado/Versión','CRC detectado','Estado')):
            self.tree.heading(col,text=name); self.tree.column(col,width=180)
        self.tree.pack(fill='both',expand=True)
    def choose(self):
        p=filedialog.askdirectory();
        if p:self.folder.set(p)
    def fill(self,rows):
        self.rows=rows; self.tree.delete(*self.tree.get_children())
        for r in rows:self.tree.insert('', 'end', values=r)
    def scan(self):
        self.fill(scan_version(Path(self.folder.get()), self.version.get()))
        self.app.log(f'Escaneo CRC {self.version.get()} terminado.')
    def scan_tools(self):
        rows=[]; rows += identify_w3l(Path(self.folder.get())); rows += scan_known(Path(self.folder.get()))
        self.fill(rows); self.app.log('Escaneo W3L/tools terminado.')
    def export(self):
        dest=Path(__file__).resolve().parents[1]/'reports'/'crc_report.csv'
        export_csv([('Archivo/Tipo','Esperado/Versión','CRC detectado','Estado'),*self.rows],dest)
        messagebox.showinfo('Exportado',str(dest))
