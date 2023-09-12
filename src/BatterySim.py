import argparse
import math
from dataclasses import dataclass

import numpy as np
import SimFileReader

import matplotlib.pyplot as plt

# Based on another 18650 cell, not VTC6
CELL_MASS = 0.0465  # kg
CELL_HEAT_CAPACITY = 902  # J/kg*K
MODULE_HEAT_CAPACITY = CELL_MASS * CELL_HEAT_CAPACITY * 6

VTC6_OCV_SOC = np.array([
    [0.0, 0.1666, 0.3333, 0.5, 0.6666, 0.83333, 1.0],  # SoC (0-1)
    [2.5, 3.4, 3.6, 3.75, 3.85, 4.05, 4.2]  # OCV (Open circuit voltage)
])

# TODO This data is a total guess based on VTC6 datasheet and enepaq datasheet.
# This could be greatly improved from battery testing data.
# Also, Rint varies with SoC as well as temperature...
VTC6_RINT_T = np.array([
    [-20.0, -10.0,  0.0,    23.0,   45.0, 60.0],  # Temperature (Degrees C)
    [0.013, 0.0083, 0.0069, 0.0034, 0.0028, 0.0028]  # RINT (Internal resistance) - this is of the entire module, not a single cell.
])


# TODO This data is a total guess based on VTC6 datasheet and enepaq datasheet. Also varies with temperature.
VTC6_CAPACITY_CURRENT = np.array([
    [0.0,  18.0,  60.0,  120.0],  # Current drawn
    [18.6, 18.46, 18.18, 18.0]  # Capacity (Amp-Hours)
])


@dataclass
class BatterySimOutput:
    t_internal: float
    t_anode: float
    soc: float
    voltage: float
    current: float
    rint: float


class BatteryModel:
    def __init__(self, initial_temperature, initial_soc, series_cells=84):
        self.t_internal = initial_temperature  # Internal temperature (degrees C)
        self.t_anode = initial_temperature  # Anode temperature
        self.soc = initial_soc  # State of charge (0-1)
        self.series = series_cells

    def update(self, power, timestep) -> BatterySimOutput:
        cell_ocv = np.interp(x=self.soc, xp=VTC6_OCV_SOC[0], fp=VTC6_OCV_SOC[1])
        ocv = cell_ocv * self.series
        cell_rint = np.interp(x=self.t_internal, xp=VTC6_RINT_T[0], fp=VTC6_RINT_T[1])
        rint = cell_rint * self.series
        det = ocv * ocv - 4 * power * rint
        if det < 0:
            print("Simulation failed: Battery cannot provide needed power")
            return None
        current = (ocv - math.sqrt(det)) / (2 * rint)
        voltage = ocv - current * rint
        # print(current)
        power = current * current * rint
        energy = power * timestep
        temp_rise = energy / (MODULE_HEAT_CAPACITY * self.series)
        # print(temp_rise)

        capacity = np.interp(x=current, xp=VTC6_CAPACITY_CURRENT[0], fp=VTC6_CAPACITY_CURRENT[1])
        capacity_loss = current * timestep
        soc_loss = capacity_loss / (capacity * 3600)
        self.soc -= soc_loss

        self.t_internal += temp_rise

        self.t_anode = self.t_internal

        return BatterySimOutput(t_internal=self.t_internal, t_anode=self.t_anode, soc=self.soc, voltage=voltage,
                                current=current, rint=rint)


def frange(x, y, jump):
    while x < y:
        yield x
        x += jump


def plot_results(results, times):
    # Extract data from the results
    t_internal_values = [result.t_internal for result in results]
    t_anode_values = [result.t_anode for result in results]
    soc_values = [result.soc for result in results]
    voltage_values = [result.voltage for result in results]
    current_values = [result.current for result in results]
    rint_values = [result.rint for result in results]

    # Create subplots
    fig, axs = plt.subplots(2, 1, figsize=(10, 8))
    fig.suptitle('Transient Thermal Simulation Results')

    ax1 = axs[1]
    # Plot Voltage, Rint, and Current on separate y-axes
    color = 'tab:blue'
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Voltage', color=color)
    ax1.plot(times, voltage_values, label='Voltage', color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    # Create a second y-axis for Current
    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Current', color=color)
    ax2.plot(times, current_values, label='Current', color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    # Create a third y-axis for Rint
    ax3 = ax1.twinx()
    color = 'tab:green'
    ax3.spines['right'].set_position(('outward', 60))  # Adjust the position of the third y-axis
    ax3.set_ylabel('Rint', color=color)
    ax3.plot(times, rint_values, label='Rint', color=color)
    ax3.tick_params(axis='y', labelcolor=color)

    # Add legends
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    lines3, labels3 = ax3.get_legend_handles_labels()
    ax1.legend(lines + lines2 + lines3, labels + labels2 + labels3, loc='upper left')

    # Plot Temperatures and SOC on the same subplot with separate y-axes
    ax0 = axs[0]
    ax0.set_xlabel('Time (s)')
    ax0.set_ylabel('Temperatures (°C)')
    ax0.plot(times, t_internal_values, label='t_internal', color='tab:blue')
    ax0.plot(times, t_anode_values, label='t_anode', color='tab:green')
    ax0.tick_params(axis='y', labelcolor='tab:blue')

    # Create a twin y-axis for SOC
    axs2 = ax0.twinx()
    axs2.set_ylabel('SOC (%)', color='tab:red')
    axs2.plot(times, soc_values, label='SOC', color='tab:red')
    axs2.tick_params(axis='y', labelcolor='tab:red')

    lines, labels = ax0.get_legend_handles_labels()
    lines2, labels2 = axs2.get_legend_handles_labels()
    ax0.legend(lines + lines2, labels + labels2, loc='upper left')

    # Adjust layout
    plt.tight_layout()
    plt.subplots_adjust(top=0.9)

    # Show the plots
    plt.show()


def main():
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description="Test a battery with simulation results")

    # Add arguments for simulation file path and number of laps
    parser.add_argument("simulation_file", type=str, help="Path to the simulation file")
    parser.add_argument("-n", "--n_laps", type=int, default=1, help="Number of laps to simulate (default: 1)")
    parser.add_argument("-t", "--timestep", type=float, default=1, help="Transient simulation timestep in seconds ("
                                                                        "default: 1)")

    parser.add_argument("--break-after", type=int, default=None, help="Stop after this many laps")
    parser.add_argument("--break-time", type=int, default=0, help="Stop for this many seconds")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Access the values of the arguments
    simulation_file = args.simulation_file
    num_laps = args.n_laps
    timestep = args.timestep
    break_after = args.break_after
    break_time = args.break_time

    # Print the values of the arguments
    print(f"Simulation File Path: {simulation_file}")
    print(f"Number of Laps: {num_laps}")

    sim_data = SimFileReader.SimFile(simulation_file)

    lap_energy = np.trapz(sim_data.power, x=sim_data.time)
    lap_time = sim_data.time[-1]

    bm = BatteryModel(23, 1, series_cells=84)

    results = []
    result_times = []

    def sim_lap(results_array, times_array, battery_model: BatteryModel):
        for time in frange(0, lap_time, timestep):
            start_idx = np.searchsorted(sim_data.time, time)
            end_idx = np.searchsorted(sim_data.time, time + timestep)
            if end_idx >= len(sim_data.time):
                end_idx = len(sim_data.time) - 1
            # print(f"{start_idx},{end_idx}")

            start_time = sim_data.time[start_idx]
            end_time = sim_data.time[end_idx]
            dt = end_time - start_time

            powers = sim_data.power[start_idx:end_idx+1]
            times = sim_data.time[start_idx:end_idx+1]

            avg_power = np.trapz(powers, x=times) / dt
            results_array.append(battery_model.update(avg_power, dt))
            times_array.append(times_array[-1] + dt)

    # print(f"Lap energy: {lap_energy}\n Energy from one lap: {sim_lap()}")

    #
    print("--------------")
    print(" Starting sim")
    print("--------------")
    results.append(bm.update(0, 1))
    result_times.append(0)

    if break_after is not None:
        print(f"Simulating {break_after} laps...")
        for lap in range(break_after):
            sim_lap(results, result_times, bm)

        print(f"Simulating {break_time} second break")
        for _t in range(math.ceil(break_time / timestep)):
            results.append(bm.update(0, timestep))
            result_times.append(result_times[-1] + timestep)

        print(f"Simulating {num_laps - break_after} laps...")
        for lap in range(break_after, num_laps):
            sim_lap(results, result_times, bm)
    else:
        print(f"Simulating {num_laps} laps...")
        for lap in range(num_laps):
            sim_lap(results, result_times, bm)

    print("--------------")
    print("Simulation complete")
    print(f"Ending SOC: {round(bm.soc * 100, 1)}%")
    print(f"Ending anode temp: {round(bm.t_anode, 1)}°C")
    plot_results(results, result_times)


if __name__ == "__main__":
    main()
