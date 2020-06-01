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
        #extra channels (AccEnv)
        self.nGear    = accEnvDict["nGear"]
        self.EngNm    = accEnvDict["EngNm"]
        self.EngRpm   = accEnvDict["EngRpm"]
        self.Fzaero   = accEnvDict["Fzaero"]
        self.Fxaero   = accEnvDict["Fxaero"]
        self.Fxgrip   = accEnvDict["Fxgrip"]
        self.Fxdrive   = accEnvDict["Fxdrive"]
        
        # output
        self.f1 = None
        self.f2 = None
        self.f3 = None
        self.f4 = None
        
    def plotAccEnv(self):
        f = plt.figure(1,figsize=(self.size/2,self.size/2))
        plt.title("Acceleration Envelope")
        plt.plot(self.ay,self.vxvect,'c-',label="ay")
        plt.plot(self.axacc,self.vxvect,'m-',label = "axacc")
        plt.plot(self.axdec,self.vxvect,'r-',label = "axdec")
        plt.legend()
        plt.xlabel('acceleration [m/s^2]')
        plt.ylabel('velocity [m/s]')
        plt.grid(b=True,which='major',linestyle=':')
        plt.ylim(0,self.vcarmax*1.2)
        self.f1 = f
        
    def plotAccEnvExtra(self):
        f, (ax1, ax2, ax3, ax4) = plt.subplots(1,4,figsize=(self.size*1.5,self.size/2))
        ax1.set_title("Forces[N] (vcar[m/s])")
        ax1.plot(self.Fzaero,self.vxvect,'c-',label="Fzaero")
        ax1.plot(self.Fxaero,self.vxvect,'m-',label = "Fxaero")
        ax1.plot(self.Fxgrip,self.vxvect,'r-',label = "FxGrip")
        ax1.plot(self.Fxdrive,self.vxvect,'g-',label = "FxDrive")
        ax1.legend()
        ax1.grid(b=True,which='major',linestyle=':')
        
        ax2.set_title("Gear (vcar[m/s])")
        ax2.plot(self.nGear,self.vxvect,'c-',label="nGear")
        ax2.legend()
        ax2.grid(b=True,which='major',linestyle=':')

        ax3.set_title("EngNm (vcar[m/s])")
        ax3.plot(self.EngNm,self.vxvect,'c-',label="EngNm")
        ax3.legend()
        ax3.grid(b=True,which='major',linestyle=':')

        ax4.set_title("EngRpm (vcar[m/s])")
        ax4.plot(self.EngRpm,self.vxvect,'c-',label="EngRpm")
        ax4.legend()
        ax4.grid(b=True,which='major',linestyle=':')
        self.f4 = f

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


