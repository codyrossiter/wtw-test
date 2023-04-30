from datetime import datetime, timedelta
from utils import csv_helper


def calculate_downtime(downtime_entry, query_start, query_end):
    """
    Calculate the amount of downtime that a windmill has experienced during
    some queried time period.

    :param downtime_entry: The entry containing a windmill's downtime information.
    :param query_start: The start date of the time period.
    :param query_end: The end date of the time period.
    :return: A timedelta containing the total downtime during the queried time period.
    """
    # Get and convert the times into datetime objects
    # in order to perform date calculations
    entry_start = downtime_entry.get(csv_helper.START)
    windmill_start = datetime.fromisoformat(entry_start)
    entry_end = downtime_entry.get(csv_helper.END)
    windmill_end = datetime.fromisoformat(entry_end)

    # Calculate the total downtime during the query time period.
    # The assumption is that all times are valid and that the start times
    # are before the end times.

    # If both times are within the query
    if query_start <= windmill_start and windmill_end < query_end:
        return windmill_end - windmill_start
    # If the downtime starts within the query but ends afterwards
    elif query_start <= windmill_start and query_end <= windmill_end:
        return query_end - windmill_start
    # If the downtime starts before the query but ends during it
    elif windmill_start < query_start and windmill_end < query_end:
        return windmill_end - query_start
    # If the downtime starts before the query and ends after it
    elif windmill_start < query_start and query_end <= windmill_end:
        return query_end - query_start

    # return a zero value timedelta
    return timedelta()


if __name__ == "__main__":
    # To make the script look a little more 'real world' I'm writing it like it
    # was passed some search parameters rather than hard coding Dec 2022 into the date calculations.
    query_start_date = datetime.fromisoformat("2022-12-01")
    query_end_date = datetime.fromisoformat("2023-01-01")

    downtime_entries = csv_helper.read_entries("downtime.csv")
    metadata_entries = csv_helper.read_entries("turbine_metadata.csv")

    # Create the windmill id to farm map
    # in order to group downtime by farm later.
    windmill_to_farm = {}
    for entry in metadata_entries:
        windmill = entry.get(csv_helper.METADATA_ID)
        farm = entry.get(csv_helper.FARM)
        windmill_to_farm[windmill] = farm

    # Print total downtime in Dec 2022
    total_downtime = timedelta()
    for entry in downtime_entries:
        total_downtime += calculate_downtime(entry, query_start_date, query_end_date)
    print(f"Total Downtime from {query_start_date} to {query_end_date}: {total_downtime}\n")

    # Print breakdown of downtime by windfarm
    farm_downtimes = {farm_name: timedelta() for farm_name in csv_helper.FARMS}
    for entry in downtime_entries:
        windmill_id = entry.get(csv_helper.DOWNTIME_ID)
        farm = windmill_to_farm[windmill_id]
        farm_downtimes[farm] += calculate_downtime(entry, query_start_date, query_end_date)

    print("Downtime by Windmill Farm:")
    for farm, downtime in farm_downtimes.items():
        print(f"\t{farm}: {downtime}")
