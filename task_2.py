import matplotlib.pyplot as plt
import os

from datetime import datetime
from utils import calculations, csv_helper


def create_vibration_graph(x_vibrations, y_vibrations, times):
    """
    Use Matplotlib to create a .png file containing two graphs that display vibration measurements over time.
    A file 'vibration_chart.png' will be created in the output folder.
    :param x_vibrations: The list of x radial vibration measurements.
    :param y_vibrations: The list of y radial vibration measurements.
    :param times: The list of measurement dates.
    :return: None
    """
    fig, (ax1, ax2) = plt.subplots(2, 1)
    # This function makes the dates readable on the x-axis.
    fig.autofmt_xdate()
    fig.suptitle('Vibration Measurement 12 Hour Rolling Average')

    ax1.plot(times, x_vibrations)
    ax1.set_ylabel('Radial Vibration X')

    ax2.plot(times, y_vibrations)
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Radial Vibration Y')

    filepath = os.path.join("output", "vibration_chart.png")
    print(f"Saving chart to {filepath}")
    fig.savefig(filepath)


if __name__ == "__main__":
    downtime_entries = csv_helper.read_entries("downtime.csv")

    # I've selected entry 2 (Windmill 3058) as it contains data for two shutdowns but
    # the code should work for any of the files.
    entry = downtime_entries[1]
    entry_id = entry.get(csv_helper.DOWNTIME_ID)

    filename = f"{entry_id}.csv"
    filepath = os.path.join("time_series", filename)
    time_series_entries = csv_helper.read_entries(filepath)

    # Load and convert the string values from the .csv file into types that we can work with (datetime and floats).
    times = [datetime.fromisoformat(entry.get(csv_helper.TIMESTAMP)) for entry in time_series_entries]
    x_values = calculations.get_float_values(time_series_entries, csv_helper.RADIAL_VIB_X)
    y_values = calculations.get_float_values(time_series_entries, csv_helper.RADIAL_VIB_Y)

    # Calculate the rolling average for both the x and y vibration values.
    # A window size of 72 gives us the rolling average over 12 hours
    # and shows the trend of increasing vibration before failure.
    rolling_x = calculations.calculate_rolling_average(x_values, window_size=72)
    rolling_y = calculations.calculate_rolling_average(y_values, window_size=72)
    create_vibration_graph(rolling_x, rolling_y, times)
