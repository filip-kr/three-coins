import tkinter as tk
from collections.abc import Callable
from tkinter import font as tkfont
from tkinter import ttk

import gui
from gui import theme

_input_frame: ttk.Frame | None = None
_question: tk.Text | None = None
toss_btn: ttk.Button | None = None
reset_btn: ttk.Button | None = None


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
    _question.configure(**_text_colors())


def build(on_toss: Callable[[], None], on_reset: Callable[[], None]):
    global _input_frame, _question, toss_btn, reset_btn

    s = gui.scaled
    base_size = tkfont.nametofont('TkDefaultFont').cget('size')
    txt_font = ('TkDefaultFont', s(base_size))

    _input_frame = ttk.Frame(gui.root)
    _input_frame.pack(side=tk.TOP)

    question_frame = ttk.Frame(_input_frame)
    question_frame.pack(side=tk.TOP, ipady=s(10))

    buttons = ttk.Frame(_input_frame)
    buttons.pack(side=tk.TOP, ipadx=s(10))

    question_label = ttk.Label(question_frame, text='What is your question?', font=txt_font)
    question_label.pack(side=tk.TOP, ipady=s(10))

    _question = tk.Text(
        question_frame, height=4, width=40, font=txt_font, wrap=tk.WORD,
        highlightthickness=s(1), relief=tk.FLAT, padx=s(8), pady=s(8), **_text_colors(),
    )
    _question.pack(side=tk.TOP)
    _question.focus()

    _question.bind('<Control-a>', _select_all)
    _question.bind('<Control-A>', _select_all)

    toss_btn = ttk.Button(buttons, text='Toss coins', command=on_toss)
    toss_btn.pack(side=tk.LEFT, ipadx=s(10), ipady=s(10))

    reset_btn = ttk.Button(buttons, text='Reset', command=on_reset)
    reset_btn.pack(side=tk.RIGHT, ipadx=s(10), ipady=s(10))
    reset_btn.config(state=tk.DISABLED)

    # ttk.Style is global: this also rescales any buttons already built.
    ttk.Style().configure('TButton', font=txt_font)


def destroy():
    _input_frame.destroy()


def get_question() -> str:
    return _question.get('1.0', tk.END).rstrip('\n')


def set_question(text: str) -> None:
    _question.delete('1.0', tk.END)
    _question.insert('1.0', text)


def question_reset():
    _question.delete('1.0', tk.END)


def question_disable():
    _question.config(state=tk.DISABLED)


def question_enable():
    _question.config(state=tk.NORMAL)


def toss_enable():
    toss_btn.config(state=tk.NORMAL)


def toss_disable():
    toss_btn.config(state=tk.DISABLED)


def reset_enable():
    reset_btn.config(state=tk.NORMAL)


def reset_disable():
    reset_btn.config(state=tk.DISABLED)
