ORC = {
    'bg': '#050c07',
    'panel': '#0e1c12',
    'panel2': '#17281a',
    'panel3': '#223319',
    'green': '#45f06a',
    'green2': '#1e8e3e',
    'green3': '#0f5f2e',
    'gold': '#d8a64a',
    'gold2': '#f1c76b',
    'red': '#b93131',
    'text': '#e8f4df',
    'muted': '#a8bfa5',
    'entry': '#07110a',
}

def apply_style(root):
    import tkinter as tk
    from tkinter import ttk
    root.configure(bg=ORC['bg'])
    style = ttk.Style(root)
    try:
        style.theme_use('clam')
    except Exception:
        pass
    style.configure('.', background=ORC['bg'], foreground=ORC['text'], fieldbackground=ORC['entry'], font=('Segoe UI', 9))
    style.configure('TFrame', background=ORC['bg'])
    style.configure('Panel.TFrame', background=ORC['panel'], relief='flat')
    style.configure('TLabel', background=ORC['bg'], foreground=ORC['text'])
    style.configure('Muted.TLabel', background=ORC['bg'], foreground=ORC['muted'])
    style.configure('Title.TLabel', background=ORC['bg'], foreground=ORC['gold2'], font=('Segoe UI Black', 15))
    style.configure('Header.TLabel', background=ORC['panel'], foreground=ORC['gold'], font=('Segoe UI Semibold', 10))

    style.configure('TLabelFrame', background=ORC['bg'], foreground=ORC['gold'], bordercolor=ORC['green3'], lightcolor=ORC['green3'], darkcolor=ORC['panel'])
    style.configure('TLabelFrame.Label', background=ORC['bg'], foreground=ORC['gold2'], font=('Segoe UI Semibold', 9))

    style.configure('TButton', background=ORC['green2'], foreground='white', borderwidth=1, focusthickness=2, focuscolor=ORC['gold'], padding=(9, 5), font=('Segoe UI Semibold', 9))
    style.map('TButton', background=[('active', ORC['green']), ('pressed', ORC['gold'])], foreground=[('pressed', '#111')])
    style.configure('Danger.TButton', background=ORC['red'], foreground='white')
    style.configure('Gold.TButton', background=ORC['gold'], foreground='#111', font=('Segoe UI Black', 10))
    style.map('Gold.TButton', background=[('active', ORC['gold2']), ('pressed', ORC['green'])])

    style.configure('TCheckbutton', background=ORC['bg'], foreground=ORC['text'])
    style.map('TCheckbutton', background=[('active', ORC['panel2'])], foreground=[('active', ORC['gold2'])])
    style.configure('TRadiobutton', background=ORC['bg'], foreground=ORC['text'])
    style.map('TRadiobutton', background=[('active', ORC['panel2'])], foreground=[('active', ORC['gold2'])])

    style.configure('TEntry', fieldbackground=ORC['entry'], foreground=ORC['text'], insertcolor=ORC['gold'])
    style.configure('TCombobox', fieldbackground=ORC['entry'], background=ORC['panel2'], foreground=ORC['text'], arrowcolor=ORC['gold'])
    style.configure('TNotebook', background=ORC['bg'], borderwidth=0)
    style.configure('TNotebook.Tab', background=ORC['panel2'], foreground=ORC['text'], padding=(12, 5), font=('Segoe UI Semibold', 9))
    style.map('TNotebook.Tab', background=[('selected', ORC['green2']), ('active', ORC['panel3'])], foreground=[('selected', '#fff'), ('active', ORC['gold2'])])
    style.configure('Treeview', background=ORC['entry'], foreground=ORC['text'], fieldbackground=ORC['entry'], rowheight=23)
    style.configure('Treeview.Heading', background=ORC['panel2'], foreground=ORC['gold'], font=('Segoe UI Semibold', 9))
