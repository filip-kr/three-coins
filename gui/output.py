import tkinter as tk
from tkinter import ttk

import gui
from gui import background, linestyle, theme
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
_HEX_TOP_PAD = 115  # see _build_tab_content

# What's currently drawn on each canvas, so redraw_lines() can repaint it in a
# new line style without the session: side -> [(position_from_top, broken, accent)]
_lines: dict[str, list] = {'true': [], 'reverse': []}

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
    tab.pack_propagate(False)  # hold (width, height); don't shrink to fit the content
    return tab


def _style_labels() -> None:
    palette = theme.current()
    style = ttk.Style()
    style.configure('Caption.TLabel', font=('TkDefaultFont', _s(11)), foreground=palette.ink_muted, background=palette.bg)
    style.configure('Name.TLabel', font=(palette.name_font_family, _s(18)), foreground=palette.ink, background=palette.bg)
    style.configure('Subtitle.TLabel', font=('TkDefaultFont', _s(13)), foreground=palette.ink_muted, background=palette.bg)


def _canvases() -> tuple[tk.Canvas, tk.Canvas]:
    return _true_hex_canvas, _reverse_hex_canvas


def redraw_background() -> None:
    for canvas in _canvases():
        background.draw(canvas, theme.current())


def restyle() -> None:
    """Recolor the built widgets to the current palette in place (theme preview)."""
    palette = theme.current()
    _style_labels()
    for canvas in _canvases():
        canvas.configure(bg=palette.surface, highlightbackground=palette.ink_muted, highlightcolor=palette.ink_muted)
        canvas.itemconfigure('ink', fill=palette.ink)
        canvas.itemconfigure('accent', fill=palette.accent)
        background.draw(canvas, palette)


def _build_tab_content(tab: ttk.Frame, wrap: int) -> tuple:
    palette = theme.current()

    # Everything packs top-down in the fixed-size tab: the frame sits at a fixed
    # offset and a long (wrapped) name grows downward instead of nudging it.
    canvas = tk.Canvas(tab, width=_s(_HEX_CANVAS_WIDTH), height=_s(_HEX_CANVAS_HEIGHT),
                       bg=palette.surface, bd=0, highlightthickness=_s(1),
                       highlightbackground=palette.ink_muted, highlightcolor=palette.ink_muted)
    canvas.pack(side=tk.TOP, pady=(_s(_HEX_TOP_PAD), _s(16)))
    background.draw(canvas, palette)

    caption = ttk.Label(tab, style='Caption.TLabel', justify=tk.CENTER, anchor=tk.CENTER)
    caption.pack(side=tk.TOP)

    name = ttk.Label(tab, style='Name.TLabel', justify=tk.CENTER, anchor=tk.CENTER, wraplength=wrap)
    name.pack(side=tk.TOP, pady=(_s(4), 0))

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
    _lines['true'].clear()
    _lines['reverse'].clear()

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

    _true_tab = _build_tab(tab_width, tab_height)
    _notebook.add(_true_tab, text='')
    (_true_hex_canvas, _true_caption_label,
     _true_name_label, _true_subtitle_label) = _build_tab_content(_true_tab, wrap)

    _reverse_tab = _build_tab(tab_width, tab_height)
    _notebook.add(_reverse_tab, text='')
    (_reverse_hex_canvas, _reverse_caption_label,
     _reverse_name_label, _reverse_subtitle_label) = _build_tab_content(_reverse_tab, wrap)
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


def _side(canvas: tk.Canvas) -> str:
    return 'true' if canvas is _true_hex_canvas else 'reverse'


def _paint_line(canvas: tk.Canvas, position_from_top: int, broken: bool, accent: bool) -> None:
    x0, x1 = _line_x_bounds()
    palette = theme.current()
    linestyle.draw(
        canvas, x0, x1, _line_y(position_from_top), _s(_HEX_LINE_WIDTH),
        broken=broken, color=palette.accent if accent else palette.ink,
        tags=('line', 'accent') if accent else ('line', 'ink'),  # 'line' to clear, colour tag for restyle()
    )


def _draw_line(canvas: tk.Canvas, position_from_top: int, *, broken: bool, accent: bool = False) -> None:
    _lines[_side(canvas)].append((position_from_top, broken, accent))
    _paint_line(canvas, position_from_top, broken, accent)


def redraw_lines() -> None:
    for side, canvas in (('true', _true_hex_canvas), ('reverse', _reverse_hex_canvas)):
        canvas.delete('line')
        for position, broken, accent in _lines[side]:
            _paint_line(canvas, position, broken, accent)


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
    _lines['true'].clear()
    _lines['reverse'].clear()
    for canvas in _canvases():
        canvas.delete('all')
    redraw_background()
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
