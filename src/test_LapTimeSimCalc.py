"""Unit Test for LapTimeSimCalc.py"""


import unittest
from SetupFileLoader import SetupFileLoader
from AccEnvCalc import AccEnvCalc
from LapTimeSimCalc import LapTimeSimCalc


class test_LapTimeSimCalc(unittest.TestCase):

    setupPath = "setupFiles/SetupFile.json"
    SFL = SetupFileLoader(setupPath)
    SFL.loadJSON()
    AEC = AccEnvCalc(SFL.setupDict)
    AEC.Run()
    trackPath = "trackFiles/TrackFile.txt"
    LTSC = LapTimeSimCalc(trackPath, AEC.accEnvDict, 10)
    LTSC.Run()

    def test_1(self):
        dist = self.LTSC.lapTimeSimDict["dist"]
        actual = dist[-1]
        print(actual)
        expected = 6950  # track distance
        self.assertEqual(actual, expected, "Error in test 1")


if __name__ == '__main__':
    unittest.main()
