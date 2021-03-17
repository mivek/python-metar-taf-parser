import abc
import re
from datetime import time

from metar_taf_parser.command.common import CommandSupplier
from metar_taf_parser.command.metar import CommandSupplier as MetarCommandSupplier
from metar_taf_parser.command.remark import RemarkCommandSupplier
from metar_taf_parser.commons import converter
from metar_taf_parser.commons.exception import TranslationError
from metar_taf_parser.model.enum import Intensity, Descriptive, Phenomenon, TimeIndicator, WeatherChangeType
from metar_taf_parser.model.model import WeatherCondition, Visibility, Metar, TemperatureDated, \
    AbstractWeatherContainer, TAF, TAFTrend, MetarTrend, Validity, FMValidity, MetarTrendTime


def parse_delivery_time(abstract_weather_code, time_string):
    """
    Parses the delivery time of a METAR/TAF
    :param abstract_weather_code: The TAF or METAR object
    :param time_string: The string representing the delivery time
    :return: None
    """
    abstract_weather_code.day = int(time_string[0:2])
    abstract_weather_code.time = time(int(time_string[2:4]), int(time_string[4:6]))


def parse_remark(container: AbstractWeatherContainer, line: [str], index: int):
    """
    This function parses the array containing the remark and concat the array into a string
    :param container: the metar, taf or taf trend to update
    :param line: The array containing the current line tokens
    :param index: the index starting the remark ie token RMK
    :return: None
    """
    remarks = RemarkParser().parse(str.join(' ', line[index + 1:]))
    container.remarks = remarks
    container.remark = str.join(' ', remarks)


def _parse_temperature(input: str):
    """
    Parses the temperature in a TAF
    :param input: the string containing the temperature
    :return: TemperatureDated object
    """
    parts = input.split('/')
    temperature = TemperatureDated()

    temperature.temperature = converter.convert_temperature(parts[0][2:])
    temperature.day = int(parts[1][0:2])
    temperature.hour = int(parts[1][2:4])
    return temperature


def _parse_validity(input: str):
    """
    Parses validity of a TAF or a TAFTrend
    :param input: the string containing the validity
    :return: Validity object
    """
    validity = Validity()
    parts = input.split('/')
    validity.start_day = int(parts[0][0:2])
    validity.start_hour = int(parts[0][2:])
    validity.end_day = int(parts[1][0:2])
    validity.end_hour = int(parts[1][2:])
    return validity


def _parse_from_validity(input: str):
    """
    Parses the validity for a FROM taf trend
    :param input: the string containing the validity
    :return: a Validity object
    """
    validity = FMValidity()
    validity.start_day = int(input[2:4])
    validity.start_hour = int(input[4:6])
    validity.start_minutes = int(input[6:8])

    return validity


class AbstractParser(abc.ABC):
    """
    Abstract class.
    Base parser.
    """
    FM = 'FM'
    TEMPO = 'TEMPO'
    BECMG = 'BECMG'
    RMK = 'RMK'
    TOKENIZE_REGEX = r'\s((?=\d\/\dSM)(?<!\s\d\s)|(?!\d\/\dSM))|='
    INTENSITY_REGEX = r'^(-|\+|VC)'
    CAVOK = 'CAVOK'

    def __init__(self):
        self._common_supplier = CommandSupplier()
        self._tokenize_regex_pattern = re.compile(AbstractParser.TOKENIZE_REGEX)
        self._intensity_regex_pattern = re.compile(AbstractParser.INTENSITY_REGEX)

    @abc.abstractmethod
    def parse(self, input: str):
        pass

    def _parse_weather_condition(self, input: str):
        """
        Parses a string into a weather condition. The result is not necessarily valid
        :param input: The input to parse
        :return: WeatherCondition object
        """
        weather_condition = WeatherCondition()
        if self._intensity_regex_pattern.match(input):
            match = self._intensity_regex_pattern.findall(input)[0]
            weather_condition.intensity = Intensity(match)

        for name, member in Descriptive.__members__.items():
            if member.value in input:
                weather_condition.descriptive = member

        for name, member in Phenomenon.__members__.items():
            if member.value in input:
                weather_condition.add_phenomenon(member)

        return weather_condition

    def tokenize(self, input: str):
        """
        Parses the message into different tokens
        :param input: The metar or TAF as string
        :return: List of tokens
        """
        return list(filter(None, self._tokenize_regex_pattern.split(input)))

    def general_parse(self, abstract_weather_container: AbstractWeatherContainer, input: str):
        """
        Common parse method for METAR, TAF and trends object
        :param abstract_weather_container: the object to update
        :param input: The token to parse
        :return: True if the token was parsed false otherwise
        """
        if AbstractParser.CAVOK == input:
            abstract_weather_container.cavok = True
            if abstract_weather_container.visibility is None:
                abstract_weather_container.visibility = Visibility()
            abstract_weather_container.visibility.distance = '> 10km'
            return True

        command = self._common_supplier.get(input)
        if command:
            return command.execute(abstract_weather_container, input)

        return abstract_weather_container.add_weather_condition(self._parse_weather_condition(input))


class MetarParser(AbstractParser):
    """
    Parser to Metar messages.
    """
    AT = 'AT'
    TL = 'TL'

    def __init__(self):
        super().__init__()
        self._metar_command_supplier = MetarCommandSupplier()

    def _parse_trend(self, index: int, trend: MetarTrend, trend_parts: [str]):
        """
        Parses a trend of a metar
        :param index: the index starting the trend in the list
        :param trend: The trend to update
        :param trend_parts: string[] array of tokens
        :return: the last index of the token that was last parsed
        """
        i = index + 1
        while i < len(trend_parts) and AbstractParser.TEMPO != trend_parts[i] and AbstractParser.BECMG != trend_parts[i]:
            if trend_parts[i].startswith(AbstractParser.FM) or trend_parts[i].startswith(MetarParser.TL) or trend_parts[i].startswith(MetarParser.AT):

                trend_time = MetarTrendTime(TimeIndicator[trend_parts[i][0:2]])
                trend_time.time = time(int(trend_parts[i][2:4]), int(trend_parts[i][4:6]))
                trend.add_time(trend_time)
            else:
                self.general_parse(trend, trend_parts[i])
            i = i + 1
        return i - 1

    def parse(self, input: str):
        """
        Parses an message and returns a METAR
        :param input: The message to parse
        :return: METAR
        """
        metar = Metar()

        metar_tab = self.tokenize(input)
        metar.station = metar_tab[0]

        metar.message = input

        parse_delivery_time(metar, metar_tab[1])
        index = 2
        while index < len(metar_tab):
            if not super().general_parse(metar, metar_tab[index]):
                if 'NOSIG' == metar_tab[index]:
                    metar.nosig = True
                elif 'AUTO' == metar_tab[index]:
                    metar.auto = True
                elif AbstractParser.TEMPO == metar_tab[index] or AbstractParser.BECMG == metar_tab[index]:
                    trend = MetarTrend(WeatherChangeType[metar_tab[index]])
                    index = self._parse_trend(index, trend, metar_tab)
                    metar.add_trend(trend)
                elif AbstractParser.RMK == metar_tab[index]:
                    parse_remark(metar, metar_tab, index)
                    break
                else:
                    command = self._metar_command_supplier.get(metar_tab[index])
                    if command:
                        command.execute(metar, metar_tab[index])
            index = index + 1
        return metar


class TAFParser(AbstractParser):
    """
    Parser of TAF messages.
    """
    TAF = 'TAF'
    PROB = 'PROB'
    TX = 'TX'
    TN = 'TN'

    def __init__(self):
        super().__init__()
        self._validity_pattern = re.compile(r'^\d{4}/\d{4}$')

    def parse(self, input: str):
        """
        Parses a message into a TAF
        :param input: the message to parse
        :return: a TAF object or None if the message is invalid
        """
        taf = TAF()
        lines = self._extract_lines_tokens(input)
        if TAFParser.TAF != lines[0][0]:
            return
        index = 1
        if TAFParser.TAF == lines[0][1]:
            index = 2
        if 'AMD' == lines[0][index]:
            taf.amendment = True
            index += 1

        taf.station = lines[0][index]
        index += 1
        taf.message = input
        parse_delivery_time(taf, lines[0][index])
        index += 1
        taf.validity = _parse_validity(lines[0][index])

        for i in range(index + 1, len(lines[0])):
            token = lines[0][i]
            if AbstractParser.RMK == token:
                parse_remark(taf, lines[0], i)
            elif token.startswith(TAFParser.TX):
                taf.max_temperature = _parse_temperature(token)
            elif token.startswith(TAFParser.TN):
                taf.min_temperature = _parse_temperature(token)
            else:
                self.general_parse(taf, token)

        # Handle the other lines
        for line in lines[1:]:
            self._parse_line(taf, line)

        return taf

    def _extract_lines_tokens(self, taf_code: str):
        """
        Format the message as a multiple line code so each line can be parsed
        :param taf_code: The base message
        :return: a list of string representing the lines of the message.
        """
        single_line = taf_code.replace('\n', ' ')
        clean_line = re.sub(r'\s{2,}', ' ', single_line)
        lines = re.sub(r'\s(PROB\d{2}\sTEMPO|TEMPO|BECMG|FM|PROB)', '\n\g<1>', clean_line).splitlines()
        lines_token = [self.tokenize(line) for line in lines]

        if len(lines_token) > 1:
            last_line = lines_token[len(lines) - 1]
            temperatures = list(filter(lambda x: x.startswith(TAFParser.TX) or x.startswith(TAFParser.TN), last_line))

            if temperatures:
                lines_token[0] = lines_token[0] + temperatures
                lines_token[len(lines) - 1] = list(filter(lambda x: not x.startswith(TAFParser.TX) and not x.startswith(TAFParser.TN), last_line))
        return lines_token

    def _parse_line(self, taf: TAF, line_tokens: [str]):
        """
        Parses the tokens of the line and updates the TAF object.
        :param taf: TAF object to update
        :param line_tokens: the array of tokens representing a line
        :return: None
        """
        index = 1
        if line_tokens[0].startswith(TAFParser.FM):
            trend = TAFTrend(WeatherChangeType.FM)
            trend.validity = _parse_from_validity(line_tokens[0])
        elif line_tokens[0].startswith(TAFParser.PROB):
            trend = TAFTrend(WeatherChangeType.PROB)
            if len(line_tokens) > 1 and TAFParser.TEMPO == line_tokens[1]:
                trend = TAFTrend(WeatherChangeType(line_tokens[1]))
                index = 2
            trend.probability = int(line_tokens[0][4:])
        else:
            trend = TAFTrend(WeatherChangeType(line_tokens[0]))
        self._parse_trend(index, line_tokens, trend)
        taf.add_trend(trend)

    def _parse_trend(self, index: int, line: [str], trend: TAFTrend):
        """
        Parses a trend of the TAF
        :param index: the index at which the array should be parsed
        :param line: The array of string containing the line
        :param trend: The trend object to update
        :return: None
        """
        for i in range(index, len(line)):
            if AbstractParser.RMK == line[i]:
                parse_remark(trend, line, i)
            elif self._validity_pattern.search(line[i]):
                trend.validity = _parse_validity(line[i])
            else:
                super().general_parse(trend, line[i])


class RemarkParser:
    def __init__(self):
        self._supplier = RemarkCommandSupplier()

    def parse(self, code: str) -> [str]:
        rmk_str = code
        rmk_list = []

        while rmk_str:
            try:
                (rmk_str, rmk_list) = self._supplier.get(rmk_str).execute(rmk_str, rmk_list)
            except TranslationError:
                (rmk_str, rmk_list) = self._supplier.default_command.execute(rmk_str, rmk_list)
        return rmk_list
