from tkinter import ttk
from typing import NamedTuple

from gui import settings


class Palette(NamedTuple):
    bg: str
    surface: str
    tab_unselected: str
    ink: str
    ink_muted: str
    accent: str
    border: str
    name_font_family: str


THEMES: dict[str, Palette] = {
    'Parchment': Palette(
        bg='#f2ece0', surface='#f8f4ea', tab_unselected='#e7e0cd',
        ink='#2b2620', ink_muted='#6f6659', accent='#a8402e', border='#d9cfba',
        name_font_family='DejaVu Serif',
    ),
    'Midnight': Palette(
        bg='#1b1917', surface='#242220', tab_unselected='#302c27',
        ink='#e9e2d3', ink_muted='#9c9284', accent='#d68a3c', border='#3a352f',
        name_font_family='DejaVu Serif',
    ),
    'Jade': Palette(
        bg='#eef1ea', surface='#f7f9f4', tab_unselected='#dde3d4',
        ink='#24332a', ink_muted='#66766c', accent='#b0483a', border='#cdd6c3',
        name_font_family='DejaVu Serif',
    ),
    'Slate': Palette(
        bg='#eceef1', surface='#f7f8fa', tab_unselected='#dbdfe5',
        ink='#23272e', ink_muted='#636973', accent='#b1432f', border='#ccd0d6',
        name_font_family='TkDefaultFont',
    ),
    'Sumi-e': Palette(
        bg='#f7f7f5', surface='#ffffff', tab_unselected='#e3e3e0',
        ink='#111111', ink_muted='#6e6e6b', accent='#a8402e', border='#d5d5d0',
        name_font_family='DejaVu Serif',
    ),
}

DEFAULT_THEME = 'Parchment'

_current = DEFAULT_THEME


def load_saved() -> None:
    """Restore the last-selected theme from disk. Call once at startup."""
    global _current
    name = settings.load_theme_name()
    _current = name if name in THEMES else DEFAULT_THEME


def current_name() -> str:
    return _current


def current() -> Palette:
    return THEMES[_current]


def set_current(name: str) -> None:
    global _current
    _current = name
    settings.save_theme_name(name)


def apply(root) -> None:
    palette = current()
    root.configure(bg=palette.bg)

    style = ttk.Style()
    style.theme_use('clam')

    style.configure('.', background=palette.bg, foreground=palette.ink)
    style.configure('TFrame', background=palette.bg)
    style.configure('TLabel', background=palette.bg, foreground=palette.ink)
    style.configure(
        'TButton', background=palette.surface, foreground=palette.ink,
        bordercolor=palette.border, focuscolor=palette.border,
    )
    style.map(
        'TButton',
        background=[('active', palette.bg), ('disabled', palette.bg)],
        foreground=[('disabled', palette.ink_muted)],
    )
    style.configure('TNotebook', background=palette.bg, bordercolor=palette.border)
    style.configure(
        'TNotebook.Tab', background=palette.tab_unselected, foreground=palette.ink_muted, padding=(12, 6),
    )
    style.map(
        'TNotebook.Tab',
        background=[('selected', palette.surface)],
        foreground=[('selected', palette.ink)],
    )

    root.option_add('*Menu.background', palette.surface)
    root.option_add('*Menu.foreground', palette.ink)
    root.option_add('*Menu.activeBackground', palette.bg)
    root.option_add('*Menu.activeForeground', palette.ink)


def style_menu(menu) -> None:
    """Color a single tk.Menu (bar or cascade) to the current theme.

    The *option_add calls in apply() only affect menus created afterward - Tk's
    option database doesn't retroactively restyle a menu that already exists,
    and the app's menu bar is built once at startup, not recreated on a theme
    change. Callers that keep a menu alive across a theme switch need to
    re-call this directly on it.
    """
    palette = current()
    menu.configure(
        bg=palette.surface, fg=palette.ink,
        activebackground=palette.bg, activeforeground=palette.ink,
    )
