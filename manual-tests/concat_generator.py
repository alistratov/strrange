
def gen(n: int = 1):
    for i in range(1, n + 1):
        yield str(i)


class ag:
    """
    Addable generator
    """
    def __init__(self, n: int = 1, left=None, right=None):
        self._n = n
        self._left = left
        self._right = right

    def __iter__(self):
        if self._left is not None:
            yield from self._left
        yield from gen(self._n)
        if self._right is not None:
            yield from self._right

    def __add__(self, other):
        return ag(self._n, right=other)

    def __radd__(self, other):
        return ag(self._n, left=other)

# class IterableBase:
#     """
#     A base class for iterable objects that supports iteration, counting, and resetting.
#     Derived classes should implement the _create_iterator method.
#     """
#
#     def __init__(self):
#         """
#         Initializes the iterable object.
#         """
#         self._iterator: Iterator = self._create_iterator()
#         self._buffer: List[Any] = []  # Stores iterated elements
#         self._index: int = 0           # Current position in iteration
#         self._exhausted: bool = False  # Indicates if the iterator is exhausted
#         self._total_count: Optional[int] = None  # Total count, if known
#
#     def _create_iterator(self) -> Iterator:
#         """
#         Creates and returns an iterator.
#         Must be implemented by derived classes.
#         """
#         raise NotImplementedError("Derived classes must implement _create_iterator")
#
#     def __iter__(self):
#         """
#         Returns the iterator object itself.
#         """
#         return self
#
#     def __next__(self):
#         """
#         Returns the next item from the iterator or buffer.
#         Raises StopIteration when no more items are available.
#         """
#         if self._index < len(self._buffer):
#             # Return from buffer if available
#             value = self._buffer[self._index]
#         else:
#             if self._exhausted:
#                 # Iterator already exhausted
#                 raise StopIteration
#             try:
#                 # Fetch next item from the internal iterator
#                 value = next(self._iterator)
#                 self._buffer.append(value)
#             except StopIteration:
#                 self._exhausted = True
#                 raise StopIteration
#         self._index += 1
#         return value
#
#     def count(self) -> int:
#         """
#         Returns the total number of elements.
#         - If _total_count is set (in derived classes), returns it.
#         - Otherwise, iterates through all remaining elements to count them.
#         """
#         if self._total_count is not None:
#             return self._total_count
#
#         if self._exhausted:
#             return len(self._buffer)
#
#         # Iterate through the remaining iterator to count elements
#         count = len(self._buffer)
#         try:
#             while True:
#                 value = next(self._iterator)
#                 self._buffer.append(value)
#                 count += 1
#         except StopIteration:
#             self._exhausted = True
#
#         return count
#
#     def reset(self):
#         """
#         Resets the iteration to the beginning.
#         """
#         self._index = 0
#
#     def seek(self, index: int):
#         """
#         Seeks to the specified index in the iteration.
#         """
#         if index < 0:
#             raise ValueError("Index must be non-negative")
#         if index < self._index:
#             # Reset if the index is before the current position
#             self.reset()
#         for _ in range(index - self._index):
#             try:
#                 next(self)
#             except StopIteration:
#                 break


def main():
    # print('gen', list(gen(3) + gen(4)))
    print('ag:', ag(3) + ag(4))


if __name__ == '__main__':
    main()
