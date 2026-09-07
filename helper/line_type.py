from enum import IntEnum


class LineType(IntEnum):
    """A tossed line (DeKorne's terms): magnetic = yin, dynamic = yang, stressed =
    changing. Values 6-9 match the traditional line numbers; gender comes from the
    coins (see helper.coin), not from summing them."""
    STRESSED_MAGNETIC = 6
    DYNAMIC = 7
    MAGNETIC = 8
    STRESSED_DYNAMIC = 9
