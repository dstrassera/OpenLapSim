"""
---------------------------
Acceleration Envelope Calculator - OLS
---------------------------
"""
# Import Packages
import numpy as np
import scipy.constants as sc

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
        #output
        self.accEnvDict = {
            "vxvect"    : None, 
            "axacc"     : None,
            "axdec"     : None,
            "ay"        : None,
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
            outMfinaldrive = max(Mfinaldrive)
            return outMfinaldrive
            
        def Fxaero(vx):
            outFxaero = 0.5*self.rho*pow(vx,2)*self.afrcar*self.cx #[N]
            return outFxaero
        
        def Fzaero(vx):
            outFzaero = 0.5*self.rho*pow(vx,2)*self.afrcar*self.clt #[N]
            return outFzaero
        
        vxmax = 1
        e = 0.1
        while e>0.05:
            e =((Mfinaldrive(vxmax,self.EngNm,self.EngRpm,self.rGearRat)/self.rtyre)-Fxaero(vxmax))/self.mcar
            vxmax += 0.1
        
        # Ax & Ay Calculation
        nSteps = self.nSteps
        vxstep = vxmax/nSteps+1
        small = 0.00000001 # to avoid division by zero
        vxvect = np.arange(small,vxmax,vxstep)
            
        ay = [0]*len(vxvect)
        for i in range(len(vxvect)):
            ay[i] = (Fzaero(vxvect[i])+self.mcar*self.g)*self.gripy/self.mcar
                
        Fxbrk = self.mbrk/self.rtyre
        axacc = [0]*len(vxvect)
        axdec = [0]*len(vxvect)
        Fxgrip = [0]*len(vxvect)
        Fxaero_ = [0]*len(vxvect)
        Fxdrive = [0]*len(vxvect)
        for i in range(len(vxvect)):
            Fxgrip[i]=(Fzaero(vxvect[i])+self.mcar*self.g)*self.gripx #grip limit Fx
            Fxaero_[i] = Fxaero(vxvect[i])
            Fxdrive[i] = Mfinaldrive(vxvect[i],self.EngNm,self.EngRpm,self.rGearRat)*self.reff/self.rtyre
            axacc[i] = max(0,(min(Fxdrive[i],Fxgrip[i])-Fxaero_[i])/self.mcar)
            axdec[i] = -(min(Fxbrk,Fxgrip[i])+Fxaero_[i])/self.mcar 
            
        self.accEnvDict = {
            "vxvect"    : vxvect, 
            "axacc"     : axacc,
            "axdec"     : axdec,
            "ay"        : ay, 
        }
        
        print("AccEnvCalc completed")


