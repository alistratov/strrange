import time

from strrange.util import is_alphanum
from strrange.alphabet import detect_symbol_class


def main():
    N = 100_000
    cases = [
        'abc123',
        'abc123!',
        '!@#',
        'abcXYZ',
        '123456',
        'abc',
        'ABC',
        '123',
        '!!!',
        'abc123XYZ!@#',
    ]

    tm1 = time.perf_counter()
    for i in range(N):
        for c in cases:
            is_alphanum(c)
    tm2 = time.perf_counter()
    print(f'is_alphanum: {tm2 - tm1:.6f} seconds')

    tm1 = time.perf_counter()
    for i in range(N):
        for c in cases:
            detect_symbol_class(c)
    tm2 = time.perf_counter()
    print(f'detect_symbol_class: {tm2 - tm1:.6f} seconds')


if __name__ == '__main__':
    main()
