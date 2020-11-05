"""
---------------------------
Acceleration Envelope Calculator - OLS
---------------------------
"""
# Import Packages
import numpy as np
import scipy.constants as sc
import scipy.interpolate as interp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class AccEnvCalc:
        
    def __init__(self,setupDict):
        #input
        self.mcar    = setupDict["mcar"]
        self.clt     = setupDict["clt"]       
        self.cx      = setupDict["cx"]
        self.afrcar  = setupDict["afrcar"]
        self.mbrk    = setupDict["mbrk"]
        self.gripx   = setupDict["gripx"]
        self.gripy   = setupDict["gripy"]
        self.loadEff = setupDict["loadEff"]
        self.rtyre   = setupDict["rtyre"]
        self.rGearRat = setupDict["rGearRat"]
        self.reff    = setupDict["reff"]
        self.EngNm  = setupDict["EngNm"]
        self.EngRpm  = setupDict["EngRpm"] 
        self.rho     = setupDict["rho"]
        # constants
        self.g       = sc.g     # 9.80665
        self.pi      = sc.pi    # 3.14159
        #parameters
        self.nSteps = 20
        self.LOAD_EFF_SCALE = 10000 #[N]
        #output
        self.accEnvDict = {
            "vxvect"    : None, 
            "axacc"     : None,
            "axdec"     : None,
            "ay"        : None,
            # extra Channels
            "nGear"     : None,
            "EngNm"     : None,
            "EngRpm"    : None,
            "Fzaero"    : None,
            "Fxaero"    : None,
            "gripx"     : None,
            "gripy"     : None,
            "Fxgrip"    : None,
            "Fxdrive"   : None,
            # GGV
            "GGVacc"    : None,
            "GGVdec"    : None,
            "GGVfull"    : None,
        }
    
    #VxMax Calculation (forces equilibrium)
    def Run(self): 
        # Functions Definitions
        def Mfinaldrive(vx,EngNm,EngRpm,rGear):
            neng = np.zeros(len(self.rGearRat))
            meng = np.zeros(len(self.rGearRat))
            Mfinaldrive = np.zeros(len(self.rGearRat))
            for i in range(len(self.rGearRat)):
                ntyre = vx/(2*self.pi*self.rtyre)*60
                neng[i] = ntyre*self.rGearRat[i]
                meng[i] = np.interp(neng[i],self.EngRpm,self.EngNm)
                #check nengine is in range of rmp max (revlimit) and min (stall)
                if min(EngRpm)<neng[i]<max(EngRpm):
                    meng[i] = meng[i]
                else:
                    meng[i] = 0
                Mfinaldrive[i] = meng[i]*self.rGearRat[i]
            # from the Mfinaldrive[i] array select index which has max Torque
            indexArray = np.where(Mfinaldrive == np.amax(Mfinaldrive))
            #outMfinaldrive = max(Mfinaldrive)
            index = indexArray[0][0]# WARNING can have 2 pos with same resutl!!!
            outMfinaldrive = Mfinaldrive[index]
            outmeng = meng[index]
            outneng = neng[index]
            outnGear = index+1
            return  outMfinaldrive, outmeng, outneng, outnGear
            
        def Fxaero(vx):
            outFxaero = 0.5*self.rho*pow(vx,2)*self.afrcar*self.cx #[N]
            return outFxaero
        
        def Fzaero(vx):
            outFzaero = 0.5*self.rho*pow(vx,2)*self.afrcar*self.clt #[N]
            return outFzaero
        
        def gripLoadEff(grip, fz):
            deltaGripLoadEff = grip*(self.loadEff*(fz/self.LOAD_EFF_SCALE))
            newGrip = grip - deltaGripLoadEff
            return newGrip
        
        vxmax = 1
        e = 0.1
        while e>0.05: 
            e =((Mfinaldrive(vxmax,self.EngNm,self.EngRpm,self.rGearRat)[0]/self.rtyre)-Fxaero(vxmax))/self.mcar
            vxmax += 0.1
        
        # Ax & Ay Calculation
        nSteps = self.nSteps
        vxstep = vxmax/nSteps+1
        small = 0.00000001 # to avoid division by zero
        vxvect = np.arange(small,vxmax,vxstep)
            
        ay = [0]*len(vxvect)
        for i in range(len(vxvect)):
            Fzaero_ = Fzaero(vxvect[i])
            ay[i] = (Fzaero_+self.mcar*self.g)*gripLoadEff(self.gripy,Fzaero_+self.mcar*self.g)/self.mcar
                
        Fxbrk = self.mbrk/self.rtyre
        axacc = [0]*len(vxvect)
        axdec = [0]*len(vxvect)
        Fxgrip = [0]*len(vxvect)
        Fxaero_ = [0]*len(vxvect)
        Fzaero_ = [0]*len(vxvect)
        Fxdrive = [0]*len(vxvect)
        outmeng = [0]*len(vxvect)
        outneng = [0]*len(vxvect)
        outnGear = [0]*len(vxvect)
        for i in range(len(vxvect)):
            Fzaero_[i] = Fzaero(vxvect[i])
            Fxgrip[i]=(Fzaero_[i]+self.mcar*self.g)*gripLoadEff(self.gripx,Fzaero_[i]+self.mcar*self.g) #grip limit Fx
            Fxaero_[i] = Fxaero(vxvect[i])
            outMfinaldrive, outmeng[i], outneng[i], outnGear[i] = Mfinaldrive(vxvect[i],self.EngNm,self.EngRpm,self.rGearRat)
            Fxdrive[i] = outMfinaldrive*self.reff/self.rtyre
            axacc[i] = max(0,(min(Fxdrive[i],Fxgrip[i])-Fxaero_[i])/self.mcar)
            axdec[i] = -(min(Fxbrk,Fxgrip[i])+Fxaero_[i])/self.mcar 
            
        self.accEnvDict = {
            "vxvect"    : vxvect, 
            "axacc"     : axacc,
            "axdec"     : axdec,
            "ay"        : ay,
            # extra Channels
            "nGear"     : outnGear,
            "EngNm"     : outmeng,
            "EngRpm"    : outneng,
            "Fzaero"    : Fzaero_,
            "Fxaero"    : Fxaero_,
            "gripx"     : None,
            "gripy"     : None,
            "Fxgrip"    : Fxgrip,
            "Fxdrive"   : Fxdrive,
        }
        
        def generateGGV(axacc,axdec,ay,vxvect): 
            nAx = 100 
            nVx = len(vxvect)
            size = nVx*nAx
            # GGV ACCELERATION
            GGVacc = np.zeros((size,3)) # ay,ax,vx
            for i in range (nVx):   
                ayStep = np.absolute(ay[i])/(nAx)
                for j in range(nAx):
                    ayreal = ay[i] - ayStep*j
                    axcombine = np.sqrt(np.absolute(np.power(axacc[i],2)*(1-(np.power(ayreal,2)/np.power(ay[i],2)))))
                    index = (i*nAx)+j
                    GGVacc[index,0] = np.round(axcombine,2)
                    GGVacc[index,1] = np.round(ayreal,2)
                    GGVacc[index,2] = np.round(vxvect[i],2)        
            #GGV DECELERATION
            GGVdec = np.zeros((size,3)) # ax,ay,vx
            for i in range (nVx):   
                ayStep = np.absolute(ay[i])/(nAx)
                for j in range(nAx):
                    ayreal = ay[i] - ayStep*j
                    axcombine = - np.sqrt(np.absolute(np.power(axdec[i],2)*(1-(np.power(ayreal,2)/np.power(ay[i],2)))))
                    index = ((i*nAx)+j)
                    GGVdec[index,0] = np.round(axcombine,2)
                    GGVdec[index,1] = np.round(ayreal,2)
                    GGVdec[index,2] = np.round(vxvect[i],2)     
            return GGVacc, GGVdec
        
        ay = self.accEnvDict["ay"]
        axdec = self.accEnvDict["axdec"]
        axacc = self.accEnvDict["axacc"]
        vxvect = self.accEnvDict["vxvect"]
        
        GGVacc, GGVdec = generateGGV(axacc,axdec,ay,vxvect)
       
        # Mirror the GGV to left and concat GGVacc and GGVdec 
        GGVfull = np.concatenate((GGVacc, GGVdec))        
        GGVaccLeft = GGVacc* [1,-1,1]
        GGVacc = np.concatenate((GGVacc,GGVaccLeft))
        GGVdecLeft = GGVdec* [1,-1,1]
        GGVdec = np.concatenate((GGVdec,GGVdecLeft))        
        
        self.accEnvDict["GGVacc"] = GGVacc
        self.accEnvDict["GGVdec"] = GGVdec
        self.accEnvDict["GGVfull"] = GGVfull
        
        xyz1 = GGVacc
        X1= xyz1[:,0]
        Y1= xyz1[:,1]
        Z1= xyz1[:,2]
        ploty1,plotz1, = np.meshgrid(np.linspace(np.min(Y1),np.max(Y1),30),\
                                   np.linspace(np.min(Z1),np.max(Z1),30))
        # Griddata
        plotx1 = interp.griddata((Y1,Z1),X1,(ploty1,plotz1),method='linear',fill_value=0.0)
        
        xyz2 = GGVdec
        X2= xyz2[:,0]
        Y2= xyz2[:,1]
        Z2= xyz2[:,2]
        ploty2,plotz2, = np.meshgrid(np.linspace(np.min(Y2),np.max(Y2),30),\
                                   np.linspace(np.min(Z2),np.max(Z2),30))
        plotx2 = interp.griddata((Y2,Z2),X2,(ploty2,plotz2),method='linear', fill_value=0.0)
       
        xyz3= GGVfull
        X3= xyz3[:,0]
        Y3= xyz3[:,1]
        Z3= xyz3[:,2]
        plotx3,plotz3, = np.meshgrid(np.linspace(np.min(X3),np.max(X3),30),\
                                   np.linspace(np.min(Z3),np.max(Z3),30))
        # Griddata
        ploty3 = interp.griddata((X3,Z3),Y3,(plotx3,plotz3),method='linear',fill_value=0.0)
       
        # RBF (radius basis function)
        # rbfi = interp.Rbf(X3, Z3, Y3, functionc='cubic', smooth=0)  # default smooth=0 for interpolation
        # ploty3 = rbfi(plotx3, plotz3)  # not really a function, but a callable class instance
        
        axcombine = interp.griddata((Y2,Z2),X2,(0.0,40),method='cubic')
        print(axcombine)
        
        
        fig = plt.figure(5)
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(plotx1,ploty1,plotz1,cstride=1,rstride=1,cmap='viridis')
        ax.scatter(X1,Y1,Z1)
        ax.plot_surface(plotx2,ploty2,plotz2,cstride=1,rstride=1,cmap='viridis')
        ax.scatter(X2,Y2,Z2)

        fig = plt.figure(6)
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(plotx3,ploty3,plotz3,cstride=1,rstride=1,cmap='viridis')
        ax.scatter(X3,Y3,Z3)
        
        print("AccEnvCalc completed")


