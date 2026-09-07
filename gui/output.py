import tkinter as tk
from tkinter import ttk
from typing import NamedTuple

import gui
from gui import background, linestyle, theme
from helper.line_type import LineType


class _Tab(NamedTuple):
    frame: ttk.Frame
    canvas: tk.Canvas
    caption: ttk.Label
    name: ttk.Label
    subtitle: ttk.Label


_overframe: ttk.Frame | None = None
_notebook: ttk.Notebook | None = None
_tabs: dict[str, _Tab] = {}

# Per side, [(position_from_top, broken, accent), ...] shadowing what's drawn, so
# redraw_lines() can repaint it in a new line style without the session.
_lines: dict[str, list] = {'true': [], 'reverse': []}

# Frozen at build() time: canvases are sized once, so later drawing math must use
# the scale they were built with, not a since-changed gui.scale.
_scale = 1.0

# Geometry in unscaled px; run through _s() at draw time.
_HEX_CANVAS_WIDTH = 340
_HEX_CANVAS_HEIGHT = 350
_HEX_LINE_SPAN = 200
_HEX_LINE_MARGIN = (_HEX_CANVAS_WIDTH - _HEX_LINE_SPAN) // 2
_HEX_LINE_WIDTH = 14
_LINE_SPACING = 50
_TOP_LINE_Y = 50
_HEX_TOP_PAD = 115  # gap above the frame; see _build_tab_content

# Fixed, not measured from content, so tab contents never shift on a redraw.
_TAB_CONTENT_HEIGHT = 660


def _s(value: float) -> int:
    return round(value * _scale)


def _sentence_case(text: str) -> str:
    return text[0] + text[1:].lower() if text else text


def _split_name(name: str) -> tuple[str, str]:
    """Split a compound hexagram name into a primary term and an optional
    subtitle: "Abundance (Expansion of Awareness)" or "Enthusiasm/Self-Deception"
    become (primary, subtitle) rather than one long wrapped line."""
    if '(' in name:
        primary, _, rest = name.partition('(')
        return primary.strip(), _sentence_case(rest.rstrip(')').strip())
    if '/' in name:
        parts = [part.strip() for part in name.split('/')]
        return parts[0], ' · '.join(_sentence_case(part) for part in parts[1:])
    return name, ''


def _style_labels() -> None:
    palette = theme.current()
    style = ttk.Style()
    style.configure('Caption.TLabel', font=('TkDefaultFont', _s(11)),
                    foreground=palette.ink_muted, background=palette.bg)
    style.configure('Name.TLabel', font=(palette.name_font_family, _s(18)),
                    foreground=palette.ink, background=palette.bg)
    style.configure('Subtitle.TLabel', font=('TkDefaultFont', _s(13)),
                    foreground=palette.ink_muted, background=palette.bg)


def _build_tab(width: int, height: int) -> ttk.Frame:
    frame = ttk.Frame(_notebook, width=width, height=height)
    frame.pack_propagate(False)  # hold (width, height); don't shrink to fit the content
    return frame


def _build_tab_content(frame: ttk.Frame, wrap: int) -> _Tab:
    palette = theme.current()

    # Everything packs top-down in the fixed-size frame: the canvas sits at a
    # fixed offset and a long (wrapped) name grows downward without nudging it.
    canvas = tk.Canvas(frame, width=_s(_HEX_CANVAS_WIDTH), height=_s(_HEX_CANVAS_HEIGHT),
                       bg=palette.surface, bd=0, highlightthickness=_s(1),
                       highlightbackground=palette.ink_muted, highlightcolor=palette.ink_muted)
    canvas.pack(side=tk.TOP, pady=(_s(_HEX_TOP_PAD), _s(16)))
    background.draw(canvas, palette)

    caption = ttk.Label(frame, style='Caption.TLabel', justify=tk.CENTER, anchor=tk.CENTER)
    caption.pack(side=tk.TOP)

    name = ttk.Label(frame, style='Name.TLabel', justify=tk.CENTER, anchor=tk.CENTER, wraplength=wrap)
    name.pack(side=tk.TOP, pady=(_s(4), 0))

    subtitle = ttk.Label(frame, style='Subtitle.TLabel', justify=tk.CENTER, anchor=tk.CENTER, wraplength=wrap)
    subtitle.pack(side=tk.TOP)

    return _Tab(frame, canvas, caption, name, subtitle)


def build():
    global _overframe, _notebook, _scale

    _scale = gui.scale
    s = _s
    _lines['true'].clear()
    _lines['reverse'].clear()
    _tabs.clear()

    _overframe = ttk.Frame(gui.root)
    _overframe.pack(side=tk.TOP, fill=tk.BOTH, padx=s(20), pady=s(20))

    # width is in characters: a fixed 3 stops the tab resizing as its number changes.
    ttk.Style().configure('TNotebook.Tab', font=('TkDefaultFont', s(14)), width=3, anchor='center')
    _style_labels()

    _notebook = ttk.Notebook(_overframe)
    _notebook.pack()

    tab_width = gui.target_width() - s(80)
    tab_height = s(_TAB_CONTENT_HEIGHT)
    wrap = tab_width - s(40)  # wide: real hexagram names then fit on one line

    for side in ('true', 'reverse'):
        frame = _build_tab(tab_width, tab_height)
        _notebook.add(frame, text='')
        _tabs[side] = _build_tab_content(frame, wrap)
    _notebook.tab(_tabs['reverse'].frame, state=tk.DISABLED)

    gui.root.update_idletasks()
    gui.register_min_height(gui.root.winfo_reqheight())


def destroy():
    _overframe.destroy()


def redraw_background() -> None:
    for tab in _tabs.values():
        background.draw(tab.canvas, theme.current())


def restyle() -> None:
    """Recolor the built widgets to the current palette in place (theme preview)."""
    palette = theme.current()
    _style_labels()
    for tab in _tabs.values():
        tab.canvas.configure(bg=palette.surface, highlightbackground=palette.ink_muted,
                             highlightcolor=palette.ink_muted)
        tab.canvas.itemconfigure('ink', fill=palette.ink)
        tab.canvas.itemconfigure('accent', fill=palette.accent)
        background.draw(tab.canvas, palette)


def _line_y(position_from_top: int) -> int:
    return _s(_TOP_LINE_Y + position_from_top * _LINE_SPACING)


def _line_x_bounds() -> tuple[int, int]:
    return _s(_HEX_LINE_MARGIN), _s(_HEX_CANVAS_WIDTH - _HEX_LINE_MARGIN)


def _paint_line(canvas: tk.Canvas, position_from_top: int, broken: bool, accent: bool) -> None:
    x0, x1 = _line_x_bounds()
    palette = theme.current()
    linestyle.draw(
        canvas, x0, x1, _line_y(position_from_top), _s(_HEX_LINE_WIDTH),
        broken=broken, color=palette.accent if accent else palette.ink,
        tags=('line', 'accent') if accent else ('line', 'ink'),  # 'line' clears, colour tag restyles
    )


def _add_line(side: str, position_from_top: int, *, broken: bool, accent: bool = False) -> None:
    _lines[side].append((position_from_top, broken, accent))
    _paint_line(_tabs[side].canvas, position_from_top, broken, accent)


def redraw_lines() -> None:
    for side, tab in _tabs.items():
        tab.canvas.delete('line')
        for position, broken, accent in _lines[side]:
            _paint_line(tab.canvas, position, broken, accent)


def _hex_line(side: str, count: int, line: LineType) -> None:
    is_broken = line in (LineType.STRESSED_MAGNETIC, LineType.MAGNETIC)
    is_stressed = line in (LineType.STRESSED_MAGNETIC, LineType.STRESSED_DYNAMIC)
    # count is toss order (0 = bottom/first toss); lines are drawn bottom-up.
    _add_line(side, 5 - count, broken=is_broken, accent=is_stressed)


def draw_true_line(count: int, line: LineType) -> None:
    _hex_line('true', count, line)


def draw_reverse_hex(reverse_binary: list[str]) -> None:
    for position, bit_char in enumerate(reverse_binary):
        _add_line('reverse', position, broken=(bit_char != '1'))


def _apply_hex_info(side: str, hex_data: tuple) -> None:
    number, full_name = hex_data[0], hex_data[1]
    primary, sub = _split_name(full_name)
    tab = _tabs[side]
    _notebook.tab(tab.frame, text=number, state=tk.NORMAL)
    tab.caption.config(text=f'HEXAGRAM {number}')
    tab.name.config(text=primary)
    tab.subtitle.config(text=sub)


def draw_true_info(true_hex: tuple) -> None:
    _apply_hex_info('true', true_hex)


def draw_reverse_info(reverse_hex: tuple) -> None:
    _apply_hex_info('reverse', reverse_hex)


def draw_no_change(true_hex: tuple, lines: list[LineType]) -> None:
    """No changing lines, so there's no distinct reverse hexagram - mirror the
    true tab onto the reverse tab rather than leave it blank."""
    for count, line in enumerate(lines):
        _hex_line('reverse', count, line)
    _apply_hex_info('reverse', true_hex)


def canvas_reset() -> None:
    for side, tab in _tabs.items():
        _lines[side].clear()
        tab.canvas.delete('all')
        _notebook.tab(tab.frame, text='')
        for label in (tab.caption, tab.name, tab.subtitle):
            label.config(text='')
    redraw_background()
    _notebook.select(_tabs['true'].frame)
    _notebook.tab(_tabs['reverse'].frame, state=tk.DISABLED)
