from array import array

class RingBuffer:

    def __init__(self, capacity):
        self._data = array("d", [0] * capacity)
        self._capacity = capacity
        self._front = 0
        self._rear = 0
        self._size = 0

        if capacity < 1:
            raise ValueError

    def capacity(self):
        return self._capacity

    def size(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    def is_full(self):
        return self._size == self._capacity

    def enqueue(self, x):
        if self.is_full():
            raise IndexError
        
        self._data[self._rear] = x
        self._rear += 1
        self._size += 1

        if self._rear == self._capacity:
            self._rear = 0

    def dequeue(self):
        if self.is_empty():
            raise IndexError

        hold = self._data[self._front]
        self._data[self._front] = 0
        self._front += 1
        self._size -= 1 

        if self._front == self._capacity:
            self._front = 0

        return hold

    def peek(self):
        if self.is_empty():
            raise IndexError

        return self._data[self._front]

    def __len__(self):
        return self.size()