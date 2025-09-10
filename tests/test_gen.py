import unittest

from strrange.gen import gen_words, gen_repeating, gen_integers


def ln(start, stop, pad_char='', width=None):
    return list(gen_integers(start, stop, width, pad_char))


def lw(start, stop):
    return list(gen_words(start, stop))


def nw(start, stop):
    # Length without storing all elements in memory
    n = 0
    for _ in gen_words(start, stop):
        n += 1
    return n


class TestGenerators(unittest.TestCase):
    def test_integers_without_padding(self):
        self.assertEqual(ln(0, 0), ['0'])
        self.assertEqual(ln(1, 1), ['1'])
        self.assertEqual(ln(-1, -1), ['-1'])
        self.assertEqual(ln(0, 2), ['0', '1', '2'])
        self.assertEqual(ln(2, 0), ['2', '1', '0'])
        self.assertEqual(ln(-2, 2), ['-2', '-1', '0', '1', '2'])
        self.assertEqual(ln(2, -2), ['2', '1', '0', '-1', '-2'])

    def test_integers_with_padding(self):
        self.assertEqual(ln(0, 0, '0', 3), ['000'])
        self.assertEqual(ln(1, 1, '0', 3), ['001'])
        self.assertEqual(ln(-1, -1, '0', 3), ['-01'])

        self.assertEqual(ln(0, 0, ' ', 3), ['  0'])
        self.assertEqual(ln(1, 1, ' ', 3), ['  1'])
        self.assertEqual(ln(-1, -1, ' ', 3), [' -1'])

        self.assertEqual(ln(0, 2, '0', 2), ['00', '01', '02'])
        self.assertEqual(ln(1, 3, '0', 2), ['01', '02', '03'])
        self.assertEqual(ln(1, 3, '0', 3), ['001', '002', '003'])

        self.assertEqual(ln(0, 2, ' ', 2), [' 0', ' 1', ' 2'])
        self.assertEqual(ln(1, 3, ' ', 2), [' 1', ' 2', ' 3'])
        self.assertEqual(ln(1, 3, ' ', 3), ['  1', '  2', '  3'])

        self.assertEqual(ln(-1, 1, '0', None), ['-1', '0', '1'])
        # self.assertEqual(ls(-1, 1, '0', 1), ['-1', '0', '1'])
        self.assertEqual(ln(-1, 1, '0', 2), ['-1', '00', '01'])
        self.assertEqual(ln(-1, 1, '0', 3), ['-01', '000', '001'])

        self.assertEqual(ln(-1, 1, ' ', None), ['-1', '0', '1'])
        # self.assertEqual(ln(-1, 1, ' ', 1), ['-1', '0', '1'])
        self.assertEqual(ln(-1, 1, ' ', 2), ['-1', ' 0', ' 1'])
        self.assertEqual(ln(-1, 1, ' ', 3), [' -1', '  0', '  1'])

        self.assertEqual(ln(99, 101, '0', 2), ['99', '100', '101'])
        self.assertEqual(ln(99, 101, '0', 3), ['099', '100', '101'])
        self.assertEqual(ln(99, 101, '0', 4), ['0099', '0100', '0101'])

        self.assertEqual(ln(99, 101, ' ', 2), ['99', '100', '101'])
        self.assertEqual(ln(99, 101, ' ', 3), [' 99', '100', '101'])
        self.assertEqual(ln(99, 101, ' ', 4), ['  99', ' 100', ' 101'])

    def test_words(self):
        self.assertEqual(lw('0', '3'), ['0', '1', '2', '3'])
        self.assertEqual(lw('999', '995'), ['999', '998', '997', '996', '995'])

        self.assertEqual(lw('a', 'd'), ['a', 'b', 'c', 'd'])
        self.assertEqual(lw('z', 'w'), ['z', 'y', 'x', 'w'])

        self.assertEqual(lw('A', 'D'), ['A', 'B', 'C', 'D'])
        self.assertEqual(lw('Z', 'W'), ['Z', 'Y', 'X', 'W'])

        self.assertEqual(lw('a1', 'a3'), ['a1', 'a2', 'a3'])
        self.assertEqual(lw('A1', 'A3'), ['A1', 'A2', 'A3'])

        self.assertEqual(lw('Aa', 'Ac'), ['Aa', 'Ab', 'Ac'])
        self.assertEqual(lw('xA', 'xC'), ['xA', 'xB', 'xC'])

        with self.assertRaises(AssertionError):
            lw('-1', '1')  # contains minus

        with self.assertRaises(AssertionError):
            lw('file001.txt', 'file003.txt')  # contains dot

        self.assertEqual(lw('file001', 'file003'), ['file001', 'file002', 'file003'])

        self.assertEqual(
            lw('A', 'AA'),
            ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
             'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
             'AA'])

        self.assertEqual(
            lw('A0', 'B2'),
            ['A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
             'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ', 'AK', 'AL', 'AM',
             'AN', 'AO', 'AP', 'AQ', 'AR', 'AS', 'AT', 'AU', 'AV', 'AW', 'AX', 'AY', 'AZ',
             'B0', 'B1', 'B2'])

        # A .. Z, 00, 01 .. 0A .. 0Z, 10 .. 1Z, ..., 90 .. 9Z, A0
        t = lw('A', 'A0')
        self.assertEqual(t[0], 'A')
        self.assertEqual(t[25], 'Z')
        self.assertEqual(t[26], '00')
        self.assertEqual(t[61], '0Z')
        self.assertEqual(t[-2], '9Z')
        self.assertEqual(t[-1], 'A0')
        self.assertEqual(len(t), 26 + 36 * 10 + 1)

        t = lw('A', 'Aa')
        self.assertEqual(t[0], 'A')
        self.assertEqual(t[25], 'Z')
        self.assertEqual(t[26], 'a')
        self.assertEqual(t[-2], 'AZ')
        self.assertEqual(t[-1], 'Aa')
        self.assertEqual(len(t), 79)

        t = lw('dea', 'bee')
        self.assertEqual(t[1], 'ddz')
        self.assertEqual(t[-2], 'bef')
        self.assertEqual(len(t), 1349)

        # Long sequences, only check length
        self.assertEqual(nw('foo', 'bar'), 3066)

        # True, Truf, Trug, ... Falsd, False
        # for w in gen_words(str(True), str(False)):
        #     ...
        # Total length of sequence is 44_837_625

    def test_repeating(self):
        self.assertEqual(list(gen_repeating(0, 0, 'a')), [''])
        self.assertEqual(list(gen_repeating(0, 0, 'abc')), [''])

        self.assertEqual(list(gen_repeating(0, 1, 'a')), ['', 'a'])
        self.assertEqual(list(gen_repeating(0, 1, 'abc')), ['', 'abc'])

        self.assertEqual(list(gen_repeating(1, 0, 'a')), ['a', ''])
        self.assertEqual(list(gen_repeating(1, 0, 'abc')), ['abc', ''])

        self.assertEqual(list(gen_repeating(1, 5, 'a')), ['a', 'aa', 'aaa', 'aaaa', 'aaaaa'])
        self.assertEqual(list(gen_repeating(5, 1, 'a')), ['aaaaa', 'aaaa', 'aaa', 'aa', 'a'])
        self.assertEqual(list(gen_repeating(1, 3, '...')), ['...', '......', '.........'])
        self.assertEqual(list(gen_repeating(3, 1, '...')), ['.........', '......', '...'])
        self.assertEqual(list(gen_repeating(1, 3, '.×.')), ['.×.', '.×..×.', '.×..×..×.'])
        self.assertEqual(list(gen_repeating(3, 1, '.×.')), ['.×..×..×.', '.×..×.', '.×.'])
