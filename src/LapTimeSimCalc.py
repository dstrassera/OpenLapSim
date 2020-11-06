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
            self.GGVacc     = None 
            self.GGVdec     = None 
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

        @staticmethod
        def splitGGVfull(GGVfull):
            GGVacc = np.array([])
            GGVdec = np.array([])
            j, k = 0, 0
            for i in range(len(GGVfull[:, 0])):
                if GGVfull[i, 0] >= 0:
                    GGVacc = np.concatenate((GGVacc, GGVfull[i, :]))
                    j += 1
                if GGVfull[i, 0] <= 0:
                    GGVdec = np.concatenate((GGVdec, GGVfull[i, :]))
                    k += 1
            print("j: ", j, "k: ", k)
            ncol = np.size(GGVfull, axis=1)
            GGVacc = np.resize(GGVacc, (j, 3))
            #print(GGVacc)
            GGVdec = np.resize(GGVdec, (k, 3))
            return GGVacc, GGVdec

        def Run(self):
            # Split the full GGV in acc and dec
            self.GGVacc, self.GGVdec = LapTimeSimCalc.splitGGVfull(self.GGVfull)
           
            # Plotting splitted GGV %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            xyz1 = self.GGVacc 
            X1= xyz1[:,0]
            Y1= xyz1[:,1]
            Z1= xyz1[:,2]
            ploty1,plotz1, = np.meshgrid(np.linspace(np.min(Y1),np.max(Y1),30),\
                                       np.linspace(np.min(Z1),np.max(Z1),30))
            # Griddata
            plotx1 = interp.griddata((Y1,Z1),X1,(ploty1,plotz1),method='linear',fill_value=0.0)
            
            xyz2 = self.GGVdec 
            X2= xyz2[:,0]
            Y2= xyz2[:,1]
            Z2= xyz2[:,2]
            ploty2,plotz2, = np.meshgrid(np.linspace(np.min(Y2),np.max(Y2),30),\
                                       np.linspace(np.min(Z2),np.max(Z2),30))
            plotx2 = interp.griddata((Y2,Z2),X2,(ploty2,plotz2),method='linear', fill_value=0.0)
       
            fig = plt.figure(9)
            ax = fig.add_subplot(111, projection='3d')
            ax.plot_surface(plotx1,ploty1,plotz1,cstride=1,rstride=1,cmap='viridis')
            ax.scatter(X1,Y1,Z1)
            ax.plot_surface(plotx2,ploty2,plotz2,cstride=1,rstride=1,cmap='viridis')
            ax.scatter(X2,Y2,Z2)
            # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

            # Load TrackFile
            track = np.loadtxt(self.TrackFile)
            dist = track[:, 0]
            curv = track[:, 1]
            
            # Speed Calculations
            small = 0.00000001  # to avoid division by zero
            
            # 1. Max Cornering Speed -----------------------------------------
            curvvect = np.array([])
            vxvect = np.array([])
            for i in range(len(self.GGVacc[:, 2])):
                # if ax == 0 & ay is positive
                if(self.GGVacc[i, 0] == 0) and (self.GGVacc[i, 1] >= 0):
                    vxclipped = max(self.GGVacc[i, 2], small)  # to avoid div by zero
                    curvvect = np.append(curvvect, self.GGVacc[i, 1]/pow(vxclipped, 2))  # C=ay/v^2
                    vxvect = np.append(vxvect, vxclipped)
                    print(i, " ", vxclipped, " ", self.GGVacc[i, 1])
            print(curvvect)
            curvvect[0] = 0.5
            curvclipped = np.zeros(len(curv))
            for i in range(len(curv)):
                # curvature clipped to max speed
                curvclipped[i] = max(np.absolute(curv[i]), min(curvvect))
            # v corner from pure lateral (ay)
            vxcor = np.interp(curvclipped, curvvect, vxvect, period=360)

            # Max Acceleration Speed -----------------------------------------
            vxacc = np.zeros(len(curv))
            vxacc[0] = self.vxaccStart  # must be the last vacc
            ayreal = np.zeros(len(curv))
            axcombine = np.zeros(len(curv))

            # GGV surface
            def GGVaccSurf(self, vxacc, ay):
                X, Y, Z = self.GGVacc[:, 0], self.GGVacc[:, 1], self.GGVacc[:, 2]
                axcombine = interp.griddata((Y, Z), X, (ay, vxacc), method='linear')#,fill_value=0.0)
                return axcombine

            for i in range(len(dist)-1):
                ayreal[i] = pow(vxacc[i], 2)/(1/max(curv[i], small))
                axcombine[i] = GGVaccSurf(self, vxacc[i], ayreal[i])
                vxacc[i+1] = min(vxcor[i+1], (vxacc[i]+(dist[i+1]-dist[i])
                                              / vxacc[i]*axcombine[i]))

            # Max Deceleration Speed -----------------------------------------
            vxdec = np.zeros(len(curv))
            vxdec[-1] = vxacc[-1]
            ayreal = np.zeros(len(curv))
            axcombine = np.zeros(len(curv))

            # GGV surface
            def GGVdecSurf(self, vxdec, ay):
                X, Y, Z = self.GGVdec[:, 0], self.GGVdec[:, 1], self.GGVdec[:, 2]
                axcombine = interp.griddata((Y, Z), X, (ay, vxdec), method='linear')#,fill_value=0.0)
                return axcombine

            for i in reversed(range(len(dist))):
                ayreal[i] = pow(vxdec[i], 2)/(1/max(curv[i], small))
                axcombine[i] = GGVdecSurf(self, vxdec[i], ayreal[i])
                vxdec[i-1] = min(vxcor[i-1], (vxdec[i]+(dist[i-1]-dist[i])
                                              / vxdec[i]*axcombine[i]))
            vxdec[-1] = vxacc[-1]

            # Final speed (vcar) ---------------------------------------------
            vcar = np.zeros(len(dist))
            timestep = np.zeros(len(dist))
            time = np.zeros(len(dist))
            for i in range(len(dist)-1):
                vcar[i] = min(vxcor[i],vxacc[i],vxdec[i])
                timestep[i] = (dist[i+1]-dist[i])/vcar[i]
                time[i] = sum(timestep)
            
            vcar[(len(vcar)-1)] = vcar[(len(vcar)-2)] 
            
            laptime = np.round(max(time),3)
            vcarmax = np.round(max(vcar),3)
            
            self.lapTimeSimDict = {
                "vcar"      : vcar,
                "dist"      : dist,
                "time"      : time,
                "laptime"   : laptime,
                "vcarmax"   : vcarmax,
                "vxaccEnd"  : vcar[(len(vcar)- 1)],
                "vxacc"     : vxacc,
                "vxdec"     : vxdec,
                "vxcor"     : vxcor,
            }
            
            print("LapSimTimeCalc completed")
