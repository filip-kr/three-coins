from db import conn
from gui import tk, ttk, root
from gui.input import btns, \
    qstn_reset, qstn_disable, qstn_enable
from gui.output import \
    draw_line_left, draw_reverse_hex, \
    draw_true_info, draw_reverse_info, \
    draw_no_change, canvas_reset
from helper.counter import counter
from helper.proto_hex import proto_hex


def main():
    def __get_hex_line():
        rst_btn.config(state=tk.NORMAL)
        qstn_disable()

        if counter.count < 6:
            proto_hex.add_line(counter.count)
            draw_line_left(counter.count, proto_hex.lines[counter.count])
            counter.add(1)

            if counter.count == 6:
                toss_btn.config(state=tk.DISABLED)

                proto_hex.binary.reverse()
                true_hex = conn.get_by_binary(proto_hex.binary)
                draw_true_info(true_hex)

                if 6 not in proto_hex.lines and 9 not in proto_hex.lines:
                    draw_no_change()
                    return

                proto_hex.reverse_binary.reverse()
                reverse_hex = conn.get_by_binary(proto_hex.reverse_binary)
                draw_reverse_hex(proto_hex.reverse_binary)
                draw_reverse_info(reverse_hex)

    def __reset():
        qstn_enable()
        toss_btn.config(state=tk.NORMAL)
        rst_btn.config(state=tk.DISABLED)
        qstn_reset()
        counter.reset()
        proto_hex.reset()
        canvas_reset()

    toss_btn = ttk.Button(root, text='Toss coins', command=__get_hex_line)
    toss_btn.pack(in_=btns, side=tk.LEFT, ipadx=10, ipady=10)

    rst_btn = ttk.Button(root, text='Reset', command=__reset)
    rst_btn.pack(in_=btns, side=tk.RIGHT, ipadx=10, ipady=10)
    rst_btn.config(state=tk.DISABLED)

    root.mainloop()
