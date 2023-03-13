import tkinter as tk


def mainloop() -> None:
    root = tk.Tk()

    try:
        from ctypes import windll
    except ImportError:
        root.iconbitmap('@three_coins/asset/icon.xbm')
    else:
        windll.shcore.SetProcessDpiAwareness(1)
        root.iconbitmap('three_coins/asset/icon.ico')
    finally:
        root.title('Three Coins')
        window_width = 800
        window_height = 600
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        root.resizable(False, False)
        root.mainloop()
