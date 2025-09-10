import unittest

from strrange.concat import StrRange as sr


class TestConcatenation(unittest.TestCase):
    def test_sr_add(self):
        a = sr('a', 'c')
        b = sr('1', '3')
        self.assertEqual(
            list(a + b),
            ['a', 'b', 'c', '1', '2', '3'])

    def test_left_add(self):
        a = sr('a', 'c')
        b = ['1', '2', '3']
        self.assertEqual(
            list(a + b),
            ['a', 'b', 'c', '1', '2', '3'])

        a = sr('a', 'c')
        b = ('1', '2', '3')
        self.assertEqual(
            list(a + b),
            ['a', 'b', 'c', '1', '2', '3'])

        a = sr('a', 'c')
        b = '123'
        self.assertEqual(
            list(a + b),
            ['a', 'b', 'c', '123'])

    def test_right_add(self):
        a = ['1', '2', '3']
        b = sr('a', 'c')
        self.assertEqual(
            list(a + b),
            ['1', '2', '3', 'a', 'b', 'c'])

        a = ('1', '2', '3')
        b = sr('a', 'c')
        self.assertEqual(
            list(a + b),
            ['1', '2', '3', 'a', 'b', 'c'])

        a = '123'
        b = sr('a', 'c')
        self.assertEqual(
            list(a + b),
            ['123', 'a', 'b', 'c'])

    def test_chain(self):
        r = sr('a', 'c') + sr('1', '3') + ['X', 'Y'] + 'Z'
        self.assertEqual(
            list(r),
            ['a', 'b', 'c', '1', '2', '3', 'X', 'Y', 'Z']
        )

        r = sr('a', 'c') + 'd' + ('e', 'f') + sr('g', 'j') + 'k'
        self.assertEqual(
            list(r),
            ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k']
        )

        with self.assertRaises(TypeError):
            _ = 'A' + ['B', 'C', 'D'] + sr('1', '3')

        r = ['A', 'B', 'C'] + sr('D', 'F') + ('G', 'H', 'I')
        self.assertEqual(
            list(r),
            ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        )

        r = sr('1', '3') + sr('A', 'C') + sr('x', 'z')
        self.assertEqual(
            list(r),
            ['1', '2', '3', 'A', 'B', 'C', 'x', 'y', 'z']
        )
        r = 'A' + sr('B', 'D') + sr('1', '3') + '4'
        self.assertEqual(
            list(r),
            ['A', 'B', 'C', 'D', '1', '2', '3', '4']
        )

    def test_other(self):
        # Not list of strings, but OK
        r = sr('a', 'c') + [1, 2, 3] + 'X'
        self.assertEqual(
            list(r),
            ['a', 'b', 'c', 1, 2, 3, 'X']
        )

        with self.assertRaises(TypeError):
            _ = sr('a', 'c') + 1

        with self.assertRaises(TypeError):
            _ = 1 + sr('a', 'c')
