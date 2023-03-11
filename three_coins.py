import random


def toss():
    count = 0
    result = 0

    while count < 3:
        result += random.choice([2, 3])
        count += 1

    return result
