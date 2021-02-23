from metar_taf_parser.model.model import Pressure


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


def convert_inhg_to_hpa(input):
    return float('{:4.0f}'.format(float(input / 100) / 0.029529983071445))


def convert_hpa_to_inhg(input):
    return float('{:5.2f}'.format(float(input) * 0.029529983071445))


def convert_pressure(input):
    pressure = Pressure()
    if input.startswith('Q'):
        pressure.pressure = float('{:4.0f}'.format(float(input.split('Q')[1])))
        pressure.unit = 'hPa'
    else:
        pressure.pressure = float('{:5.2f}'.format(float(input.split('A')[1]) / 100))
        pressure.unit = 'inHg'
    return pressure
