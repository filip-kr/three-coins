from gui import root, tk, ttk

__overframe = ttk.Frame(root, borderwidth=5)
__overframe.pack(side=tk.BOTTOM, fill=tk.BOTH, padx=20, pady=20)

__hex_frame = ttk.Frame(root, borderwidth=5, relief='sunken')
__hex_frame.pack(in_=__overframe, side=tk.TOP)

__info_frame = ttk.Frame(root, borderwidth=5, relief='raised')
__info_frame.pack(in_=__overframe, side=tk.BOTTOM, fill=tk.BOTH)

__left_hex_canvas = tk.Canvas(root, height=350)
__left_hex_canvas.pack(in_=__hex_frame, side=tk.LEFT)

__right_hex_canvas = tk.Canvas(root, height=350)
__right_hex_canvas.pack(in_=__hex_frame, side=tk.RIGHT)

__left_info_canvas = tk.Canvas(root)
__left_info_canvas.pack(in_=__info_frame, side=tk.LEFT)

__right_info_canvas = tk.Canvas(root)
__right_info_canvas.pack(in_=__info_frame, side=tk.RIGHT)


def __get_left_coordinates(count: int) -> dict:
    x0 = 50
    y0 = 300
    x1 = 250
    y1 = 300

    match count:
        case 1:
            y0 -= 50
            y1 -= 50
        case 2:
            y0 -= 100
            y1 -= 100
        case 3:
            y0 -= 150
            y1 -= 150
        case 4:
            y0 -= 200
            y1 -= 200
        case 5:
            y0 -= 250
            y1 -= 250

    return {
        'x0': x0,
        'x1': x1,
        'y0': y0,
        'y1': y1
    }


def draw_line_left(count: int, coin_toss_result: int):
    coordinates = __get_left_coordinates(count)
    x0 = coordinates.get('x0')
    x1 = coordinates.get('x1')
    y0 = coordinates.get('y0')
    y1 = coordinates.get('y1')
    width = 20

    match coin_toss_result:
        case 6:
            __left_hex_canvas.create_line((x0, y0), (x1, y1), width=width, dash=(80, 40), fill='red')
        case 7:
            __left_hex_canvas.create_line((x0, y0), (x1, y1), width=width)
        case 8:
            __left_hex_canvas.create_line((x0, y0), (x1, y1), width=width, dash=(80, 40))
        case 9:
            __left_hex_canvas.create_line((x0, y0), (x1, y1), width=width, fill='red')


def draw_reverse_hex(reverse_binary: list):
    x0 = 110
    y0 = 50
    x1 = 310
    y1 = 50
    width = 20

    for bit in reverse_binary:
        if bit == '1':
            __right_hex_canvas.create_line((x0, y0), (x1, y1), width=width)
        else:
            __right_hex_canvas.create_line((x0, y0), (x1, y1), width=width, dash=(80, 40))

        y0 += 50
        y1 += 50


def draw_true_info(true_hex: tuple):
    number = '#' + true_hex[0]
    name = true_hex[1]

    __left_info_canvas.create_text((140, 50), text=number, font=('TkDefaultFont', 15))
    __left_info_canvas.create_text((140, 100), text=name, font=('TkDefaultFont', 20))


def draw_reverse_info(reverse_hex: tuple):
    number = '#' + reverse_hex[0]
    name = reverse_hex[1]

    __right_info_canvas.create_text((210, 50), text=number, font=('TkDefaultFont', 15))
    __right_info_canvas.create_text((210, 100), text=name, font=('TkDefaultFont', 20))


def draw_no_change():
    __right_info_canvas.create_text((210, 50), text='No changing lines', font=('TkDefaultFont', 15))


def canvas_reset():
    __left_hex_canvas.delete('all')
    __right_hex_canvas.delete('all')
    __left_info_canvas.delete('all')
    __right_info_canvas.delete('all')
