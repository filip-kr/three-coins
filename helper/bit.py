from helper.line_type import LineType

# Hexagram bits: 0 = magnetic (yin), 1 = dynamic (yang). reverse_from_toss first
# applies the changing-line transform (stressed lines flip gender).
_MAGNETIC_LINES = (LineType.STRESSED_MAGNETIC, LineType.MAGNETIC)
_RESULTS_IN_DYNAMIC = (LineType.STRESSED_MAGNETIC, LineType.DYNAMIC)


def from_toss(line: LineType) -> int:
    return 0 if line in _MAGNETIC_LINES else 1


def reverse_from_toss(line: LineType) -> int:
    return 1 if line in _RESULTS_IN_DYNAMIC else 0
