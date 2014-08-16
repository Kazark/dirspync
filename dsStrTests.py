#!/usr/bin/python3
import unittest
from dsStr import minusstr, fill, ellipsize

class dsStrTests(unittest.TestCase):
    def test_subtracting_empty_strings_should_yield_empty_string(self):
        self.assertEqual('', minusstr('', ''))

if __name__ == '__main__':
    unittest.main()
