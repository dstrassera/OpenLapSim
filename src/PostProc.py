"""
---------------------------
Post Processing - OLS
---------------------------

This class computes the post processing of the simulation.

---------------------------
@autor: Davide Strassera
@first release: 2019-12-21
by Python 3.7
---------------------------

"""
# Import packages
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate as interp


class PostProc:

    def __init__(self, accEnvDict, lapSimTimeDict):
        self.size = 10
        # inputs
        self.GGVfull = accEnvDict["GGVfull"]
        self.GGVacc = lapSimTimeDict["GGVacc"]
        self.GGVdec = lapSimTimeDict["GGVdec"]

        self.vxvect = accEnvDict["vxvect"]
        self.ay = accEnvDict["ay"]
        self.axacc = accEnvDict["axacc"]
        self.axdec = accEnvDict["axdec"]
        self.dist = lapSimTimeDict["dist"]
        self.vcar = lapSimTimeDict["vcar"]
        self.laptime = lapSimTimeDict["laptime"]
        self.vcarmax = lapSimTimeDict["vcarmax"]
        self.vxacc = lapSimTimeDict["vxacc"]
        self.vxdec = lapSimTimeDict["vxdec"]
        self.vxcor = lapSimTimeDict["vxcor"]
        # extra channels (AccEnv)
        self.nGear = accEnvDict["nGear"]
        self.EngNm = accEnvDict["EngNm"]
        self.EngRpm = accEnvDict["EngRpm"]
        self.Fzaero = accEnvDict["Fzaero"]
        self.Fxaero = accEnvDict["Fxaero"]
        self.Fxgrip = accEnvDict["Fxgrip"]
        self.Fxdrive = accEnvDict["Fxdrive"]

    def plotAccEnv(self):
        plt.figure(1, figsize=(self.size/2, self.size/2))
        plt.title("Acceleration Envelope")
        plt.plot(self.ay, self.vxvect, 'c-', label="ay")
        plt.plot(self.axacc, self.vxvect, 'm-', label="axacc")
        plt.plot(self.axdec, self.vxvect, 'r-', label="axdec")
        plt.legend()
        plt.xlabel('acceleration [m/s^2]')
        plt.ylabel('velocity [m/s]')
        plt.grid(b=True, which='major', linestyle=':')
        plt.ylim(0, self.vcarmax*1.2)

    def plotGGV(self, bPlotGGVfull=0):
        GGVacc = self.GGVacc
        GGVdec = self.GGVdec
        GGVfull = self.GGVfull

        xyz1 = GGVacc
        X1 = xyz1[:, 0]
        Y1 = xyz1[:, 1]
        Z1 = xyz1[:, 2]
        # Griddata
        ploty1, plotz1, = np.meshgrid(np.linspace(np.min(Y1), np.max(Y1), 30),
                                      np.linspace(np.min(Z1), np.max(Z1), 30))
        plotx1 = interp.griddata((Y1, Z1), X1, (ploty1, plotz1),
                                 method='linear', fill_value=0.0)

        xyz2 = GGVdec
        X2 = xyz2[:, 0]
        Y2 = xyz2[:, 1]
        Z2 = xyz2[:, 2]
        # Griddata
        ploty2, plotz2, = np.meshgrid(np.linspace(np.min(Y2), np.max(Y2), 30),
                                      np.linspace(np.min(Z2), np.max(Z2), 30))
        plotx2 = interp.griddata((Y2, Z2), X2, (ploty2, plotz2),
                                 method='linear', fill_value=0.0)

        xyz3 = GGVfull
        X3 = xyz3[:, 0]
        Y3 = xyz3[:, 1]
        Z3 = xyz3[:, 2]

        fig = plt.figure(5)
        ax = fig.add_subplot(111, projection='3d')
        surf1 = ax.plot_surface(plotx1, ploty1, plotz1,
                                cstride=1, rstride=1, cmap='coolwarm',
                                edgecolor='black', linewidth=0.2,
                                antialiased=True)
        surf2 = ax.plot_surface(plotx2, ploty2, plotz2,
                                cstride=1, rstride=1, cmap='coolwarm',
                                edgecolor='black', linewidth=0.2,
                                antialiased=True)
        if bPlotGGVfull == 1:
            ax.scatter(X3, Y3, Z3, color="black", label="GGVfull sparse")
            ax.legend()

        # Add a color bar which maps values to colors.
        fig.colorbar(surf1, shrink=0.5, aspect=5)

        plt.title("OpenLapSim - Performance Envelope")
        plt.xlabel('ax [m/s^2]')
        plt.ylabel('ay [m/s^2]')
        ax.set_zlabel('velocity [m/s]')

    def plotAccEnvExtra(self):
        f, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4,
                                               figsize=(self.size*1.5,
                                                        self.size/2))
        ax1.set_title("Forces[N] (vcar[m/s])")
        ax1.plot(self.Fzaero, self.vxvect, 'c-', label="Fzaero")
        ax1.plot(self.Fxaero, self.vxvect, 'm-', label="Fxaero")
        ax1.plot(self.Fxgrip, self.vxvect, 'r-', label="FxGrip")
        ax1.plot(self.Fxdrive, self.vxvect, 'g-', label="FxDrive")
        ax1.legend()
        ax1.grid(visible=True, which='major', linestyle=':')

        ax2.set_title("Gear (vcar[m/s])")
        ax2.plot(self.nGear, self.vxvect, 'c-', label="nGear")
        ax2.legend()
        ax2.grid(visible=True, which='major', linestyle=':')

        ax3.set_title("EngNm (vcar[m/s])")
        ax3.plot(self.EngNm, self.vxvect, 'c-', label="EngNm")
        ax3.legend()
        ax3.grid(visible=True, which='major', linestyle=':')

        ax4.set_title("EngRpm (vcar[m/s])")
        ax4.plot(self.EngRpm, self.vxvect, 'c-', label="EngRpm")
        ax4.legend()
        ax4.grid(visible=True, which='major', linestyle=':')

    def plotLapTimeSim(self):
        plt.figure(2, figsize=(self.size, self.size/2))
        plt.title("OpenLapSim - Lap Time Simulation")
        plt.plot(self.dist, self.vcar, 'b-', linewidth=2, label="vcar")
        plt.xlabel('distance [m]')
        plt.ylabel('velocity [m/s]')
        plt.legend()
        plt.grid(visible=True, which='major', linestyle=':')
        plt.ylim(0, self.vcarmax*1.2)
        plt.xlim(0, max(self.dist))

    def plotLapTimeSimExtra(self):
        plt.figure(3, (self.size, self.size/2))
        plt.title("Lap Time Simulation - Extra")
        plt.plot(self.dist, self.vxcor, 'c-', label="vxcor")
        plt.plot(self.dist, self.vxacc, 'm-', label="vxacc")
        plt.plot(self.dist, self.vxdec, 'r-', label="vxdec")
        plt.plot(self.dist, self.vcar, 'b-', linewidth=2, label="vcar")
        plt.xlabel('distance [m]')
        plt.ylabel('velocity [m/s]')
        plt.legend()
        plt.grid(visible=True, which='major', linestyle=':')
        plt.ylim(0, self.vcarmax*1.2)
        plt.xlim(0, max(self.dist))
