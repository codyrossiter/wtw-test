import csv
import os.path

# Below are constants for accessing csv field names and windmill values.
# I would prefer to have these in an enum or class structure
# but String enums are a new feature in python 3.11 (I'm on 3.10)
# and constructing classes or custom functionality exceeds the scope of this project.

# Metadata
NAME = "name"
METADATA_ID = "id"
FARM = "wind_farm"

# Windfarms
ALPHA = "Alpha"
BRAVO = "Bravo"
CHARLIE = "Charlie"
DELTA = "Delta"
FARMS = [ALPHA, BRAVO, CHARLIE, DELTA]

# Time Series ID constants
WINDMILL_ID_START = 3057
WINDMILL_ID_END = 3109

ALPHA_ID_START = 3057
BRAVO_ID_START = 3061
CHARLIE_ID_START = 3065
DELTA_ID_START = 3069

# Downtime
DOWNTIME_ID = "id"
START = "start"
END = "end"

# Timeseries
TIMESTAMP = ""
RADIAL_VIB_X = "RadialVibX"
RADIAL_VIB_Y = "RadialVibY"
ACTIVE_POWER = "ActivePower"


def read_entries(filename):
    """
    Load a csv file into a list of dictionaries where each dictionary contains a mapping of
    field names to entry data.
    :param filename: The csv to load.
    :return: A list containing a dictionary of csv entries.
    """
    entries = []
    filepath = os.path.join("data", filename)
    with open(filepath, 'r') as downtime_file:
        reader = csv.DictReader(downtime_file)
        for entry in reader:
            entries.append(entry)

    return entries
