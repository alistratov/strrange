"""
String range generator function.
"""
from collections.abc import Iterator

from .util import (is_alphanum, is_digits, is_alpha,
                   is_padded_int, calculate_padding_width,
                   is_repeating_substring)
from .alphabet import detect_symbol_class, Alphabet
from .pattern import pattern, fallback_digits, fallback_alnum


__all__ = [
    'gen_integers',
    'gen_repeating',
    'gen_words',
    'gen_auto',
]


MAX_GEN_LENGTH = 238_328  # Distance between '000' and 'zzz'


def gen_integers(start: int, stop: int, width: int | None, pad_char: str) -> Iterator[str]:
    """
    Generate a range of numbers (stringified) from start to stop (inclusive), with optional padding.
    """
    if start <= stop:
        r = range(start, stop + 1)
    else:
        r = range(start, stop - 1, -1)

    # No padding
    if width is None:
        yield from (str(n) for n in r)
        return

    # Padding required
    assert width >= 2, 'Width must be at least 2'
    assert pad_char in ('0', ' '), 'Padding character must be "0" or space'
    if pad_char == '0':
        yield from (f"{n:0{width}d}" for n in r)
    else:
        yield from (f"{n:>{width}d}" for n in r)


def gen_repeating(start_count: int, stop_count: int, unit: str) -> Iterator[str]:
    """
    Generate a range of strings made of repeating substrings.
    """
    assert start_count >= 0
    assert stop_count >= 0
    r = range(start_count, stop_count + 1) if start_count <= stop_count else range(start_count, stop_count - 1, -1)
    for k in r:
        yield unit * k


def gen_words(start: str, stop: str) -> Iterator[str]:
    """
    Generate a range of "words" from start to stop (inclusive),
    where "words" are strings made of letters (a-z, A-Z) and/or digits (0-9).
    The "alphabet" is determined by the common symbol classes of start and stop.
    """
    sc1 = detect_symbol_class(start)
    assert sc1 != 0
    sc2 = detect_symbol_class(stop)
    assert sc2 != 0
    common = sc1 | sc2
    abc = Alphabet.for_symbol_class(common)
    yield from abc.range(start, stop)


def gen_auto(start: str, stop: str) -> Iterator[str]:
    """
    Automatically determine the type of range to generate.
    """
    if not isinstance(start, str) or not isinstance(stop, str):
        raise TypeError("start and stop must be str")

    # 1. If `start` and `stop` are the same, return sequence with just `start`
    # 2. If both are empty, return empty sequence
    if start == stop:
        if start != '':
            yield start
        return

    # 3. If both `start` and `stop` can be parsed as integers, return integer range
    is_start_int, start_n, start_pad_char, start_pad_len = is_padded_int(start)
    if is_start_int:
        is_stop_int, stop_n, stop_pad_char, stop_pad_len = is_padded_int(stop)
        if is_stop_int:
            # Padding is fully determined by `start` value.
            width = calculate_padding_width(start_n, start_pad_char, start_pad_len)
            yield from gen_integers(start_n, stop_n, width, start_pad_char)
            return

    # Length difference
    len_diff = abs(len(start) - len(stop))

    # 4. If repeating substring pattern is detected, return repeating substring range.
    # Also handles the case where one of the strings is empty and the other is
    # a repeating (more than once) substring.
    if len_diff >= 2:
        k1, unit1 = is_repeating_substring(start)
        k2, unit2 = is_repeating_substring(stop)
        if k1 > 1 or k2 > 1:
            if k1 == 0:
                yield from gen_repeating(0, k2, unit2)
                return
            elif k2 == 0:
                yield from gen_repeating(k1, 0, unit1)
                return
            elif unit1 == unit2:
                yield from gen_repeating(k1, k2, unit1)
                return

    # Split to prefix, variable parts and suffix
    prefix, start_var, stop_var, suffix = pattern(start, stop)
    var_len_diff = abs(len(start_var) - len(stop_var))

    # 5. Repeating substring pattern in variable parts, but not numbers
    if var_len_diff >= 2 and not is_digits(start_var) and not is_digits(stop_var):
        k1, unit1 = is_repeating_substring(start_var)
        k2, unit2 = is_repeating_substring(stop_var)
        if k1 > 1 or k2 > 1:
            if k1 == 0:
                yield from (prefix + v + suffix for v in gen_repeating(0, k2, unit2))
                return
            else:
                assert k2 == 0
                yield from (prefix + v + suffix for v in gen_repeating(k1, 0, unit1))
                return
            # Unreachable code: prefix includes repeating substring pattern, so k1 or k2 must be 0
            # elif unit1 == unit2:
            #     yield from (prefix + v + suffix for v in gen_repeating(k1, k2, unit1))
            #     return

    # 6. Alpha range, without digits in variable parts
    if is_alpha(start_var) and is_alpha(stop_var):
        # Note: the code is the same as gen_words(), but with additional check of sequence length.
        # If the length is too large, it is better to refuse generation.
        sc1 = detect_symbol_class(start_var)
        assert sc1 != 0
        sc2 = detect_symbol_class(stop_var)
        assert sc2 != 0
        common = sc1 | sc2
        abc = Alphabet.for_symbol_class(common)
        gen_length = abc.range_length(start_var, stop_var)
        if gen_length <= MAX_GEN_LENGTH:
            yield from (prefix + v + suffix for v in abc.range(start_var, stop_var))
            return

    # Return digits back in variable parts
    prefix, start_var, stop_var, suffix = fallback_digits(prefix, start_var, stop_var, suffix)
    # print(f"DEBUG 1: {prefix=}, {start_var=}, {stop_var=}, {suffix=}")

    # 7. If variable parts are both integers, return integer range with prefix and suffix
    is_start_int, start_n, start_pad_char, start_pad_len = is_padded_int(start_var)
    if is_start_int:
        is_stop_int, stop_n, stop_pad_char, stop_pad_len = is_padded_int(stop_var)
        if is_stop_int:
            width = calculate_padding_width(start_n, start_pad_char, start_pad_len)
            yield from (prefix + v + suffix for v in gen_integers(start_n, stop_n, width, start_pad_char))
            return

    # Return letters back in variable parts
    prefix, start_var, stop_var, suffix = fallback_alnum(prefix, start_var, stop_var, suffix)
    # print(f"DEBUG 2: {prefix=}, {start_var=}, {stop_var=}, {suffix=}")

    # 8. Alphanumeric range
    # Note: the code is the same as gen_words(), but with additional check of sequence length.
    # If the length is too large, it is better to refuse generation.
    if is_alphanum(start_var) and is_alphanum(stop_var):
        sc1 = detect_symbol_class(start_var)
        assert sc1 != 0
        sc2 = detect_symbol_class(stop_var)
        assert sc2 != 0
        common = sc1 | sc2
        abc = Alphabet.for_symbol_class(common)
        gen_length = abc.range_length(start_var, stop_var)
        if gen_length <= MAX_GEN_LENGTH:
            yield from (prefix + v + suffix for v in abc.range(start_var, stop_var))
            return

    # print(f'DEBUG: not covered case: {start=}, {stop=}')
    yield from (start, stop)
