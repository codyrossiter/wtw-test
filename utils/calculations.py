def calculate_rolling_average(values, window_size):
    rolling_average = []
    for i in range(len(values)):
        # For the first few entries the starting value is a negative number
        # we use the max function to select index 0 as our starting point.
        window_start = max(i - window_size + 1, 0)
        value_section = values[window_start: i + 1]
        rolling_average.append(sum(value_section) / len(value_section))

    return rolling_average


def get_float_values(entries, field):
    values = []
    for entry in entries:
        string_value = entry.get(field)
        if len(string_value) == 0:
            values.append(0.0)
        else:
            values.append(float(string_value))

    return values
