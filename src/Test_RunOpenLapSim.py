"""
---------------------------
OpenLapSim - OLS
---------------------------
This is a quasi-static Lap Time Simulator for a simple point mass vehicle 
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
#-----------------------------------------------------------------------------
"""
---------------------------
Select Files
---------------------------
"""
# SetupFile.json
setupFileName = "SetupFile.json"

# TrackFile.txt
trackFileName = "TrackFile.txt"

bExport = 1
bPlotExtra = 1
#-----------------------------------------------------------------------------

# import packages generic
import datetime

# import packages (OLP)
from AccEnvCalc import*
from LapTimeSimCalc_Test import*
from PostProc import*
from SetupFileLoader import SetupFileLoader

class RunOpenLapSim:
    
        def __init__(self, setupFileName, trackFileName, bExport, bPlotExtra): 
            # inputs
            self.setupFileName = setupFileName
            self.trackFileName = trackFileName
            self.bExport = bExport
            self.bPlotExtra = bPlotExtra
            self.trackFilesPath = "trackFiles/"
            self.exportFilesPath = "exportFiles/"
            self.setupFilesPath = "setupFiles/"
        
        @staticmethod
        def createExportSimFile(vcar, dist,exportFilesPath):        
            time = datetime.datetime.now()
            timestrf = time.strftime("%b-%d-%Y")
            NewExportFileName = (exportFilesPath+"SimExport_" + str(timestrf) + ".txt")
            newFile = open(NewExportFileName, "w")
            
            for i in range(len(dist)):  
                lineToWrite = (str(dist[i]) + "\t" + str(vcar[i]) + "\n")
                newFile.write(lineToWrite)
            newFile.close()
            return NewExportFileName;
        
        def run(self):                       
            """
            ---------------------------
            Run Simulation
            ---------------------------
            """
            #SetupFile obj instantiation
            s = SetupFileLoader(self.setupFilesPath + self.setupFileName)
            s.loadJSON()
            
            # Run Acceleration Envelope
            aE = AccEnvCalc(s.setupDict)
            aE.Run()
            
            # Run Lap time Simulation
            trackFile = (self.trackFilesPath+self.trackFileName)
            l1 = LapTimeSimCalc(trackFile,aE.accEnvDict,10)
            l1.Run()

#-----------------------------------------------------------------------------

#object instantiation
runOpenLapSim = RunOpenLapSim(setupFileName,trackFileName,bExport,bPlotExtra)
runOpenLapSim.run()


