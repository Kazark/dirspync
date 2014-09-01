#!/usr/bin/python3
import unittest
from dsCmp import FileComparer, SA, SZ

class FileStub:
    def __init__(self, mtime, size):
        self.__mtime = mtime
        self.__size = size
    def mtime(self):
        return self.__mtime
    def size(self):
        return self.__size

class FileComparerSpecs(unittest.TestCase):
    def test_files_with_same_time_and_size_are_considered_the_same(self):
        self.assertEqual(SA, FileComparer().compare(FileStub(123, 456), FileStub(123, 456)))
    def test_files_with_same_time_and_different_size(self):
        self.assertEqual(SZ, FileComparer().compare(FileStub(123, 456), FileStub(123, 789)))

if __name__ == '__main__':
    unittest.main()
