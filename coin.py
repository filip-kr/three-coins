import random


class Coin:
    @staticmethod
    def toss_three():
        result = 0

        count = 0
        while count < 3:
            result += random.choice([2, 3])
            count += 1

        return result
