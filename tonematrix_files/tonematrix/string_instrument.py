from tonematrix.audio import SAMPLE_RATE
from tonematrix.ring_buffer import RingBuffer

PLUCK_AMPLITUDE = 0.05
DECAY = 0.995


class StringInstrument:

    def __init__(self, frequency, sample_rate=SAMPLE_RATE):
        if frequency <= 0 or sample_rate // frequency < 2:
            raise ValueError

        length = int(sample_rate // frequency)

        self.buffer = RingBuffer(length)
        self.frequency = frequency

        for _ in range(length):
            self.buffer.enqueue(0)

    @classmethod
    def make_from_array(cls, values, frequency=None, sample_rate=SAMPLE_RATE):
        string = cls.__new__(cls)
        string.frequency = (frequency if frequency is not None
                            else sample_rate / len(values))
        string.buffer = RingBuffer(len(values))
        for value in values:
            string.buffer.enqueue(value)
        return string

    def __len__(self):
        return self.buffer.size()

    def pluck(self):
        for _ in range(self.buffer.size() // 2):
            self.buffer.dequeue()
            self.buffer.enqueue(+PLUCK_AMPLITUDE)

        for _ in range((self.buffer.size() + 1) // 2):
            self.buffer.dequeue()
            self.buffer.enqueue(-PLUCK_AMPLITUDE)

    def next_sample(self):
        first = self.buffer.dequeue()
        second = self.buffer.peek()
        self.buffer.enqueue((first + second) / 2 * DECAY)
        return first

    def energy(self):
        total = 0.0
        n = self.buffer.size()
        for _ in range(n):
            value = self.buffer.dequeue()
            total += abs(value)
            self.buffer.enqueue(value)
        return total / n
