"""
Concatenable string range generator.
"""
from collections.abc import Iterable, Iterator
from itertools import chain

from .gen import gen_auto


__all__ = [
    'StrRange',
]


class StrRange(Iterable[str]):
    def __init__(self, start: str, stop: str) -> None:
        self.start = start
        self.stop = stop
        self._before: Iterable[str] | None = None
        self._after:  Iterable[str] | None = None

    @staticmethod
    def _as_iterable(x) -> 'StrRange | Iterable[str] | None':
        # Normalize operand to an iterable (treat str as a single item)
        if isinstance(x, StrRange):
            return x
        if isinstance(x, str):
            return (x,)
        if isinstance(x, Iterable):
            return x
        return None

    def _clone(self, before: Iterable[str] | None, after: Iterable[str] | None) -> 'StrRange':
        y = StrRange(self.start, self.stop)
        y._before = before
        y._after = after
        return y

    def __iter__(self) -> Iterator[str]:
        if self._before is not None:
            yield from self._before
        yield from gen_auto(self.start, self.stop)
        if self._after is not None:
            yield from self._after

    def __add__(self, other) -> 'StrRange':
        it = self._as_iterable(other)
        if it is None:
            return NotImplemented
        return self._clone(
            before=self._before,
            after=chain(self._after or (), it),
        )

    def __radd__(self, other) -> 'StrRange':
        it = self._as_iterable(other)
        if it is None:
            return NotImplemented
        return self._clone(
            before=chain(it, self._before or ()),
            after=self._after,
        )
