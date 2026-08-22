import json
import os
from pathlib import Path

# The label only names width, not "WxH": the window's height is content-driven
# (gui.finalize() grows it to fit the fixed-size tab layout, see
# gui.register_min_height) and is reliably taller than the width, so a "WxW"
# label would promise a square window this app never actually shows.
RESOLUTIONS = [
    ('Small (800px wide)', 800, 800),
    ('Medium (1000px wide)', 1000, 1000),
    ('Large (1200px wide)', 1200, 1200),
    ('X-Large (1400px wide)', 1400, 1400),
    ('XX-Large (1600px wide)', 1600, 1600),
]

DEFAULT_RESOLUTION = RESOLUTIONS[1]

_CONFIG_DIR = Path(os.environ.get('XDG_CONFIG_HOME', Path.home() / '.config')) / 'three-coins'
_CONFIG_FILE = _CONFIG_DIR / 'settings.json'


def _load_data() -> dict:
    try:
        return json.loads(_CONFIG_FILE.read_text())
    except (OSError, ValueError, json.JSONDecodeError):
        return {}


def _save_data(updates: dict) -> None:
    # Read-modify-write rather than overwrite, so saving one setting (e.g.
    # resolution) never clobbers another (e.g. theme) already on disk.
    data = _load_data()
    data.update(updates)
    _CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    _CONFIG_FILE.write_text(json.dumps(data))


def load_resolution() -> tuple[str, int, int]:
    data = _load_data()
    try:
        width, height = int(data['width']), int(data['height'])
    except (KeyError, ValueError, TypeError):
        return DEFAULT_RESOLUTION

    for label, saved_width, saved_height in RESOLUTIONS:
        if (saved_width, saved_height) == (width, height):
            return label, saved_width, saved_height

    return DEFAULT_RESOLUTION


def save_resolution(width: int, height: int) -> None:
    _save_data({'width': width, 'height': height})


def load_theme_name() -> str | None:
    name = _load_data().get('theme')
    return name if isinstance(name, str) else None


def save_theme_name(name: str) -> None:
    _save_data({'theme': name})
