"""
---------------------------
Lap Time Simulation Calculator - OLS
---------------------------
"""
# Import Packages
import numpy as np
import math as mt
import scipy.interpolate as interp
import matplotlib.pyplot as plt

class LapTimeSimCalc:
    
        def __init__(self,TrackFile,accEnvDict,vxaccStart):
            #inputs
            self.TrackFile  = TrackFile
            self.vxvect     = accEnvDict["vxvect"]
            self.axacc      = accEnvDict["axacc"]
            self.axdec      = accEnvDict["axdec"]
            self.ay         = accEnvDict["ay"]
            self.GGVacc     = accEnvDict["GGVacc"] # ax,ay,vx
            self.GGVdec     = accEnvDict["GGVdec"] # ax,ay,vx
            self.GGVfull     = accEnvDict["GGVfull"] # ax,ay,vx
            self.vxaccStart = vxaccStart
            #outputs
            self.lapTimeSimDict = {
                "vcar"       : None,
                "dist"       : None,
                "time"       : None,
                "laptime"    : None,
                "vcarmax"    : None,
                "vxaccEnd"   : None,
                "vxacc"      : None,
                "vxdec"      : None,
                "vxcor"      : None,
            }


        def Run(self):
            small = 0.0000001

            # GGV std
            def GGVstd(self, vxacc, ayreal):
                axaccmap = np.interp(vxacc, self.vxvect, self.axacc, period=360)
                aymap = max(np.interp(vxacc, self.vxvect, self.ay, period=360), small)
                # ayreal = pow(vxacc, 2)/(1/max(curv, small))
                # axcombine = axaccmap*mt.sqrt(np.absolute(1-(ayreal/aymap)))
                axcombine = np.sqrt(np.absolute(np.power(axaccmap,2)*(1-(np.power(ayreal,2)/np.power(aymap,2)))))
                return axcombine
 
            # GGV surface
            def GGVsurf(self, vxacc, ayreal):
                X,Y,Z = self.GGVacc[:,0],self.GGVacc[:,1],self.GGVacc[:,2]
                # X,Y,Z = self.GGVfull[:,0],self.GGVfull[:,1],self.GGVfull[:,2]
                ay = ayreal
                axcombine = interp.griddata((Y,Z),X,(ay,vxacc),method='linear')#,fill_value=0.0)
                return axcombine

            vxacc = 30
            #ayrealarr = [0, 10, 20, 30, 40, 50, 60, 70] 
            ayrealarr = np.array([0, 2, 4, 6, 8, 10, 12, 14, 16])
            axcombine_std = np.zeros(len(ayrealarr))
            axcombine_surf = np.zeros(len(ayrealarr))
            i = 0
            for ayreal in ayrealarr:
                axcombine_std[i] = GGVstd(self, vxacc, ayreal)
                axcombine_surf[i] = GGVsurf(self, vxacc, ayreal)
                print("")
                print("vx: ", vxacc, "ayreal: ", ayreal)
                print("GGVstd: ", axcombine_std[i])
                print("GGVsurf: ", axcombine_surf[i])
                i = i+1
            # print(ayrealarr," ", axcombine_std) 
            plt.figure(1)
            plt.plot(axcombine_std, ayrealarr, 'o-', label="GGV std")
            plt.plot(axcombine_surf, ayrealarr, 'o-', label="GGV surf")
            plt.legend()
            plt.show()
