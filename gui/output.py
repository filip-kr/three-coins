import tkinter as tk
from tkinter import font as tkfont
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

# Fixed regardless of content - see build()'s pack_propagate(False) - rather
# than measured/probed from hexagram text, so nothing in a tab (including the
# hex lines) ever shifts position or size once a result is drawn in.
_TAB_CONTENT_HEIGHT = 660

# Frozen at build() time and used for all drawing math below, rather than reading
# gui.scaled()/gui.scale live. The canvases are sized once, at build() time; if a
# resolution change later moves the global scale, redoing this module's own
# coordinate math against the new scale would draw outside the (unresized) canvas.
_scale = 1.0


def _s(value: float) -> int:
    return round(value * _scale)


def _sentence_case(text: str) -> str:
    return text[0] + text[1:].lower() if text else text


def _split_name(name: str) -> tuple[str, str]:
    """Hexagram names are often compound phrases - a plain word/phrase, a
    parenthetical qualifier ("Abundance (Expansion of Awareness)"), or a
    slash-joined list ("Enthusiasm/Self-Deception/Repose"). Split into a short
    primary term and an optional subtitle instead of wrapping the whole thing
    as one run of text.
    """
    if '(' in name:
        primary, _, rest = name.partition('(')
        return primary.strip(), _sentence_case(rest.rstrip(')').strip())
    if '/' in name:
        parts = [part.strip() for part in name.split('/')]
        return parts[0], ' · '.join(_sentence_case(part) for part in parts[1:])
    return name, ''


def _build_tab(width: int, height: int) -> ttk.Frame:
    tab = ttk.Frame(_notebook, width=width, height=height)
    # Without this, the frame would grow/shrink to fit whatever text is later
    # placed in its labels - pack_propagate(False) pins it to the given size
    # regardless, which is what makes the layout (and the hex lines within it)
    # stay fixed in place no matter how long or short a hexagram name turns out.
    tab.pack_propagate(False)
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
    # width is in characters, not pixels, but it still pins the tab to a fixed
    # size regardless of the actual text length - without it, a tab visibly
    # grows/shrinks as its title goes from empty to a 1- or 2-digit number.
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
    # Not switchable until its hexagram is actually ready - see draw_reverse_info
    # and draw_no_change, which re-enable it once there's something to show.
    _notebook.tab(_reverse_tab, state=tk.DISABLED)

    gui.root.update_idletasks()
    gui.register_min_height(gui.root.winfo_reqheight())


def destroy():
    _overframe.destroy()


def _left_line_coordinates(count: int) -> tuple[int, int, int, int]:
    x0, x1 = _s(_HEX_LINE_MARGIN), _s(_HEX_CANVAS_WIDTH - _HEX_LINE_MARGIN)
    y0 = y1 = _s(300 - count * 50)
    return x0, y0, x1, y1


def _draw_hex_line(canvas: tk.Canvas, count: int, line: LineType) -> None:
    x0, y0, x1, y1 = _left_line_coordinates(count)
    is_broken = line in (LineType.OLD_YIN, LineType.YOUNG_YIN)
    is_changing = line in (LineType.OLD_YIN, LineType.OLD_YANG)

    palette = theme.current()
    kwargs = {'width': _s(_HEX_LINE_WIDTH), 'fill': palette.accent if is_changing else palette.ink}
    if is_broken:
        kwargs['dash'] = (_s(80), _s(40))

    canvas.create_line((x0, y0), (x1, y1), **kwargs)


def draw_line_left(count: int, line: LineType):
    _draw_hex_line(_true_hex_canvas, count, line)


def draw_reverse_hex(reverse_binary: list):
    x0, x1 = _s(_HEX_LINE_MARGIN), _s(_HEX_CANVAS_WIDTH - _HEX_LINE_MARGIN)
    y0 = y1 = _s(50)
    step = _s(50)
    ink = theme.current().ink

    for bit_char in reverse_binary:
        kwargs = {'width': _s(_HEX_LINE_WIDTH), 'fill': ink}
        if bit_char != '1':
            kwargs['dash'] = (_s(80), _s(40))

        _reverse_hex_canvas.create_line((x0, y0), (x1, y1), **kwargs)
        y0 += step
        y1 += step


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
    """No reverse hexagram to show, so mirror the true tab onto the reverse tab
    instead of leaving it empty."""
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
