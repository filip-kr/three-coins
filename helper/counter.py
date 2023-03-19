class Counter:
    count = 0

    def add(self, incr: int) -> None:
        self.count += incr

    def reset(self) -> None:
        self.count = 0


counter = Counter()
