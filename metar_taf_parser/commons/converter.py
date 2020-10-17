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
        return '> 10km'
    return str(int(input)) + 'm'


def convert_temperature(input):
    if input.startswith('M'):
        return -int(input.split('M')[1])
    return int(input)


def convert_inches_mercury_to_pascal(input):
    return 33.8639 * input
