"""
---------------------------
OpenLapSim - OLS
---------------------------

This is a steady state Lap Time Simulator for a simple point mass vehicle
with aero forces, constant tyre grip(x and y), engine torque map and gears.

Steps:
    1 - Select Files: TrackFile.txt and SetupFile.py
    2 - Calculate the Acceleration Envelope
    3 - Calculate the Lap Time Simulation (vcar)
    4 - Plot Results

---------------------------
@autor: Davide Strassera
@first release: 2019-12-21
by Python 3.7
---------------------------

"""

# ----------------------------------------------------------------------------

# import packages generic
import datetime
import matplotlib.pyplot as plt
import time

# import packages (OLP)
from AccEnvCalc import AccEnvCalc
from LapTimeSimCalc import LapTimeSimCalc
from PostProc import PostProc
from SetupFileLoader import SetupFileLoader


class RunOpenLapSim:

    def __init__(self, setupFileName, trackFileName,
                 bExport, bPlot, bPlotExtra):
        # inputs
        self.setupFileName = setupFileName
        self.trackFileName = trackFileName
        self.bExport = bExport
        self.bPlot = bPlot
        self.bPlotExtra = bPlotExtra
        self.trackFilesPath = "trackFiles/"
        self.exportFilesPath = "exportFiles/"
        self.setupFilesPath = "setupFiles/"
        # outputs
        self.laptime = None
        self.vcarmax = None
        self.tcomp = None  # computational time

    @staticmethod
    def createExportSimFile(vcar, dist, exportFilesPath):
        time = datetime.datetime.now()
        timestrf = time.strftime("%b-%d-%Y")
        NewExportFileName = (exportFilesPath + "SimExport_"
                             + str(timestrf) + ".txt")
        newFile = open(NewExportFileName, "w")

        for i in range(len(dist)):
            lineToWrite = (str(dist[i]) + "\t" + str(vcar[i]) + "\n")
            newFile.write(lineToWrite)
        newFile.close()
        return NewExportFileName

    def run(self):
        print("---------------------------")
        print("OpenLapSim")
        print("---------------------------")

        # Computation time start
        tstart = time.time()

        # SetupFile obj instantiation
        s = SetupFileLoader(self.setupFilesPath + self.setupFileName)
        s.loadJSON()

        # Run Acceleration Envelope
        aE = AccEnvCalc(s.setupDict)
        aE.Run()

        # Run Lap time Simulation
        trackFile = (self.trackFilesPath+self.trackFileName)
        l1 = LapTimeSimCalc(trackFile, aE.accEnvDict, 10)
        l1.Run()
        l2 = LapTimeSimCalc(trackFile, aE.accEnvDict,
                            l1.lapTimeSimDict["vxaccEnd"])
        l2.Run()

        # set output channels from simulation for Export
        vcar = l2.lapTimeSimDict["vcar"]  # car speed [m/s]
        dist = l2.lapTimeSimDict["dist"]  # circuit dist [m]

        # export
        if self.bExport == 1:
            RunOpenLapSim.createExportSimFile(vcar, dist, self.exportFilesPath)

        # Computation time end
        tend = time.time()
        tcomp = round(tend - tstart, 1)
        print("Computational time: ", tcomp)

        # Post Processing
        pP = PostProc(aE.accEnvDict, l2.lapTimeSimDict)
        pP.printData()
        if self.bPlot == 1:
            # pP.plotAccEnv()
            pP.plotGGV()
            pP.plotLapTimeSim()
        if self.bPlotExtra == 1:
            pP.plotLapTimeSimExtra()
            pP.plotAccEnvExtra()
        plt.show()  # plot all figure once at the end

        # output values
        self.laptime = l2.lapTimeSimDict["laptime"]
        self.vcarmax = l2.lapTimeSimDict["vcarmax"]
        self.tcomp = tcomp

# ----------------------------------------------------------------------------


if __name__ == '__main__':

    # SetupFile.json
    setupFileName = "SetupFile.json"
    # TrackFile.txt
    trackFileName = "TrackFile.txt"
    # Additional Options
    bExport = 1
    bPlot = 1
    bPlotExtra = 0

    # object instantiation
    runOpenLapSim = RunOpenLapSim(setupFileName, trackFileName,
                                  bExport, bPlot, bPlotExtra)
    runOpenLapSim.run()
