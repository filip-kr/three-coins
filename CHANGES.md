# Changelog

## v2.0.0 - 2026-08-22

### Added

- **Tabbed hexagram display.** The two hexagrams (current and, when there are stressed lines, future) are now shown as switchable tabs labeled by hexagram number, instead of two fixed side-by-side canvases.
- **Adjustable window resolution.** Settings > Resolution offers five presets (Small 800x800 up to XX-Large 1600x1600); the whole UI - fonts, spacing, hexagram lines - scales to match, and the choice is remembered between runs.
- **Selectable color themes.** Settings > Theme offers five palettes (Parchment, Midnight, Jade, Slate, Sumi-e), also remembered between runs.
- **Persistent local settings**, stored as JSON at `~/.config/three-coins/settings.json` (or under `$XDG_CONFIG_HOME/three-coins/` if that's set).
- **Multi-monitor-aware window centering.** Windows now center against the primary monitor's actual bounds (via `xrandr`) rather than the combined virtual desktop, which could previously place a window straddling monitors or in the gap between two displays with different offsets.
- In-repo screenshots under `docs/screenshots/`, referenced directly from the README instead of external imgur links.

### Changed

- **Hexagram names and I Ching terminology now follow James DeKorne's *The Gnostic Book of Changes*** throughout the app and docs: yin/yang are called magnetic/dynamic, and changing/moving lines are called stressed lines. All 64 hexagram names in the database were updated to DeKorne's translation.
- **Coin-toss algorithm rewritten to match DeKorne's actual method.** Previously each toss summed two arbitrary numeric values (2s and 3s, in the manner of the traditional yarrow-stalk-derived formula) to get a 6-9 total. DeKorne considers that formula obsolete for the coin oracle and instead reads the coins directly - heads is the magnetic (yin) side, tails the dynamic (yang) side; a 2-1 split takes the minority coin's gender, a unanimous throw becomes a stressed line in the shared face's gender. The toss probabilities are unchanged (each stressed line 1/8, each stable line 3/8) - only which physical coin pattern produces which line gender changed, to match DeKorne's convention instead of the generic one.
- Popup windows (Instructions, About) are now theme-colored, stay on top of the main window, and scale with the chosen resolution, instead of using plain OS-default styling at a fixed size.
- Re-clicking an already-selected resolution or theme in its menu no longer visibly un-checks it.
- About dialog now shows the current version (`v2.0.0`) and an extended copyright range (`2023-2026`).
- Instructions dialog text proofread: lowercased "oracle" (was "Oracle"), "in regards to" -> "regarding", "resources of choice" -> "resources of your choice", added missing articles, "changing lines" -> "stressed lines".
- `apsw` dependency bumped from a pinned `==3.41.0.0` to `>=3.46.0.0` - the old pin predates Python 3.13's C API changes and fails to build under it.
- README rewritten: added an AI-assisted-development disclaimer, an explanation of why the app's coin-toss odds are correct, where settings are stored, and DeKorne attribution for both hexagram names and terminology; the Wikipedia/Wikibooks quotes were replaced with original explanations based on DeKorne's book, and all images moved in-repo.
- License copyright range extended to `2023-2026`.

### Fixed

- Looking up a binary pattern with no matching hexagram now raises a clear `ValueError` instead of silently indexing into an empty result.
- The database connection is now opened once and reused, instead of opening and closing a new connection on every hexagram lookup.

### Internal

- Replaced the `helper.counter`/`helper.proto_hex` module-level singletons with a single `HexagramSession` class (`helper/session.py`) holding all in-progress toss state.
- Toss results are now a typed `LineType` enum instead of raw integers.
- Input and output widgets are now built via explicit `build()`/`destroy()` functions instead of being constructed once at import time, which is what makes runtime resolution/theme changes possible without restarting the app.
- Deduplicated repeated drawing and session-restore logic in `three_coins/__main__.py` and `gui/output.py`.
- Removed dead code: an unused `db.conn.all_names()` function and an unused `tkinter.font` import.
- `.venv/` added to `.gitignore`.
