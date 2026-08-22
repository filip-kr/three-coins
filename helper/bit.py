from helper.line_type import LineType

_MAGNETIC_LINES = (LineType.STRESSED_MAGNETIC, LineType.MAGNETIC)
_RESULTS_IN_DYNAMIC = (LineType.STRESSED_MAGNETIC, LineType.DYNAMIC)


def from_toss(line: LineType) -> int:
    """Bit for the line as originally tossed (0 = magnetic, 1 = dynamic)."""
    return 0 if line in _MAGNETIC_LINES else 1


def reverse_from_toss(line: LineType) -> int:
    """Bit for the line after stressed lines transform (0 = magnetic, 1 = dynamic)."""
    return 1 if line in _RESULTS_IN_DYNAMIC else 0
