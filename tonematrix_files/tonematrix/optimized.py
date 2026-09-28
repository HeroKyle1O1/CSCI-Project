from tonematrix.matrix import ToneMatrix as _ToneMatrix

class ToneMatrix(_ToneMatrix):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._active = set()

    def pluck_column(self, col):
        for row in range(self.grid_size):
            if self.is_on(row, col):
                self.instruments[row].pluck()
                self._active.add(row)

    ENERGY_THRESHOLD = 1e-4

    def _retire_quiet_strings(self):
        quiet = [row for row in self._active
                 if self.instruments[row].energy() < self.ENERGY_THRESHOLD]
        for row in quiet:
            self._active.discard(row)

    def next_sample(self):
        if self._calls == 0:
            self.pluck_column(self.column)
            self._retire_quiet_strings()
            self.column += 1
            if self.column == self.grid_size:
                self.column = 0

        total = 0
        for row in self._active:
            total += self.instruments[row].next_sample()

        self._calls += 1
        if self._calls == self._samples_per_column:
            self._calls = 0

        return total

    def resize(self, new_size):
        super().resize(new_size)
        self._active = {row for row in self._active if row < new_size}