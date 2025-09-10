import unittest

from strrange import range as strrange, Alphabet


def ls(start, stop):
    return list(strrange(start, stop))


class TestSamples(unittest.TestCase):
    def test_only_gen_auto(self):
        self.assertEqual(ls('', ''), [])
        self.assertEqual(ls('abc', 'abc'), ['abc'])
        self.assertEqual(ls('[*]', '[*]'), ['[*]'])

        self.assertEqual(ls('1', '5'), ['1', '2', '3', '4', '5'])
        self.assertEqual(ls('5', '1'), ['5', '4', '3', '2', '1'])
        self.assertEqual(ls('-3', '3'), ['-3', '-2', '-1', '0', '1', '2', '3'])
        self.assertEqual(ls('1', '-1'), ['1', '0', '-1'])
        self.assertEqual(ls('+1_000', '1005'), ['1000', '1001', '1002', '1003', '1004', '1005'])

        self.assertEqual(ls('001', '005'), ['001', '002', '003', '004', '005'])
        self.assertEqual(ls('001', '5'), ['001', '002', '003', '004', '005'])
        self.assertEqual(ls('  1', '  5'), ['  1', '  2', '  3', '  4', '  5'])
        self.assertEqual(ls('  1', '5'), ['  1', '  2', '  3', '  4', '  5'])

        # Repeating substrings
        self.assertEqual(ls('i)', 'iii)'), ['i)', 'ii)', 'iii)'])
        self.assertEqual(ls('x--', 'x----'), ['x--', 'x---', 'x----'])

        # Filenames and similar
        self.assertEqual(
            ls('file1.txt', 'file3.txt'),
            ['file1.txt', 'file2.txt', 'file3.txt'])
        self.assertEqual(
            ls('file001.txt', 'file003.txt'),
            ['file001.txt', 'file002.txt', 'file003.txt'])
        self.assertEqual(
            ls('access.log.1', 'access.log.4'),
            ['access.log.1', 'access.log.2', 'access.log.3', 'access.log.4'])
        self.assertEqual(
            ls('1.png', '12.png'),
            ['1.png', '2.png', '3.png', '4.png', '5.png',
             '6.png', '7.png', '8.png', '9.png', '10.png',
             '11.png', '12.png'])
        self.assertEqual(
            ls('S01E01.mkv', 'S01E04.mkv'),
            ['S01E01.mkv', 'S01E02.mkv', 'S01E03.mkv', 'S01E04.mkv'])
        self.assertEqual(
            ls('/dev/tty1', '/dev/tty4'),
            ['/dev/tty1', '/dev/tty2', '/dev/tty3', '/dev/tty4'])
        self.assertEqual(
            ls('Vol10No01', 'Vol10No03'),
            ['Vol10No01', 'Vol10No02', 'Vol10No03'])

        # Not a date, actually
        self.assertEqual(
            ls('db-backup-20250901.sql', 'db-backup-20250903.sql'),
            ['db-backup-20250901.sql', 'db-backup-20250902.sql', 'db-backup-20250903.sql'])

        # IANA ranges
        self.assertEqual(len(ls('qaa', 'qtz')), 520)
        self.assertEqual(len(ls('Qaaa', 'Qabx')), 50)
        self.assertEqual(len(ls('QM', 'QZ') + ls('XA', 'XZ')), 14 + 26)

        # Excel columns
        self.assertEqual(len(ls('A', 'ZZ')), 702)
        self.assertEqual(ls('A', 'Z') + ls('AA', 'AZ'), ls('A', 'AZ'))
        self.assertEqual(len(ls('A', 'XFD')), 16384)

        # Alphabetic sequences
        self.assertEqual(ls('A', 'D'), ['A', 'B', 'C', 'D'])
        self.assertEqual(ls('a)', 'e)'), ['a)', 'b)', 'c)', 'd)', 'e)'])

        # Serial numbers, revisions etc.
        self.assertEqual(
            ls('SN-A001', 'SN-A005'),
            ['SN-A001', 'SN-A002', 'SN-A003', 'SN-A004', 'SN-A005'])
        self.assertEqual(
            ls('REV-A', 'REV-C'),
            ['REV-A', 'REV-B', 'REV-C'])
        self.assertEqual(
            ls('LOT000123', 'LOT000125'),
            ['LOT000123', 'LOT000124', 'LOT000125'])
        self.assertEqual(
            ls('INV-2025-001', 'INV-2025-005'),
            ['INV-2025-001', 'INV-2025-002', 'INV-2025-003', 'INV-2025-004', 'INV-2025-005'])
        self.assertEqual(
            ls('PROJ-101', 'PROJ-103'),
            ['PROJ-101', 'PROJ-102', 'PROJ-103'])

        # Version numbers (limited support)
        self.assertEqual(
            ls('v1.0.0', 'v1.0.3'),
            ['v1.0.0', 'v1.0.1', 'v1.0.2', 'v1.0.3'])
        self.assertEqual(
            ls('v1.2.0', 'v1.2.3'),
            ['v1.2.0', 'v1.2.1', 'v1.2.2', 'v1.2.3'])
        self.assertEqual(
            ls('v1.0', 'v1.3'),
            ['v1.0', 'v1.1', 'v1.2', 'v1.3'])
        self.assertEqual(
            ls('ver.1', 'ver.3'),
            ['ver.1', 'ver.2', 'ver.3'])
        self.assertEqual(
            ls('v1.0', 'v3.0'),
            ['v1.0', 'v2.0', 'v3.0'])
        self.assertEqual(
            ls('v1.2.3', 'v7.8.9'),
            ['v1.2.3', 'v7.8.9'])

    def test_concatenated(self):
        # Full list of IANA private regions
        r = 'AA' + strrange('QM', 'QZ') + strrange('XA', 'XZ') + 'ZZ'
        self.assertEqual(len(list(r)), 1 + 14 + 26 + 1)

    def test_alphabet_class(self):
        abc = Alphabet('abc')
        self.assertEqual(abc.word(5), 'ab')
        self.assertEqual(abc.ordinal('ab'), 5)

        words = list(abc.range('a', 'ba'))
        self.assertEqual(words, ['a', 'b', 'c', 'aa', 'ab', 'ac', 'ba'])

        self.assertEqual(abc.range_length('a', 'ba'), 7)
