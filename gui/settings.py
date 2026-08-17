import json
import os
from pathlib import Path

RESOLUTIONS = [
    ('Small (800x800)', 800, 800),
    ('Medium (1000x1000)', 1000, 1000),
    ('Large (1200x1200)', 1200, 1200),
    ('X-Large (1400x1400)', 1400, 1400),
    ('XX-Large (1600x1600)', 1600, 1600),
]

DEFAULT_RESOLUTION = RESOLUTIONS[1]

_CONFIG_DIR = Path(os.environ.get('XDG_CONFIG_HOME', Path.home() / '.config')) / 'three-coins'
_CONFIG_FILE = _CONFIG_DIR / 'settings.json'


def load_resolution() -> tuple[str, int, int]:
    try:
        data = json.loads(_CONFIG_FILE.read_text())
        width, height = int(data['width']), int(data['height'])
    except (OSError, ValueError, KeyError, json.JSONDecodeError):
        return DEFAULT_RESOLUTION

    for label, saved_width, saved_height in RESOLUTIONS:
        if (saved_width, saved_height) == (width, height):
            return label, saved_width, saved_height

    return DEFAULT_RESOLUTION


def save_resolution(width: int, height: int) -> None:
    _CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    _CONFIG_FILE.write_text(json.dumps({'width': width, 'height': height}))
