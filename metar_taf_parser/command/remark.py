import abc
import re

from metar_taf_parser.commons.converter import convert_temperature_remarks, convert_precipitation_amount
from metar_taf_parser.commons.exception import TranslationError
from metar_taf_parser.commons.i18n import _


CLOUD_QUANTITY = 'CloudQuantity.'
CONVERTER = 'Converter.'
DESCRIPTIVE = 'Descriptive.'
PHENOMENON = 'Phenomenon.'
REMARK = 'Remark.'


def empty_if_none(code: str) -> str:
    return '' if code is None else code


class Command(abc.ABC):

    @abc.abstractmethod
    def execute(self, code: str, remark: list) -> tuple:
        pass

    @abc.abstractmethod
    def can_parse(self, code: str) -> any:
        pass


class CeilingHeightCommand(Command):
    regex = r'^CIG (\d{3})V(\d{3})\b'

    def __init__(self):
        self._pattern = re.compile(CeilingHeightCommand.regex)

    def can_parse(self, code: str) -> any:
        return self._pattern.match(code)

    def execute(self, code: str, remark: list) -> tuple:
        matches = self._pattern.search(code).groups()
        min_ceiling = int(matches[0]) * 100
        max_ceiling = int(matches[1]) * 100
        remark.append(_('Remark.Ceiling.Height').format(min_ceiling, max_ceiling))
        return self._pattern.sub('', code, 1), remark


class CeilingSecondLocationCommand(Command):
    regex = r'^CIG (\d{3}) (\w+)\b'

    def __init__(self):
        self._pattern = re.compile(CeilingSecondLocationCommand.regex)

    def can_parse(self, code: str) -> any:
        return self._pattern.match(code)

    def execute(self, code: str, remark: list) -> tuple:
        matches = self._pattern.search(code).groups()
        height = 100 * int(matches[0])
        remark.append(_('Remark.Ceiling.Second.Location').format(height, matches[1]))
        return self._pattern.sub('', code, 1), remark


class HailSizeCommand(Command):
    regex = r'^GR ((\d/\d)|((\d) ?(\d/\d)?))'

    def __init__(self):
        self._pattern = re.compile(HailSizeCommand.regex)

    def can_parse(self, code: str) -> any:
        return self._pattern.match(code)

    def execute(self, code: str, remark: list) -> tuple:
        matches = self._pattern.search(code).groups()
        remark.append(_('Remark.Hail').format(matches[0]))
        return self._pattern.sub('', code, 1), remark


class HourlyMaximumMinimumTemperatureCommand(Command):
    regex = r'^4([01])(\d{3})([01])(\d{3})\b'

    def __init__(self):
        self._pattern = re.compile(HourlyMaximumMinimumTemperatureCommand.regex)

    def can_parse(self, code: str) -> any:
        return self._pattern.match(code)

    def execute(self, code: str, remark: list) -> tuple:
        matches = self._pattern.search(code).groups()
        remark.append(_('Remark.Hourly.Maximum.Minimum.Temperature').format(
            convert_temperature_remarks(matches[0], matches[1]),
            convert_temperature_remarks(matches[2], matches[3])
        ))
        return self._pattern.sub('', code, 1), remark


class HourlyMaximumTemperatureCommand(Command):
    regex = r'^1([01])(\d{3})\b'

    def __init__(self):
        self._pattern = re.compile(HourlyMaximumTemperatureCommand.regex)

    def can_parse(self, code: str) -> any:
        return self._pattern.match(code)

    def execute(self, code: str, remark: list) -> tuple:
        matches = self._pattern.search(code).groups()
        remark.append(_('Remark.Hourly.Maximum.Temperature').format(
            convert_temperature_remarks(matches[0], matches[1])
        ))
        return self._pattern.sub('', code, 1), remark


class HourlyMinimumTemperatureCommand(Command):
    regex = r'^2([01])(\d{3})\b'

    def __init__(self):
        self._pattern = re.compile(HourlyMinimumTemperatureCommand.regex)

    def can_parse(self, code: str) -> any:
        return self._pattern.match(code)

    def execute(self, code: str, remark: list) -> tuple:
        matches = self._pattern.search(code).groups()
        remark.append(_('Remark.Hourly.Minimum.Temperature').format(
            convert_temperature_remarks(matches[0], matches[1])
        ))
        return self._pattern.sub('', code, 1), remark


class HourlyPrecipitationAmountCommand(Command):
    regex = r'^P(\d{4})\b'

    def __init__(self):
        self._pattern = re.compile(HourlyPrecipitationAmountCommand.regex)

    def can_parse(self, code: str) -> any:
        return self._pattern.match(code)

    def execute(self, code: str, remark: list) -> tuple:
        matches = self._pattern.search(code).groups()
        remark.append(_('Remark.Precipitation.Amount.Hourly').format(
            int(matches[0])
        ))
        return self._pattern.sub('', code, 1), remark


class HourlyPressureCommand(Command):
    regex = r'^5(\d)(\d{3})\b'

    barometer_tendency = {
        0: 'Remark.Barometer.0',
        1: 'Remark.Barometer.1',
        2: 'Remark.Barometer.2',
        3: 'Remark.Barometer.3',
        4: 'Remark.Barometer.4',
        5: 'Remark.Barometer.5',
        6: 'Remark.Barometer.6',
        7: 'Remark.Barometer.7',
        8: 'Remark.Barometer.8'
    }

    def __init__(self):
        self._pattern = re.compile(HourlyPressureCommand.regex)

    def can_parse(self, code: str) -> any:
        return self._pattern.match(code)

    def execute(self, code: str, remark: list) -> tuple:
        matches = self._pattern.search(code).groups()
        remark.append(
            _(HourlyPressureCommand.barometer_tendency[int(matches[0])])
            + ' '
            + _('Remark.Pressure.Tendency').format(float(matches[1]) / 10)
        )
        return self._pattern.sub('', code, 1), remark


class HourlyTemperatureDewPointCommand(Command):
    regex = r'^T([01])(\d{3})(([01])(\d{3}))?'

    def __init__(self):
        self._pattern = re.compile(HourlyTemperatureDewPointCommand.regex)

    def can_parse(self, code: str) -> any:
        return self._pattern.match(code)

    def execute(self, code: str, remark: list) -> tuple:
        matches = self._pattern.search(code).groups()
        if matches[2] is None:
            remark.append(_('Remark.Hourly.Temperature').format(convert_temperature_remarks(matches[0], matches[1])))
        else:
            remark.append(_('Remark.Hourly.Temperature.Dew.Point').format(
                convert_temperature_remarks(matches[0], matches[1]),
                convert_temperature_remarks(matches[3], matches[4])
            ))
        return self._pattern.sub('', code, 1), remark


class IceAccretionCommand(Command):
    regex = r'^l(\d)(\d{3})\b'

    def __init__(self):
        self._pattern = re.compile(IceAccretionCommand.regex)

    def can_parse(self, code: str) -> any:
        return self._pattern.match(code)

    def execute(self, code: str, remark: list) -> tuple:
        matches = self._pattern.search(code).groups()
        remark.append(_('Remark.Ice.Accretion.Amount').format(int(matches[1]), int(matches[0])))
        return self._pattern.sub('', code, 1), remark


class ObscurationCommand(Command):
    regex = r'^([A-Z]{2}) ([A-Z]{3})(\d{3})'

    def __init__(self):
        self._pattern = re.compile(ObscurationCommand.regex)

    def execute(self, code: str, remark: list) -> tuple:
        matches = self._pattern.search(code).groups()
        layer = _(CLOUD_QUANTITY + matches[1])
        height = 100 * int(matches[2])
        detail = _(PHENOMENON + matches[0])
        remark.append(_('Remark.Obscuration').format(layer, height, detail))
        return self._pattern.sub('', code, 1), remark

    def can_parse(self, code: str) -> any:
        return self._pattern.match(code)


class PrecipitationAmount24HourCommand(Command):
    regex = r'^7(\d{4})\b'

    def __init__(self):
        self._pattern = re.compile(PrecipitationAmount24HourCommand.regex)

    def can_parse(self, code: str) -> any:
        return self._pattern.match(code)

    def execute(self, code: str, remark: list) -> tuple:
        matches = self._pattern.search(code).groups()
        remark.append(_('Remark.Precipitation.Amount.24').format(convert_precipitation_amount(matches[0])))
        return self._pattern.sub('', code, 1), remark


class PrecipitationAmount36HourCommand(Command):
    regex = r'^([36])(\d{4})\b'

    def __init__(self):
        self._pattern = re.compile(PrecipitationAmount36HourCommand.regex)

    def can_parse(self, code: str) -> any:
        return self._pattern.match(code)

    def execute(self, code: str, remark: list) -> tuple:
        matches = self._pattern.search(code).groups()
        remark.append(_('Remark.Precipitation.Amount.3.6').
                      format(matches[0], convert_precipitation_amount(matches[1])))
        return self._pattern.sub('', code, 1), remark


class PrecipitationBegCommand(Command):
    regex = r'^(([A-Z]{2})?([A-Z]{2})B(\d{2})?(\d{2}))'

    def __init__(self) -> None:
        super().__init__()
        self._pattern = re.compile(PrecipitationBegCommand.regex)

    def execute(self, code: str, remark: list) -> tuple:
        matches = self._pattern.search(code).groups()
        remark.append(_('Remark.Precipitation.Beg').format(
            '' if matches[1] is None else _(DESCRIPTIVE + matches[1]),
            _(PHENOMENON + matches[2]),
            empty_if_none(matches[3]),
            matches[4]
        ))
        return self._pattern.sub('', code, 1), remark

    def can_parse(self, code: str) -> any:
        return self._pattern.match(code)


class PrecipitationBegEndCommand(Command):
    regex = r'^(([A-Z]{2})?([A-Z]{2})B(\d{2})?(\d{2})E(\d{2})?(\d{2}))'

    def __init__(self):
        self._pattern = re.compile(PrecipitationBegEndCommand.regex)

    def execute(self, code: str, remark: list) -> tuple:
        matches = self._pattern.search(code).groups()
        remark.append(_('Remark.Precipitation.Beg.End').format(
            '' if matches[1] is None else _(DESCRIPTIVE + matches[1]),
            _(PHENOMENON + matches[2]),
            empty_if_none(matches[3]),
            matches[4],
            empty_if_none(matches[5]),
            matches[6]
        ))
        return self._pattern.sub('', code, 1), remark

    def can_parse(self, code: str) -> any:
        return self._pattern.match(code)


class PrecipitationEndCommand(Command):
    regex = r'^(([A-Z]{2})?([A-Z]{2})E(\d{2})?(\d{2}))'

    def __init__(self):
        self._pattern = re.compile(PrecipitationEndCommand.regex)

    def can_parse(self, code: str) -> any:
        return self._pattern.match(code)

    def execute(self, code: str, remark: list) -> tuple:
        matches = self._pattern.search(code).groups()
        remark.append(_('Remark.Precipitation.End').format(
            '' if matches[1] is None else _(DESCRIPTIVE + matches[1]),
            _(PHENOMENON + matches[2]),
            empty_if_none(matches[3]),
            matches[4]
        ))
        return self._pattern.sub('', code, 1), remark


class PrevailingVisibilityCommand(Command):
    regex = r'^VIS ((\d)*( )?(\d?/?\d))V((\d)*( )?(\d?/?\d))'

    def __init__(self):
        self._pattern = re.compile(PrevailingVisibilityCommand.regex)

    def execute(self, code: str, remark: list) -> tuple:
        matches = self._pattern.search(code).groups()
        remark.append(_('Remark.Variable.Prevailing.Visibility').format(
            matches[0], matches[4])
        )
        return self._pattern.sub('', code, 1), remark

    def can_parse(self, code: str) -> any:
        return self._pattern.match(code)


class SeaLevelPressureCommand(Command):
    regex = r'^SLP(\d{2})(\d)'

    def __init__(self):
        self._pattern = re.compile(SeaLevelPressureCommand.regex)

    def execute(self, code: str, remark: list) -> tuple:
        matches = self._pattern.search(code).groups()
        pressure = '9' if matches[0].startswith('9') else '10'
        pressure += matches[0] + '.' + matches[1]
        remark.append(_('Remark.Sea.Level.Pressure').format(pressure))
        return self._pattern.sub('', code, 1), remark

    def can_parse(self, code: str) -> any:
        return self._pattern.match(code)


class SecondLocationVisibilityCommand(Command):
    regex = r'^VIS ((\d)*( )?(\d?/?\d)) (\w+)'

    def __init__(self):
        self._pattern = re.compile(SecondLocationVisibilityCommand.regex)

    def execute(self, code: str, remark: list) -> tuple:
        matches = self._pattern.search(code).groups()
        remark.append(_('Remark.Second.Location.Visibility').format(
            matches[0], matches[4])
        )
        return self._pattern.sub('', code, 1), remark

    def can_parse(self, code: str) -> any:
        return self._pattern.match(code)


class SectorVisibilityCommand(Command):
    regex = r'^VIS ([A-Z]{1,2}) ((\d)*( )?(\d?/?\d))'

    def __init__(self):
        self._pattern = re.compile(SectorVisibilityCommand.regex)

    def execute(self, code: str, remark: list) -> tuple:
        matches = self._pattern.search(code).groups()
        remark.append(_('Remark.Sector.Visibility').format(
            _(CONVERTER + matches[0]),
            matches[1]
        ))
        return self._pattern.sub('', code, 1), remark

    def can_parse(self, code: str) -> any:
        return self._pattern.match(code)


class SmallHailSizeCommand(Command):
    regex = r'^GR LESS THAN ((\d )?(\d/\d)?)'

    def __init__(self):
        self._pattern = re.compile(SmallHailSizeCommand.regex)

    def execute(self, code: str, remark: list) -> tuple:
        matches = self._pattern.search(code).groups()
        remark.append(_('Remark.Hail.LesserThan').format(matches[0]))
        return self._pattern.sub('', code, 1), remark

    def can_parse(self, code: str) -> any:
        return self._pattern.match(code)


class SnowDepthCommand(Command):
    regex = r'^4/(\d{3})'

    def __init__(self):
        self._pattern = re.compile(SnowDepthCommand.regex)

    def can_parse(self, code: str) -> any:
        return self._pattern.match(code)

    def execute(self, code: str, remark: list) -> tuple:
        matches = self._pattern.search(code).groups()
        remark.append(_('Remark.Snow.Depth').format(int(matches[0])))
        return self._pattern.sub('', code, 1), remark


class SnowIncreaseCommand(Command):
    regex = r'^SNINCR (\d+)/(\d+)'

    def __init__(self):
        self._pattern = re.compile(SnowIncreaseCommand.regex)

    def execute(self, code: str, remark: list) -> tuple:
        matches = self._pattern.search(code).groups()
        remark.append(_('Remark.Snow.Increasing.Rapidly').format(matches[0], matches[1]))
        return self._pattern.sub('', code, 1), remark

    def can_parse(self, code: str) -> any:
        return self._pattern.match(code)


class SnowPelletsCommand(Command):
    regex = r'^GS (LGT|MOD|HVY)'

    def __init__(self):
        self._pattern = re.compile(SnowPelletsCommand.regex)

    def execute(self, code: str, remark: list) -> tuple:
        matches = self._pattern.search(code).groups()
        remark.append(_('Remark.Snow.Pellets').format(_(REMARK + matches[0])))
        return self._pattern.sub('', code, 1), remark

    def can_parse(self, code: str) -> any:
        return self._pattern.match(code)


class SunshineDurationCommand(Command):
    regex = r'^98(\d{3})'

    def __init__(self):
        self._pattern = re.compile(SunshineDurationCommand.regex)

    def execute(self, code: str, remark: list) -> tuple:
        matches = self._pattern.search(code).groups()
        remark.append(_('Remark.Sunshine.Duration').format(int(matches[0])))
        return self._pattern.sub('', code, 1), remark

    def can_parse(self, code: str) -> any:
        return self._pattern.match(code)


class SurfaceVisibilityCommand(Command):
    regex = r'^SFC VIS ((\d)*( )?(\d?/?\d))'

    def __init__(self):
        self._pattern = re.compile(SurfaceVisibilityCommand.regex)

    def execute(self, code: str, remark: list) -> tuple:
        matches = self._pattern.search(code).groups()
        remark.append(_('Remark.Surface.Visibility').format(matches[0]))
        return self._pattern.sub('', code, 1), remark

    def can_parse(self, code: str) -> any:
        return self._pattern.match(code)


class ThunderStormLocationCommand(Command):
    regex = r'^TS ([A-Z]{2})'

    def __init__(self):
        self._pattern = re.compile(ThunderStormLocationCommand.regex)

    def execute(self, code: str, remark: list) -> tuple:
        matches = self._pattern.search(code).groups()
        remark.append(_('Remark.Thunderstorm.Location').format(_(CONVERTER + matches[0])))
        return self._pattern.sub('', code, 1), remark

    def can_parse(self, code: str) -> any:
        return self._pattern.match(code)


class ThunderStormLocationMovingCommand(Command):
    regex = r'^TS ([A-Z]{2}) MOV ([A-Z]{2})'

    def __init__(self):
        self._pattern = re.compile(ThunderStormLocationMovingCommand.regex)

    def execute(self, code: str, remark: list) -> tuple:
        matches = self._pattern.search(code).groups()
        remark.append(_('Remark.Thunderstorm.Location.Moving').format(
            _(CONVERTER + matches[0]), _(CONVERTER + matches[1])
        ))
        return self._pattern.sub('', code, 1), remark

    def can_parse(self, code: str) -> any:
        return self._pattern.match(code)


class TornadicActivityBegCommand(Command):
    regex = '^(TORNADO|FUNNEL CLOUD|WATERSPOUT) (B(\d{2})?(\d{2}))( (\d+)? ([A-Z]{1,2})?)?'

    def __init__(self):
        self._pattern = re.compile(TornadicActivityBegCommand.regex)

    def execute(self, code: str, remark: list) -> tuple:
        matches = self._pattern.search(code).groups()
        remark.append(_('Remark.Tornadic.Activity.Beginning').format(
            _(REMARK + matches[0].replace(' ', '')),
            empty_if_none(matches[2]),
            matches[3],
            matches[5],
            _(CONVERTER + matches[6])
        ))
        return self._pattern.sub('', code, 1), remark

    def can_parse(self, code: str) -> any:
        return self._pattern.match(code)


class TornadicActivityBegEndCommand(Command):
    regex = r'^(TORNADO|FUNNEL CLOUD|WATERSPOUT) (B(\d{2})?(\d{2}))(E(\d{2})?(\d{2}))( (\d+)? ([A-Z]{1,2})?)?'

    def __init__(self):
        self._pattern = re.compile(TornadicActivityBegEndCommand.regex)

    def execute(self, code: str, remark: list) -> tuple:
        matches = self._pattern.search(code).groups()
        remark.append(_('Remark.Tornadic.Activity.BegEnd').format(
            _(REMARK + matches[0].replace(' ', '')),
            empty_if_none(matches[2]),
            matches[3],
            empty_if_none(matches[5]),
            matches[6],
            matches[8],
            _(CONVERTER + matches[9])
        ))
        return self._pattern.sub('', code, 1), remark

    def can_parse(self, code: str) -> any:
        return self._pattern.match(code)


class TornadicActivityEndCommand(Command):
    regex = r'^(TORNADO|FUNNEL CLOUD|WATERSPOUT) (E(\d{2})?(\d{2}))( (\d+)? ([A-Z]{1,2})?)?'

    def __init__(self):
        self._pattern = re.compile(TornadicActivityEndCommand.regex)

    def execute(self, code: str, remark: list) -> tuple:
        matches = self._pattern.search(code).groups()
        remark.append(_('Remark.Tornadic.Activity.Ending').format(
            _(REMARK + matches[0].replace(' ', '')),
            empty_if_none(matches[2]),
            matches[3],
            matches[5],
            _(CONVERTER + matches[6])
        ))
        return self._pattern.sub('', code, 1), remark

    def can_parse(self, code: str) -> any:
        return self._pattern.match(code)


class TowerVisibilityCommand(Command):
    regex = r'^TWR VIS ((\d)*( )?(\d?/?\d))'

    def __init__(self):
        self._pattern = re.compile(TowerVisibilityCommand.regex)

    def execute(self, code: str, remark: list) -> tuple:
        matches = self._pattern.search(code).groups()
        remark.append(_('Remark.Tower.Visibility').format(matches[0]))
        return self._pattern.sub('', code, 1), remark

    def can_parse(self, code: str) -> any:
        return self._pattern.match(code)


class VariableSkyCommand(Command):
    regex = r'^([A-Z]{3}) V ([A-Z]{3})'

    def __init__(self):
        self._pattern = re.compile(VariableSkyCommand.regex)

    def execute(self, code: str, remark: list) -> tuple:
        matches = self._pattern.search(code).groups()
        remark.append(_('Remark.Variable.Sky.Condition').format(
            _(CLOUD_QUANTITY + matches[0]),
            _(CLOUD_QUANTITY + matches[1])
        ))
        return self._pattern.sub('', code, 1), remark

    def can_parse(self, code: str) -> any:
        return self._pattern.match(code)


class VariableSkyHeightCommand(Command):
    regex = r'^([A-Z]{3})(\d{3}) V ([A-Z]{3})'

    def __init__(self):
        self._pattern = re.compile(VariableSkyHeightCommand.regex)

    def execute(self, code: str, remark: list) -> tuple:
        matches = self._pattern.search(code).groups()
        remark.append(_('Remark.Variable.Sky.Condition.Height').format(
            100 * int(matches[1]),
            _(CLOUD_QUANTITY + matches[0]),
            _(CLOUD_QUANTITY + matches[2])
        ))
        return self._pattern.sub('', code, 1), remark

    def can_parse(self, code: str) -> any:
        return self._pattern.match(code)


class VirgaDirectionCommand(Command):
    regex = r'^VIRGA ([A-Z]{2})'

    def __init__(self):
        self._pattern = re.compile(VirgaDirectionCommand.regex)

    def execute(self, code: str, remark: list) -> tuple:
        match = self._pattern.search(code).groups()
        remark.append(_('Remark.Virga.Direction').format(_(CONVERTER + match[0])))
        return self._pattern.sub('', code, 1), remark

    def can_parse(self, code: str) -> any:
        return self._pattern.match(code)


class WaterEquivalentSnowCommand(Command):
    regex = r'^933(\d{3})\b'

    def __init__(self):
        self._pattern = re.compile(WaterEquivalentSnowCommand.regex)

    def can_parse(self, code: str) -> any:
        return self._pattern.match(code)

    def execute(self, code: str, remark: list) -> tuple:
        matches = self._pattern.search(code).groups()
        remark.append(_('Remark.Water.Equivalent.Snow.Ground').format(
            float(matches[0]) / 10
        ))
        return self._pattern.sub('', code, 1), remark


class WindPeakCommand(Command):
    regex = r'^PK WND (\d{3})(\d{2,3})/(\d{2})?(\d{2})'

    def __init__(self):
        self._pattern = re.compile(WindPeakCommand.regex)

    def execute(self, code: str, remark: list) -> tuple:
        matches = self._pattern.search(code).groups()
        remark.append(_('Remark.PeakWind').format(
            matches[0],
            matches[1],
            empty_if_none(matches[2]),
            matches[3]
        ))
        return self._pattern.sub('', code, 1), remark

    def can_parse(self, code: str) -> any:
        return self._pattern.match(code)


class WindShiftCommand(Command):
    regex = r'^WSHFT (\d{2})?(\d{2})'

    def __init__(self):
        self._pattern = re.compile(WindShiftCommand.regex)

    def execute(self, code: str, remark: list) -> tuple:
        matches = self._pattern.search(code).groups()
        remark.append(_('Remark.WindShift').format(
            empty_if_none(matches[0]),
            matches[1]
        ))
        return self._pattern.sub('', code, 1), remark

    def can_parse(self, code: str) -> any:
        return self._pattern.match(code)


class WindShiftFropaCommand(Command):
    regex = r'^WSHFT (\d{2})?(\d{2}) FROPA'

    def __init__(self):
        self._pattern = re.compile(WindShiftFropaCommand.regex)

    def execute(self, code: str, remark: list) -> tuple:
        matches = self._pattern.search(code).groups()
        remark.append(_('Remark.WindShift.FROPA').format(
            empty_if_none(matches[0]),
            matches[1]
        ))
        return self._pattern.sub('', code, 1), remark

    def can_parse(self, code: str) -> any:
        return self._pattern.match(code)


class DefaultCommand(Command):
    def can_parse(self, code: str) -> any:
        return True

    def execute(self, code: str, remark: list) -> tuple:
        rmk_split = code.split(' ', 1)
        try:
            rem = _(REMARK + rmk_split[0])
            remark.append(rem)
        except TranslationError:
            remark.append(rmk_split[0])
        return '' if len(rmk_split) == 1 else rmk_split[1], remark


class RemarkCommandSupplier:

    def __init__(self):
        self.default_command = DefaultCommand()
        self._command_list = [WindPeakCommand(),
                              WindShiftFropaCommand(),
                              WindShiftCommand(),
                              TowerVisibilityCommand(),
                              SurfaceVisibilityCommand(),
                              PrevailingVisibilityCommand(),
                              SecondLocationVisibilityCommand(),
                              SectorVisibilityCommand(),
                              TornadicActivityBegEndCommand(),
                              TornadicActivityBegCommand(),
                              TornadicActivityEndCommand(),
                              PrecipitationBegEndCommand(),
                              PrecipitationBegCommand(),
                              PrecipitationEndCommand(),
                              ThunderStormLocationMovingCommand(),
                              ThunderStormLocationCommand(),
                              SmallHailSizeCommand(),
                              HailSizeCommand(),
                              SnowPelletsCommand(),
                              VirgaDirectionCommand(),
                              CeilingHeightCommand(),
                              ObscurationCommand(),
                              VariableSkyHeightCommand(),
                              VariableSkyCommand(),
                              CeilingSecondLocationCommand(),
                              SeaLevelPressureCommand(),
                              SnowIncreaseCommand(),
                              HourlyMaximumMinimumTemperatureCommand(),
                              HourlyMaximumTemperatureCommand(),
                              HourlyMinimumTemperatureCommand(),
                              HourlyPrecipitationAmountCommand(),
                              HourlyTemperatureDewPointCommand(),
                              HourlyPressureCommand(),
                              IceAccretionCommand(),
                              PrecipitationAmount36HourCommand(),
                              PrecipitationAmount24HourCommand(),
                              SnowDepthCommand(),
                              SunshineDurationCommand(),
                              WaterEquivalentSnowCommand()
                              ]

    def get(self, code: str) -> Command:
        for command in self._command_list:
            if command.can_parse(code):
                return command
        return self.default_command
