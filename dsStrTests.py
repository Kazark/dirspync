#!/usr/bin/python3
import unittest
from dsStr import minusstr, fill, ellipsize

class dsStrTests(unittest.TestCase):
    def test_subtract_empty_strings_should_yield_empty_string(self):
        self.assertEqual('', minusstr('', ''))

    def test_subtract_empty_string_from_asdf_should_yield_asdf(self):
        self.assertEqual('asdf', minusstr('asdf', ''))

    def test_subtract_bar_from_foobar_should_yield_foo(self):
        self.assertEqual('foo', minusstr('foobar', 'bar'))

    def test_subtract_string_from_itself_should_yield_empty_string(self):
        self.assertEqual('', minusstr('foo', 'foo'))

    def test_subtract_baz_from_foobar_should_raise_exception(self):
        self.assertRaises(ValueError, lambda: minusstr('foobar', 'baz'))

if __name__ == '__main__':
    unittest.main()
