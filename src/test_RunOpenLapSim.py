"""Unit Test for RunOpenLapSim.py"""


import unittest
from RunOpenLapSim import RunOpenLapSim


class test_LapTimeSimCalc(unittest.TestCase):

    setupFileName = "SetupFile.json"
    trackFileName = "TrackFile.txt"
    bExport = 0
    bPlot = 0
    bPlotExtra = 0
    ROLS = RunOpenLapSim(setupFileName, trackFileName, bExport, bPlot,  bPlotExtra)
    ROLS.run()

    def test_1(self):
        actual = self.ROLS.laptime 
        expected = 121.813  # laptime 
        self.assertEqual(actual, expected, "Error in test 1")


if __name__ == '__main__':
    unittest.main()
