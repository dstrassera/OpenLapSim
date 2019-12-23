"""
---------------------------
Post Processing - OLS
---------------------------
"""
# Import packages
import matplotlib.pyplot as plt
import numpy as np

class PostProc:
    
    def __init__(self, accEnvDict, lapSimTimeDict):
        self.size   = 10
        # input
        self.vxvect  = accEnvDict["vxvect"]
        self.ay      = accEnvDict["ay"]
        self.axacc   = accEnvDict["axacc"]
        self.axdec   = accEnvDict["axdec"]
        self.dist    = lapSimTimeDict["dist"]
        self.vcar    = lapSimTimeDict["vcar"]
        self.laptime = lapSimTimeDict["laptime"]
        self.vcarmax = lapSimTimeDict["vcarmax"]
        self.vxacc   = lapSimTimeDict["vxacc"]
        self.vxdec   = lapSimTimeDict["vxdec"]
        self.vxcor   = lapSimTimeDict["vxcor"]
        # output
        self.f1 = None
        self.f2 = None
        self.f3 = None
        
    def plotAccEnv(self):
        f = plt.figure(1,figsize=(self.size/2,self.size/2))
        plt.title("Acceleration Envelope")
        plt.plot(self.ay,self.vxvect,'c-',label="ay")
        plt.plot(self.axacc,self.vxvect,'m-',label = "ax acc")
        plt.plot(self.axdec,self.vxvect,'r-',label = "ax dec")
        plt.legend()
        plt.xlabel('acceleration [m/s^2]')
        plt.ylabel('velocity [m/s]')
        plt.grid(b=True,which='major',linestyle=':')
        plt.ylim(0,self.vcarmax*1.2)
        #plt.xlim(-60,60)
        self.f1 = f

    def plotLapTimeSim(self):
        f = plt.figure(2,figsize=(self.size,self.size/2))
        plt.title("Lap Time Simulation")
        plt.plot(self.dist,self.vcar,'b-',linewidth=2,label = "vcar")
        plt.xlabel('distance [m]')
        plt.ylabel('velocity [m/s]')
        plt.legend()
        plt.grid(b=True,which='major',linestyle=':')
        plt.ylim(0,self.vcarmax*1.2)
        plt.xlim(0,max(self.dist))
        self.f2 = f
        
    def plotLapTimeSimExtra(self):
        f = plt.figure(3,(self.size,self.size/2))
        plt.title("Lap Time Simulation - Extra")
        plt.plot(self.dist,self.vxcor,'c-',label = "vxcor")
        plt.plot(self.dist,self.vxacc,'m-',label = "vxacc")
        plt.plot(self.dist,self.vxdec,'r-',label = "vxdec")
        plt.plot(self.dist,self.vcar,'b-',linewidth=2,label = "vcar")
        plt.xlabel('distance [m]')
        plt.ylabel('velocity [m/s]')
        plt.legend()
        plt.grid(b=True,which='major',linestyle=':')
        plt.ylim(0,self.vcarmax*1.2)
        plt.xlim(0,max(self.dist))
        self.f3 = f
        
    def printData(self):
        print("PostProc completed")
        print("---------------------------")
        print("LapTime: ",self.laptime,"[s]")
        print("TopSpeed: ",np.round(self.vcarmax*3.6,1),"[Km/h]")
        print("---------------------------")


