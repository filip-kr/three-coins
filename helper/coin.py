import random

from helper.line_type import LineType

_HEADS = 'H'
_TAILS = 'T'


def toss_three() -> LineType:
    """Per James DeKorne's The Gnostic Book of Changes (ch. 5), following Wilhelm:
    heads is the coin's inscribed, magnetic (yin) side; tails its reverse, dynamic
    (yang) side. A mixed throw takes the gender of its minority coin; a unanimous
    throw is a stressed line in the gender of that shared face. DeKorne considers
    the older numerical formula (summing 2s and 3s to get 6-9) obsolete for the
    coin oracle, so this counts heads/tails directly instead.
    """
    heads = sum(random.choice((_HEADS, _TAILS)) == _HEADS for _ in range(3))

    if heads == 0:
        return LineType.STRESSED_DYNAMIC
    if heads == 1:
        return LineType.MAGNETIC
    if heads == 2:
        return LineType.DYNAMIC
    return LineType.STRESSED_MAGNETIC
