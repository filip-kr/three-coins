from helper.line_type import LineType

_YIN_LINES = (LineType.OLD_YIN, LineType.YOUNG_YIN)
_RESULTS_IN_YANG = (LineType.OLD_YIN, LineType.YOUNG_YANG)


def from_toss(line: LineType) -> int:
    """Bit for the line as originally tossed (0 = yin, 1 = yang)."""
    return 0 if line in _YIN_LINES else 1


def reverse_from_toss(line: LineType) -> int:
    """Bit for the line after changing lines transform (0 = yin, 1 = yang)."""
    return 1 if line in _RESULTS_IN_YANG else 0
