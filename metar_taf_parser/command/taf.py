import re

from metar_taf_parser.model.enum import IcingIntensity, TurbulenceIntensity
from metar_taf_parser.model.model import ITafGroups, Icing, Turbulence


class IcingCommand:
    regex = r'^6(\d)(\d{3})(\d)$'

    def __init__(self):
        self._pattern = re.compile(IcingCommand.regex)

    def can_parse(self, input: str):
        return self._pattern.search(input)

    def execute(self, itaf: ITafGroups, input: str):
        """

        :param itaf: metar_taf_parser.model.model.ITafGroups
        :param input: string
        :return:
        """
        matches = self._pattern.search(input).groups()
        icing = Icing()
        icing.intensity = IcingIntensity(matches[0])
        icing.base_height = 100 * int(matches[1])
        icing.depth = 1000 * int(matches[2])
        itaf.add_icing(icing)


class TurbulenceCommand:
    regex = r"^5(\d|'X')(\d{3})(\d)$"

    def __init__(self):
        self._pattern = re.compile(TurbulenceCommand.regex)

    def can_parse(self, input: str):
        return self._pattern.search(input)

    def execute(self, itaf: ITafGroups, input: str):
        """

        :param itaf: metar_taf_parser.model.model.ITafGroups
        :param input: string
        :return:
        """
        matches = self._pattern.search(input).groups()
        turbulence = Turbulence()
        turbulence.intensity = TurbulenceIntensity(matches[0])
        turbulence.base_height = 100 * int(matches[1])
        turbulence.depth = 1000 * int(matches[2])
        itaf.add_turbulence(turbulence)


class TAFCommandSupplier:
    def __init__(self):
        self._commands = [IcingCommand(), TurbulenceCommand()]

    def get(self, input: str):
        for command in self._commands:
            if command.can_parse(input):
                return command
