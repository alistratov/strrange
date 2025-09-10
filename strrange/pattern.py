"""
Utilities for analyzing string patterns.
"""
import re


__all__ = [
    'pattern',
    'fallback_digits',
    'fallback_alnum',
]


def pattern(start: str, stop: str) -> tuple[str, str, str, str]:
    """
    Extracts the common prefix and suffix from start and stop strings.
    The prefix is the longest common starting substring of any characters.
    The suffix is the longest common ending substring of any characters.
    The prefix and suffix may be empty strings and must not overlap.
    Returns a tuple (prefix, start_var, stop_var, suffix).
    """
    # Find common prefix
    prefix_length = 0
    for s_char, e_char in zip(start, stop):
        if s_char == e_char:
            prefix_length += 1
        else:
            break
    prefix = start[:prefix_length]

    # Find common suffix, not overlapping with prefix
    suffix_length = 0
    for s_char, e_char in zip(reversed(start[prefix_length:]), reversed(stop[prefix_length:])):
        if s_char == e_char:
            suffix_length += 1
        else:
            break
    suffix = start[len(start)-suffix_length:] if suffix_length > 0 else ''

    # Extract the variable parts
    start_var = start[prefix_length:len(start) - suffix_length] if suffix_length > 0 else start[prefix_length:]
    stop_var = stop[prefix_length:len(stop) - suffix_length] if suffix_length > 0 else stop[prefix_length:]

    return prefix, start_var, stop_var, suffix


def fallback_digits(prefix: str, start: str, stop: str, suffix: str) -> tuple[str, str, str, str]:
    """
    Moves trailing digits from the prefix, or leading ones from the suffix,
    into the variable parts. Returns (prefix, start_var, stop_var, suffix).
    """
    m = re.search(r'([0-9]+)$', prefix)
    if m:
        digit_part = m.group(1)
        prefix = prefix[:-len(digit_part)]
        start = digit_part + start
        stop = digit_part + stop

    m = re.match(r'^([0-9]+)', suffix)
    if m:
        digit_part = m.group(1)
        suffix = suffix[len(digit_part):]
        start = start + digit_part
        stop = stop + digit_part

    return prefix, start, stop, suffix


def fallback_alnum(prefix: str, start: str, stop: str, suffix: str) -> tuple[str, str, str, str]:
    """
    Moves trailing alphanumeric characters from the prefix, or leading ones from the suffix,
    into the variable parts. Returns (prefix, start_var, stop_var, suffix).
    """
    m = re.search(r'([A-Za-z0-9]+)$', prefix)
    if m:
        letter_part = m.group(1)
        prefix = prefix[:-len(letter_part)]
        start = letter_part + start
        stop = letter_part + stop

    # Unreachable code
    # m = re.match(r'^([A-Za-z0-9]+)', suffix)
    # if m:
    #     letter_part = m.group(1)
    #     suffix = suffix[len(letter_part):]
    #     start = start + letter_part
    #     stop = stop + letter_part

    return prefix, start, stop, suffix
