import re

from metar_taf_parser.commons import converter
from metar_taf_parser.model.enum import DepositType, DepositCoverage
from metar_taf_parser.model.model import RunwayInfo, Metar
from metar_taf_parser.commons.i18n import _


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
    runway_max_range_regex = r'^R(\d{2}\w?)/(\d{4})V(\d{3,4})([UDN])?(FT)?'
    runway_regex = r'^R(\d{2}\w?)/([MP])?(\d{4})([UDN])?(FT)?$'
    runway_deposit_regex = r'^R(\d{2}\w?)/([/\d])([/\d])(//|\d{2})(//|\d{2})$'

    def __init__(self):
        self._generic_pattern = re.compile(RunwayCommand.generic_regex)
        self._max_range_pattern = re.compile(RunwayCommand.runway_max_range_regex)
        self._runway_pattern = re.compile(RunwayCommand.runway_regex)
        self._runway_deposit_pattern = re.compile(RunwayCommand.runway_deposit_regex)
        self._deposit_thickness = {
            '//': 'DepositThickness.//',
            '00': 'DepositThickness.00',
            '92': 'DepositThickness.92',
            '93': 'DepositThickness.93',
            '94': 'DepositThickness.94',
            '96': 'DepositThickness.96',
            '97': 'DepositThickness.97',
            '98': 'DepositThickness.98',
            '99': 'DepositThickness.99'
        }
        self._deposit_braking_capacity = {
            '//': 'DepositBrakingCapacity.//',
            '91': 'DepositBrakingCapacity.91',
            '92': 'DepositBrakingCapacity.92',
            '93': 'DepositBrakingCapacity.93',
            '94': 'DepositBrakingCapacity.94',
            '95': 'DepositBrakingCapacity.95',
            '99': 'DepositBrakingCapacity.99'
        }

    def can_parse(self, input: str):
        return self._generic_pattern.match(input)

    def execute(self, metar: Metar, input: str):
        matches = self._runway_deposit_pattern.findall(input)
        runway = RunwayInfo()
        if matches:
            runway.name = matches[0][0]
            runway.deposit_type = DepositType(matches[0][1])
            runway.coverage = DepositCoverage(matches[0][2])
            runway.thickness = self.__parse_deposit_thickness(matches[0][3])
            runway.braking_capacity = self.__parse_deposit_braking_capacity(matches[0][4])
            metar.add_runway_info(runway)
            return

        matches = self._runway_pattern.findall(input)
        if matches:
            runway.name = matches[0][0]
            runway.indicator = matches[0][1]
            runway.min_range = int(matches[0][2])
            runway.trend = matches[0][3]
            metar.add_runway_info(runway)
            return

        matches = self._max_range_pattern.findall(input)
        if matches:
            runway.name = matches[0][0]
            runway.min_range = int(matches[0][1])
            runway.max_range = int(matches[0][2])
            runway.trend = matches[0][3]
            metar.add_runway_info(runway)

    def __parse_deposit_thickness(self, input):
        thickness = self._deposit_thickness.get(input, 'DepositThickness.default')
        return _(thickness).format(input)

    def __parse_deposit_braking_capacity(self, input):
        braking_capacity = self._deposit_braking_capacity.get(input, 'DepositBrakingCapacity.default')
        return _(braking_capacity).format(float(input) / 100)


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
