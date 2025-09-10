import unittest

from strrange.util import is_padded_int as ipi, is_alphanum as ian, is_repeating_substring, is_alpha, is_digits


class TestUtilities(unittest.TestCase):
    def test_is_padded_int(self):
        # Non-string inputs
        for v in (None, (), [], {}, 0, -12.34, True, 1+2j):
            with self.assertRaises(TypeError):
                ipi(v)  # type: ignore

        # Non-string, but numeric inputs - just to document behavior
        # self.assertEqual(ipi(0), (True, 0))  # type: ignore
        # self.assertEqual(ipi(-12.34), (True, -12))  # type: ignore
        # self.assertEqual(ipi(True), (True, 1))  # type: ignore

        NOT_INT = (False, 0, '', 0)

        # Empty and non-numeric strings
        self.assertEqual(ipi(''), NOT_INT)
        self.assertEqual(ipi(' '), NOT_INT)
        self.assertEqual(ipi('  '), NOT_INT)
        self.assertEqual(ipi('abc'), NOT_INT)
        self.assertEqual(ipi('NaN'), NOT_INT)
        self.assertEqual(ipi('+inf'), NOT_INT)

        # String inputs
        self.assertEqual(ipi('0'), (True, 0, '', 0))
        self.assertEqual(ipi(' -0'), (True, 0, ' ', 1))

        self.assertEqual(ipi('12'), (True, 12, '', 0))
        self.assertEqual(ipi('  12'), (True, 12, ' ', 2))
        self.assertEqual(ipi('12  '), (True, 12, '', 0))

        self.assertEqual(ipi('-12'), (True, -12, '', 0))
        self.assertEqual(ipi(' +12'), (True, 12, ' ', 1))

        self.assertEqual(ipi('00000'), (True, 0, '0', 5))
        self.assertEqual(ipi('    0'), (True, 0, ' ', 4))

        self.assertEqual(ipi('00006'), (True, 6, '0', 4))
        self.assertEqual(ipi('-0006'), (True, -6, '', 0))
        self.assertEqual(ipi(' -006'), (True, -6, ' ', 1))
        self.assertEqual(ipi(' - 6 '), NOT_INT)

        self.assertEqual(ipi('    6'), (True, 6, ' ', 4))
        self.assertEqual(ipi('   -6'), (True, -6, ' ', 3))

        self.assertEqual(ipi('1_000'), (True, 1000, '', 0))

        # Parsing float and scientific notation is disabled for now
        # self.assertEqual(ipi('12345678901234567890.99'), (True, 12345678901234567168, '', 0))
        # self.assertEqual(ipi('12.34'), (True, 12, '', 0))
        # self.assertEqual(ipi(' -012.34'), (True, -12, ' ', 1))
        # self.assertEqual(ipi('-1e3'), (True, -1000, '', 0))
        # self.assertEqual(ipi('1e308')[0], True)  # Value is long but valid

        self.assertEqual(ipi('12345678901234567890.99'), NOT_INT)
        self.assertEqual(ipi('12.34'), NOT_INT)
        self.assertEqual(ipi(' -012.34'), NOT_INT)
        self.assertEqual(ipi('-1e3'), NOT_INT)
        self.assertEqual(ipi('1e308'), NOT_INT)
        self.assertEqual(ipi('1e309'), NOT_INT)

        self.assertEqual(ipi('0x10'), NOT_INT)
        self.assertEqual(ipi('0o10'), NOT_INT)
        self.assertEqual(ipi('12-34'), NOT_INT)
        self.assertEqual(ipi('--5'), NOT_INT)

    def test_is_alphanum(self):
        for w in (None, (), [], {}, 123, 12.34, True, 1+2j):
            with self.assertRaises(TypeError):
                ian(w)  # type: ignore

        for w in ('', ' ', '  ', 'abc!', 'a b', 'a\nb', 'a\tb', 'a-b', 'a.b',
                  'a,b', 'a@b', 'a#b', 'a$b', 'a%b', 'a^b', 'a&b', 'a*b', 'a(b)',
                  'a[b]', 'a{b}', 'a|b', 'a\\b', 'a/b', 'a<b>c', 'a=b'):
            self.assertEqual(ian(w), False)
            self.assertEqual(w.isalnum(), False)

        for w in ('a', 'Z', '0', '9', 'abc', 'ABC', 'AbC123', '123abcXYZ'):
            self.assertEqual(ian(w), True)
            self.assertEqual(w.isalnum(), True)

        for w in ('á', 'ß', 'ç', 'ñ', 'ø', 'ü', 'Α', 'Б', 'Д', 'א', 'م', 'あ', 'ア', 'あい123'):
            self.assertEqual(ian(w), False)
            self.assertEqual(w.isalnum(), True)

    def test_is_alpha(self):
        for w in (None, (), [], {}, 123, 12.34, True, 1+2j):
            with self.assertRaises(TypeError):
                is_alpha(w)  # type: ignore

        for w in ('', ' ', '  ', 'abc!', 'a b', 'a\nb', 'a\tb', 'a-b', 'a.b',
                  'a,b', 'a@b', 'a#b', 'a$b', 'a%b', 'a^b', 'a&b', 'a*b', 'a(b)',
                  'a[b]', 'a{b}', 'a|b', 'a\\b', 'a/b', 'a<b>c', 'a=b', 'abc123', '123'):
            self.assertEqual(is_alpha(w), False)
            self.assertEqual(w.isalpha(), False)

        for w in ('a', 'Z', 'abc', 'ABC', 'AbCxyzXYZ'):
            self.assertEqual(is_alpha(w), True)
            self.assertEqual(w.isalpha(), True)

        for w in ('á', 'ß', 'ç', 'ñ', 'ø', 'ü', 'Α', 'Б', 'Д', 'א', 'م', 'あ', 'ア', 'あいabc'):
            self.assertEqual(is_alpha(w), False)
            self.assertEqual(w.isalpha(), True)

    def test_is_digits(self):
        for w in (None, (), [], {}, 123, 12.34, True, 1+2j):
            with self.assertRaises(TypeError):
                is_digits(w)  # type: ignore

        for w in ('', ' ', '  ', '123!', '12 34', '12\n34', '12\t34', '12-34', '12.34',
                  '12,34', '12@34', '12#34', '12$34', '12%34', '12^34', '12&34', '12*34', '12(34)',
                  '12[34]', '12{34}', '12|34', '12\\34', '12/34', '12<34>56', '12=34'):
            self.assertEqual(is_digits(w), False)
            self.assertEqual(w.isdigit(), False)

        for w in ('0', '9', '123', '0123456789', '1234567890'):
            self.assertEqual(is_digits(w), True)
            self.assertEqual(w.isdigit(), True)

        for w in ('٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩'):
            self.assertEqual(is_digits(w), False)
            self.assertEqual(w.isdigit(), True)

    def test_is_repeating(self):
        self.assertEqual(is_repeating_substring(''), (0, ''))
        self.assertEqual(is_repeating_substring('a'), (1, 'a'))
        self.assertEqual(is_repeating_substring('aa'), (2, 'a'))
        self.assertEqual(is_repeating_substring('a' * 50), (50, 'a'))
        self.assertEqual(is_repeating_substring('abcabc'), (2, 'abc'))
        self.assertEqual(is_repeating_substring('abc abc'), (1, 'abc abc'))
        self.assertEqual(is_repeating_substring('abc' * 50), (50, 'abc'))
