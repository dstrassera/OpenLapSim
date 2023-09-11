import numpy as np


class SimFile:
    def __init__(self, filepath):
        # Use numpy.genfromtxt to read the CSV file with tab delimiters
        data = np.genfromtxt(filepath, delimiter='\t', dtype=None, names=True, encoding=None)

        # Extract column names from the CSV file
        column_names = data.dtype.names

        # Create NumPy arrays for each column
        arrays = {col_name: data[col_name] for col_name in column_names}

        # Store the arrays as instance variables
        self.time = arrays["time_s"]
        self.vcar = arrays["vcar_ms"]
        self.distance = arrays["distance_m"]
        self.power = arrays["battery_power_W"]
