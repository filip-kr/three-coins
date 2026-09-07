import re
import subprocess
import tkinter as tk
from tkinter import ttk

from gui import settings, theme
from gui.asset.icon import icon_str

root = tk.Tk()
icon = tk.PhotoImage(data=icon_str)

_resolution_vars: dict[str, tk.BooleanVar] = {}
_theme_vars: dict[str, tk.BooleanVar] = {}
_menus: list[tk.Menu] = []

_BASE_SIZE = settings.RESOLUTIONS[0][1]
_MONITOR_RE = re.compile(r'(\d+)x(\d+)\+(\d+)\+(\d+)')

scale: float = 1.0
_min_height = 0
_rebuild_hook = None
_theme_preview_hook = None
_theme_revert_id: str | None = None
_current_resolution_label: str | None = None


def scaled(value: float) -> int:
    return round(value * scale)


def target_width() -> int:
    """Pixel width of the resolution this build is targeting."""
    return round(scale * _BASE_SIZE)


def register_min_height(height: int) -> None:
    """Raise the floor under the root window's final height. finalize() sets an
    explicit geometry, which disables Tk's grow-to-fit, so callers that know their
    worst-case content height must report it here before finalize() runs."""
    global _min_height
    _min_height = max(_min_height, height)


def reset_min_height() -> None:
    """Clear the floor so a rebuild re-probes from scratch."""
    global _min_height
    _min_height = 0


def set_rebuild_hook(fn) -> None:
    """Register the callback that rebuilds all widgets on a resolution or theme
    change. Owned by three_coins, which knows how to replay session state."""
    global _rebuild_hook
    _rebuild_hook = fn


def set_theme_preview_hook(fn) -> None:
    """Like set_rebuild_hook, but recolors widgets in place - no rebuild, no
    persist - for Theme-menu hover preview."""
    global _theme_preview_hook
    _theme_preview_hook = fn


def refresh_theme() -> None:
    """Re-apply the theme's shared ttk styles and recolor the menus. Both are set
    once in build() and aren't recreated by a widget rebuild, so a theme change
    has to redo them here (menus especially - see theme.style_menu)."""
    theme.apply(root)
    for menu in _menus:
        theme.style_menu(menu)


def _primary_monitor_geometry() -> tuple[int, int, int, int] | None:
    """(x, y, width, height) of the primary monitor, or None if undetectable.
    winfo_screenwidth/height() span the whole multi-monitor desktop, so centering
    against them can drop the window in the gap between screens."""
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
    """Center win, using (min_width, min_height) as a floor and growing to fit
    packed content when measured text needs more room."""
    win.update_idletasks()
    width = max(min_width, win.winfo_reqwidth())
    height = max(min_height, win.winfo_reqheight())
    _center_window(win, width, height)


def _on_resolution_selected(label: str, width: int, height: int) -> None:
    global scale, _current_resolution_label

    if label == _current_resolution_label:
        # Re-clicking the active item: undo the checkbutton's auto-toggle and
        # skip the rebuild.
        _resolution_vars[label].set(True)
        return

    for res_label, var in _resolution_vars.items():
        var.set(res_label == label)

    _current_resolution_label = label
    scale = width / _BASE_SIZE
    settings.save_resolution(width, height)

    if _rebuild_hook is not None:
        _rebuild_hook()
    else:
        _center_window(root, width, max(height, _min_height))


def _apply_theme_preview() -> None:
    (_theme_preview_hook or refresh_theme)()


def _active_menu_label(widget) -> str | None:
    # event.widget can be a menubar-clone path string, not a widget - go via Tcl.
    path = widget if isinstance(widget, str) else str(widget)
    try:
        index = int(root.tk.call(path, 'index', 'active'))
    except (tk.TclError, ValueError):
        return None
    try:
        return root.tk.call(path, 'entrycget', index, '-label') or None
    except tk.TclError:
        return None


def _on_theme_hover(event) -> None:
    global _theme_revert_id
    name = _active_menu_label(event.widget)
    if name not in theme.THEMES or name == theme.current_name():
        return
    if _theme_revert_id is not None:
        root.after_cancel(_theme_revert_id)
        _theme_revert_id = None
    theme.preview(name)
    _apply_theme_preview()


def _on_theme_menu_closed(event) -> None:
    # after_idle, not now: on a click Tk unposts (this event) before running the
    # entry command, so a direct revert here would undo the commit.
    global _theme_revert_id
    if theme.current_name() != theme.committed_name() and _theme_revert_id is None:
        _theme_revert_id = root.after_idle(_revert_theme_preview)


def _revert_theme_preview() -> None:
    global _theme_revert_id
    _theme_revert_id = None
    if theme.current_name() != theme.committed_name():
        theme.clear_preview()
        _apply_theme_preview()


def _on_theme_selected(name: str) -> None:
    global _theme_revert_id
    if _theme_revert_id is not None:
        root.after_cancel(_theme_revert_id)
        _theme_revert_id = None

    # Clicking a checkbutton toggled one var; re-sync all (see _on_resolution_selected).
    for theme_name, var in _theme_vars.items():
        var.set(theme_name == name)

    if name == theme.committed_name():
        if theme.current_name() != name:  # a preview is still showing - drop it
            theme.clear_preview()
            _apply_theme_preview()
        return

    theme.set_current(name)

    if _rebuild_hook is not None:
        _rebuild_hook()
    else:
        refresh_theme()


def _show_instructions():
    instr_win = tk.Toplevel(bg=theme.current().bg)
    instr_win.title('Instructions')
    instr_win.resizable(False, False)
    instr_win.transient(root)
    instr_win.attributes('-topmost', True)
    instr_win.grab_set()

    instr_frame = ttk.Frame(instr_win)
    instr_frame.pack(padx=scaled(15))

    instr_text = '1. Think of a problem\n' \
                 '2. Turn it into an open-ended question\n' \
                 '3. Write the question into the application (optional, but helps with step 4)\n' \
                 '4. Focus on it\n' \
                 '5. Toss coins until a hexagram is formed\n' \
                 '6. Consult external resources of your choice for detailed line meanings\n\n' \
                 'The left hexagram explains your current position regarding your question,\n' \
                 'with its stressed lines explaining what can be done about it.\n\n' \
                 'The right hexagram foretells the possible future if the oracle\'s advice is heeded.'

    instr_label = ttk.Label(instr_win, text=instr_text, font=('TkDefaultFont', scaled(10)))
    instr_label.pack(in_=instr_frame, pady=scaled(20))

    _center_to_content(instr_win, scaled(600), scaled(250))


def _show_about():
    about_win = tk.Toplevel(bg=theme.current().bg)
    about_win.title('About')
    about_win.resizable(False, False)
    about_win.transient(root)
    about_win.attributes('-topmost', True)
    about_win.grab_set()

    about_frame = ttk.Frame(about_win)
    about_frame.pack(padx=scaled(15))

    about_title = 'Three Coins'
    about_ver = 'v2.0.0'
    about_body = 'I Ching divination using the 3-coin method'
    about_footer = 'Copyright (c) 2023-2026 Filip Krnjaković\n' \
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
    global scale, _current_resolution_label

    # Stay hidden until finalize() reveals it, so construction isn't visible.
    root.withdraw()

    theme.load_saved()
    theme.apply(root)

    root.iconphoto(True, icon)
    root.title('Three Coins')
    root.resizable(False, False)

    current_label, width, height = settings.load_resolution()
    _current_resolution_label = current_label
    scale = width / _BASE_SIZE

    root_menu = tk.Menu(root, tearoff=False)
    root.config(menu=root_menu)

    root_menu.add_command(label='Instructions', command=_show_instructions)

    settings_menu = tk.Menu(root_menu, tearoff=False)
    root_menu.add_cascade(label='Settings', menu=settings_menu)

    resolution_menu = tk.Menu(settings_menu, tearoff=False)
    for res_label, res_width, res_height in settings.RESOLUTIONS:
        var = tk.BooleanVar(value=(res_label == current_label))
        _resolution_vars[res_label] = var
        resolution_menu.add_checkbutton(
            label=res_label,
            variable=var,
            command=lambda l=res_label, w=res_width, h=res_height: _on_resolution_selected(l, w, h),
        )
    settings_menu.add_cascade(label='Resolution', menu=resolution_menu)

    theme_menu = tk.Menu(settings_menu, tearoff=False)
    for theme_name in theme.THEMES:
        var = tk.BooleanVar(value=(theme_name == theme.committed_name()))
        _theme_vars[theme_name] = var
        theme_menu.add_checkbutton(
            label=theme_name,
            variable=var,
            command=lambda n=theme_name: _on_theme_selected(n),
        )
    theme_menu.bind('<<MenuSelect>>', _on_theme_hover)  # fires on highlight change, i.e. hover
    theme_menu.bind('<Unmap>', _on_theme_menu_closed)
    settings_menu.add_cascade(label='Theme', menu=theme_menu)

    root_menu.add_command(label='About', command=_show_about)

    _menus[:] = [root_menu, settings_menu, resolution_menu, theme_menu]
    for menu in _menus:
        theme.style_menu(menu)


def finalize():
    """Size, center, and reveal the root window. Call after all widgets are built."""
    _, width, height = settings.load_resolution()
    height = max(height, _min_height)
    _center_window(root, width, height)
    root.deiconify()
