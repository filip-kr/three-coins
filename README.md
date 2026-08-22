<div align="center">
    <img src="gui/asset/icon.gif" alt="icon" width="150"/>
    <h1 align="center">Three Coins</h1>
</div>
<br>

## About

A simple Linux desktop application for I Ching divination using the 3-coin method.
<br>
Precompiled executables ```three_coins_vX.X.X``` can be found in Releases.

**Disclaimer:** Starting with v2.0.0, AI was used to assist in developing this application.

<br>

## Usage

### Running the precompiled executable

Each release's ```three_coins_vX.X.X``` is a self-contained, single-file build for 64-bit Linux (x86_64), produced with PyInstaller. It bundles the Python runtime, the Tcl/Tk GUI toolkit, the `apsw`/SQLite dependency, and the hexagram database - no separate Python, pip, or apt install is needed to run it.

To run it:

```bash
chmod +x three_coins_vX.X.X
./three_coins_vX.X.X
```

**System requirements:**

- 64-bit Linux (x86_64) with a glibc-based distro (e.g. Debian, Ubuntu, Fedora, Arch) - not tested on musl-based distros like Alpine.
- A running X11 display server, or Xwayland on a Wayland session. The bundled Tk toolkit is X11-only and will fail to start under native Wayland with no XWayland compatibility layer.
- The system X11 client libraries (`libX11`, `libXft`, `libXext`, `libXrender`, `libXss`) and `fontconfig`/`freetype`. These come preinstalled with essentially any Linux desktop environment; a minimal/headless server install may need an X11 package group added.
- The `DejaVu Serif` font is used for hexagram names in most themes. It's preinstalled on nearly all Linux distros; if missing, Tk silently falls back to a default font instead of failing.

**Verifying your download:** each release includes a `.sha256` checksum file alongside the executable. Verify with:

```bash
sha256sum -c three_coins_vX.X.X.sha256
```

### Settings

Resolution and theme preferences are saved to `~/.config/three-coins/settings.json` (or under `$XDG_CONFIG_HOME/three-coins/` instead, if that environment variable is set).

<br>

## I Ching background

### I Ching divination

The I Ching, or Book of Changes, is a Chinese oracle text first set down around 1143 BCE and still in active use today. At its core are 64 hexagrams: six-line figures built from two kinds of lines, each carrying commentary that's studied in relation to a question the querent brings to it.

James DeKorne's commentary drops the traditional yin/yang labels in favor of a gender-neutral pair he calls magnetic and dynamic - incoming, receptive, structural energy versus outgoing, expressive, functional energy - specifically to strip out the "negative femininity" bias that crept into the text's older, patriarchal-era translations. A hexagram is cast one line at a time, and some lines come out "stressed": they're read as actively transforming into their opposite, turning the first hexagram into a second one that's studied alongside it. This app follows that same vocabulary throughout.

- Based on James DeKorne's [*The Gnostic Book of Changes*, Chapter 1](https://jamesdekorne.com/GBCh/ch1.htm)

### The 3-coin method

Three coins are thrown together, six times, one throw building one line of the hexagram from the bottom upward. Following Richard Wilhelm's convention, DeKorne treats a coin's engraved (heads) face as its magnetic, yin side, and the plain reverse (tails) as its dynamic, yang side.

Each throw is read by how the three coins land: when they split two-to-one, the line takes the gender of the single dissenting coin. When all three agree, the line is stressed - it's read as its shared face's gender, but marked to transform into the opposite gender in the second hexagram. After six throws, the resulting six-line figure is looked up among the 64 hexagrams, and any stressed lines are interpreted specifically against the question asked.

- Based on James DeKorne's [*The Gnostic Book of Changes*, Chapter 5](https://jamesdekorne.com/GBCh/ch5.htm)

### Why use three-coins

Many digital coin-oracle tools quietly get the odds wrong by treating the four possible lines as equally likely - e.g. picking uniformly at random between them. That's not how three physical coins actually behave. three-coins tosses three independent, fair coins under the hood and reads them exactly as described above (rather than summing a numerical value per coin, an older, yarrow-stalk-derived formula DeKorne considers obsolete for the coin oracle), which reproduces the true probabilities: a stressed line lands only 1/8 of the time, a stable line 3/8 of the time.

### Hexagram names and terminology

Hexagram names, and the line terminology used throughout this app (magnetic/dynamic in place of yin/yang, stressed in place of changing/moving), are taken from James DeKorne's [*The Gnostic Book of Changes*](https://jamesdekorne.com/GBCh/GBCh.htm) - recommended reading for anyone who wants to know what the I Ching *really* is.

<br>

## Gallery

<p>
  <img src="docs/screenshots/01_initial.png" width="300"/>
  <img src="docs/screenshots/02_reading_true.png" width="300"/>
  <img src="docs/screenshots/03_reading_reverse.png" width="300"/>
</p>
