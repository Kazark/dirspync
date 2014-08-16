#!/usr/bin/python3
import unittest
from dsTerm import LinuxTerm, WinTerm

class dsTermTests(unittest.TestCase):
    def test_Windows_terminal_has_size_25_by_79(self):
        self.assertEqual(25, WinTerm().getSize().rows)
        self.assertEqual(79, WinTerm().getSize().cols)

    def test_Linux_terminal_defaults_to_25_by_80(self):
        self.assertEqual(25, LinuxTerm(lambda: []).getSize().rows)
        self.assertEqual(80, LinuxTerm(lambda: []).getSize().cols)

if __name__ == '__main__':
    unittest.main()
