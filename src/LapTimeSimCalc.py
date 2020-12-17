"""
---------------------------
Lap Time Simulation Calculator - OLS
---------------------------

This class computes the speed trace given the Performance Envelope and
the track file (track curvature).

---------------------------
@autor: Davide Strassera
@first release: 2019-12-21
by Python 3.7
---------------------------

"""
# Import Packages
import numpy as np
import scipy.interpolate as interp


class LapTimeSimCalc:

    def __init__(self, TrackFile, accEnvDict, vxaccStart):
        # inputs
        self.TrackFile = TrackFile
        self.GGVacc = None
        self.GGVdec = None
        self.GGVfull = accEnvDict["GGVfull"]  # ax,ay,vx
        self.vxaccStart = vxaccStart
        # outputs
        self.lapTimeSimDict = {
            "vcar": None,
            "dist": None,
            "time": None,
            "laptime": None,
            "vcarmax": None,
            "vxaccEnd": None,
            "vxacc": None,
            "vxdec": None,
            "vxcor": None,
            "GGVacc": None,
            "GGVdec": None,
        }

    @staticmethod
    def splitGGVfull(GGVfull):
        """This method split the GGVfull (which means complete acc, dec and
           mirror left, right), and split it into two matrices: GGVacc
           and GGVdec. This is needed for proper griddata interpolation."""
        GGVacc = np.array([])
        GGVdec = np.array([])
        j, k = 0, 0
        for i in range(len(GGVfull[:, 0])):
            # GGVacc with ax >=0
            if GGVfull[i, 0] >= 0:
                GGVacc = np.concatenate((GGVacc, GGVfull[i, :]))
                j += 1
            # GGVdec with ax < 0 or (with ax=0 and not max speed)
            vxmax = max(GGVfull[:, 2])
            bAxZeroAndNotTopSpeed = GGVfull[i, 0] == 0 and GGVfull[i, 2] < vxmax
            if GGVfull[i, 0] < 0 or bAxZeroAndNotTopSpeed:
                GGVdec = np.concatenate((GGVdec, GGVfull[i, :]))
                k += 1
        # ncol = np.size(GGVfull, axis=1)
        GGVacc = np.resize(GGVacc, (j, 3))
        GGVdec = np.resize(GGVdec, (k, 3))
        return GGVacc, GGVdec

    # GGV surface
    @staticmethod
    def GGVSurfInterp(vx, ay, X, Y, Z):
        """ given vx, ay and the GGV vectors (X=ax, Y=ay, Z=speed) returns
            the ax combined using griddata interpolation """
        axcombine = interp.griddata((Y, Z), X, (ay, vx),
                                    method='linear')  # ,fill_value=0.0)
        return axcombine

    def Run(self):
        # Split the full GGV in acc and dec
        self.GGVacc, self.GGVdec = LapTimeSimCalc.splitGGVfull(self.GGVfull)

        # Load TrackFile
        track = np.loadtxt(self.TrackFile)
        dist = track[:, 0]
        curv = track[:, 1]

        # Speed Calculations
        small = 0.00000001  # to avoid division by zero

        # 1. Max Cornering Speed ---------------------------------------------
        curvvect = np.array([])
        vxvect = np.array([])
        for i in range(len(self.GGVacc[:, 2])):
            # if ax == 0 & ay is positive
            if(self.GGVacc[i, 0] == 0) and (self.GGVacc[i, 1] >= 0):
                vxclipped = max(self.GGVacc[i, 2], small)  # to avoid div by zero
                curvvect = np.append(curvvect, self.GGVacc[i, 1]/pow(vxclipped, 2))  # C=ay/v^2
                vxvect = np.append(vxvect, vxclipped)
        curvvect[0] = 0.5
        curvclipped = np.zeros(len(curv))
        for i in range(len(curv)):
            # curvature clipped to max speed
            curvclipped[i] = max(np.absolute(curv[i]), min(curvvect))
        # v corner from pure lateral (ay)
        vxcor = np.interp(curvclipped, curvvect, vxvect, period=360)

        # 2. Max Acceleration Speed ------------------------------------------
        vxacc = np.zeros(len(curv))
        vxacc[0] = self.vxaccStart  # must be the last vacc
        ayreal = np.zeros(len(curv))
        axcombine = np.zeros(len(curv))

        X, Y, Z = self.GGVacc[:, 0], self.GGVacc[:, 1], self.GGVacc[:, 2]
        for i in range(len(dist)-1):
            ayreal[i] = pow(vxacc[i], 2)/(1/max(curv[i], small))
            axcombine[i] = LapTimeSimCalc.GGVSurfInterp(vxacc[i], ayreal[i],
                                                        X, Y, Z)
            vxacc[i+1] = min(vxcor[i+1], (vxacc[i]+(dist[i+1]-dist[i])
                                          / vxacc[i]*axcombine[i]))

        # 3. Max Deceleration Speed ------------------------------------------
        vxdec = np.zeros(len(curv))
        vxdec[-1] = vxacc[-1]
        ayreal = np.zeros(len(curv))
        axcombine = np.zeros(len(curv))

        X, Y, Z = self.GGVdec[:, 0], self.GGVdec[:, 1], self.GGVdec[:, 2]
        for i in reversed(range(len(dist))):
            ayreal[i] = pow(vxdec[i], 2)/(1/max(curv[i], small))
            axcombine[i] = LapTimeSimCalc.GGVSurfInterp(vxdec[i], ayreal[i],
                                                        X, Y, Z)
            vxdec[i-1] = min(vxcor[i-1], (vxdec[i]+(dist[i-1]-dist[i])
                                          / vxdec[i]*axcombine[i]))
        vxdec[-1] = vxacc[-1]

        # Final speed (vcar) ---------------------------------------------
        vcar = np.zeros(len(dist))
        timestep = np.zeros(len(dist))
        time = np.zeros(len(dist))
        for i in range(len(dist)-1):
            vcar[i] = min(vxcor[i], vxacc[i], vxdec[i])
            timestep[i] = (dist[i+1]-dist[i])/vcar[i]
            time[i] = sum(timestep)

        vcar[(len(vcar)-1)] = vcar[(len(vcar)-2)]

        laptime = np.round(max(time), 3)
        vcarmax = np.round(max(vcar), 3)

        self.lapTimeSimDict = {
            "vcar": vcar,
            "dist": dist,
            "time": time,
            "laptime": laptime,
            "vcarmax": vcarmax,
            "vxaccEnd": vcar[(len(vcar) - 1)],
            "vxacc": vxacc,
            "vxdec": vxdec,
            "vxcor": vxcor,
            "GGVacc": self.GGVacc,
            "GGVdec": self.GGVdec,
        }

        print("LapSimTimeCalc completed")
