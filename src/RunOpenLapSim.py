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
#SetupFile obj instantiation
s = SetupFile()

# Run Acceleration Envelope
from AccEnvCalc import*
aE = AccEnvCalc(s.setupDict)
aE.Run()

# Run Lap time Simulation
from LapTimeSimCalc import*
l1 = LapTimeSimCalc(TrackFile,aE.accEnvDict,10)
l1.Run()
l2 = LapTimeSimCalc(TrackFile,aE.accEnvDict,l1.lapTimeSimDict["vxaccEnd"])
l2.Run()

# Post Processing
from PostProc import*
pP = PostProc(aE.accEnvDict, l2.lapTimeSimDict)
pP.plotAccEnv()
pP.f1.show()
pP.plotLapTimeSim()
pP.f2.show()
#pP.plotLapTimeSimExtra()
#pP.f3.show()
pP.printData()

#-----------------------------------------------------------------------------





