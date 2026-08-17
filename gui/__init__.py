import re
import subprocess
import tkinter as tk
from tkinter import ttk

from gui import settings
from gui.asset.icon import icon_str

root = tk.Tk()
icon = tk.PhotoImage(data=icon_str)

_resolution_vars: dict[str, tk.BooleanVar] = {}

_BASE_SIZE = settings.RESOLUTIONS[0][1]
_MONITOR_RE = re.compile(r'(\d+)x(\d+)\+(\d+)\+(\d+)')

scale: float = 1.0
_min_height = 0
_resolution_change_hook = None


def scaled(value: float) -> int:
    return round(value * scale)


def register_min_height(height: int) -> None:
    """Raise the floor under the root window's final height.

    Explicit .geometry() calls disable Tk's automatic resize-to-fit-content, so a
    window sized from empty widgets at startup won't grow later when real (and
    possibly long, wrapped) hexagram text is drawn in. Callers that know their
    worst-case content size ahead of time report it here before finalize() runs.
    """
    global _min_height
    _min_height = max(_min_height, height)


def reset_min_height() -> None:
    """Clear the registered floor so a rebuild's fresh probe isn't inflated by a
    previous (possibly larger-scale) build's leftover value."""
    global _min_height
    _min_height = 0


def set_resolution_change_hook(fn) -> None:
    """Register the callback that rebuilds all widgets at the new scale whenever
    the user picks a different resolution from the menu. Owned by three_coins,
    since only it knows how to replay in-progress session state onto fresh
    widgets; gui/__init__.py just needs to trigger it."""
    global _resolution_change_hook
    _resolution_change_hook = fn


def _primary_monitor_geometry() -> tuple[int, int, int, int] | None:
    """(x, y, width, height) of the primary/first connected monitor, or None if undetectable.

    winfo_screenwidth/height() report the combined virtual desktop across all
    monitors, which can be offset or misaligned between monitors (e.g. a laptop
    panel positioned lower than an external display). Centering against that
    combined size can place a window straddling monitors or in the gap between
    them, so we center against a single monitor's real bounds instead.
    """
    try:
        output = subprocess.run(
            ['xrandr', '--query'], capture_output=True, text=True, timeout=2, check=True,
        ).stdout
    except (OSError, subprocess.SubprocessError):
        return None

    connected_lines = [line for line in output.splitlines() if ' connected ' in line]
    if not connected_lines:
        return None

    primary_line = next((line for line in connected_lines if 'primary' in line), connected_lines[0])
    match = _MONITOR_RE.search(primary_line)
    if not match:
        return None

    width, height, x, y = (int(group) for group in match.groups())
    return x, y, width, height


def _center_window(win: tk.Wm, width: int, height: int) -> None:
    monitor = _primary_monitor_geometry()
    if monitor is not None:
        mon_x, mon_y, mon_width, mon_height = monitor
    else:
        mon_x, mon_y = 0, 0
        mon_width, mon_height = root.winfo_screenwidth(), root.winfo_screenheight()

    x = mon_x + int(mon_width / 2 - width / 2)
    y = mon_y + int(mon_height / 2 - height / 2)
    win.geometry(f'{width}x{height}+{x}+{y}')


def _center_to_content(win: tk.Toplevel, min_width: int, min_height: int) -> None:
    """Center win at (min_width, min_height), growing to fit its packed content if larger.

    Content built from measured text/fonts (long hexagram names, HiDPI font metrics)
    can need more room than a guessed baseline, so the guess is only ever a floor.
    """
    win.update_idletasks()
    width = max(min_width, win.winfo_reqwidth())
    height = max(min_height, win.winfo_reqheight())
    _center_window(win, width, height)


def _on_resolution_selected(label: str, width: int, height: int) -> None:
    global scale

    for res_label, var in _resolution_vars.items():
        var.set(res_label == label)

    scale = width / _BASE_SIZE
    settings.save_resolution(width, height)

    if _resolution_change_hook is not None:
        _resolution_change_hook()
    else:
        _center_window(root, width, max(height, _min_height))


def _show_instructions():
    instr_win = tk.Toplevel()
    instr_win.title('Instructions')
    instr_win.resizable(False, False)
    instr_win.grab_set()

    instr_frame = tk.Frame(instr_win)
    instr_frame.pack(padx=scaled(15))

    instr_text = '1. Think of a problem\n' \
                 '2. Turn it into an open-ended question\n' \
                 '3. Write the question into the application (optional, but helps with step 4)\n' \
                 '4. Focus on it\n' \
                 '5. Toss coins until a hexagram is formed\n' \
                 '6. Consult external resources of choice for detailed line meanings\n\n' \
                 'Left hexagram explains your current position in regards to your question,\n' \
                 'with its changing lines explaining what can be done about it.\n\n' \
                 'Right hexagram foretells the possible future if Oracle\'s advice is heeded.'

    instr_label = ttk.Label(instr_win, text=instr_text, font=('TkDefaultFont', scaled(10)))
    instr_label.pack(in_=instr_frame, pady=scaled(20))

    _center_to_content(instr_win, scaled(600), scaled(250))


def _show_about():
    about_win = tk.Toplevel()
    about_win.title('About')
    about_win.resizable(False, False)
    about_win.grab_set()

    about_frame = tk.Frame(about_win)
    about_frame.pack(padx=scaled(15))

    about_title = 'Three Coins'
    about_ver = 'v1.0.0'
    about_body = 'I Ching divination using the 3-coin method'
    about_footer = 'Copyright (c) 2023 Filip Krnjaković\n' \
                   'github.com/filip-kr/three-coins'

    about_icon_label = ttk.Label(about_win, image=icon)
    about_icon_label.pack(in_=about_frame, pady=scaled(15))

    about_title_label = ttk.Label(about_win, text=about_title, font=('TkDefaultFont', scaled(10), 'bold'))
    about_title_label.pack(in_=about_frame)

    about_ver_label = ttk.Label(about_win, text=about_ver, font=('TkDefaultFont', scaled(10)))
    about_ver_label.pack(in_=about_frame)

    about_body_label = ttk.Label(about_win, text=about_body, font=('TkDefaultFont', scaled(10)))
    about_body_label.pack(in_=about_frame, pady=scaled(20))

    about_footer_label = ttk.Label(
        about_win, text=about_footer, justify=tk.CENTER, font=('TkDefaultFont', scaled(8)),
    )
    about_footer_label.pack(in_=about_frame, pady=scaled(10))

    _center_to_content(about_win, scaled(300), scaled(300))


def build():
    global scale

    root.iconphoto(True, icon)
    root.title('Three Coins')
    root.resizable(False, False)

    current_label, width, height = settings.load_resolution()
    scale = width / _BASE_SIZE

    root_menu = tk.Menu(root)
    root.config(menu=root_menu)

    resolution_menu = tk.Menu(root_menu, tearoff=False)
    for res_label, res_width, res_height in settings.RESOLUTIONS:
        var = tk.BooleanVar(value=(res_label == current_label))
        _resolution_vars[res_label] = var
        resolution_menu.add_checkbutton(
            label=res_label,
            variable=var,
            command=lambda l=res_label, w=res_width, h=res_height: _on_resolution_selected(l, w, h),
        )
    root_menu.add_cascade(label='Resolution', menu=resolution_menu)

    root_menu.add_command(label='Instructions', command=_show_instructions)
    root_menu.add_command(label='About', command=_show_about)


def finalize():
    """Size and center the root window. Call once all widgets (menu, input, output) are built."""
    _, width, height = settings.load_resolution()
    height = max(height, _min_height)
    _center_window(root, width, height)
