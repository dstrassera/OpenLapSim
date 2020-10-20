"""Unit Test fir AccEnvCalc.py"""


import unittest
from AccEnvCalc import AccEnvCalc
from SetupFileLoader import SetupFileLoader


class test_AccEnvCalc(unittest.TestCase):

    SFL = SetupFileLoader("setupFiles/SetupFile.json")
    SFL.loadJSON()
    AEC = AccEnvCalc(SFL.setupDict)
    AEC.Run()

    def test_1(self):
        actual = len(self.AEC.accEnvDict["vxvect"])
        expected = self.AEC.nSteps
        self.assertEqual(actual, expected, "Error in test 1")

    def test_2(self):
        actual = len(self.AEC.accEnvDict["axacc"])
        expected = self.AEC.nSteps
        self.assertEqual(actual, expected, "Error in test 2")

    def test_3(self):
        actual = len(self.AEC.accEnvDict["axdec"])
        expected = self.AEC.nSteps
        self.assertEqual(actual, expected, "Error in test 3")

    def test_4(self):
        actual = len(self.AEC.accEnvDict["ay"])
        expected = self.AEC.nSteps
        self.assertEqual(actual, expected, "Error in test 4")


if __name__ == '__main__':
    unittest.main()
