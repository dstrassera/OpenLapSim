"""Unit Test for RunOpenLapSim.py"""


import unittest
from RunOpenLapSim import RunOpenLapSim


class test_LapTimeSimCalc(unittest.TestCase):

    setupFileName = "SetupFile.json"
    trackFileName = "TrackFile.txt"
    bExport = 0
    bPlot = 0
    bPlotExtra = 0
    ROLS = RunOpenLapSim(setupFileName, trackFileName,
                         bExport, bPlot,  bPlotExtra)
    ROLS.run()

    # Test the laptime is as expected
    def test_1(self):
        actual = self.ROLS.laptime
        expected = 121.054  # laptime
        self.assertEqual(actual, expected, "Error in test 1")

    # Test the vxcarmax in kph is as expected
    def test_2(self):
        actual = round(self.ROLS.vcarmax*3.6, 1)
        expected = 296.6  # vxcarmax
        self.assertEqual(actual, expected, "Error in test 2")

    # (TEST OFF FOR CI) Test the computational time is less then expected
    # def test_3(self):
    #     actual = self.ROLS.tcomp
    #     expected = 15  # sec
    #     bTimeLessThanExp = actual < expected
    #     self.assertTrue(bTimeLessThanExp, "Error in test 3")

if __name__ == '__main__':
    unittest.main()
