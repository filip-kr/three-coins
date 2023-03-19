from gui import root, tk, ttk

hex_frame = ttk.Frame(root, borderwidth=5, relief='sunken')
hex_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, padx=20, pady=20)

left_hex_canvas = tk.Canvas(root, height=350)
left_hex_canvas.pack(in_=hex_frame, side=tk.LEFT, fill=tk.BOTH)

right_hex_canvas = tk.Canvas(root, height=350)
right_hex_canvas.pack(in_=hex_frame, side=tk.RIGHT, fill=tk.BOTH)


def __get_left_coordinates(count: int):
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
            left_hex_canvas.create_line((x0, y0), (x1, y1), width=width, dash=(80, 40), fill='red')
        case 7:
            left_hex_canvas.create_line((x0, y0), (x1, y1), width=width)
        case 8:
            left_hex_canvas.create_line((x0, y0), (x1, y1), width=width, dash=(80, 40))
        case 9:
            left_hex_canvas.create_line((x0, y0), (x1, y1), width=width, fill='red')


def draw_reverse_hex(reverse_binary: list):
    right_hex_canvas.create_line((120, 300), (320, 300), width=20)
    right_hex_canvas.create_line((120, 250), (320, 250), width=20)
    right_hex_canvas.create_line((120, 200), (320, 200), width=20)
    right_hex_canvas.create_line((120, 150), (320, 150), width=20)
    right_hex_canvas.create_line((120, 100), (320, 100), width=20)
    right_hex_canvas.create_line((120, 50), (320, 50), width=20)
