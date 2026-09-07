import tkinter as tk
from tkinter import ttk

import gui
from gui import theme
from helper.line_type import LineType

_overframe: ttk.Frame | None = None
_notebook: ttk.Notebook | None = None
_true_tab: ttk.Frame | None = None
_reverse_tab: ttk.Frame | None = None

_true_hex_canvas: tk.Canvas | None = None
_reverse_hex_canvas: tk.Canvas | None = None
_true_caption_label: ttk.Label | None = None
_true_name_label: ttk.Label | None = None
_true_subtitle_label: ttk.Label | None = None
_reverse_caption_label: ttk.Label | None = None
_reverse_name_label: ttk.Label | None = None
_reverse_subtitle_label: ttk.Label | None = None

_HEX_CANVAS_WIDTH = 340
_HEX_CANVAS_HEIGHT = 350
_HEX_LINE_MARGIN = (_HEX_CANVAS_WIDTH - 200) // 2
_HEX_LINE_WIDTH = 14

# Fixed, not measured from content, so tab contents never shift on a redraw.
_TAB_CONTENT_HEIGHT = 660

# Frozen at build() time: canvases are sized once, so later drawing math must use
# the same scale they were built with, not a since-changed gui.scale.
_scale = 1.0


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


def _build_tab(width: int, height: int) -> ttk.Frame:
    tab = ttk.Frame(_notebook, width=width, height=height)
    tab.pack_propagate(False)  # hold (width, height); don't shrink to fit labels
    return tab


def _build_tab_content(tab: ttk.Frame, wrap: int) -> tuple[tk.Canvas, ttk.Label, ttk.Label, ttk.Label]:
    s = _s

    canvas = tk.Canvas(
        tab, width=s(_HEX_CANVAS_WIDTH), height=s(_HEX_CANVAS_HEIGHT),
        bg=theme.current().surface, highlightthickness=0, bd=0,
    )
    canvas.pack(side=tk.TOP, pady=(s(20), s(16)))

    caption = ttk.Label(tab, style='Caption.TLabel', justify=tk.CENTER, anchor=tk.CENTER)
    caption.pack(side=tk.TOP)

    name = ttk.Label(tab, style='Name.TLabel', justify=tk.CENTER, anchor=tk.CENTER, wraplength=wrap)
    name.pack(side=tk.TOP, pady=(s(4), 0))

    subtitle = ttk.Label(tab, style='Subtitle.TLabel', justify=tk.CENTER, anchor=tk.CENTER, wraplength=wrap)
    subtitle.pack(side=tk.TOP)

    return canvas, caption, name, subtitle


def build():
    global _overframe, _notebook, _true_tab, _reverse_tab, _true_hex_canvas, _reverse_hex_canvas
    global _true_caption_label, _true_name_label, _true_subtitle_label
    global _reverse_caption_label, _reverse_name_label, _reverse_subtitle_label
    global _scale

    _scale = gui.scale
    s = _s

    _overframe = ttk.Frame(gui.root)
    _overframe.pack(side=tk.TOP, fill=tk.BOTH, padx=s(20), pady=s(20))

    palette = theme.current()
    style = ttk.Style()
    # width is in characters: a fixed 3 stops the tab resizing as its number changes.
    style.configure('TNotebook.Tab', font=('TkDefaultFont', s(14)), width=3, anchor='center')
    style.configure(
        'Caption.TLabel', font=('TkDefaultFont', s(11)), foreground=palette.ink_muted, background=palette.bg,
    )
    style.configure(
        'Name.TLabel', font=(palette.name_font_family, s(22)), foreground=palette.ink, background=palette.bg,
    )
    style.configure(
        'Subtitle.TLabel', font=('TkDefaultFont', s(13)), foreground=palette.ink_muted, background=palette.bg,
    )

    _notebook = ttk.Notebook(_overframe)
    _notebook.pack()

    tab_width = gui.target_width() - s(80)
    tab_height = s(_TAB_CONTENT_HEIGHT)
    wrap = tab_width - s(40)

    _true_tab = _build_tab(tab_width, tab_height)
    _notebook.add(_true_tab, text='')
    _true_hex_canvas, _true_caption_label, _true_name_label, _true_subtitle_label = _build_tab_content(
        _true_tab, wrap,
    )

    _reverse_tab = _build_tab(tab_width, tab_height)
    _notebook.add(_reverse_tab, text='')
    _reverse_hex_canvas, _reverse_caption_label, _reverse_name_label, _reverse_subtitle_label = _build_tab_content(
        _reverse_tab, wrap,
    )
    _notebook.tab(_reverse_tab, state=tk.DISABLED)

    gui.root.update_idletasks()
    gui.register_min_height(gui.root.winfo_reqheight())


def destroy():
    _overframe.destroy()


_LINE_SPACING = 50
_TOP_LINE_Y = 50


def _line_y(position_from_top: int) -> int:
    return _s(_TOP_LINE_Y + position_from_top * _LINE_SPACING)


def _line_x_bounds() -> tuple[int, int]:
    return _s(_HEX_LINE_MARGIN), _s(_HEX_CANVAS_WIDTH - _HEX_LINE_MARGIN)


def _draw_line(canvas: tk.Canvas, position_from_top: int, *, broken: bool, accent: bool = False) -> None:
    x0, x1 = _line_x_bounds()
    y = _line_y(position_from_top)

    palette = theme.current()
    kwargs = {'width': _s(_HEX_LINE_WIDTH), 'fill': palette.accent if accent else palette.ink}
    if broken:
        kwargs['dash'] = (_s(80), _s(40))

    canvas.create_line((x0, y), (x1, y), **kwargs)


def _draw_hex_line(canvas: tk.Canvas, count: int, line: LineType) -> None:
    is_broken = line in (LineType.STRESSED_MAGNETIC, LineType.MAGNETIC)
    is_stressed = line in (LineType.STRESSED_MAGNETIC, LineType.STRESSED_DYNAMIC)
    # count is toss order (0 = bottom/first toss); lines are drawn bottom-up.
    _draw_line(canvas, 5 - count, broken=is_broken, accent=is_stressed)


def draw_line_left(count: int, line: LineType):
    _draw_hex_line(_true_hex_canvas, count, line)


def draw_reverse_hex(reverse_binary: list):
    for position, bit_char in enumerate(reverse_binary):
        _draw_line(_reverse_hex_canvas, position, broken=(bit_char != '1'))


def _apply_hex_info(tab: ttk.Frame, caption: ttk.Label, name: ttk.Label, subtitle: ttk.Label, hex_data: tuple):
    number, full_name = hex_data[0], hex_data[1]
    primary, sub = _split_name(full_name)
    _notebook.tab(tab, text=number, state=tk.NORMAL)
    caption.config(text=f'HEXAGRAM {number}')
    name.config(text=primary)
    subtitle.config(text=sub)


def draw_true_info(true_hex: tuple):
    _apply_hex_info(_true_tab, _true_caption_label, _true_name_label, _true_subtitle_label, true_hex)


def draw_reverse_info(reverse_hex: tuple):
    _apply_hex_info(_reverse_tab, _reverse_caption_label, _reverse_name_label, _reverse_subtitle_label, reverse_hex)


def draw_no_change(true_hex: tuple, lines: list[LineType]):
    """No changing lines, so there's no distinct reverse hexagram - mirror the
    true tab onto the reverse tab rather than leave it blank."""
    for count, line in enumerate(lines):
        _draw_hex_line(_reverse_hex_canvas, count, line)

    _apply_hex_info(_reverse_tab, _reverse_caption_label, _reverse_name_label, _reverse_subtitle_label, true_hex)


def canvas_reset():
    _true_hex_canvas.delete('all')
    _reverse_hex_canvas.delete('all')
    for tab, caption, name, subtitle in (
        (_true_tab, _true_caption_label, _true_name_label, _true_subtitle_label),
        (_reverse_tab, _reverse_caption_label, _reverse_name_label, _reverse_subtitle_label),
    ):
        _notebook.tab(tab, text='')
        caption.config(text='')
        name.config(text='')
        subtitle.config(text='')
    _notebook.select(_true_tab)
    _notebook.tab(_reverse_tab, state=tk.DISABLED)
