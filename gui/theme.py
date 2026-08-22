BG = '#f2ece0'
SURFACE = '#f8f4ea'
TAB_UNSELECTED = '#e7e0cd'
INK = '#2b2620'
INK_MUTED = '#6f6659'
ACCENT = '#a8402e'
BORDER = '#d9cfba'

NAME_FONT_FAMILY = 'DejaVu Serif'


def apply(root) -> None:
    import tkinter as tk
    from tkinter import ttk

    root.configure(bg=BG)

    style = ttk.Style()
    style.theme_use('clam')

    style.configure('.', background=BG, foreground=INK)
    style.configure('TFrame', background=BG)
    style.configure('TLabel', background=BG, foreground=INK)
    style.configure('TButton', background=SURFACE, foreground=INK, bordercolor=BORDER, focuscolor=BORDER)
    style.map(
        'TButton',
        background=[('active', BG), ('disabled', BG)],
        foreground=[('disabled', INK_MUTED)],
    )
    style.configure('TNotebook', background=BG, bordercolor=BORDER)
    style.configure(
        'TNotebook.Tab', background=TAB_UNSELECTED, foreground=INK_MUTED, padding=(12, 6),
    )
    style.map(
        'TNotebook.Tab',
        background=[('selected', SURFACE)],
        foreground=[('selected', INK)],
    )

    root.option_add('*Menu.background', SURFACE)
    root.option_add('*Menu.foreground', INK)
    root.option_add('*Menu.activeBackground', BG)
    root.option_add('*Menu.activeForeground', INK)
