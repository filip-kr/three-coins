import tkinter as tk
from tkinter import ttk
from gui import root

qstn = ttk.Frame(root)
qstn.pack(side=tk.TOP, ipady=10)

btns = ttk.Frame(root)
btns.pack(side=tk.TOP, ipadx=10)

qstn_label = ttk.Label(root, text='What is your question?')
qstn_label.pack(in_=qstn, side=tk.TOP, ipady=10)

qstn_txtbox = tk.Text(root, height=4, width=40)
qstn_txtbox.pack(in_=qstn, side=tk.TOP)
qstn_txtbox.focus()
