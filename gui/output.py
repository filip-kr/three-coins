import tkinter as tk
from tkinter import ttk

from gui import root
from helper.line_type import LineType

_left_hex_canvas: tk.Canvas | None = None
_right_hex_canvas: tk.Canvas | None = None
_left_info_canvas: tk.Canvas | None = None
_right_info_canvas: tk.Canvas | None = None


def build():
    global _left_hex_canvas, _right_hex_canvas, _left_info_canvas, _right_info_canvas

    overframe = ttk.Frame(root, borderwidth=5)
    overframe.pack(side=tk.BOTTOM, fill=tk.BOTH, padx=20, pady=20)

    hex_frame = ttk.Frame(root, borderwidth=5, relief='sunken')
    hex_frame.pack(in_=overframe, side=tk.TOP)

    info_frame = ttk.Frame(root, borderwidth=5, relief='raised')
    info_frame.pack(in_=overframe, side=tk.BOTTOM, fill=tk.BOTH)

    _left_hex_canvas = tk.Canvas(root, height=350)
    _left_hex_canvas.pack(in_=hex_frame, side=tk.LEFT)

    _right_hex_canvas = tk.Canvas(root, height=350)
    _right_hex_canvas.pack(in_=hex_frame, side=tk.RIGHT)

    _left_info_canvas = tk.Canvas(root)
    _left_info_canvas.pack(in_=info_frame, side=tk.LEFT)

    _right_info_canvas = tk.Canvas(root)
    _right_info_canvas.pack(in_=info_frame, side=tk.RIGHT)


def _left_line_coordinates(count: int) -> tuple[int, int, int, int]:
    x0, x1 = 50, 250
    y0 = y1 = 300 - count * 50
    return x0, y0, x1, y1


def draw_line_left(count: int, line: LineType):
    x0, y0, x1, y1 = _left_line_coordinates(count)
    is_broken = line in (LineType.OLD_YIN, LineType.YOUNG_YIN)
    is_changing = line in (LineType.OLD_YIN, LineType.OLD_YANG)

    kwargs = {'width': 20}
    if is_broken:
        kwargs['dash'] = (80, 40)
    if is_changing:
        kwargs['fill'] = 'red'

    _left_hex_canvas.create_line((x0, y0), (x1, y1), **kwargs)


def draw_reverse_hex(reverse_binary: list):
    x0, y0, x1, y1 = 110, 50, 310, 50

    for bit_char in reverse_binary:
        kwargs = {'width': 20}
        if bit_char != '1':
            kwargs['dash'] = (80, 40)

        _right_hex_canvas.create_line((x0, y0), (x1, y1), **kwargs)
        y0 += 50
        y1 += 50


def _draw_hex_info(canvas: tk.Canvas, hex_data: tuple, x: int):
    number = '#' + hex_data[0]
    name = hex_data[1]

    canvas.create_text((x, 50), text=number, font=('TkDefaultFont', 15))
    canvas.create_text((x, 100), text=name, font=('TkDefaultFont', 20))


def draw_true_info(true_hex: tuple):
    _draw_hex_info(_left_info_canvas, true_hex, 140)


def draw_reverse_info(reverse_hex: tuple):
    _draw_hex_info(_right_info_canvas, reverse_hex, 200)


def draw_no_change():
    _right_info_canvas.create_text((210, 50), text='No changing lines', font=('TkDefaultFont', 15))


def canvas_reset():
    _left_hex_canvas.delete('all')
    _right_hex_canvas.delete('all')
    _left_info_canvas.delete('all')
    _right_info_canvas.delete('all')
