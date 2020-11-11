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
import time
# import packages (OLP)
from AccEnvCalc import*
from LapTimeSimCalc import*
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
            # Computation time start
            tstart = time.time()
            
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
            l2 = LapTimeSimCalc(trackFile,aE.accEnvDict,l1.lapTimeSimDict["vxaccEnd"])
            l2.Run()
            
            # Computation time end
            tend = time.time()
            tcomp = round(tend - tstart,1)
            print("Computational time: ", tcomp)

            # Post Processing
            pP = PostProc(aE.accEnvDict, l2.lapTimeSimDict)
            pP.plotAccEnv()
            pP.plotGGV()
            #pP.f1.show()
            pP.plotLapTimeSim()
            #pP.f2.show()
            if self.bPlotExtra==1 :
                pP.plotLapTimeSimExtra()
                #pP.f3.show()
                pP.plotAccEnvExtra()
                #pP.f4.show()
            pP.printData()
            plt.show() 
            # set output channels from simulation
            vcar = l2.lapTimeSimDict["vcar"] #car speed [m/s]
            dist = l2.lapTimeSimDict["dist"] #circuit dist [m]
            
            # export
            if self.bExport==1:
                RunOpenLapSim.createExportSimFile(vcar, dist,self.exportFilesPath)

#-----------------------------------------------------------------------------

#object instantiation
runOpenLapSim = RunOpenLapSim(setupFileName,trackFileName,bExport,bPlotExtra)
runOpenLapSim.run()


