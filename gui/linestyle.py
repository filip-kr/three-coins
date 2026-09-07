import math
import random

from gui import settings

STANDARD = 'Standard'


def _standard(canvas, x0, x1, y, width, color, tags, **_):
    canvas.create_line(x0, y, x1, y, width=width, fill=color, capstyle='butt', tags=tags)


def _round(canvas, x0, x1, y, width, color, tags, **_):
    r = width / 2  # inset by the cap radius so the rounded ends still land on x0..x1
    canvas.create_line(x0 + r, y, x1 - r, y, width=width, fill=color, capstyle='round', tags=tags)


def _ink(canvas, x0, x1, y, width, color, tags, *, full):
    # A painted brush stroke: a bold bar with the faintest upward lift, a wavy
    # outline and blunt ends. The lift spans the whole line ('full'), so a broken
    # line's two halves share one arc; its size and the edge wobble are seeded
    # (per line / per segment) so redraws don't shimmer.
    fx0, fx1 = full
    h = width * 0.46
    arch = (fx1 - fx0) * 0.014 * random.Random(hash((round(fx0), round(fx1), round(y)))).uniform(0.85, 1.15)
    edge = random.Random(hash((round(x0), round(x1), round(y))))
    steps = max(6, round((x1 - x0) / (h * 1.3)))

    def half(sign):
        row = []
        for k in range(steps + 1):
            px = x0 + k / steps * (x1 - x0)
            centre = y - arch * math.sin(math.pi * (px - fx0) / (fx1 - fx0))
            dip = edge.uniform(0.06, 0.16) if k in (0, steps) else 0.0  # blunt end taper
            row.append((px, centre + sign * (h - (edge.uniform(0, 0.1) + dip) * width)))
        return row

    pts = []
    for px, py in half(-1) + list(reversed(half(1))):
        pts += [px, py]
    canvas.create_polygon(pts, fill=color, outline='', smooth=False, tags=tags)


_PAINTERS = {STANDARD: _standard, 'Round': _round, 'Ink': _ink}
NAMES = list(_PAINTERS)

_current = STANDARD
_committed = STANDARD


def load_saved() -> None:
    global _current, _committed
    name = settings.load_line_style_name()
    _current = _committed = name if name in NAMES else STANDARD


def current_name() -> str:
    return _current


def committed_name() -> str:
    return _committed


def set_current(name: str) -> None:
    global _current, _committed
    _current = _committed = name
    settings.save_line_style_name(name)


def preview(name: str) -> None:
    global _current
    _current = name


def clear_preview() -> None:
    global _current
    _current = _committed


def _segments(x0, x1):
    gap = (x1 - x0) * 0.2  # centre gap of a broken line - the same in every style
    cx = (x0 + x1) / 2
    return [(x0, cx - gap / 2), (cx + gap / 2, x1)]


def draw(canvas, x0: int, x1: int, y: int, width: int, *, broken: bool, color: str, tags: tuple) -> None:
    """Paint one hexagram line in the current style. Every style spans exactly
    x0..x1 and is about `width` tall, so switching style never changes the size."""
    paint = _PAINTERS[_current]
    for sx0, sx1 in (_segments(x0, x1) if broken else [(x0, x1)]):
        paint(canvas, sx0, sx1, y, width, color, tags, full=(x0, x1))
