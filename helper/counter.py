class Counter:
    count = 0

    def add(self, incr: int):
        self.count += incr

    def reset(self):
        self.count = 0


counter = Counter()
