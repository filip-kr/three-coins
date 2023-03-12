class Hexagram:

    def __init__(self):
        self.lines = []

    def __str__(self):
        binary = ''
        for line in self.lines:
            if line == 6 or line == 8:
                binary += '0'
            else:
                binary += '1'
        return binary

    def __reversed__(self):
        return self.lines[::-1]

    def __add__(self, index, line):
        self.lines.insert(index, line)
