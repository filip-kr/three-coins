import random

from helper.line_type import LineType


def toss_three() -> LineType:
    result = sum(random.choice([2, 3]) for _ in range(3))
    return LineType(result)
