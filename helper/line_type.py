from enum import IntEnum


class LineType(IntEnum):
    """A tossed line, named per James DeKorne's The Gnostic Book of Changes:
    magnetic=yin, dynamic=yang, stressed=changing (all three coins agree on one
    face - see helper.coin for how a line's gender is actually determined).
    Numbered 6-9 to match the traditional line values, though DeKorne derives
    the gender straight from the coins rather than by summing numeric values."""
    STRESSED_MAGNETIC = 6
    DYNAMIC = 7
    MAGNETIC = 8
    STRESSED_DYNAMIC = 9
