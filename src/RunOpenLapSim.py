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
import argparse

import numpy as np

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
        trackFile = (self.trackFilesPath + self.trackFileName)
        l1 = LapTimeSimCalc(trackFile, aE.accEnvDict, 10)
        l1.Run()

        # Run second simulation using starting speed from first lap
        l2 = LapTimeSimCalc(trackFile, aE.accEnvDict,
                            l1.lapTimeSimDict["vxaccEnd"])
        l2.Run()



        # set output channels from simulation for Export
        vcar = l2.lapTimeSimDict["vcar"]  # car speed [m/s]
        dist = l2.lapTimeSimDict["dist"]  # circuit dist [m]
        lap_time = l2.lapTimeSimDict["time"]
        acc = np.gradient(vcar, lap_time)
        force = s.setupDict["mcar"] * acc + (0.5 * s.setupDict["rho"] * np.square(vcar) * s.setupDict["cx"] * s.setupDict["afrcar"])
        power = force * vcar
        # No regen braking :(
        positive_power = np.maximum(power, np.zeros(power.shape))
        rms_power = np.sqrt(np.average(np.square(positive_power)))
        print(f"RMS Power: {rms_power / 1000} kW")

        if self.bPlotExtra:
            plt.plot(lap_time, power)

        # plt.show()


        # export
        if self.bExport:
            RunOpenLapSim.createExportSimFile(vcar, dist, self.exportFilesPath)

        # Computation time end
        tend = time.time()
        tcomp = round(tend - tstart, 1)
        print("Computational time: ", tcomp)

        # Post Processing
        pP = PostProc(aE.accEnvDict, l2.lapTimeSimDict)
        pP.printData()
        if self.bPlot:
            # pP.plotAccEnv()
            pP.plotGGV()
            pP.plotLapTimeSim()
        if self.bPlotExtra:
            pP.plotLapTimeSimExtra()
            pP.plotAccEnvExtra()
        plt.show()  # plot all figure once at the end

        # output values
        self.laptime = l2.lapTimeSimDict["laptime"]
        self.vcarmax = l2.lapTimeSimDict["vcarmax"]
        self.tcomp = tcomp


# ----------------------------------------------------------------------------



def main():
    parser = argparse.ArgumentParser(description="OpenLapSim")

    parser.add_argument("--setup", type=str, default="SetupFile.json", help="Name of the setup file.")
    parser.add_argument("--track", type=str, default="TrackFile.txt", help="Name of the track file.")
    parser.add_argument("--export", action="store_true", help="Export results.")
    parser.add_argument("--plot", action="store_true", help="Plot basic results.")
    parser.add_argument("--plot-extra", action="store_true", help="Enable extra plots.")

    args = parser.parse_args()

    setupFileName = args.setup
    trackFileName = args.track
    bExport = args.export
    bPlot = args.plot
    bPlotExtra = args.plot_extra

    # object instantiation
    runOpenLapSim = RunOpenLapSim(setupFileName, trackFileName,
                                  bExport, bPlot, bPlotExtra)
    runOpenLapSim.run()


if __name__ == '__main__':
    main()
