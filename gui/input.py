import tkinter as tk
from tkinter import ttk

from gui import root

btns: ttk.Frame | None = None
_qstn_txtbox: tk.Text | None = None


def build():
    global btns, _qstn_txtbox

    qstn = ttk.Frame(root)
    qstn.pack(side=tk.TOP, ipady=10)

    btns = ttk.Frame(root)
    btns.pack(side=tk.TOP, ipadx=10)

    qstn_label = ttk.Label(root, text='What is your question?')
    qstn_label.pack(in_=qstn, side=tk.TOP, ipady=10)

    _qstn_txtbox = tk.Text(root, height=4, width=40)
    _qstn_txtbox.pack(in_=qstn, side=tk.TOP)
    _qstn_txtbox.focus()


def qstn_reset():
    _qstn_txtbox.delete('1.0', tk.END)


def qstn_disable():
    _qstn_txtbox.config(state=tk.DISABLED)


def qstn_enable():
    _qstn_txtbox.config(state=tk.NORMAL)
