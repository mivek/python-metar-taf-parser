import re

from metar_taf_parser.commons import converter
from metar_taf_parser.model.model import RunwayInfo, Metar


class AltimeterCommand:
    regex = r'^Q(\d{4})$'

    def __init__(self):
        self._pattern = re.compile(AltimeterCommand.regex)

    def can_parse(self, input: str):
        return self._pattern.search(input)

    def execute(self, metar: Metar, input: str):
        """

        :param metar: metar_taf_parser.model.model.Metar
        :param input: string
        :return:
        """
        matches = self._pattern.search(input).groups()
        metar.altimeter = int(matches[0])


class AltimeterMercuryCommand:
    regex = r'^A(\d{4})$'

    def __init__(self):
        self._pattern = re.compile(AltimeterMercuryCommand.regex)

    def can_parse(self, input: str):
        return self._pattern.search(input)

    def execute(self, metar: Metar, input: str):
        matches = self._pattern.search(input).groups()
        mercury = float(matches[0]) / 100
        metar.altimeter = int(converter.convert_inches_mercury_to_pascal(mercury))


class RunwayCommand:
    generic_regex = r'^(R\d{2}\w?/)'
    runway_max_range_regex = r'^R(\d{2}\w?)/(\d{4})V(\d{3})(\w{0,2})'
    runway_regex = r'^R(\d{2}\w?)/(\w)?(\d{4})(\w{0,2})$'

    def __init__(self):
        self._generic_pattern = re.compile(RunwayCommand.generic_regex)
        self._max_range_pattern = re.compile(RunwayCommand.runway_max_range_regex)
        self._runway_pattern = re.compile(RunwayCommand.runway_regex)

    def can_parse(self, input: str):
        return self._generic_pattern.match(input)

    def execute(self, metar: Metar, input: str):
        matches = self._runway_pattern.findall(input)
        runway = RunwayInfo()
        if matches:
            runway.name = matches[0][0]
            runway.min_range = int(matches[0][2])
            runway.trend = matches[0][3]
            metar.add_runway_info(runway)

        matches = self._max_range_pattern.findall(input)
        if matches:
            runway.name = matches[0][0]
            runway.min_range = int(matches[0][1])
            runway.max_range = int(matches[0][2])
            runway.trend = matches[0][3]
            metar.add_runway_info(runway)


class TemperatureCommand:
    regex = r'^(M?\d{2})/(M?\d{2})$'

    def __init__(self):
        self._pattern = re.compile(TemperatureCommand.regex)

    def can_parse(self, input: str):
        return self._pattern.match(input)

    def execute(self, metar: Metar, input: str):
        matches = self._pattern.search(input).groups()
        metar.temperature = converter.convert_temperature(matches[0])
        metar.dew_point = converter.convert_temperature(matches[1])


class CommandSupplier:
    def __init__(self):
        self._commands = [RunwayCommand(), TemperatureCommand(), AltimeterCommand(), AltimeterMercuryCommand()]

    def get(self, input: str):
        for command in self._commands:
            if command.can_parse(input):
                return command
