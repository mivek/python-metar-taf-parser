
import re

from metar_taf_parser.commons import converter
from metar_taf_parser.commons.converter import convert_visibility
from metar_taf_parser.model.enum import CloudQuantity, CloudType
from metar_taf_parser.model.model import Visibility, Wind, WindShear, Cloud, AbstractWeatherContainer


def set_wind_elements(wind: Wind, direction: str, speed: str, gust: str, unit: str):
    """
    This function updates a wind element.
    :param wind: Wind. The wind object
    :param direction: str. The direction in degrees
    :param speed: str. The speed
    :param gust: int. The speed of the gust.
    :param unit: str. The speed unit
    :return: None.
    """
    wind.speed = int(speed)
    wind.direction = converter.degrees_to_cardinal(direction)

    if 'VRB' != direction:
        wind.degrees = int(direction)
    if gust:
        wind.gust = int(gust)
    if unit:
        wind.unit = unit
    else:
        wind.unit = 'KT'


class CloudCommand:
    cloud_regex = r'^([A-Z]{3})(\d{3})?([A-Z]{2,3})?$'

    def __init__(self):
        self._pattern = re.compile(CloudCommand.cloud_regex)

    def parse(self, cloud_string: str):
        m = self._pattern.search(cloud_string).groups()
        cloud = Cloud()
        try:
            if CloudQuantity[m[0]]:
                cloud.quantity = CloudQuantity[m[0]]
            if m[1]:
                cloud.height = 100 * int(m[1])
            if m[2] and CloudType[m[2]]:
                cloud.type = CloudType[m[2]]
            return cloud
        except KeyError:
            return

    def execute(self, container: AbstractWeatherContainer, cloud_string: str):
        cloud = self.parse(cloud_string)
        if cloud and cloud.quantity:
            container.add_cloud(cloud)
            return True

    def can_parse(self, cloud_string: str):
        return self._pattern.search(cloud_string)


class MainVisibilityCommand:
    regex = r'^(\d{4})(|NDV)$'

    def __init__(self):
        self._pattern = re.compile(MainVisibilityCommand.regex)

    def can_parse(self, visibility_string: str):
        return self._pattern.search(visibility_string)

    def execute(self, container: AbstractWeatherContainer, visibility_string: str):
        matches = self._pattern.search(visibility_string).groups()
        if container.visibility is None:
            container.visibility = Visibility()
        container.visibility.distance = convert_visibility(matches[0])
        return True


class WindCommand:
    regex = r'^(VRB|\d{3})(\d{2})G?(\d{2})?(KT|MPS|KM\/H)?'

    def __init__(self):
        self._pattern = re.compile(WindCommand.regex)

    def can_parse(self, wind_string: str):
        """

        :param wind_string: str
            The string to parse
        :return:
        """
        return self._pattern.search(wind_string)

    def parse_wind(self, wind_string: str):
        wind = Wind()
        matches = self._pattern.search(wind_string).groups()
        set_wind_elements(wind, matches[0], matches[1], matches[2], matches[3])
        return wind

    def execute(self, container: AbstractWeatherContainer, wind_string: str):
        wind = self.parse_wind(wind_string)
        container.wind = wind
        return True


class WindVariationCommand:
    regex = r'^(\d{3})V(\d{3})'

    def __init__(self):
        self._pattern = re.compile(WindVariationCommand.regex)

    def can_parse(self, wind_string: str):
        return self._pattern.search(wind_string)

    def parse_wind_variation(self, wind: Wind, wind_string: str):
        matches = self._pattern.search(wind_string).groups()
        wind.min_variation = int(matches[0])
        wind.max_variation = int(matches[1])

    def execute(self, container, wind_string):
        self.parse_wind_variation(container.wind, wind_string)
        return True


class WindShearCommand:
    regex = r'^WS(\d{3})\/(\w{3})(\d{2})G?(\d{2})?(KT|MPS|KM\/H)'

    def __init__(self):
        self._pattern = re.compile(WindShearCommand.regex)

    def can_parse(self, wind_string: str):
        return self._pattern.search(wind_string)

    def parse_wind_shear(self, wind_string: str):
        wind_shear = WindShear()
        matches = self._pattern.search(wind_string).groups()

        wind_shear.height = 100 * int(matches[0])
        set_wind_elements(wind_shear, matches[1], matches[2], matches[3], matches[4])
        return wind_shear

    def execute(self, container: AbstractWeatherContainer, wind_string: str):
        container.wind_shear = self.parse_wind_shear(wind_string)
        return True


class VerticalVisibilityCommand:

    regex = r'^VV(\d{3})$'

    def __init__(self):
        self._pattern = re.compile(VerticalVisibilityCommand.regex)

    def execute(self, container: AbstractWeatherContainer, visibility_string: str):
        matches = self._pattern.search(visibility_string).groups()
        container.vertical_visibility = 100 * int(matches[0])
        return True

    def can_parse(self, visibility_string: str):
        return self._pattern.search(visibility_string)


class MinimalVisibilityCommand:
    regex = r'^(\d{4}[a-z])$'

    def __init__(self):
        self._pattern = re.compile(MinimalVisibilityCommand.regex)

    def can_parse(self, visibility_string: str):
        return self._pattern.search(visibility_string)

    def execute(self, container: AbstractWeatherContainer, visibility_string: str):
        """

        :param container: AbstractWeatherContainer
        :param visibility_string: string
        :return:
        """
        matches = self._pattern.search(visibility_string).groups()
        container.visibility.min_distance = int(matches[0][0:4])
        container.visibility.min_direction = matches[0][4]
        return True


class MainVisibilityNauticalMilesCommand:

    regex = r'^(\d)*(\s)?((\d\/\d)?SM)$'

    def __init__(self):
        self._pattern = re.compile(MainVisibilityNauticalMilesCommand.regex)

    def can_parse(self, wind_string: str):
        return self._pattern.search(wind_string)

    def execute(self, container: AbstractWeatherContainer, visibility_string: str):
        if container.visibility is None:
            container.visibility = Visibility()
        container.visibility.distance = visibility_string
        return True


class CommandSupplier:

    def __init__(self):
        self._commands = [
            WindShearCommand(), WindCommand(), WindVariationCommand(), MainVisibilityCommand(),
            MainVisibilityNauticalMilesCommand(), MinimalVisibilityCommand(),
            VerticalVisibilityCommand(), CloudCommand()
        ]

    def get(self, input: str):
        for command in self._commands:
            if command.can_parse(input):
                return command
