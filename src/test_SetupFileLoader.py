"""Unit Test for SetupFileLoader.py"""


import unittest
from SetupFileLoader import SetupFileLoader


class test_SetupFileLoader(unittest.TestCase):

    setupPath = "setupFiles/SetupFile.json"
    SFL = SetupFileLoader(setupPath)
    SFL.loadJSON()

    def test_1(self):
        """test loadJSON method for string variable"""
        actual = self.SFL.setupDict["setupName"]
        expected = "Gp2Dummy"
        self.assertEqual(actual, expected, "Error in loadJSON 1")

    def test_2(self):
        """test loadJSON method for int variable"""
        actual = self.SFL.setupDict["mcar"]
        expected = 728
        self.assertEqual(actual, expected, "Error in loadJSON 2")

    def test_3(self):
        """test loadJSON method for int array"""
        actual = self.SFL.setupDict["EngNm"]
        expected = [200, 300, 430, 380]
        self.assertEqual(actual, expected, "Error in loadJSON 3")


if __name__ == '__main__':
    unittest.main()
