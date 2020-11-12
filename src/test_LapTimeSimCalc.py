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

    # Test the loaded track distance is the same as from the TrackFile.txt
    def test_1(self):
        dist = self.LTSC.lapTimeSimDict["dist"]
        actual = dist[-1]
        print(actual)
        expected = 6950  # track distance
        self.assertEqual(actual, expected, "Error in test 1")

    # Test griddata Interpolation of the GGV
    def test_2(self):
        GGVdec = self.LTSC.GGVdec
        GGVfull = self.LTSC.GGVfull
        X, Y, Z = GGVdec[:, 0], GGVdec[:, 1], GGVdec[:, 2]
        vxmax = max(GGVfull[:, 2])
        expected = min(GGVfull[:, 1])  # min axdec is as maxspeed
        actual = self.LTSC.GGVSurfInterp(vxmax, 0, X, Y, Z)
        bInRange = (actual < expected+0.5 and actual > expected-0.5)
        self.assertTrue(bInRange, "Error in test 2")
        # print("act: ", actual, "; exp: ", expected)

if __name__ == '__main__':
    unittest.main()
