"""
---------------------------
OpenLapSim - OLS
---------------------------
This is a quasi-static Lap Time Simulator for a simple point mass vehicle 
with aero forces, constant tyre grip(x and y), engine torque map and gears.

Steps:
    1 - Select Files: TrackFile.txt and SetupFile.py
    2 - Calculates the Performance Envelope
    3 - Calculates the Lap Simulation(vcar)
    4 - Plot Results
---------------------------
@autor: Davide Strassera
@vesrion: 2019-12-21
by Python 3.7
---------------------------
"""
#-----------------------------------------------------------------------------
"""
---------------------------
Select Files
---------------------------
"""
# TrackFile.txt
TrackFile = 'TrackFile.txt'

# SetupFile.py
from SetupFile import*

#-----------------------------------------------------------------------------
"""
---------------------------
Run Simulation
---------------------------
"""
#load SetupFile
s = SetupFile()

# Run Performance Envelope
from PerfEnvCalc import*
pE = PerfEnvCalc(s.setupDict)
pE.Run()

# Run Lap time Simulation
from LapSimCalc import*
l1 = LapSimCalc(TrackFile,pE.perfEnvDict,10)
l1.Run()
l2 = LapSimCalc(TrackFile,pE.perfEnvDict,l1.lapSimDict["vxaccEnd"])
l2.Run()

# Post Processing
from PostProc import*
pP = PostProc(pE.perfEnvDict, l2.lapSimDict)
pP.plotPerfEnv()
pP.f1.show()
pP.plotLapSim()
pP.f2.show()
pP.plotLapSimExtra()
pP.f3.show()
pP.printData()

#-----------------------------------------------------------------------------





