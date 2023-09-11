import argparse
import numpy as np
import SimFileReader


def main():
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description="Test a battery with simulation results")

    # Add arguments for simulation file path and number of laps
    # parser.add_argument("simulation_file", type=str, help="Path to the simulation file")
    parser.add_argument("-n", "--n_laps", type=int, default=1, help="Number of laps to simulate (default: 1)")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Access the values of the arguments
    simulation_file = 'exports/SimExport_Sep-11-2023.txt' #args.simulation_file
    num_laps = args.n_laps

    # Print the values of the arguments
    print(f"Simulation File Path: {simulation_file}")
    print(f"Number of Laps: {num_laps}")

    sim_data = SimFileReader.SimFile(simulation_file)


if __name__ == "__main__":
    main()
