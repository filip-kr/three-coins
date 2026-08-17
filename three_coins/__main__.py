import tkinter as tk
from tkinter import ttk

import gui
import gui.input as gui_input
import gui.output as gui_output
from db import conn
from helper.session import session


def main():
    def _on_toss():
        rst_btn.config(state=tk.NORMAL)
        gui_input.qstn_disable()

        if session.is_complete:
            return

        line_index = session.count
        line = session.toss_line()
        gui_output.draw_line_left(line_index, line)

        if not session.is_complete:
            return

        toss_btn.config(state=tk.DISABLED)

        true_binary = list(reversed(session.binary))
        true_hex = conn.get_by_binary(true_binary)
        gui_output.draw_true_info(true_hex)

        if not session.has_changing_lines:
            gui_output.draw_no_change()
            return

        reverse_binary = list(reversed(session.reverse_binary))
        reverse_hex = conn.get_by_binary(reverse_binary)
        gui_output.draw_reverse_hex(reverse_binary)
        gui_output.draw_reverse_info(reverse_hex)

    def _on_reset():
        gui_input.qstn_enable()
        toss_btn.config(state=tk.NORMAL)
        rst_btn.config(state=tk.DISABLED)
        gui_input.qstn_reset()
        session.reset()
        gui_output.canvas_reset()

    gui.build()
    gui_input.build()
    gui_output.build()

    toss_btn = ttk.Button(gui.root, text='Toss coins', command=_on_toss)
    toss_btn.pack(in_=gui_input.btns, side=tk.LEFT, ipadx=10, ipady=10)

    rst_btn = ttk.Button(gui.root, text='Reset', command=_on_reset)
    rst_btn.pack(in_=gui_input.btns, side=tk.RIGHT, ipadx=10, ipady=10)
    rst_btn.config(state=tk.DISABLED)

    gui.root.mainloop()
