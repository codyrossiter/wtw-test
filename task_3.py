import os

from utils import calculations, csv_helper


def get_windmill_list(farm):
    """
    Return a list of windmill ids that belong to a specified farm.

    Given the turbine_metadata information and time_series filenames we infer
    that the windmills are arranged into groups of 4 with ids that start at 3057 and end at 3109.
    Every group of four is assigned to a windmill farm in order starting from Alpha
    and the assumption is that the order repeats after Delta e.g., A,B,C,D,A,B,C,D,...
    :param farm: The farm whose windmill ids we want to return.
    :return: A list of windmill ids
    """
    if farm == csv_helper.ALPHA:
        start_id = csv_helper.ALPHA_ID_START
    elif farm == csv_helper.BRAVO:
        start_id = csv_helper.BRAVO_ID_START
    elif farm == csv_helper.CHARLIE:
        start_id = csv_helper.CHARLIE_ID_START
    else:
        start_id = csv_helper.DELTA_ID_START

    # Generate windmill ids in groups of four that correspond to the specified farm.
    windmill_ids = []
    for i in range(start_id, csv_helper.WINDMILL_ID_END + 1, 16):
        windmill_ids += [windmill for windmill in range(i, i + 4)]

    # Not all windmills have files in the dataset.
    # Go through the generated IDs and only keep the ones that
    # have an associated time_series file
    valid_windmill_ids = []
    for windmill in windmill_ids:
        filename = f"{windmill}.csv"
        filepath = os.path.join("data", "time_series", filename)

        if os.path.exists(filepath):
            valid_windmill_ids.append(windmill)

    return valid_windmill_ids


def has_active_power(entry):
    """
    Helper function that checks if the active power field has a non-zero/empty value.
    :param entry: The entry whose active power field should be checked
    :return: Boolean indicating if the active power field has a non-zero value.
    """
    active_power = entry.get(csv_helper.ACTIVE_POWER)
    # active power may be '' which cannot be cast to a float.
    if len(active_power) == 0 or float(active_power) == 0.0:
        return False

    return True


def get_windmill_status(timestamp, windmill_id):
    """
    Determine the status of a windmill at a specified time.

    A windmill that has no active power is determined to be DOWN.
    Then, the earliest vibration measurements are compared to the measurements near the timestamp.
    If the vibration has greatly increased, then the status is WARNING.
    Otherwise, the status is OK.
    :param timestamp: The time in which to check the windmill.
    :param windmill_id: The id of the selected windmill.
    :return: A status value indicating if the windmill is DOWN, WARNING, or OK
    """
    # Load the windmill timeseries data
    filename = f"{windmill_id}.csv"
    filepath = os.path.join("time_series", filename)
    time_series_entries = csv_helper.read_entries(filepath)

    # Get the entry corresponding to the timestamp
    # We will consider entries up to and including the timestamp entry
    timestamp_index = 0
    for i in range(len(time_series_entries)):
        entry = time_series_entries[i]
        if entry.get(csv_helper.TIMESTAMP) == timestamp:
            timestamp_index = i
            break

    # Start with the simple check: if active power is 0 then the windmill is down
    entry = time_series_entries[timestamp_index]
    if not has_active_power(entry):
        return "Down"

    # Now we have to see if the windmill is functioning properly
    # and we do so by comparing the current vibration measurements with earlier vibration measurements.
    # We start by working backwards from the current timestamp index and look for either the
    # windmill restarting after a shutdown or the earliest measurement.
    # We assume that the windmill is at its "healthiest" state after a restart
    # and use the found index as our starting, healthy index.
    start_index = 0
    for i in range(timestamp_index, 0, -1):
        entry = time_series_entries[i]
        if not has_active_power(entry):
            start_index = i
            break

    # For brevity, we only consider the X vibration measurements.
    # The Y measurements will use the same logic, and it appears that both vibration measures increase before failure.
    # A more robust check may require domain knowledge e.g., what happens if X increases but Y doesn't?
    x_values = calculations.get_float_values(time_series_entries[start_index: timestamp_index + 1],
                                             csv_helper.RADIAL_VIB_X)
    # average the starting healthy measurements
    # The window size of 72 gives an average for 12 hours of measurements
    window_size = 72
    starting_values = x_values[0:window_size]
    start_avg = sum(starting_values) / len(starting_values)

    # average the measurements before and up to the timestamp
    ending_values = x_values[-window_size:]
    end_avg = sum(ending_values) / len(ending_values)

    # Check if the timestamp average has increased.
    # If the increase ratio exceeds the threshold value then the windmill may be de-stabilizing.
    # The choice of 1.5 works as an arbitrary starting point but further testing could provide a better threshold.
    threshold = 1.5
    if end_avg / start_avg < threshold:
        return "OK"
    else:
        return "Warning"


def get_farm_status(query_timestamp, query_farm):
    """
    Print the status of each windmill on a specified farm at a specified time.
    :param query_timestamp: The time at which the windmills should be evaluated.
    :param query_farm: The farm whose windmills should be evaluated.
    :return: None
    """
    windmills = get_windmill_list(query_farm)

    print(f"Checking the status of Farm {query_farm} at {query_timestamp}:")
    for windmill in windmills:
        status = get_windmill_status(query_timestamp, windmill)
        print(f"\tWindmill {windmill}: {status}")


if __name__ == "__main__":
    """
    A few tests to ensure that the get_farm_status() method is working.
    These tests would ideally be in a dedicated testing directory.
    """
    get_farm_status("2022-12-08 12:30:00", csv_helper.DELTA)
    print()  # Add space between outputs
    get_farm_status("2022-12-24 17:20:00", csv_helper.BRAVO)
