import re


def degrees_to_cardinal(input):
    if input.isnumeric():
        degrees = int(input)
        dirs = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
        ix = int((degrees + 11.25) / 22.5)
        return dirs[ix % 16]
    else:
        return 'VRB'


def convert_visibility(input):
    if '9999' == input:
        return '>10000'
    return str(int(input))


def convert_temperature(input):
    if input.startswith('M'):
        return -int(input.split('M')[1])
    return int(input)


def convert_inches_mercury_to_pascal(input):
    return 33.8639 * input


def convert_temperature_remarks(sign: str, temperature: str):
    temp = float(temperature) / 10
    return temp if '0' == sign else -1 * temp


def convert_precipitation_amount(amount: str):
    return float(amount) / 100


SM_TO_KM = 1.609344


def convert_visibility_to_km(raw_visibility: str, unit_shortcut: str):
    """
    Converts the visibility to a value in km using the provided unit shortcut.
    :param raw_visibility: The raw visibility string (no unit suffix expected)
    :param unit_shortcut: The unit shortcut ('M', 'SM', 'KM', 'FT')
    :return: The visibility in km as a float, or None if not parsable
    """
    cleaned = raw_visibility.replace('>', '')
    match = re.search(r'(\d+)', cleaned)
    if not match:
        return None
    value = int(match.group(1))
    shortcut = unit_shortcut.upper()
    if shortcut == 'SM':
        return value * SM_TO_KM
    elif shortcut == 'KM':
        return float(value)
    elif shortcut == 'M':
        return value / 1000.0
    return None
