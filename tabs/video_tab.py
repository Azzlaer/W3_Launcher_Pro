import tkinter as tk
from tkinter import ttk, messagebox
from core.registry_tools import set_video

COMMON_RES=[(640,400),(640,480),(800,600),(1024,768),(1280,720),(1280,768),(1360,768),(1366,768),(1440,900),(1600,900),(1680,1050),(1920,1080),(2560,1440)]
class VideoTab(ttk.Frame):
    def __init__(self,parent,app):
        super().__init__(parent,padding=10); self.app=app; self.cfg=app.config_manager
        self.res=tk.StringVar(value=f"{self.cfg.get('VIDEO','reswidth','1024')}x{self.cfg.get('VIDEO','resheight','768')}")
        self.shadows=tk.BooleanVar(value=self.cfg.getbool('VIDEO','unitshadows',True)); self._build()
    def _build(self):
        ttk.Label(self,text='🎥 Video / Resolución',style='Title.TLabel').pack(anchor='w')
        box=ttk.LabelFrame(self,text='Configuración de video',padding=8); box.pack(fill='x',pady=8)
        ttk.Label(box,text='Resolución:').pack(side='left')
        ttk.Combobox(box,textvariable=self.res,values=[f'{w}x{h}' for w,h in COMMON_RES],width=18).pack(side='left',padx=6)
        ttk.Checkbutton(box,text='Sombras de unidades',variable=self.shadows).pack(side='left',padx=8)
        ttk.Button(box,text='Aplicar al registro',command=self.apply).pack(side='left',padx=8)
    def apply(self):
        try:
            w,h=self.res.get().lower().split('x'); rows=set_video(int(w),int(h),self.shadows.get())
            self.cfg.set('VIDEO','reswidth',w); self.cfg.set('VIDEO','resheight',h); self.cfg.set('VIDEO','unitshadows',str(self.shadows.get()).lower())
            for r in rows:self.app.log(r)
            messagebox.showinfo('OK','Video aplicado al registro.')
        except Exception as e: messagebox.showerror('Error',str(e))
