class Hexagram:

    def __init__(self) -> None:
        self.lines = []

    def __str__(self) -> str:
        binary = ''
        for line in self.lines:
            if line == 6 or line == 8:
                binary += '0'
            else:
                binary += '1'

        return binary

    def __reversed__(self) -> str:
        reversed_binary = ''
        for line in self.lines:
            match line:
                case 6:
                    reversed_binary += '1'
                case 7:
                    reversed_binary += '1'
                case 8:
                    reversed_binary += '0'
                case 7:
                    reversed_binary += '0'

        return reversed_binary

    def __add__(self, index: int, coin_toss_result: int) -> None:
        self.lines.insert(index, coin_toss_result)
