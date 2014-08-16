#!/usr/bin/python3
import unittest
from dsStr import minusstr, fill, ellipsize

class string_subtration_specs(unittest.TestCase):
    def test_subtract_empty_strings_should_return_empty_string(self):
        self.assertEqual('', minusstr('', ''))

    def test_subtract_empty_string_from_asdf_should_return_asdf(self):
        self.assertEqual('asdf', minusstr('asdf', ''))

    def test_subtract_bar_from_foobar_should_return_foo(self):
        self.assertEqual('foo', minusstr('foobar', 'bar'))

    def test_subtract_string_from_itself_should_return_empty_string(self):
        self.assertEqual('', minusstr('foo', 'foo'))

    def test_subtract_baz_from_foobar_should_raise_exception(self):
        self.assertRaises(ValueError, lambda: minusstr('foobar', 'baz'))

class fill_string_with_character_to_length_specs(unittest.TestCase):
    def test_fill_empty_string_with_with_empty_string_to_zero_should_return_empty(self):
        self.assertEqual('', fill('', '', 0))

    def test_fill_empty_string_with_with_empty_string_to_positive_should_return_spaces(self):
        self.assertEqual('    ', fill('', '', 4))

    def test_fill_empty_string_with_with_z_to_three_should_return_zzz(self):
        self.assertEqual('zzz', fill('', 'z', 3))

class ellipsizing_specs(unittest.TestCase):
    def test_ellipsize_empty_string_to_zero_length_should_return_empty_string(self):
        self.assertEqual('', ellipsize('', 0))

    def test_ellipsize_empty_string_to_positive_length_should_return_empty_string(self):
        self.assertEqual('', ellipsize('', 10))

    def test_ellipsize_short_string_to_long_length_should_return_string_untouched(self):
        self.assertEqual('asdf', ellipsize('asdf', 10))

    def test_ellipsize_string_to_its_own_length_should_return_string_untouched(self):
        self.assertEqual('123456789', ellipsize('123456789', 9))

    def test_ellipsize_string_to_smaller_length_should_return_string_with_ellipsis(self):
        self.assertEqual('12345...', ellipsize('123456789', 8))

if __name__ == '__main__':
    unittest.main()
