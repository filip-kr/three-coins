from helper import bit, coin


class ProtoHexagram:
    lines = []
    binary = []
    reverse_binary = []

    def add_line(self, index: int) -> None:
        coin_toss_result = coin.toss_three()
        self.lines.insert(index, coin_toss_result)

        line_bit = bit.get(coin_toss_result)
        self.binary.insert(index, str(line_bit))

        reverse_bit = bit.get_reverse(coin_toss_result)
        self.reverse_binary.insert(index, str(reverse_bit))

    def get_binary(self) -> list:
        return self.binary

    def reset(self) -> None:
        self.lines = []
        self.binary = []
        self.reverse_binary = []
