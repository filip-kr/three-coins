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


def _select_all(event: tk.Event) -> str:
    event.widget.tag_add(tk.SEL, '1.0', 'end-1c')
    return 'break'  # suppress Tk's default (cursor to line start)


def _text_colors() -> dict:
    palette = theme.current()
    return {
        'bg': palette.surface, 'fg': palette.ink, 'insertbackground': palette.ink,
        'highlightbackground': palette.border, 'highlightcolor': palette.accent,
    }


def restyle() -> None:
    _qstn_txtbox.configure(**_text_colors())


def build(on_toss: Callable[[], None], on_reset: Callable[[], None]):
    global _input_frame, _qstn_txtbox, toss_btn, rst_btn

    s = gui.scaled
    base_size = tkfont.nametofont('TkDefaultFont').cget('size')
    txt_font = ('TkDefaultFont', s(base_size))

    _input_frame = ttk.Frame(gui.root)
    _input_frame.pack(side=tk.TOP)

    qstn = ttk.Frame(_input_frame)
    qstn.pack(side=tk.TOP, ipady=s(10))

    btns = ttk.Frame(_input_frame)
    btns.pack(side=tk.TOP, ipadx=s(10))

    qstn_label = ttk.Label(qstn, text='What is your question?', font=txt_font)
    qstn_label.pack(side=tk.TOP, ipady=s(10))

    _qstn_txtbox = tk.Text(
        qstn, height=4, width=40, font=txt_font, wrap=tk.WORD,
        highlightthickness=1, relief=tk.FLAT, padx=8, pady=8, **_text_colors(),
    )
    _qstn_txtbox.pack(side=tk.TOP)
    _qstn_txtbox.focus()

    _qstn_txtbox.bind('<Control-a>', _select_all)
    _qstn_txtbox.bind('<Control-A>', _select_all)

    toss_btn = ttk.Button(btns, text='Toss coins', command=on_toss)
    toss_btn.pack(side=tk.LEFT, ipadx=s(10), ipady=s(10))

    rst_btn = ttk.Button(btns, text='Reset', command=on_reset)
    rst_btn.pack(side=tk.RIGHT, ipadx=s(10), ipady=s(10))
    rst_btn.config(state=tk.DISABLED)

    # ttk.Style is global: this also rescales any buttons already built.
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
