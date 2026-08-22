import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk
from typing import Callable

import gui
from gui import theme

_input_frame: ttk.Frame | None = None
_qstn_txtbox: tk.Text | None = None
toss_btn: ttk.Button | None = None
rst_btn: ttk.Button | None = None


def build(on_toss: Callable[[], None], on_reset: Callable[[], None]):
    global _input_frame, _qstn_txtbox, toss_btn, rst_btn

    s = gui.scaled
    base_size = tkfont.nametofont('TkDefaultFont').cget('size')
    txt_font = ('TkDefaultFont', s(base_size))
    palette = theme.current()

    _input_frame = ttk.Frame(gui.root)
    _input_frame.pack(side=tk.TOP)

    qstn = ttk.Frame(_input_frame)
    qstn.pack(side=tk.TOP, ipady=s(10))

    btns = ttk.Frame(_input_frame)
    btns.pack(side=tk.TOP, ipadx=s(10))

    qstn_label = ttk.Label(qstn, text='What is your question?', font=txt_font)
    qstn_label.pack(side=tk.TOP, ipady=s(10))

    _qstn_txtbox = tk.Text(
        qstn, height=4, width=40, font=txt_font,
        bg=palette.surface, fg=palette.ink, insertbackground=palette.ink,
        highlightthickness=1, highlightbackground=palette.border, highlightcolor=palette.accent,
        relief=tk.FLAT, padx=8, pady=8,
    )
    _qstn_txtbox.pack(side=tk.TOP)
    _qstn_txtbox.focus()

    toss_btn = ttk.Button(btns, text='Toss coins', command=on_toss)
    toss_btn.pack(side=tk.LEFT, ipadx=s(10), ipady=s(10))

    rst_btn = ttk.Button(btns, text='Reset', command=on_reset)
    rst_btn.pack(side=tk.RIGHT, ipadx=s(10), ipady=s(10))
    rst_btn.config(state=tk.DISABLED)

    # ttk.Style is global, so this also re-applies to (and thereby scales) any
    # already-existing button using the default style.
    ttk.Style().configure('TButton', font=txt_font)


def destroy():
    _input_frame.destroy()


def get_question() -> str:
    return _qstn_txtbox.get('1.0', tk.END).rstrip('\n')


def set_question(text: str) -> None:
    _qstn_txtbox.delete('1.0', tk.END)
    _qstn_txtbox.insert('1.0', text)


def qstn_reset():
    _qstn_txtbox.delete('1.0', tk.END)


def qstn_disable():
    _qstn_txtbox.config(state=tk.DISABLED)


def qstn_enable():
    _qstn_txtbox.config(state=tk.NORMAL)


def toss_enable():
    toss_btn.config(state=tk.NORMAL)


def toss_disable():
    toss_btn.config(state=tk.DISABLED)


def reset_enable():
    rst_btn.config(state=tk.NORMAL)


def reset_disable():
    rst_btn.config(state=tk.DISABLED)
