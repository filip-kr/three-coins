import tkinter as tk
from tkinter import ttk
from gui import root

__qstn = ttk.Frame(root)
__qstn.pack(side=tk.TOP, ipady=10)

btns = ttk.Frame(root)
btns.pack(side=tk.TOP, ipadx=10)

__qstn_label = ttk.Label(root, text='What is your question?')
__qstn_label.pack(in_=__qstn, side=tk.TOP, ipady=10)

__qstn_txtbox = tk.Text(root, height=4, width=40)
__qstn_txtbox.pack(in_=__qstn, side=tk.TOP)
__qstn_txtbox.focus()


def qstn_reset():
    __qstn_txtbox.delete('1.0', tk.END)
