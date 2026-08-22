from helper import bit, coin
from helper.line_type import LineType


class HexagramSession:
    def __init__(self):
        self.count = 0
        self.lines: list[LineType] = []
        self.binary: list[str] = []
        self.reverse_binary: list[str] = []

    @property
    def is_complete(self) -> bool:
        return self.count == 6

    @property
    def has_stressed_lines(self) -> bool:
        return LineType.STRESSED_MAGNETIC in self.lines or LineType.STRESSED_DYNAMIC in self.lines

    def toss_line(self) -> LineType:
        line = coin.toss_three()
        self.lines.insert(self.count, line)
        self.binary.insert(self.count, str(bit.from_toss(line)))
        self.reverse_binary.insert(self.count, str(bit.reverse_from_toss(line)))
        self.count += 1
        return line

    def reset(self):
        self.count = 0
        self.lines = []
        self.binary = []
        self.reverse_binary = []


session = HexagramSession()
