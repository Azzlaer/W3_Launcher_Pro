from __future__ import annotations

import sys
import tkinter as tk
from tkinter import ttk

from core.config_manager import ConfigManager
from core.logger import GuiLogger
from core import admin
from tabs.dashboard_tab import DashboardTab
from tabs.launcher_tab import LauncherTab
from tabs.registry_tab import RegistryTab
from tabs.worldedit_tab import WorldEditTab
from tabs.video_tab import VideoTab
from tabs.tools_tab import ToolsTab
from tabs.integrity_tab import IntegrityTab
from tabs.gproxy_tab import GProxyTab
from tabs.maps_tab import MapsTab


class WC3LauncherApp(tk.Tk):
    """GUI compacto con estética Orc/Frozen Throne y pestañas modulares."""

    BG = "#07120A"
    PANEL = "#102016"
    PANEL_2 = "#162A1B"
    FG = "#E9F2D0"
    MUTED = "#A9B98E"
    ORC = "#62D24F"
    ORC_DARK = "#2E7D32"
    GOLD = "#D4A017"
    RED = "#B13B2E"
    FIELD = "#0A180E"

    def __init__(self):
        super().__init__()
        self.title("WC3 Orc Launcher Pro - Frozen Throne / Reign of Chaos")
        self.geometry("980x650")
        self.minsize(900, 590)
        self.cfg = ConfigManager("config.ini")
        self.logger = GuiLogger()
        self.build_style()
        self.build_ui()

    def build_style(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        self.configure(bg=self.BG)
        style.configure("TFrame", background=self.BG)
        style.configure("Panel.TFrame", background=self.PANEL)
        style.configure("TLabel", background=self.BG, foreground=self.FG, font=("Segoe UI", 9))
        style.configure("Muted.TLabel", background=self.BG, foreground=self.MUTED, font=("Segoe UI", 8))
        style.configure("Title.TLabel", background=self.BG, foreground=self.ORC, font=("Segoe UI", 13, "bold"))
        style.configure("Header.TLabel", background=self.BG, foreground=self.GOLD, font=("Segoe UI", 16, "bold"))
        style.configure("Status.TLabel", background=self.BG, foreground=self.MUTED, font=("Segoe UI", 9, "bold"))

        style.configure("TLabelframe", background=self.BG, foreground=self.GOLD, bordercolor=self.GOLD, lightcolor=self.GOLD, darkcolor=self.ORC_DARK, relief="ridge")
        style.configure("TLabelframe.Label", background=self.BG, foreground=self.GOLD, font=("Segoe UI", 9, "bold"))

        style.configure("TButton", background=self.PANEL_2, foreground=self.FG, bordercolor=self.GOLD, focusthickness=1, focuscolor=self.ORC, font=("Segoe UI", 9, "bold"), padding=(8, 4))
        style.map("TButton", background=[("active", self.ORC_DARK)], foreground=[("active", "#FFFFFF")])
        style.configure("Accent.TButton", background=self.ORC_DARK, foreground="#FFFFFF", bordercolor=self.GOLD, padding=(10, 5), font=("Segoe UI", 9, "bold"))
        style.map("Accent.TButton", background=[("active", self.ORC)], foreground=[("active", "#051008")])
        style.configure("Danger.TButton", background=self.RED, foreground="#FFFFFF", bordercolor=self.GOLD, padding=(8, 4), font=("Segoe UI", 9, "bold"))

        style.configure("TCheckbutton", background=self.BG, foreground=self.FG, font=("Segoe UI", 9))
        style.map("TCheckbutton", background=[("active", self.BG)], foreground=[("active", self.ORC)])
        style.configure("TRadiobutton", background=self.BG, foreground=self.FG, font=("Segoe UI", 9))
        style.map("TRadiobutton", background=[("active", self.BG)], foreground=[("active", self.ORC)])
        style.configure("TEntry", fieldbackground=self.FIELD, foreground=self.FG, insertcolor=self.FG, bordercolor=self.GOLD, padding=(4, 3))
        style.configure("TCombobox", fieldbackground=self.FIELD, background=self.PANEL_2, foreground=self.FG, arrowcolor=self.GOLD, padding=(4, 3))
        style.map("TCombobox", fieldbackground=[("readonly", self.FIELD)], foreground=[("readonly", self.FG)])

        style.configure("Treeview", background=self.FIELD, foreground=self.FG, fieldbackground=self.FIELD, rowheight=22, font=("Segoe UI", 8))
        style.configure("Treeview.Heading", background=self.PANEL_2, foreground=self.GOLD, font=("Segoe UI", 8, "bold"))
        style.map("Treeview", background=[("selected", self.ORC_DARK)], foreground=[("selected", "#FFFFFF")])

        style.configure("TNotebook", background=self.BG, borderwidth=0, tabmargins=(0, 4, 0, 0))
        style.configure("TNotebook.Tab", background=self.PANEL, foreground=self.MUTED, padding=(9, 5), font=("Segoe UI", 9, "bold"))
        style.map("TNotebook.Tab", background=[("selected", self.ORC_DARK), ("active", self.PANEL_2)], foreground=[("selected", "#FFFFFF"), ("active", self.ORC)])

    def build_ui(self):
        root = ttk.Frame(self, padding=8)
        root.pack(fill="both", expand=True)

        header = ttk.Frame(root)
        header.pack(fill="x")
        title_box = ttk.Frame(header)
        title_box.pack(side="left", fill="x", expand=True)
        ttk.Label(title_box, text="⚔ WC3 ORC LAUNCHER PRO", style="Header.TLabel").pack(anchor="w")
        ttk.Label(title_box, text="Inicio · Loaders · CRC · GProxy · Registro · WorldEdit · Video · Mapas", style="Muted.TLabel").pack(anchor="w")
        admin_text = "🛡 Admin: Sí" if admin.is_admin() else "⚠ Admin: No"
        ttk.Label(header, text=admin_text, style="Status.TLabel").pack(side="right", padx=(8, 0))

        self.tabs = ttk.Notebook(root)
        self.tabs.pack(fill="both", expand=True, pady=(7, 6))
        self.tabs.add(DashboardTab(self.tabs, self), text="🏠 Inicio")
        self.tabs.add(LauncherTab(self.tabs, self), text="Opciones")
        self.tabs.add(RegistryTab(self.tabs, self), text="Registro")
        self.tabs.add(WorldEditTab(self.tabs, self), text="WorldEdit")
        self.tabs.add(VideoTab(self.tabs, self), text="Video")
        self.tabs.add(ToolsTab(self.tabs, self), text="Fix Tools")
        self.tabs.add(IntegrityTab(self.tabs, self), text="CRC")
        self.tabs.add(GProxyTab(self.tabs, self), text="GProxy")
        self.tabs.add(MapsTab(self.tabs, self), text="Mapas")

        log_box = ttk.LabelFrame(root, text="Consola Orc", padding=5)
        log_box.pack(fill="x", expand=False)
        self.log_text = tk.Text(log_box, height=4, bg="#050B06", fg="#80FF68", insertbackground="#D4A017", relief="flat", font=("Consolas", 9), padx=6, pady=4, highlightthickness=1, highlightbackground=self.GOLD, highlightcolor=self.ORC)
        self.log_text.pack(fill="x", expand=False)
        self.log_text.configure(state="disabled")
        self.logger.bind(self.log_text)
        self.logger.log("⚔ Inicio cargado: Frozen Throne / Reign of Chaos + Loader normal/Rubattle")
        self.logger.log("Tip: para HKLM/HKCR ejecuta como Administrador")


if __name__ == "__main__":
    if sys.platform != "win32":
        print("Este launcher está diseñado para Windows porque usa el Registro de Windows.")
    app = WC3LauncherApp()
    app.mainloop()
