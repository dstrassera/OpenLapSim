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
            # Load TrackFile
            track = np.loadtxt(self.TrackFile)
            dist = track[:,0]
            curv = track[:,1]
            
            #Speed Calculations
            small = 0.00000001 # to avoid division by zero
            
            # 1. Max Cornering Speed
            curvvect = 1/(pow(self.vxvect,2)/self.ay) # ay=v^2/R
            curvvect[0] = 0.5
            curvclipped = np.zeros(len(curv))
            for i in range(len(curv)):
                #curvature clipped to max speed
                curvclipped[i] = max(np.absolute(curv[i]),min(curvvect))
            # v corner from pure lateral (ay)
            vxcor = np.interp(curvclipped,curvvect,self.vxvect,period=360)
            
            ## 2. Max Acceleration Speed
            #vxacc = np.zeros(len(curv))
            #vxacc[0] = self.vxaccStart #must be the last vacc
#           # axaccmap = np.zeros(len(curv))
#           # aymap = np.zeros(len(curv))
            #ayreal = np.zeros(len(curv))
            #axcombine = np.zeros(len(curv))
            #X,Y,Z = self.GGVacc[:,0],self.GGVacc[:,1],self.GGVacc[:,2]
            #for i in range(len(dist)-1):
#           #     axaccmap[i] = np.interp(vxacc[i],self.vxvect,self.axacc,period=360)
#           #     aymap[i] = max(np.interp(vxacc[i],self.vxvect,self.ay,period=360),small)
            #    ayreal[i] = pow(vxacc[i],2)/(1/max(curv[i],small))
#           #     axcombine[i] = axaccmap[i]*mt.sqrt(np.absolute(1-(ayreal[i]/aymap[i])))
            #    ay = max(ayreal[i],0)
            #    axcombine[i] = interp.griddata((Y,Z),X,(ay,vxacc[i]),method='linear')
            #    vxacc[i+1] = (vxacc[i]+(dist[i+1]-dist[i])/vxacc[i]*axcombine[i])
            #    
            #plt.figure(1)
            #plt.plot(axcombine, ayreal, 'o-', label="GGV surf")
            #plt.legend()
            #plt.show()

            # Max Acceleration Speedl
            vxacc = np.zeros(len(curv))
            vxacc[0] = self.vxaccStart  # must be the last vacc
            axaccmap = np.zeros(len(curv))
            aymap = np.zeros(len(curv))
            ayreal = np.zeros(len(curv))
            axcombine = np.zeros(len(curv))

            # GGV surface
            def GGVsurf(self, vxacc, ayreal):
                X, Y, Z = self.GGVacc[:, 0], self.GGVacc[:, 1], self.GGVacc[:, 2]
                ay = ayreal
                axcombine = interp.griddata((Y, Z), X, (ay, vxacc), method='linear')#,fill_value=0.0)
                return axcombine

            for i in range(len(dist)-1):
                # axaccmap[i] = np.interp(vxacc[i], self.vxvect, self.axacc,
                #                         period=360)
                # aymap[i] = max(np.interp(vxacc[i], self.vxvect, self.ay,
                #                period=360), small)
                ayreal[i] = pow(vxacc[i], 2)/(1/max(curv[i], small))
                # axcombine[i] = axaccmap[i]*mt.sqrt(np.absolute(1-(ayreal[i]
                #                                                   / aymap[i])))
                axcombine[i] = GGVsurf(self, vxacc[i], ayreal[i])
                vxacc[i+1] = min(vxcor[i+1], (vxacc[i]+(dist[i+1]-dist[i])
                                              / vxacc[i]*axcombine[i]))


            # Max Deceleration Speed
            vxdec = np.zeros(len(curv))
            vxdec[-1] = vxacc[-1]
            axdecmap = np.zeros(len(curv))
            aymap = np.zeros(len(curv))
            ayreal = np.zeros(len(curv))
            axcombine = np.zeros(len(curv))
            for i in reversed(range(len(dist))):
                axdecmap[i] = np.interp(vxdec[i], self.vxvect, self.axdec,
                                        period=360)
                aymap[i] = max(np.interp(vxacc[i], self.vxvect, self.ay,
                               period=360), small)
                ayreal[i] = pow(vxdec[i], 2)/(1/max(curv[i], small))
                axcombine[i] = axdecmap[i]*mt.sqrt(np.absolute(1-(ayreal[i]
                                                                  / aymap[i])))
                vxdec[i-1] = min(vxcor[i-1], (vxdec[i]+(dist[i-1]-dist[i])
                                              / vxdec[i]*axcombine[i]))
            vxdec[-1] = vxacc[-1]

            #Final speed (vcar)
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
