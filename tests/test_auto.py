import unittest

from strrange.gen import gen_auto


def ls(start, stop):
    return list(gen_auto(start, stop))


class TestAuto(unittest.TestCase):
    def test_type_error(self):
        cases = [
            ([], ''),
            ({}, ''),
            (set(), ''),
            ((), ''),
            (1.5, '2.5'),
            ('a', 5),
            ('a', 5.5),
            (None, None),
            (None, 5),
            (None, '5'),
            ('a', None),
            (5, None),
            (5.5, None),
        ]
        for start, stop in cases:
            with self.subTest(start=start, stop=stop):
                with self.assertRaises(TypeError):
                    ls(start, stop)

    def test_equal(self):
        # If `start` and `stop` are empty, return nothing
        self.assertEqual(ls('', ''), [])

        # If `start` and `stop` are the same, return sequence with just `start`
        self.assertEqual(ls('abc', 'abc'), ['abc'])
        self.assertEqual(ls('1', '1'), ['1'])
        self.assertEqual(ls(str(1_000), str(50 * 20)), ['1000'])
        self.assertEqual(ls(' ', ' '), [' '])

    def test_numbers(self):
        self.assertEqual(ls('0', '0'), ['0'])
        self.assertEqual(ls('1', '5'), ['1', '2', '3', '4', '5'])
        self.assertEqual(ls('5', '1'), ['5', '4', '3', '2', '1'])
        self.assertEqual(ls('-1', '1'), ['-1', '0', '1'])
        self.assertEqual(ls('1', '-1'), ['1', '0', '-1'])

        t = ls('1', '+1000')
        self.assertEqual(t[0], '1')
        self.assertEqual(t[-1], '1000')
        self.assertEqual(len(t), 1000)

        # self.assertEqual(ls('1.4142', '3.1416'), ['1', '2', '3'])
        # self.assertEqual(ls('3.1416', '-1.4142'), ['3', '2', '1', '0', '-1'])

    def test_numbers_with_padding(self):
        # Zero-padding
        self.assertEqual(ls('01', '03'), ['01', '02', '03'])
        self.assertEqual(ls('001', '005'), ['001', '002', '003', '004', '005'])
        self.assertEqual(ls('001', '5'), ['001', '002', '003', '004', '005'])

        self.assertEqual(ls('00', '03'), ['00', '01', '02', '03'])
        self.assertEqual(ls('00000', '3'), ['00000', '00001', '00002', '00003'])

        # The sign does not cause padding
        # TODO: reconsider this decision?
        self.assertEqual(ls('-003', '1'), ['-3', '-2', '-1', '0', '1'])
        self.assertEqual(ls('+003', '1'), ['3', '2',  '1'])

        # self.assertEqual(ls('00e1', '3'), ['00', '01', '02', '03'])
        # self.assertEqual(ls('001.5e+2', '152'), ['00150', '00151', '00152'])

        # Space-padding
        self.assertEqual(ls(' 1', ' 3'), [' 1', ' 2', ' 3'])
        self.assertEqual(ls('  1', '  5'), ['  1', '  2', '  3', '  4', '  5'])
        self.assertEqual(ls('  1', '5'), ['  1', '  2', '  3', '  4', '  5'])

        self.assertEqual(ls(' 0', ' 3'), [' 0', ' 1', ' 2', ' 3'])
        self.assertEqual(ls('    0', '3'), ['    0', '    1', '    2', '    3'])

        self.assertEqual(ls(' 1', '-1'), [' 1', ' 0', '-1'])
        self.assertEqual(ls('  1', '-1'), ['  1', '  0', ' -1'])
        self.assertEqual(ls('-1', '1'), ['-1', '0', '1'])
        self.assertEqual(ls(' -1', '1'), [' -1', '  0', '  1'])

        # Not parsed as numbers, so no padding
        # self.assertEqual(ls('0-1', '3'), ['00', '01', '02', '03'])
        # self.assertEqual(ls('- 3', '1'), [' -3', ' -2', ' -1', '  0', '  1'])

    def test_repeating_simple(self):
        # No prefix/suffix, just repeating substring
        self.assertEqual(
            ls('', 'aa'),
            ['', 'a', 'aa'])
        self.assertEqual(
            ls('aa', ''),
            ['aa', 'a', ''])

        self.assertEqual(
            ls('i', 'iii'),
            ['i', 'ii', 'iii'])
        self.assertEqual(
            ls('iii', 'i'),
            ['iii', 'ii', 'i'])

        self.assertEqual(
            ls('.', '.....'),
            ['.', '..', '...', '....', '.....'])
        self.assertEqual(
            ls('ab', 'abab'),
            ['ab', 'abab'])
        self.assertEqual(
            ls('ab', 'ababab'),
            ['ab', 'abab', 'ababab'])
        self.assertEqual(
            ls('_*', '_*_*_*_*'),
            ['_*', '_*_*', '_*_*_*', '_*_*_*_*'])

        # Min length diff is required
        # Fall back to alphanumeric range
        # self.assertEqual(
        #     ls('a', 'aa'),
        #     ['a', 'aa'])
        # self.assertEqual(
        #     ls('aa', 'a'),
        #     ['aa', 'a'])

    def test_repeating_complex(self):
        self.assertEqual(
            ls('i)', 'iii)'),
            ['i)', 'ii)', 'iii)'])
        self.assertEqual(
            ls('iii.', 'i.'),
            ['iii.', 'ii.', 'i.'])

        self.assertEqual(
            ls('<a>', '<aaaaaa>'),
            ['<a>', '<aa>', '<aaa>', '<aaaa>', '<aaaaa>', '<aaaaaa>'])
        self.assertEqual(
            ls('<aaaaaa>', '<>'),
            ['<aaaaaa>', '<aaaaa>', '<aaaa>', '<aaa>', '<aa>', '<a>', '<>'])
        self.assertEqual(
            ls('<aaaaaa>', '<>'),
            ['<aaaaaa>', '<aaaaa>', '<aaaa>', '<aaa>', '<aa>', '<a>', '<>'])
        self.assertEqual(
            ls('Sex', 'Seeeeeex'),
            ['Sex', 'Seex', 'Seeex', 'Seeeex', 'Seeeeex', 'Seeeeeex'])
        self.assertEqual(
            ls('Seeeeeex', 'Sex'),
            ['Seeeeeex', 'Seeeeex', 'Seeeex', 'Seeex', 'Seex', 'Sex'])

        self.assertEqual(
            ls('N<a>', 'N<a><a><a>'),
            ['N<a>', 'N<a><a>', 'N<a><a><a>'])
        self.assertEqual(
            ls('N<a>T', 'N<a>TN<a>TN<a>T'),
            ['N<a>T', 'N<a>TN<a>T', 'N<a>TN<a>TN<a>T'])

    def test_number_inside(self):
        self.assertEqual(ls('1.5', '3.5'), ['1.5', '2.5', '3.5'])
        self.assertEqual(ls('3.5', '1.5'), ['3.5', '2.5', '1.5'])

        self.assertEqual(
            ls('file1.txt', 'file3.txt'),
            ['file1.txt', 'file2.txt', 'file3.txt'])
        self.assertEqual(
            ls('file001.txt', 'file003.txt'),
            ['file001.txt', 'file002.txt', 'file003.txt'])
        # Padding is preserved from the start
        self.assertEqual(
            ls('file001.txt', 'file3.txt'),
            ['file001.txt', 'file002.txt', 'file003.txt'])
        self.assertEqual(
            ls('file1', 'file10'),
            ['file1', 'file2', 'file3', 'file4', 'file5',
             'file6', 'file7', 'file8', 'file9', 'file10'])
        self.assertEqual(
            ls('1.png', '12.png'),
            ['1.png', '2.png', '3.png', '4.png', '5.png',
             '6.png', '7.png', '8.png', '9.png', '10.png',
             '11.png', '12.png'])
        self.assertEqual(
            ls('access.log.1', 'access.log.4'),
            ['access.log.1', 'access.log.2', 'access.log.3', 'access.log.4'])

        t = ls('img-10.jpg', 'img900.jpg')
        self.assertEqual(t[0], 'img-10.jpg')
        self.assertEqual(t[10], 'img0.jpg')
        self.assertEqual(t[-1], 'img900.jpg')
        self.assertEqual(len(t), 911)

        self.assertEqual(
            ls('S01E01.mkv', 'S01E08.mkv'),
            ['S01E01.mkv', 'S01E02.mkv', 'S01E03.mkv', 'S01E04.mkv',
             'S01E05.mkv', 'S01E06.mkv', 'S01E07.mkv', 'S01E08.mkv'])

        # It's alphanum sequence
        t = ls('S1E1.mkv', 'S2E4.mkv')
        self.assertEqual(t[0], 'S1E1.mkv')
        self.assertEqual(t[1], 'S1E2.mkv')
        self.assertEqual(t[-8], 'S2DX.mkv')
        self.assertEqual(t[-1], 'S2E4.mkv')
        self.assertEqual(len(t), 1300)

        # It's also alphanum sequence, not hex
        t = ls('0x1A', '0x2F')
        self.assertEqual(len(t), 68)

    def test_alphanum(self):
        self.assertEqual(
            ls('a', 'aa'),
            ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
             'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
             'aa'])
        self.assertEqual(
            ls('aa', 'a'),
            ['aa',
             'z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n',
             'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f', 'e', 'd', 'c', 'b', 'a'])

        self.assertEqual(ls('a', 'd'), ['a', 'b', 'c', 'd'])
        self.assertEqual(ls('z', 'w'), ['z', 'y', 'x', 'w'])

        self.assertEqual(ls('A', 'D'), ['A', 'B', 'C', 'D'])
        self.assertEqual(ls('Z', 'W'), ['Z', 'Y', 'X', 'W'])

        self.assertEqual(ls('a1', 'a3'), ['a1', 'a2', 'a3'])
        self.assertEqual(ls('A1', 'A3'), ['A1', 'A2', 'A3'])

        self.assertEqual(ls('Aa', 'Ac'), ['Aa', 'Ab', 'Ac'])
        self.assertEqual(ls('xA', 'xC'), ['xA', 'xB', 'xC'])
        self.assertEqual(ls('Au', 'Cu'), ['Au', 'Bu', 'Cu'])

        self.assertEqual(ls('7', 'A'), ['7', '8', '9', 'A'])

        self.assertEqual(
            ls('A0', 'B2'),
            ['A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
             'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ', 'AK', 'AL', 'AM',
             'AN', 'AO', 'AP', 'AQ', 'AR', 'AS', 'AT', 'AU', 'AV', 'AW', 'AX', 'AY', 'AZ',
             'B0', 'B1', 'B2'])

        self.assertEqual(ls('ax', 'ba'), ['ax', 'ay', 'az', 'ba'])
        self.assertEqual(ls('zz', 'aaa'), ['zz', 'aaa'])
        self.assertEqual(ls('zz', 'aab'), ['zz', 'aaa', 'aab'])

        self.assertEqual(ls('b', 'bc'), ['b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                                         'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                                         'aa', 'ab', 'ac', 'ad', 'ae', 'af', 'ag', 'ah', 'ai', 'aj', 'ak',
                                         'al', 'am', 'an', 'ao', 'ap', 'aq', 'ar', 'as', 'at', 'au', 'av',
                                         'aw', 'ax', 'ay', 'az',
                                         'ba', 'bb', 'bc'])

        self.assertEqual(
            ls('Qaaa', 'Qabx'),
            [
                'Qaaa', 'Qaab', 'Qaac', 'Qaad', 'Qaae', 'Qaaf', 'Qaag', 'Qaah', 'Qaai', 'Qaaj', 'Qaak',
                'Qaal', 'Qaam', 'Qaan', 'Qaao', 'Qaap', 'Qaaq', 'Qaar', 'Qaas', 'Qaat', 'Qaau', 'Qaav',
                'Qaaw', 'Qaax', 'Qaay', 'Qaaz', 'Qaba', 'Qabb', 'Qabc', 'Qabd', 'Qabe', 'Qabf', 'Qabg',
                'Qabh', 'Qabi', 'Qabj', 'Qabk', 'Qabl', 'Qabm', 'Qabn', 'Qabo', 'Qabp', 'Qabq', 'Qabr',
                'Qabs', 'Qabt', 'Qabu', 'Qabv', 'Qabw', 'Qabx'
            ])

    def test_not_covered(self):
        for start, stop in [
            ('1.2', '3.8'),
            ('[1]', '(5)'),
            ('abc.abc.', 'def.def.def.'),  # different repeating parts
            ('ABCD', 'WXYZ'),  # too big range
            ('a#$!', 'a#$*'),  # Non-alphanumeric
            ('Олег', 'Aлістратов'),  # Non-ASCII
            ('v1.3.0', 'v1.5.4'),  # Multiple numbers
            ('v1.3.0', 'v3.5.4'),  # Multiple numbers
        ]:
            with self.subTest(start=start, stop=stop):
                self.assertEqual(ls(start, stop), [start, stop])
