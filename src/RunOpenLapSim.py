"""
---------------------------
OpenLapSim - OLS
---------------------------

This is a steady state Lap Time Simulator for a simple point mass vehicle
with aero forces, constant tyre grip(x and y), engine torque map and gears.

Steps:
    1 - Select Files: TrackFile.txt and SetupFile.py
    2 - Calculate the Acceleration Envelope
    3 - Calculate the Lap Time Simulation (vcar)
    4 - Plot Results

---------------------------
@autor: Davide Strassera
@first release: 2019-12-21
by Python 3.7
---------------------------

"""

# ----------------------------------------------------------------------------

# import packages generic
import datetime
from dataclasses import dataclass

import matplotlib.pyplot as plt
import time
import argparse

import numpy
import numpy as np

# import packages (OLP)
from AccEnvCalc import AccEnvCalc
from LapTimeSimCalc import LapTimeSimCalc
from PostProc import PostProc
from SetupFileLoader import SetupFileLoader

EXPORT_FILE_PATH = "exports/"


@dataclass
class LapSimOutput:
    laptime: float  # Lap time in seconds
    vcarmax: float  # Maximum car velocity in m/s

    rms_power: float  # RMS Power drawn from battery (watts)
    total_energy: float # Total energy consumed (joules)

    trans_vcar: np.ndarray  # Velocity samples over time
    trans_dist: np.ndarray  # Distance samples over time
    trans_power: np.ndarray  # Power samples over time
    trans_time: np.ndarray  # Time for above samples

    tcomp: float  # Computation time in seconds

    post_proc: PostProc  # post-processing thingy



def createExportSimFile(sim_output: LapSimOutput, exportFilesPath):
    time = datetime.datetime.now()
    timestrf = time.strftime("%b-%d-%Y")
    NewExportFileName = (exportFilesPath + "SimExport_"
                         + str(timestrf) + ".txt")
    newFile = open(NewExportFileName, "w")

    data_names = ["time (s)", "vcar (m/s)", "distance (m)", "battery power (W)"]
    newFile.write('\t'.join(data_names) + '\n')

    for i in range(len(sim_output.trans_dist)):
        datums = [sim_output.trans_time[i], sim_output.trans_vcar[i], sim_output.trans_dist[i], sim_output.trans_power[i]]
        line_to_write = '\t'.join([str(d) for d in datums]) + '\n'
        newFile.write(line_to_write)
    newFile.close()
    return NewExportFileName


def run(setupFilePath, trackFilePath, powerLimit, print_progress=False):
    if print_progress:
        print(f"Vehicle model: {setupFilePath}")
        print(f"Track file: {trackFilePath}")
        if powerLimit is not None:
            print(f"{powerLimit}W power limit applied")

    # Computation time start
    tstart = time.time()

    if print_progress:
        print("Loading vehicle model file...")

    # SetupFile obj instantiation
    s = SetupFileLoader(setupFilePath, power_limit_kw=powerLimit)
    s.loadJSON()

    if print_progress:
        print("Calculating acceleration envelope...")

    # Run Acceleration Envelope
    aE = AccEnvCalc(s.setupDict)
    aE.Run()

    if print_progress:
        print("Simulating first lap (1 of 2)...")

    # Run Lap time Simulation
    l1 = LapTimeSimCalc(trackFilePath, aE.accEnvDict, 10)
    l1.Run()

    if print_progress:
        print("Simulating hot lap (2 of 2)...")

    # Run second simulation using starting speed from first lap
    l2 = LapTimeSimCalc(trackFilePath, aE.accEnvDict,
                        l1.lapTimeSimDict["vxaccEnd"])
    l2.Run()

    if print_progress:
        print("Processing simulation results...")

    # set output channels from simulation for Export
    vcar = l2.lapTimeSimDict["vcar"]  # car speed [m/s]
    dist = l2.lapTimeSimDict["dist"]  # circuit dist [m]
    lap_time = l2.lapTimeSimDict["time"]
    lap_time[-1] = l2.lapTimeSimDict["laptime"]
    acc = np.gradient(vcar, lap_time)
    # Calculate force (accounting for acceleration and air resistance)
    force = s.setupDict["mcar"] * acc + (0.5 * s.setupDict["rho"] * np.square(vcar) * s.setupDict["cx"] * s.setupDict["afrcar"])
    power = force * vcar

    # Factor in drivetrain efficiency
    power = power / s.setupDict["reff"]

    # No regen braking :(
    positive_power = np.maximum(power, np.zeros(power.shape))
    rms_power = np.sqrt(np.average(np.square(positive_power)))

    total_energy = numpy.trapz(positive_power, x=lap_time)


    pP = PostProc(aE.accEnvDict, l2.lapTimeSimDict)

    # Computation time end
    tend = time.time()
    tcomp = round(tend - tstart, 1)

    if print_progress:
        print(f"Simulation completed in {tcomp} seconds.")

    laptime = l2.lapTimeSimDict["laptime"]
    vcarmax = l2.lapTimeSimDict["vcarmax"]
    tcomp = tcomp

    return LapSimOutput(vcarmax=vcarmax, laptime=laptime, tcomp=tcomp, rms_power=rms_power, trans_vcar=vcar,
                        trans_dist=dist, trans_power=positive_power, trans_time=lap_time, post_proc=pP, total_energy=total_energy)


# ----------------------------------------------------------------------------



def main():
    parser = argparse.ArgumentParser(description="OpenLapSim")

    parser.add_argument("--setup", type=str, default="SetupFile.json", help="Name of the setup file.")
    parser.add_argument("--track", type=str, default="TrackFile.txt", help="Name of the track file.")
    parser.add_argument("--power-limit", type=float, help="Vehicle motor power limit.")
    parser.add_argument("--n-laps", type=int, default=1, help="Total number of laps.")
    parser.add_argument("--export", action="store_true", help="Export results.")
    parser.add_argument("--plot", action="store_true", help="Plot basic results.")
    parser.add_argument("--plot-extra", action="store_true", help="Enable extra plots.")

    args = parser.parse_args()

    setupFileName = args.setup
    trackFileName = args.track
    powerLimit = args.power_limit
    bExport = args.export
    bPlot = args.plot
    bPlotExtra = args.plot_extra
    n_laps = args.n_laps

    # object instantiation
    results = run(setupFileName, trackFileName, powerLimit, print_progress=True)
    print("------------------")
    print("    RESULTS")
    print("------------------")
    print("--Single lap--")
    print(f"Lap time: {results.laptime} seconds")
    print(f"Max speed: {results.vcarmax} m/s")
    print(f"Energy used: {round(results.total_energy / 1000, 2)} kJ ({round(results.total_energy * 2.778e-4, 2)} Wh)")
    if n_laps > 1:
        print(f"--Overall ({n_laps} laps)--")
        total_time = results.laptime * n_laps
        print(f"Total time: {int(total_time // 60)}:{round(total_time % 60, 2)}")
        total_energy = results.total_energy * n_laps
        print(f"Total energy used: {round(total_energy / 1000, 2)} kJ ({round(total_energy * 2.778e-4, 2)} Wh)")

    print(f"RMS Power: {round(results.rms_power / 1000, 2)} kW")


    # Power over time plot
    # if bPlotExtra:
    #     plt.plot(results.trans_time, results.trans_power)

    # export
    if bExport:
        createExportSimFile(sim_output=results, exportFilesPath=EXPORT_FILE_PATH)

    # Post Processing data
    if bPlot:
        # pP.plotAccEnv()
        results.post_proc.plotGGV()
        results.post_proc.plotLapTimeSim()
    if bPlotExtra:
        results.post_proc.plotLapTimeSimExtra()
        results.post_proc.plotAccEnvExtra()
    plt.show()  # plot all figure once at the end


if __name__ == '__main__':
    main()


