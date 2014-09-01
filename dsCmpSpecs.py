#!/usr/bin/python3
import unittest
from dsCmp import FileComparer, SA, SZ, RN, LN

class FileStub:
    def __init__(self, mtime, size, md5):
        self.__mtime = mtime
        self.__size = size
        self.__hash = md5
    def mtime(self):
        return self.__mtime
    def size(self):
        return self.__size
    def md5sum(self):
        return self.__hash

class FileComparerSpecs(unittest.TestCase):
    def test_files_with_same_time_and_size_are_considered_the_same_without_regard_to_hash(self):
        file1 = FileStub(123, 456, 789)
        file2 = FileStub(123, 456, 123)
        self.assertEqual(SA, FileComparer().compare(file1, file2))

    def test_files_with_same_time_and_different_sizes_are_considered_different_without_regard_to_hash(self):
        self.assertEqual(SZ, FileComparer().compare(FileStub(123, 456, 456), FileStub(123, 789, 456)))

    def test_files_with_different_times_same_sizes_and_different_hashes_are_considered_different(self):
        self.assertEqual(LN, FileComparer().compare(FileStub(456, 123, 456), FileStub(123, 123, 123)))
        self.assertEqual(RN, FileComparer().compare(FileStub(123, 456, 456), FileStub(789, 456, 789)))

    def test_files_with_different_times_same_sizes_and_same_hashes_are_considered_same(self):
        self.assertEqual(SA, FileComparer().compare(FileStub(456, 123, 456), FileStub(123, 123, 456)))
        self.assertEqual(SA, FileComparer().compare(FileStub(123, 456, 789), FileStub(789, 456, 789)))

if __name__ == '__main__':
    unittest.main()
