"""
---------------------------
SimExportCompare - OLS
---------------------------
This routine compares two SimExport.txt 

---------------------------
@autor: Davide Strassera
@first release: 2020-05-18
by Python 3.7
---------------------------
"""
import csv
from pathlib import Path
import os
import matplotlib.pyplot as plt
import numpy as np


# ----------------------------------------------------------------------------

# Constants definitions
CWD = os.getcwd()
PATH = str(Path(CWD).parent)


def calcLapTime(vCar, dist):
    """This function calculate the LapTime given the speedtrace distance based.

        inputs:
        - vCar of type array of int, is the speed trance in m/s.
        - dist of type array of int, is the distance in m.

        outputs:
        - laptime of type int, is the laptime in sec.
    """

    timestep = np.zeros(len(dist))
    time = np.zeros(len(dist))
    for i in range(len(dist)-1):
        timestep[i] = (dist[i+1]-dist[i])/vCar[i]
        time[i] = sum(timestep)

    laptime = np.round(max(time), 3)
    return laptime


def plot_vCar(vCar1, dist1, vCar2, dist2, bKph):
    """ This funtion plots two speed traces"""

    if bKph == 1:
        k = 3.6
    else:
        k = 1
    DvCar = np.zeros(len(dist1))
    for i in range(len(dist1)):
        DvCar[i] = vCar1[i]-vCar2[i]

    plt.figure(1)
    plt.title("Sim Compare")
    plt.plot(dist1, vCar1*k, 'r-', label="vCar1")
    plt.plot(dist2, vCar2*k, 'b-', label="vCar2")
    plt.plot(dist1, DvCar*k, 'r--', label="delta vCar")
    plt.xlabel('distance [m]')
    plt.ylabel('vcar')
    plt.grid(b=True, which='major', linestyle=':')
    plt.legend()
    plt.show()


def simCompare(sim1, sim2, bKph=1):
    """ This function compares two simulation exports from "src/exportFiles",
        computes the delta speed and plot the results.

        inputs:
        - sim1 of type string, is the name of the first SimExport...txt;
        - sim2 of type string, is the name of the second SimExport...txt;
        - bKph of type int [0, 1], defines if the y axle is in kph or m/s.
    """

    path1 = PATH+"/exportFiles/"+sim1
    file1 = np.loadtxt(path1)
    dist1 = file1[:, 0]
    vCar1 = file1[:, 1]

    path2 = PATH+"/exportFiles/"+sim2
    file2 = np.loadtxt(path2)
    dist2 = file2[:, 0]
    vCar2 = file2[:, 1]

    # print delta laptime
    laptime1 = calcLapTime(vCar1, dist1)
    laptime2 = calcLapTime(vCar2, dist2)
    Dlaptime = round(laptime1 - laptime2, 3)
    print("laptime1: ", laptime1, "[s]")
    print("laptime2: ", laptime2, "[s]")
    print("Delta laptime: ", Dlaptime, "[s]")

    # plot speed traces
    plot_vCar(vCar1, dist1, vCar2, dist2, bKph)


# ----------------------------------------------------------------------------


if __name__ == '__main__':

    sim1 = "SimExport_Oct-28-2020.txt"
    sim2 = "SimExport_Oct-28-2020.txt"

    simCompare(sim1, sim2, bKph=1)
