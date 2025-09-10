import unittest

from strrange.pattern import pattern, fallback_digits, fallback_alnum


class TestPattern(unittest.TestCase):
    def test_pattern(self):
        self.assertEqual(
            pattern('abc', 'abc'),
            ('abc', '', '', ''))
        self.assertEqual(
            pattern('abc', 'xyz'),
            ('', 'abc', 'xyz', ''))

        self.assertEqual(
            pattern('ab', 'abc'),
            ('ab', '', 'c', ''))
        self.assertEqual(
            pattern('abc', 'ab'),
            ('ab', 'c', '', ''))

        self.assertEqual(
            pattern('xyz', 'yz'),
            ('', 'x', '', 'yz'))
        self.assertEqual(
            pattern('yz', 'xyz'),
            ('', '', 'x', 'yz'))

        self.assertEqual(
            pattern('aXz', 'aYz'),
            ('a', 'X', 'Y', 'z'))
        self.assertEqual(
            pattern('aXz', 'aY'),
            ('a', 'Xz', 'Y', ''))

        self.assertEqual(
            pattern('a)', 'f)'),
            ('', 'a', 'f', ')'))
        self.assertEqual(
            pattern('i.', 'iii.'),
            ('i', '', 'ii', '.'))

        self.assertEqual(
            pattern('file001.txt', 'file100.txt'),
            ('file', '001', '100', '.txt'))
        self.assertEqual(
            pattern('file1.txt', 'file100.txt'),
            ('file1', '', '00', '.txt'))
        self.assertEqual(
            pattern('img_0001.png', 'img_0010.png'),
            ('img_00', '01', '10', '.png'))

        self.assertEqual(
            pattern('TAALV', 'TXXLV'),
            ('T', 'AA', 'XX', 'LV'))
        self.assertEqual(
            pattern('T-AA-LV', 'T-XX-LV'),
            ('T-', 'AA', 'XX', '-LV'))

        self.assertEqual(
            pattern('Rev A', 'Rev C'),
            ('Rev ', 'A', 'C', ''))

        self.assertEqual(
            pattern('v1.0', 'v1.9'),
            ('v1.', '0', '9', ''))
        self.assertEqual(
            pattern('v1.0', 'v2.0'),
            ('v', '1', '2', '.0'))

    def test_fallback_digits(self):
        self.assertEqual(
            pattern('file001.txt', 'file100.txt'),
            ('file', '001', '100', '.txt'))
        self.assertEqual(
            fallback_digits(*pattern('file001.txt', 'file100.txt')),
            ('file', '001', '100', '.txt'))  # No change, as digits are already in variable part

        self.assertEqual(
            pattern('file001.txt', 'file002.txt'),
            ('file00', '1', '2', '.txt'))
        self.assertEqual(
            fallback_digits(*pattern('file001.txt', 'file002.txt')),
            ('file', '001', '002', '.txt'))

        self.assertEqual(
            pattern('file100.txt', 'file200.txt'),
            ('file', '1', '2', '00.txt'))
        self.assertEqual(
            fallback_digits(*pattern('file100.txt', 'file200.txt')),
            ('file', '100', '200', '.txt'))

    def test_fallback_alnum(self):
        self.assertEqual(
            pattern('fileA.txt', 'fileC.txt'),
            ('file', 'A', 'C', '.txt'))
        self.assertEqual(
            fallback_alnum(*pattern('fileA.txt', 'fileC.txt')),
            ('', 'fileA', 'fileC', '.txt'))

        self.assertEqual(
            pattern('fileAA.txt', 'fileAC.txt'),
            ('fileA', 'A', 'C', '.txt'))
        self.assertEqual(
            fallback_alnum(*pattern('fileAA.txt', 'fileAC.txt')),
            ('', 'fileAA', 'fileAC', '.txt'))

        self.assertEqual(
            pattern('Rev A', 'Rev C'),
            ('Rev ', 'A', 'C', ''))
        self.assertEqual(
            fallback_alnum(*pattern('Rev A', 'Rev C')),
            ('Rev ', 'A', 'C', ''))  # No change, as prefix is not alphanumeric

        self.assertEqual(
            pattern('S01E01.mkv', 'S01E05.mkv'),
            ('S01E0', '1', '5', '.mkv'))
        self.assertEqual(
            fallback_digits(*pattern('S01E01.mkv', 'S01E05.mkv')),
            ('S01E', '01', '05', '.mkv'))
        self.assertEqual(
            fallback_alnum(*pattern('S01E01.mkv', 'S01E05.mkv')),
            ('', 'S01E01', 'S01E05', '.mkv'))
