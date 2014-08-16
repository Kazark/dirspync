#!/usr/bin/python3
import unittest
from dsTerm import WinTerm

class dsTermTests(unittest.TestCase):
    def test_Windows_terminal_has_size_25_by_79(self):
        self.assertEqual(25, WinTerm().getSize().rows)
        self.assertEqual(79, WinTerm().getSize().cols)

if __name__ == '__main__':
    unittest.main()
