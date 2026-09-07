import math

from gui import settings

NONE = 'None'


def _divisions(span, step):
    """Interior positions splitting span into whole cells ~`step` apart, so the
    frame border is the outer line and the cells meet the frame corners."""
    n = max(1, round(span / step))
    return [i * span / n for i in range(1, n)]


def _grid(canvas, width, height, color):
    step = max(20, width // 10)
    for x in _divisions(width, step):
        canvas.create_line(x, 0, x, height, fill=color, tags=('bg',))
    for y in _divisions(height, step):
        canvas.create_line(0, y, width, y, fill=color, tags=('bg',))


def _rings(canvas, width, height, color):
    cx, cy, step = width / 2, height / 2, max(24, width // 8)
    for r in range(step, max(width, height), step):
        canvas.create_oval(cx - r, cy - r, cx + r, cy + r, outline=color, tags=('bg',))


def _hatch(canvas, width, height, color):
    step = max(18, width // 12)
    reach = width // step + 1
    for k in range(-reach, reach + 1):  # parallel to the frame diagonal
        canvas.create_line(k * step, 0, k * step + width, height, fill=color, tags=('bg',))


def _dots(canvas, width, height, color):
    step, rad = max(22, width // 10), max(1, width // 200)
    for x in _divisions(width, step):
        for y in _divisions(height, step):
            canvas.create_oval(x - rad, y - rad, x + rad, y + rad, fill=color, outline=color, tags=('bg',))


def _bagua(canvas, width, height, color):
    cx, cy, r = width / 2, height / 2, min(width, height) // 2 - max(8, width // 52)
    corners = [
        (cx + r * math.cos(math.pi / 8 + i * math.pi / 4), cy + r * math.sin(math.pi / 8 + i * math.pi / 4))
        for i in range(8)
    ]
    for i, (x0, y0) in enumerate(corners):
        x1, y1 = corners[(i + 1) % 8]
        canvas.create_line(x0, y0, x1, y1, fill=color, tags=('bg',))
    canvas.create_oval(cx - r // 2, cy - r // 2, cx + r // 2, cy + r // 2, outline=color, tags=('bg',))


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
    width, height = int(canvas.cget('width')), int(canvas.cget('height'))
    _PATTERNS[_current](canvas, width, height, palette.border)
    canvas.tag_lower('bg')
