import unittest
import random

from strrange.alphabet import detect_symbol_class, Alphabet


class TestAlphabet(unittest.TestCase):
    def test_abc(self):
        alphabet = Alphabet('abc')
        test_cases = [
            ('', 0),
            ('a', 1),
            ('b', 2),
            ('c', 3),
            ('aa', 4),
            ('ab', 5),
            ('ac', 6),
            ('ba', 7),
            ('bb', 8),
            ('bc', 9),
            ('ca', 10),
            ('cb', 11),
            ('cc', 12),
            ('aaa', 13),
            ('aab', 14),
            ('aac', 15),
            ('aba', 16),
            ('abb', 17),
            ('abc', 18),
            ('aca', 19),
            ('acb', 20),
            ('acc', 21),
            ('baa', 22),
            ('bab', 23),
            ('bac', 24),
            ('bba', 25),
            ('bbb', 26),
            ('bbc', 27),
            ('bca', 28),
            ('bcb', 29),
            ('bcc', 30),
            ('caa', 31),
            ('cab', 32),
            ('cac', 33),
            ('cba', 34),
            ('cbb', 35),
            ('cbc', 36),
            ('cca', 37),
            ('ccb', 38),
            ('ccc', 39),
        ]

        for word, expected in test_cases:
            self.assertEqual(alphabet.ordinal(word), expected)
            self.assertEqual(alphabet.word(expected), word)

        self.assertEqual(alphabet.range_length('c', 'aab'), 12)
        r1 = list(alphabet.range('c', 'aab'))
        self.assertEqual(r1, ['c', 'aa', 'ab', 'ac', 'ba', 'bb', 'bc', 'ca', 'cb', 'cc', 'aaa', 'aab'])

        self.assertEqual(alphabet.range_length('aab', 'c'), 12)
        r2 = list(alphabet.range('aab', 'c'))
        self.assertEqual(r2, ['aab', 'aaa', 'cc', 'cb', 'ca', 'bc', 'bb', 'ba', 'ac', 'ab', 'aa', 'c'])

    def test_abcd(self):
        a4 = Alphabet('abcd')
        self.assertEqual(a4.ordinal('aaa'), 16 + 4 + 1)
        self.assertEqual(a4.word(16 + 4 + 1), 'aaa')
        self.assertEqual(a4.ordinal('abc'), 1 * 16 + 2 * 4 + 3)
        self.assertEqual(a4.word(1 * 16 + 2 * 4 + 3), 'abc')

    def test_not_unique_chars(self):
        with self.assertRaises(ValueError):
            Alphabet('abca')

    def test_random(self):
        for pattern in ('0', 'A', 'a', '0A', '0a', 'Aa', '0Aa'):
            sym_class = detect_symbol_class(pattern)
            alphabet = Alphabet.for_symbol_class(sym_class)
            self.assertIsNotNone(alphabet)

            for word_len in range(0, 20):
                for p in range(3):
                    # Generate random words of the given length using alphabet
                    word = ''.join(random.choice(alphabet._alphabet) for _ in range(word_len))
                    n = alphabet.ordinal(word)
                    word_back = alphabet.word(n)
                    self.assertEqual(word, word_back, f"Failed for word '{word}' in sym class '{pattern}'")

    def test_range_length(self):
        alphabet = Alphabet('abcdefghijklmnopqrstuvwxyz')
        self.assertEqual(alphabet.range_length('dead', 'beef'), 35_047)

        alphabet = Alphabet('0123456789abcdefghijklmnopqrstuvwxyz')
        self.assertEqual(alphabet.range_length('foo0', 'baz2'), 204_371)

        alphabet = Alphabet('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
        self.assertEqual(alphabet.range_length('True', 'False'), 227_628_025)

        alphabet = Alphabet('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')
        self.assertEqual(alphabet.range_length('True', 'False'), 44_837_625)

        # alphabet = Alphabet('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')
        # x = alphabet.range_length('000', 'zzz')
        # print(f"{x=}")

    def test_symbol_is_not_in_alphabet(self):
        alphabet = Alphabet('abcdefghijklmnopqrstuvwxyz')
        with self.assertRaises(ValueError):
            alphabet.ordinal('A')
        with self.assertRaises(ValueError):
            alphabet.range_length('DEAD', 'BEEF')

    def test_next(self):
        alphabet = Alphabet('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        self.assertEqual(alphabet.word(alphabet.ordinal('A9') + 1), 'AA')

        alphabet = Alphabet('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        self.assertEqual(alphabet.word(alphabet.ordinal('A9') + 1), 'BA')
