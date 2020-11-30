import unittest
import sys
from PyQt5.QtTest import QTest

def writeToFile(string, file):
    print("STRING IS: " + string)
    file.write(string)
    return file.read(50)

def readFromFile(file):
    return file.read()


class Test(unittest.TestCase):

    def setUp(self):
        print("SETUP Called...")
        self.SavedList = open("SavedListTest.txt", "r+")

    def test_func_1(self):
        print("TEST 1 Called...")
        result = writeToFile("test 1", self.SavedList)
        print("RESULT: " + result)
        self.assertEqual(result, "test 1")

    def test_func_2(self):
        print("TEST 2 Called...")
        readFromFile(self.SavedList)
        self.assertEqual(self.SavedList.read(50), "")

    def tearDown(self):
        print("TEARDOWN Called...")
        self.SavedList.close()

if __name__ == "__main__":
    unittest.main()