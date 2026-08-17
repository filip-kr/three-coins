from enum import IntEnum


class LineType(IntEnum):
    """Coin-toss totals per the 3-coin method (yin=2, yang=3, three coins)."""
    OLD_YIN = 6
    YOUNG_YANG = 7
    YOUNG_YIN = 8
    OLD_YANG = 9
