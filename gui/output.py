import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk

import gui
from db import conn
from helper.line_type import LineType

_overframe: ttk.Frame | None = None
_left_hex_canvas: tk.Canvas | None = None
_right_hex_canvas: tk.Canvas | None = None

_left_number_label: ttk.Label | None = None
_left_name_label: ttk.Label | None = None
_right_number_label: ttk.Label | None = None
_right_name_label: ttk.Label | None = None

_HEX_CANVAS_WIDTH = 340
_HEX_CANVAS_HEIGHT = 350
_HEX_LINE_MARGIN = (_HEX_CANVAS_WIDTH - 200) // 2

# Frozen at build() time and used for all drawing math below, rather than reading
# gui.scaled()/gui.scale live. The canvases are sized once, at build() time; if a
# resolution change later moves the global scale, redoing this module's own
# coordinate math against the new scale would draw outside the (unresized) canvas.
_scale = 1.0


def _s(value: float) -> int:
    return round(value * _scale)


def _max_word_width(font: tkfont.Font, extra_words: list[str]) -> int:
    words = [word for name in conn.all_names() for word in name.split()] + extra_words
    return max(font.measure(word) for word in words)


def build():
    global _overframe, _left_hex_canvas, _right_hex_canvas
    global _left_number_label, _left_name_label, _right_number_label, _right_name_label
    global _scale

    _scale = gui.scale
    s = _s

    _overframe = ttk.Frame(gui.root, borderwidth=5)
    _overframe.pack(side=tk.BOTTOM, fill=tk.BOTH, padx=s(20), pady=s(20))

    hex_frame = ttk.Frame(_overframe, borderwidth=5, relief='sunken')
    hex_frame.pack(side=tk.TOP)

    info_frame = ttk.Frame(_overframe, borderwidth=5, relief='raised')
    info_frame.pack(side=tk.BOTTOM, fill=tk.BOTH)

    _left_hex_canvas = tk.Canvas(hex_frame, width=s(_HEX_CANVAS_WIDTH), height=s(_HEX_CANVAS_HEIGHT))
    _left_hex_canvas.pack(side=tk.LEFT)

    _right_hex_canvas = tk.Canvas(hex_frame, width=s(_HEX_CANVAS_WIDTH), height=s(_HEX_CANVAS_HEIGHT))
    _right_hex_canvas.pack(side=tk.RIGHT)

    number_font = tkfont.Font(family='TkDefaultFont', size=s(15))
    name_font = tkfont.Font(family='TkDefaultFont', size=s(20))

    # wraplength is derived from the widest word actually measured in the current
    # (already-scaled) font, rather than a guessed pixel value, since font metrics
    # vary a lot between systems (DPI scaling can more than double glyph widths).
    number_wrap = _max_word_width(number_font, ['No', 'changing', 'lines']) + s(20)
    name_wrap = _max_word_width(name_font, []) + s(20)

    left_info_frame = ttk.Frame(info_frame)
    left_info_frame.pack(side=tk.LEFT, expand=True, padx=s(10), pady=s(10))

    right_info_frame = ttk.Frame(info_frame)
    right_info_frame.pack(side=tk.RIGHT, expand=True, padx=s(10), pady=s(10))

    _left_number_label = ttk.Label(
        left_info_frame, font=number_font, justify=tk.CENTER, anchor=tk.CENTER, wraplength=number_wrap,
    )
    _left_number_label.pack(side=tk.TOP, pady=s(5))

    _left_name_label = ttk.Label(
        left_info_frame, font=name_font, justify=tk.CENTER, anchor=tk.CENTER, wraplength=name_wrap,
    )
    _left_name_label.pack(side=tk.TOP)

    _right_number_label = ttk.Label(
        right_info_frame, font=number_font, justify=tk.CENTER, anchor=tk.CENTER, wraplength=number_wrap,
    )
    _right_number_label.pack(side=tk.TOP, pady=s(5))

    _right_name_label = ttk.Label(
        right_info_frame, font=name_font, justify=tk.CENTER, anchor=tk.CENTER, wraplength=name_wrap,
    )
    _right_name_label.pack(side=tk.TOP)

    _register_worst_case_height()


def destroy():
    _overframe.destroy()


def _register_worst_case_height() -> None:
    """Probe the tallest a toss result can make the info panels, so the root window
    can be sized for it up front (see gui.register_min_height for why this can't
    just happen reactively once real results are drawn).
    """
    worst_name = max(conn.all_names(), key=len)
    for label in (_left_number_label, _right_number_label):
        label.config(text='No changing lines')
    for label in (_left_name_label, _right_name_label):
        label.config(text=worst_name)

    gui.root.update_idletasks()
    gui.register_min_height(gui.root.winfo_reqheight())

    for label in (_left_number_label, _left_name_label, _right_number_label, _right_name_label):
        label.config(text='')


def _left_line_coordinates(count: int) -> tuple[int, int, int, int]:
    x0, x1 = _s(_HEX_LINE_MARGIN), _s(_HEX_CANVAS_WIDTH - _HEX_LINE_MARGIN)
    y0 = y1 = _s(300 - count * 50)
    return x0, y0, x1, y1


def draw_line_left(count: int, line: LineType):
    x0, y0, x1, y1 = _left_line_coordinates(count)
    is_broken = line in (LineType.OLD_YIN, LineType.YOUNG_YIN)
    is_changing = line in (LineType.OLD_YIN, LineType.OLD_YANG)

    kwargs = {'width': _s(20)}
    if is_broken:
        kwargs['dash'] = (_s(80), _s(40))
    if is_changing:
        kwargs['fill'] = 'red'

    _left_hex_canvas.create_line((x0, y0), (x1, y1), **kwargs)


def draw_reverse_hex(reverse_binary: list):
    x0, x1 = _s(_HEX_LINE_MARGIN), _s(_HEX_CANVAS_WIDTH - _HEX_LINE_MARGIN)
    y0 = y1 = _s(50)
    step = _s(50)

    for bit_char in reverse_binary:
        kwargs = {'width': _s(20)}
        if bit_char != '1':
            kwargs['dash'] = (_s(80), _s(40))

        _right_hex_canvas.create_line((x0, y0), (x1, y1), **kwargs)
        y0 += step
        y1 += step


def draw_true_info(true_hex: tuple):
    number, name = true_hex[0], true_hex[1]
    _left_number_label.config(text='#' + number)
    _left_name_label.config(text=name)


def draw_reverse_info(reverse_hex: tuple):
    number, name = reverse_hex[0], reverse_hex[1]
    _right_number_label.config(text='#' + number)
    _right_name_label.config(text=name)


def draw_no_change():
    _right_number_label.config(text='No changing lines')


def canvas_reset():
    _left_hex_canvas.delete('all')
    _right_hex_canvas.delete('all')
    _left_number_label.config(text='')
    _left_name_label.config(text='')
    _right_number_label.config(text='')
    _right_name_label.config(text='')
