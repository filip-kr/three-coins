import random

from helper.line_type import LineType

_HEADS = 'H'
_TAILS = 'T'


def toss_three() -> LineType:
    """Coin-count method from James DeKorne's The Gnostic Book of Changes (ch. 5):
    heads = magnetic (yin) face, tails = dynamic (yang). A mixed throw takes its
    minority gender; a unanimous throw is a stressed (changing) line of that
    gender. Counts faces directly rather than via the older 6-9 sum.
    """
    heads = sum(random.choice((_HEADS, _TAILS)) == _HEADS for _ in range(3))

    if heads == 0:
        return LineType.STRESSED_DYNAMIC
    if heads == 1:
        return LineType.MAGNETIC
    if heads == 2:
        return LineType.DYNAMIC
    return LineType.STRESSED_MAGNETIC
