import tkinter as tk
from tkinter import ttk

root = tk.Tk()

try:
    from ctypes import windll
except ImportError:
    root.iconbitmap('@gui/asset/icon/icon.xbm')
else:
    windll.shcore.SetProcessDpiAwareness(1)
    root.iconbitmap('gui/asset/icon/icon.ico')
finally:
    root.title('Three Coins')
    window_width = 800
    window_height = 800
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    root.resizable(False, False)
