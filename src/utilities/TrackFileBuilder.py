"""
---------------------------
TrackFileBuilder - OLS
---------------------------
This utility creates a TrackFile.txt for OpenLapSim from real Temeretry data.

Steps:
    1 - Specify the telemetry "telemetryFile.csv"
        The csv file sould be on the format:
            - Dist[m], Speed[km/h], Glat[g]
            - if different units change the convertions param
    2 - Run the routine.
    3 - The TrackFile.txt generated is saved in \src\trackFile

Options:
    4 - Adjust the filter Cutoff frequency, which is applied to smooth noize
        from Glat and Speed telemetry data if necessary (Wn).

---------------------------
@autor: Davide Strassera
@first release: 2020-05-17
by Python 3.7
---------------------------
"""
# ----------------------------------------------------------------------------

# import packages
import csv
import math as mt
import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
import datetime
from pathlib import Path
import os


class TrackFileBuilder:

    def __init__(self, telemetryFileName, firstLine,
                 rowDist, rowSpeed, rowGlat):
        # inputs
        self.telemetryFileName = telemetryFileName
        self.firstLine = firstLine
        self.rowDist = rowDist
        self.rowSpeed = rowSpeed
        self.rowGlat = rowGlat
        self.cwd = os.getcwd()
        self.trackFilesPath = str(Path(self.cwd).parent)

    def loadTelemetryFile(self):

        telemDist = []
        telemSpeed = []
        telemGlat = []

        with open(self.telemetryFileName) as csvDataFile:
            csvReader = csv.reader(csvDataFile)
            line = 0
            for row in csvReader:
                if line > self.firstLine:
                    telemDist.append(float(row[self.rowDist]))  # 1
                    telemSpeed.append(float(row[self.rowSpeed]))  # 2
                    telemGlat.append(float(row[self.rowGlat]))  # 8
                    line += 1
                else:
                    line += 1

        return telemDist, telemSpeed, telemGlat

    @staticmethod
    def filterTelemetryData(telemData, bplot):
        # First, design the Buterworth filter
        N = 2    # Filter order
        Wn = 0.1  # Cutoff frequency
        B, A = signal.butter(N, Wn, output='ba')

        # Second, apply the filter
        telemDataFilt = signal.filtfilt(B, A, telemData)

        if bplot == 1:
            plt.figure(1)
            plt.title("Data Filtering")
            plt.plot(telemData, 'r-', label="row data")
            plt.plot(telemDataFilt, 'b-', label="filtered data")
            plt.legend()
            plt.grid(b=True, which='major', linestyle=':')
            plt.show()

        return telemDataFilt

    @staticmethod
    def calculateCurvature(telemDist, telemSpeed, telemGlatFilt):
        # units conversion
        speedToms = 1/3.6  # kph to ms
        glatToms2 = 9.81  # g to ms2

        curvature = []
        radius = []

        for i in range(len(telemDist)):
            # ay = (v^2)/R --> R = (v^2)/ay
            try:
                radius.append(mt.pow((telemSpeed[i]*speedToms), 2)
                              / (telemGlatFilt[i]*glatToms2))
            except ZeroDivisionError:
                radius.append(1000)  # if it is straight line
            curvature.append(1/radius[i])

        return curvature

    @staticmethod
    def createNewTrackFile(telemDist, curvature, trackFilesPath):
        time = datetime.datetime.now()
        timestrf = time.strftime("%b-%d-%Y")
        NewTrackFileName = (trackFilesPath+"/trackFiles/TrackFile_"
                            + str(timestrf)+".txt")
        newFile = open(NewTrackFileName, "w")

        for i in range(len(telemDist)):
            lineToWrite = (str(telemDist[i]) + "\t" + str(curvature[i]) + "\n")
            newFile.write(lineToWrite)
        newFile.close()
        return NewTrackFileName

    @staticmethod
    def compareTrackFile(TrackFile1, TrackFile2):
        track1 = np.loadtxt(TrackFile1)
        dist1 = track1[:, 0]
        curv1 = track1[:, 1]

        track2 = np.loadtxt(TrackFile2)
        dist2 = track2[:, 0]
        curv2 = track2[:, 1]

        plt.figure(3)
        plt.title("Calculated Curvature")
        plt.plot(dist1, curv1, 'r-', label=TrackFile1)
        plt.plot(dist2, curv2, 'b-', label=TrackFile2)
        plt.xlabel('distance [m]')
        plt.ylabel('curvature [1/R]')
        plt.grid(b=True, which='major', linestyle=':')
        plt.show()

    def run(self):
        telemDist, telemSpeed, telemGlat = TrackFileBuilder.loadTelemetryFile(self)
        telemSpeedFilt = TrackFileBuilder.filterTelemetryData(telemSpeed, 0)
        telemGlatFilt = TrackFileBuilder.filterTelemetryData(telemGlat, 1)
        curvature = TrackFileBuilder.calculateCurvature(telemDist,
                                                        telemSpeedFilt,
                                                        telemGlatFilt)
        newTrackFileName = TrackFileBuilder.createNewTrackFile(telemDist,
                                                               curvature,
                                                               self.trackFilesPath)
        return newTrackFileName


# ----------------------------------------------------------------------------


if __name__ == '__main__':

    # TelemetryFile.csv
    telemetryFileName = "telemetryFile.csv"
    firstLine = 2
    rowDist = 1
    rowSpeed = 2
    rowGlat = 8

    # Object instantiation
    trackFileBuilder = TrackFileBuilder(telemetryFileName, firstLine,
                                        rowDist, rowSpeed, rowGlat)
    newTrackFileName = trackFileBuilder.run()
    TrackFileBuilder.compareTrackFile(newTrackFileName, newTrackFileName)
