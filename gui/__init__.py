import tkinter as tk
from tkinter import ttk

root = tk.Tk()


def __show_instructions():
    instr_win = tk.Toplevel()
    instr_win.title('Instructions')
    win_width = 600
    win_height = 300
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width / 2 - win_width / 2)
    center_y = int(screen_height / 2 - win_height / 2)
    instr_win.geometry(f'{win_width}x{win_height}+{center_x}+{center_y}')
    instr_win.resizable(False, False)
    instr_win.grab_set()

    instr_frame = tk.Frame(instr_win)
    instr_frame.pack()

    instr_text = '1. Think of a problem \n' \
                 '2. Turn it into an open-ended question \n' \
                 '3. Write the question into the program \n' \
                 '4. Focus on it \n' \
                 '5. Toss coins until a hexagram is formed \n' \
                 '6. Consult external resources of choice for detailed I Ching readings\n\n' \
                 'Left hexagram explains your current predicament in regards to your question,\n' \
                 'with its changing lines explaining what can be done about it. \n\n' \
                 'Right hexagram foretells the possible future if Oracle\'s advice is heeded.\n'

    instr_label = ttk.Label(instr_win, text=instr_text)
    instr_label.pack(in_=instr_frame, padx=10, pady=10)


def __show_about():
    pass


def __prepare_root():
    try:
        from ctypes import windll
    except ImportError:
        root.iconbitmap('@gui/asset/icon.xbm')
    else:
        windll.shcore.SetProcessDpiAwareness(1)
        root.iconbitmap('gui/asset/icon.ico')
    finally:
        root.title('Three Coins')
        win_width = 800
        win_height = 800
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        center_x = int(screen_width / 2 - win_width / 2)
        center_y = int(screen_height / 2 - win_height / 2)
        root.geometry(f'{win_width}x{win_height}+{center_x}+{center_y}')
        root.resizable(False, False)

        root_menu = tk.Menu(root)
        root.config(menu=root_menu)
        root_menu.add_command(label='Instructions', command=__show_instructions)
        root_menu.add_command(label='About', command=__show_about)


__prepare_root()
