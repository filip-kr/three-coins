from db import conn
from gui import root, tk, ttk
from gui.top import btns

from helper.proto_hex import ProtoHexagram
from helper.counter import Counter


def main():
    proto_hex = ProtoHexagram()
    counter = Counter()

    def __get_hex_line():
        if counter.count < 6:
            proto_hex.add_line(counter.count)
            print(proto_hex.lines[counter.count])
            counter.add(1)

            if counter.count == 6:
                true_hex = conn.get_by_binary(proto_hex.binary)
                print(true_hex, proto_hex.lines)

                if 6 not in proto_hex.lines and 9 not in proto_hex.lines:
                    print('No changing lines')

                reverse_hex = conn.get_by_binary(proto_hex.reverse_binary)
                print(reverse_hex)

    def __reset():
        proto_hex.reset()
        counter.reset()

    toss_btn = ttk.Button(root, text='Toss coins', command=__get_hex_line)
    toss_btn.pack(in_=btns, side=tk.LEFT, ipadx=10, ipady=10)

    rst_btn = ttk.Button(root, text='Reset', command=__reset)
    rst_btn.pack(in_=btns, side=tk.RIGHT, ipadx=10, ipady=10)

    hex_frame = ttk.Frame(root, borderwidth=5, relief='sunken')
    hex_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, padx=20, pady=20)

    hex_canvas = tk.Canvas(root, height=350)
    hex_canvas.pack(in_=hex_frame)

    root.mainloop()
