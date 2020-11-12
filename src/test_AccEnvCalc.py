"""Unit Test for AccEnvCalc.py"""


import unittest
from AccEnvCalc import AccEnvCalc
from SetupFileLoader import SetupFileLoader


class test_AccEnvCalc(unittest.TestCase):

    SFL = SetupFileLoader("setupFiles/SetupFile.json")
    SFL.loadJSON()
    AEC = AccEnvCalc(SFL.setupDict)
    AEC.Run()

    # Tests for the 2D GGV
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

    # Tests for the 3D GGV
    def test_5(self):
        actual = max(self.AEC.accEnvDict["GGVfull"][:, 2])
        expected = max(self.AEC.accEnvDict["vxvect"])
        self.assertEqual(actual, expected, "Error in test 5")
        # print("act: ", actual, "; exp: ", expected)

    def test_6(self):
        actual = round(max(self.AEC.accEnvDict["GGVfull"][:, 1]), 1)
        expected = round(max(self.AEC.accEnvDict["ay"]), 1)
        self.assertEqual(actual, expected, "Error in test 6")
        # print("act: ", actual, "; exp: ", expected)

    def test_7(self):
        actual = round(max(self.AEC.accEnvDict["GGVfull"][:, 0]), 1)
        expected = round(max(self.AEC.accEnvDict["axacc"]), 1)
        self.assertEqual(actual, expected, "Error in test 7")
        # print("act: ", actual, "; exp: ", expected)

    def test_8(self):
        actual = round(min(self.AEC.accEnvDict["GGVfull"][:, 0]), 1)
        expected = round(min(self.AEC.accEnvDict["axdec"]), 1)
        self.assertEqual(actual, expected, "Error in test 8")
        # print("act: ", actual, "; exp: ", expected)


if __name__ == '__main__':
    unittest.main()
