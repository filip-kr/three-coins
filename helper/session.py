from helper import bit, coin
from helper.line_type import LineType


class HexagramSession:
    lines: list[LineType]
    binary: list[str]
    reverse_binary: list[str]

    def __init__(self):
        self.reset()

    @property
    def count(self) -> int:
        return len(self.lines)

    @property
    def is_complete(self) -> bool:
        return self.count == 6

    @property
    def has_stressed_lines(self) -> bool:
        return LineType.STRESSED_MAGNETIC in self.lines or LineType.STRESSED_DYNAMIC in self.lines

    @property
    def binary_top_down(self) -> list[str]:
        """Toss order is bottom-up; hexagram lookup wants the top line first."""
        return list(reversed(self.binary))

    @property
    def reverse_binary_top_down(self) -> list[str]:
        return list(reversed(self.reverse_binary))

    def toss_line(self) -> LineType:
        line = coin.toss_three()
        self.lines.append(line)
        self.binary.append(str(bit.from_toss(line)))
        self.reverse_binary.append(str(bit.reverse_from_toss(line)))
        return line

    def reset(self):
        self.lines = []
        self.binary = []
        self.reverse_binary = []


session = HexagramSession()
