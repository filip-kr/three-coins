import math

from gui import settings

NONE = 'None'


def _grid(c, w, h, color):
    step = max(20, w // 10)
    for x in range(step, w, step):
        c.create_line(x, 0, x, h, fill=color, tags=('bg',))
    for y in range(step, h, step):
        c.create_line(0, y, w, y, fill=color, tags=('bg',))


def _rings(c, w, h, color):
    cx, cy, step = w // 2, h // 2, max(24, w // 8)
    for r in range(step, max(w, h), step):
        c.create_oval(cx - r, cy - r, cx + r, cy + r, outline=color, tags=('bg',))


def _hatch(c, w, h, color):
    for d in range(-h, w, max(18, w // 12)):  # 45-degree lines, top-left to bottom-right
        c.create_line(d, 0, d + h, h, fill=color, tags=('bg',))


def _dots(c, w, h, color):
    step, rad = max(22, w // 10), max(1, w // 200)
    for x in range(step, w, step):
        for y in range(step, h, step):
            c.create_oval(x - rad, y - rad, x + rad, y + rad, fill=color, outline=color, tags=('bg',))


def _bagua(c, w, h, color):
    cx, cy, r = w // 2, h // 2, min(w, h) // 2 - 8
    corners = [
        (cx + r * math.cos(math.pi / 8 + i * math.pi / 4), cy + r * math.sin(math.pi / 8 + i * math.pi / 4))
        for i in range(8)
    ]
    for i, (x0, y0) in enumerate(corners):
        x1, y1 = corners[(i + 1) % 8]
        c.create_line(x0, y0, x1, y1, fill=color, tags=('bg',))
    c.create_oval(cx - r // 2, cy - r // 2, cx + r // 2, cy + r // 2, outline=color, tags=('bg',))


# Faint backdrops behind the hexagram lines, one per theme, drawn in palette.border.
_PATTERNS = {'Grid': _grid, 'Rings': _rings, 'Hatch': _hatch, 'Dots': _dots, 'Bagua': _bagua}
NAMES = [NONE, *_PATTERNS]

_current = NONE
_committed = NONE


def load_saved() -> None:
    global _current, _committed
    name = settings.load_background_name()
    _current = _committed = name if name in NAMES else NONE


def current_name() -> str:
    return _current


def committed_name() -> str:
    return _committed


def set_current(name: str) -> None:
    global _current, _committed
    _current = _committed = name
    settings.save_background_name(name)


def preview(name: str) -> None:
    global _current
    _current = name


def clear_preview() -> None:
    global _current
    _current = _committed


def draw(canvas, palette) -> None:
    """Redraw the current backdrop on canvas (tag 'bg', lowered under the lines)."""
    canvas.delete('bg')
    if _current == NONE:
        return
    w, h = int(canvas.cget('width')), int(canvas.cget('height'))
    _PATTERNS[_current](canvas, w, h, palette.border)
    canvas.tag_lower('bg')
