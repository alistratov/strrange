"""
String range generator utility functions.
"""
import re


__all__ = [
    'is_alphanum',
    'is_alpha',
    'is_digits',
    'is_padded_int',
    'calculate_padding_width',
    'is_repeating_substring',
]


RE_ALPHANUM = re.compile(r'^[0-9A-Za-z]+$')
RE_ALPHA = re.compile(r'^[A-Za-z]+$')
RE_NUM = re.compile(r'^[0-9]+$')


def is_alphanum(s: str) -> bool:
    # Not the same as str.isalnum()
    return bool(RE_ALPHANUM.match(s))


def is_alpha(s: str) -> bool:
    # Not the same as str.isalpha()
    return bool(RE_ALPHA.match(s))


def is_digits(s: str) -> bool:
    # Not the same as str.isdigit()
    return bool(RE_NUM.match(s))


def is_padded_int(s: str) -> tuple[bool, int, str, int]:
    """
    Tries to parse a string as an integer, returns a tuple (is_integer, value, pad_char, pad_length).
    Input is guaranteed to be a string.

    If the string starts with '0' or space, pad_char is that character and pad_length is
    the number of existing padding characters (all zeroes is a special case of this).
    """
    if len(s) > 1 and s[0] in ' 0':
        pad_char = s[0]
        pad_length = len(s) - len(s.lstrip(pad_char))
    else:
        pad_char = ''
        pad_length = 0

    try:
        return True, int(s), pad_char, pad_length
    except ValueError:
        # Parsing floats is disabled
        # try:
        #     return True, int(float(s)), pad_char, pad_length
        # except (ValueError, OverflowError):
        #     return False, None, '', 0
        return False, 0, '', 0


def calculate_padding_width(num: int, pad_char: str, pad_len: int) -> int | None:
    """
    Converts padding character and length to width for formatted string.
    If no padding is required, returns None.
    Zero, padded with zeroes, is a special case.
    """
    if pad_char == '':
        return None
    elif num == 0 and pad_char == '0':
        return pad_len
    else:
        return pad_len + len(str(num))


def string_period(s: str) -> tuple[int, str]:
    """
    Returns (unit, k) where s == unit * k and unit is the smallest repeating unit.
    If no repetition, returns (s, 1).
    """
    n = len(s)
    assert n > 0

    # Build KMP prefix function (lps[i] = length of longest proper prefix == suffix for s[:i+1])
    lps = [0] * n
    j = 0
    for i in range(1, n):
        while j > 0 and s[i] != s[j]:
            j = lps[j - 1]
        if s[i] == s[j]:
            j += 1
            lps[i] = j

    p = n - lps[-1]  # candidate period length
    if p != n and n % p == 0:  # true repetition
        return n // p, s[:p]
    else:
        return 1, s


def is_repeating_substring(s: str) -> tuple[int, str]:
    n = len(s)
    if n == 0:
        return 0, ''
    if n == 1:
        return 1, s

    # Fast path for single character strings
    if all(ch == s[0] for ch in s[1:]):
        return n, s[0]

    return string_period(s)
