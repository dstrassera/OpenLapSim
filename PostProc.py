"""
---------------------------
Post Processing - OLS
---------------------------
"""
# Import packages
import matplotlib.pyplot as plt
import numpy as np

class PostProc:
    
    def __init__(self, perfEnvDict, lapSimDict):
        self.size   = 10
        # input
        self.vxvect  = perfEnvDict["vxvect"]
        self.ay      = perfEnvDict["ay"]
        self.axacc   = perfEnvDict["axacc"]
        self.axdec   = perfEnvDict["axdec"]
        self.dist    = lapSimDict["dist"]
        self.vcar    = lapSimDict["vcar"]
        self.laptime = lapSimDict["laptime"]
        self.vcarmax = lapSimDict["vcarmax"]
        self.vxacc   = lapSimDict["vxacc"]
        self.vxdec   = lapSimDict["vxdec"]
        self.vxcor   = lapSimDict["vxcor"]
        # output
        self.f1 = None
        self.f2 = None
        self.f3 = None
        
    def plotPerfEnv(self):
        f = plt.figure(1,figsize=(self.size/2,self.size/2))
        plt.title("Performance Envelope")
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

    def plotLapSim(self):
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
        
    def plotLapSimExtra(self):
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


