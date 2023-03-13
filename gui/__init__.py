import tkinter as tk
from tkinter import ttk

__root = tk.Tk()


def __show_label():
    ttk.Label(__root, text='What is your question?').pack()


def __mainloop():
    try:
        from ctypes import windll
    except ImportError:
        __root.iconbitmap('@gui/asset/icon.xbm')
    else:
        windll.shcore.SetProcessDpiAwareness(1)
        __root.iconbitmap('gui/asset/icon.ico')
    finally:
        __root.title('Three Coins')
        window_width = 800
        window_height = 600
        screen_width = __root.winfo_screenwidth()
        screen_height = __root.winfo_screenheight()
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        __root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        __root.resizable(False, False)
        __root.mainloop()


__show_label()
__mainloop()
