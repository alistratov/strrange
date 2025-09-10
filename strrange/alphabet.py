"""
Words to and from ordinals in a given alphabet.
"""
from collections.abc import Iterator


__all__ = [
    'Alphabet',
    'detect_symbol_class',
]


SYM_CLASS_DIGIT = 0x01
SYM_CLASS_LOWER = 0x02
SYM_CLASS_UPPER = 0x04
# SYM_CLASS_OTHER = 0x08


class Alphabet:
    ALPHABET_DIGIT = '0123456789'
    ALPHABET_LOWER = 'abcdefghijklmnopqrstuvwxyz'
    ALPHABET_UPPER = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    CACHE: dict[int, 'Alphabet'] = {}
    # _CACHE_LOCK = threading.Lock()

    # Thread-safety note:
    # We don’t lock around CACHE because in CPython dict get/set are atomic under the GIL.
    # The “check-then-set” isn’t atomic, so two threads might build the same Alphabet once,
    # but instances are immutable/equivalent and last-write-wins — correctness is unchanged.
    # Given the tiny key space (≤7) and cheap construction, avoiding a lock is fine here.

    __slots__ = ('_alphabet', '_base', '_table')

    def __init__(self, alphabet: str) -> None:
        self._alphabet = alphabet
        self._base = len(alphabet)
        self._table = {c: i for i, c in enumerate(alphabet, start=1)}
        if len(self._table) != self._base:
            raise ValueError("Alphabet contains duplicate characters")

    @classmethod
    def for_symbol_class(cls, sym_class: int) -> 'Alphabet':
        if sym_class in cls.CACHE:
            return cls.CACHE[sym_class]

        assert sym_class != 0
        abc = ''
        if sym_class & SYM_CLASS_DIGIT:
            abc += cls.ALPHABET_DIGIT
        if sym_class & SYM_CLASS_UPPER:
            abc += cls.ALPHABET_UPPER
        if sym_class & SYM_CLASS_LOWER:
            abc += cls.ALPHABET_LOWER
        assert abc != ''
        rv = cls(alphabet=abc)
        # with cls._CACHE_LOCK:
        cls.CACHE[sym_class] = rv
        return rv

    def ordinal(self, word: str) -> int:
        """
        Converts a word to its ordinal number in a given alphabet.
        E.g. for alphabet 'abc':
        '' -> 0, 'a' -> 1, 'b' -> 2, 'c' -> 3, 'aa' -> 4, 'ab' -> 5, ...
        """
        n = 0
        for i, c in enumerate(reversed(word)):
            try:
                n += self._table[c] * (self._base ** i)
            except KeyError:
                msg = f"Character '{c}' not in alphabet '{self._alphabet}'"
                raise ValueError(msg)

        return n

    def word(self, n: int) -> str:
        """
        Converts an ordinal number to its corresponding word in a given alphabet.
        E.g. for alphabet 'abc':
        0 -> '', 1 -> 'a', 2 -> 'b', 3 -> 'c', 4 -> 'aa', 5 -> 'ab', ...
        """
        if n == 0:
            return ''

        # Determine the length of the word and adjust n
        length = 1
        count = self._base
        while n > count:
            n -= count
            length += 1
            count *= self._base

        n -= 1  # To zero-based index
        chars = []
        for _ in range(length):
            n, r = divmod(n, self._base)
            chars.append(self._alphabet[r])

        return ''.join(reversed(chars))

    def range(self, start: str, stop: str) -> Iterator[str]:
        n1 = self.ordinal(start)
        n2 = self.ordinal(stop)
        r = range(n1, n2 + 1) if n1 <= n2 else range(n1, n2 - 1, -1)
        for n in r:
            yield self.word(n)

    def range_length(self, start: str, stop: str) -> int:
        return abs(self.ordinal(stop) - self.ordinal(start)) + 1


def detect_symbol_class(s: str) -> int:
    rv = 0
    for c in s:
        if '0' <= c <= '9':
            rv |= SYM_CLASS_DIGIT
        elif 'A' <= c <= 'Z':
            rv |= SYM_CLASS_UPPER
        elif 'a' <= c <= 'z':
            rv |= SYM_CLASS_LOWER
        else:
            # Break on non-alphanumeric character
            return 0
    return rv
