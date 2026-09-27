from tonematrix.audio import SAMPLE_RATE, SAMPLES_PER_COLUMN
from tonematrix.scales import frequency_for_row
from tonematrix.string_instrument import StringInstrument

ON = "#"
OFF = "."


class ToneMatrix:
    def __init__(self, grid_size, sample_rate=SAMPLE_RATE,
                 samples_per_column=SAMPLES_PER_COLUMN):

        if grid_size < 1:
            raise ValueError
        
        self.grid = [False] * (grid_size ** 2)
        self.instruments = []
        self.column = 0
        self._samples_per_column = samples_per_column
        self.grid_size = grid_size
        self._toggle_value = True
        self._calls = 0
        self._sample_rate = sample_rate

        for row in range(grid_size):
            self.instruments.append(StringInstrument(frequency_for_row(row, grid_size), sample_rate))

    def index_of(self, row, col):
        if row < 0 or row >= self.grid_size or col < 0 or col >= self.grid_size:
            raise IndexError

        return self.grid_size * row + col

    def is_on(self, row, col):
        return self.grid[self.index_of(row, col)]

    def set_cell(self, row, col, value):
        self.grid[self.index_of(row, col)] = bool(value)

    def press(self, row, col):
        toggle = not self.is_on(row, col)
        self.set_cell(row, col, toggle)
        self._toggle_value = toggle

    def drag(self, row, col):
        self.set_cell(row, col, self._toggle_value)

    def clear(self):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                self.set_cell(row, col, False)

    def next_sample(self):
        if self._calls == 0 or self._calls % self._samples_per_column == 0:
            self.pluck_column(self.column)
            self.column += 1

            if self.column == self.grid_size:
                self.column = 0

        total = 0
        for instrument in self.instruments:
            total += instrument.next_sample()

        self._calls += 1

        return total

    def pluck_column(self, col):
        for row in range(self.grid_size):
            if self.is_on(row, col):
                self.instruments[row].pluck()

    def resize(self, new_size):
        if new_size < 1:
            raise ValueError
        
        """Change the grid to new_size x new_size.

        Cells present in both the old and new grid keep their values; new
        cells start off. Instruments for rows that survive are reused as-is,
        rows beyond the old size get fresh instruments. The playhead resets
        to column 0 and the next call to next_sample() plucks immediately.

        Raise ValueError if new_size < 1.
        """
        # TODO (Milestone 8)
        raise NotImplementedError("ToneMatrix.resize")

    ### serialization

    def to_text(self):
        text = ""
        for row in range(self.grid_size):
            value = ""
            for col in range(self.grid_size):
                if self.is_on(row, col):
                    value += ON
                else:
                    value += OFF
            text += value
            if row != self.grid_size - 1:
                text += "\n"
        return text

    @classmethod
    def from_text(cls, text, **kwargs):
        """Build a matrix from the format to_text() produces. Provided."""
        rows = [line.strip() for line in text.strip().splitlines() if line.strip()]
        size = len(rows)
        if any(len(line) != size for line in rows):
            raise ValueError("pattern must be square")

        matrix = cls(size, **kwargs)
        for r, line in enumerate(rows):
            for c, ch in enumerate(line):
                matrix.set_cell(r, c, ch == ON)
        return matrix

    def __str__(self):
        return self.to_text()
