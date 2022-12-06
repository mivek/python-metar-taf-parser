import re

from metar_taf_parser.commons import converter
from metar_taf_parser.model.model import RunwayInfo, RunwayReportGroup, Metar
from metar_taf_parser.model.enum import RunwayDeposit, RunwayCoverage, RunwayThickness, RunwayBraking, RunwaySpecial


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


class RunwayReport:
    runway_rg_regex = r'^R((\d{2}\w?)?\/((\d{6})|(\d{2}((\d{2})|(\/\/))((\d{2})|(\/\/)))|(\w{4}\d{2})|(\D{6})))$'

    def __init__(self):
        self._runway_rg_pattern = re.compile(RunwayReport.runway_rg_regex)

    def can_parse(self, input: str):
        return self._runway_rg_pattern.match(input)

    def execute(self, metar: Metar, input: str):
        rrg_matches = self._runway_rg_pattern.findall(input)
        if rrg_matches:
            runway_rg = RunwayReportGroup()
            print(rrg_matches)
            if rrg_matches[0][1] == '88':
                runway_rg.name = 'All runways'
            elif rrg_matches[0][1] == '99':
                runway_rg.name = 'as previous bulletin'
            else:
                runway_rg.name = rrg_matches[0][1]
            if not rrg_matches[0][2][:1].isalpha():
                runway_rg.deposit = RunwayDeposit(rrg_matches[0][2][:1])
                runway_rg.coverage = RunwayCoverage(rrg_matches[0][2][1:2])
                thickness = rrg_matches[0][2][2:4]
                if thickness != '//':
                    if 1 <= int(thickness) <= 90:
                        runway_rg.thickness = thickness + ' mm'
                    else:
                        runway_rg.thickness = RunwayThickness(thickness)
                else:
                    runway_rg.thickness = RunwayThickness(thickness)
                friction = rrg_matches[0][2][4:6]
                if friction != '//':
                    if int(friction) >= 0 & int(friction) <= 90:
                        runway_rg.braking = str(RunwayBraking('coeff')) + ' ' + str(float(int(friction) / 100)) + ' %'
                    else:
                        runway_rg.braking = RunwayBraking(friction)
                else:
                    runway_rg.braking = RunwayBraking(friction)
            else:
                ch_sit_airway = rrg_matches[0][2][:1]
                if ch_sit_airway == 'C':
                    friction = rrg_matches[0][2][4:6]
                    if int(friction) >= 0 & int(friction) <= 90:
                        runway_rg.braking = str(RunwayBraking('coeff')) + ' ' + str(float(int(friction) / 100)) + ' %'
                    else:
                        runway_rg.braking = RunwayBraking(friction)
                    runway_rg.special = RunwaySpecial(rrg_matches[0][2][:4])
                else:
                    runway_rg.special = RunwaySpecial(rrg_matches[0][2])
            metar.add_runway_rg(runway_rg)


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
        self._commands = [RunwayReport(), RunwayCommand(), TemperatureCommand(), AltimeterCommand(),
                          AltimeterMercuryCommand()]

    def get(self, input: str):
        for command in self._commands:
            if command.can_parse(input):
                return command
