import time

from strrange.util import string_period, is_repeating_substring


def main():
    N = 100_000
    cases = [
        'a',
        'aa',
        'aaa',
        'aaaaa',
        'a' * 10,
        'a' * 20,
        'a' * 50,
        'a' * 100,
    ]

    for c in cases:
        w1, n1 = string_period(c)
        w2, n2 = is_repeating_substring(c)
        assert (w1, n1) == (w2, n2)

    tm1 = time.perf_counter()
    for i in range(N):
        for c in cases:
            string_period(c)
    tm2 = time.perf_counter()
    print(f'string_period: {tm2 - tm1:.6f} seconds')

    tm1 = time.perf_counter()
    for i in range(N):
        for c in cases:
            is_repeating_substring(c)
    tm2 = time.perf_counter()
    print(f'get_repeating_substring: {tm2 - tm1:.6f} seconds')


if __name__ == '__main__':
    main()
