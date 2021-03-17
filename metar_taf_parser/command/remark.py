import re
import abc

from metar_taf_parser.commons.exception import TranslationError
from metar_taf_parser.commons.i18n import _


def empty_if_none(code: str) -> str:
    return '' if code is None else code


class Command(abc.ABC):

    @abc.abstractmethod
    def execute(self, code: str, remark: [str]) -> (str, [str]):
        pass

    @abc.abstractmethod
    def can_parse(self, code: str) -> any:
        pass


class CeilingHeightCommand(Command):
    regex = r'^CIG (\d{3})V(\d{3})'

    def __init__(self):
        self._pattern = re.compile(CeilingHeightCommand.regex)

    def can_parse(self, code: str) -> any:
        return self._pattern.match(code)

    def execute(self, code: str, remark: [str]) -> (str, [str]):
        matches = self._pattern.search(code).groups()
        min_ceiling = int(matches[0]) * 100
        max_ceiling = int(matches[1]) * 100
        remark.append(_("Remark.Ceiling.Height").format(min_ceiling, max_ceiling))
        return self._pattern.sub('', code, 1), remark


class CeilingSecondLocationCommand(Command):
    regex = r'^CIG (\d{3}) (\w+)'

    def __init__(self):
        self._pattern = re.compile(CeilingSecondLocationCommand.regex)

    def can_parse(self, code: str) -> any:
        return self._pattern.match(code)

    def execute(self, code: str, remark: [str]) -> (str, [str]):
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

    def execute(self, code: str, remark: [str]) -> (str, [str]):
        matches = self._pattern.search(code).groups()
        remark.append(_('Remark.Hail').format(matches[0]))
        return self._pattern.sub('', code, 1), remark


class ObscurationCommand(Command):
    regex = r'^([A-Z]{2}) ([A-Z]{3})(\d{3})'

    def __init__(self):
        self._pattern = re.compile(ObscurationCommand.regex)

    def execute(self, code: str, remark: [str]) -> (str, [str]):
        matches = self._pattern.search(code).groups()
        layer = _('CloudQuantity.' + matches[1])
        height = 100 * int(matches[2])
        detail = _('Phenomenon.' + matches[0])
        remark.append(_('Remark.Obscuration').format(layer, height, detail))
        return self._pattern.sub('', code, 1), remark

    def can_parse(self, code: str) -> any:
        return self._pattern.match(code)


class PrecipitationBegEndCommand(Command):
    regex = r'^(([A-Z]{2})?([A-Z]{2})B(\d{2})?(\d{2})E(\d{2})?(\d{2}))'

    def __init__(self):
        self._pattern = re.compile(PrecipitationBegEndCommand.regex)

    def execute(self, code: str, remark: [str]) -> (str, [str]):
        matches = self._pattern.search(code).groups()
        remark.append(_('Remark.Precipitation.Beg.End').format(
            '' if matches[1] is None else _('Descriptive.' + matches[1]),
            _('Phenomenon.' + matches[2]),
            empty_if_none(matches[3]),
            matches[4],
            empty_if_none(matches[5]),
            matches[6]
        ))
        return self._pattern.sub('', code, 1), remark

    def can_parse(self, code: str) -> any:
        return self._pattern.match(code)


class PrevailingVisibilityCommand(Command):
    regex = r'^VIS ((\d)*( )?(\d?/?\d))V((\d)*( )?(\d?/?\d))'

    def __init__(self):
        self._pattern = re.compile(PrevailingVisibilityCommand.regex)

    def execute(self, code: str, remark: [str]) -> (str, [str]):
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

    def execute(self, code: str, remark: [str]) -> (str, [str]):
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

    def execute(self, code: str, remark: [str]) -> (str, [str]):
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

    def execute(self, code: str, remark: [str]) -> (str, [str]):
        matches = self._pattern.search(code).groups()
        remark.append(_('Remark.Sector.Visibility').format(
            _('Converter.' + matches[0]),
            matches[1]
        ))
        return self._pattern.sub('', code, 1), remark

    def can_parse(self, code: str) -> any:
        return self._pattern.match(code)


class SmallHailSizeCommand(Command):
    regex = r'^GR LESS THAN ((\d )?(\d/\d)?)'

    def __init__(self):
        self._pattern = re.compile(SmallHailSizeCommand.regex)

    def execute(self, code: str, remark: [str]) -> (str, [str]):
        matches = self._pattern.search(code).groups()
        remark.append(_('Remark.Hail.LesserThan').format(matches[0]))
        return self._pattern.sub('', code, 1), remark

    def can_parse(self, code: str) -> any:
        return self._pattern.match(code)


class SnowIncreaseCommand(Command):
    regex = r'^SNINCR (\d+)/(\d+)'

    def __init__(self):
        self._pattern = re.compile(SnowIncreaseCommand.regex)

    def execute(self, code: str, remark: [str]) -> (str, [str]):
        matches = self._pattern.search(code).groups()
        remark.append(_('Remark.Snow.Increasing.Rapidly').format(matches[0], matches[1]))
        return self._pattern.sub('', code, 1), remark

    def can_parse(self, code: str) -> any:
        return self._pattern.match(code)


class SnowPelletsCommand(Command):
    regex = r'^GS (LGT|MOD|HVY)'

    def __init__(self):
        self._pattern = re.compile(SnowPelletsCommand.regex)

    def execute(self, code: str, remark: [str]) -> (str, [str]):
        matches = self._pattern.search(code).groups()
        remark.append(_('Remark.Snow.Pellets').format(_('Remark.' + matches[0])))
        return self._pattern.sub('', code, 1), remark

    def can_parse(self, code: str) -> any:
        return self._pattern.match(code)


class SurfaceVisibilityCommand(Command):
    regex = r'^SFC VIS ((\d)*( )?(\d?/?\d))'

    def __init__(self):
        self._pattern = re.compile(SurfaceVisibilityCommand.regex)

    def execute(self, code: str, remark: [str]) -> (str, [str]):
        matches = self._pattern.search(code).groups()
        remark.append(_('Remark.Surface.Visibility').format(matches[0]))
        return self._pattern.sub('', code, 1), remark

    def can_parse(self, code: str) -> any:
        return self._pattern.match(code)


class ThunderStormLocationCommand(Command):
    regex = r'^TS ([A-Z]{2})'

    def __init__(self):
        self._pattern = re.compile(ThunderStormLocationCommand.regex)

    def execute(self, code: str, remark: [str]) -> (str, [str]):
        matches = self._pattern.search(code).groups()
        remark.append(_('Remark.Thunderstorm.Location').format(_('Converter.' + matches[0])))
        return self._pattern.sub('', code, 1), remark

    def can_parse(self, code: str) -> any:
        return self._pattern.match(code)


class ThunderStormLocationMovingCommand(Command):
    regex = r'^TS ([A-Z]{2}) MOV ([A-Z]{2})'

    def __init__(self):
        self._pattern = re.compile(ThunderStormLocationMovingCommand.regex)

    def execute(self, code: str, remark: [str]) -> (str, [str]):
        matches = self._pattern.search(code).groups()
        remark.append(_('Remark.Thunderstorm.Location.Moving').format(
            _('Converter.' + matches[0]), _('Converter.' + matches[1])
        ))
        return self._pattern.sub('', code, 1), remark

    def can_parse(self, code: str) -> any:
        return self._pattern.match(code)


class TornadicActivityBegCommand(Command):
    regex = '^(TORNADO|FUNNEL CLOUD|WATERSPOUT) (B(\d{2})?(\d{2}))( (\d+)? ([A-Z]{1,2})?)?'

    def __init__(self):
        self._pattern = re.compile(TornadicActivityBegCommand.regex)

    def execute(self, code: str, remark: [str]) -> (str, [str]):
        matches = self._pattern.search(code).groups()
        remark.append(_('Remark.Tornadic.Activity.Beginning').format(
            _('Remark.' + matches[0].replace(' ', '')),
            empty_if_none(matches[2]),
            matches[3],
            matches[5],
            _('Converter.' + matches[6])
        ))
        return self._pattern.sub('', code, 1), remark

    def can_parse(self, code: str) -> any:
        return self._pattern.match(code)


class TornadicActivityBegEndCommand(Command):
    regex = r'^(TORNADO|FUNNEL CLOUD|WATERSPOUT) (B(\d{2})?(\d{2}))(E(\d{2})?(\d{2}))( (\d+)? ([A-Z]{1,2})?)?'

    def __init__(self):
        self._pattern = re.compile(TornadicActivityBegEndCommand.regex)

    def execute(self, code: str, remark: [str]) -> (str, [str]):
        matches = self._pattern.search(code).groups()
        remark.append(_('Remark.Tornadic.Activity.BegEnd').format(
            _('Remark.' + matches[0].replace(' ', '')),
            empty_if_none(matches[2]),
            matches[3],
            empty_if_none(matches[5]),
            matches[6],
            matches[8],
            _('Converter.' + matches[9])
        ))
        return self._pattern.sub('', code, 1), remark

    def can_parse(self, code: str) -> any:
        return self._pattern.match(code)


class TornadicActivityEndCommand(Command):
    regex = r'^(TORNADO|FUNNEL CLOUD|WATERSPOUT) (E(\d{2})?(\d{2}))( (\d+)? ([A-Z]{1,2})?)?'

    def __init__(self):
        self._pattern = re.compile(TornadicActivityEndCommand.regex)

    def execute(self, code: str, remark: [str]) -> (str, [str]):
        matches = self._pattern.search(code).groups()
        remark.append(_('Remark.Tornadic.Activity.Ending').format(
            _('Remark.' + matches[0].replace(' ', '')),
            empty_if_none(matches[2]),
            matches[3],
            matches[5],
            _('Converter.' + matches[6])
        ))
        return self._pattern.sub('', code, 1), remark

    def can_parse(self, code: str) -> any:
        return self._pattern.match(code)


class TowerVisibilityCommand(Command):
    regex = r'^TWR VIS ((\d)*( )?(\d?/?\d))'

    def __init__(self):
        self._pattern = re.compile(TowerVisibilityCommand.regex)

    def execute(self, code: str, remark: [str]) -> (str, [str]):
        matches = self._pattern.search(code).groups()
        remark.append(_('Remark.Tower.Visibility').format(matches[0]))
        return self._pattern.sub('', code, 1), remark

    def can_parse(self, code: str) -> any:
        return self._pattern.match(code)


class VariableSkyCommand(Command):
    regex = r'^([A-Z]{3}) V ([A-Z]{3})'

    def __init__(self):
        self._pattern = re.compile(VariableSkyCommand.regex)

    def execute(self, code: str, remark: [str]) -> (str, [str]):
        matches = self._pattern.search(code).groups()
        remark.append(_('Remark.Variable.Sky.Condition').format(
            _('CloudQuantity.' + matches[0]),
            _('CloudQuantity.' + matches[1])
        ))
        return self._pattern.sub('', code, 1), remark

    def can_parse(self, code: str) -> any:
        return self._pattern.match(code)


class VariableSkyHeightCommand(Command):
    regex = r'^([A-Z]{3})(\d{3}) V ([A-Z]{3})'

    def __init__(self):
        self._pattern = re.compile(VariableSkyHeightCommand.regex)

    def execute(self, code: str, remark: [str]) -> (str, [str]):
        matches = self._pattern.search(code).groups()
        remark.append(_('Remark.Variable.Sky.Condition.Height').format(
            100 * int(matches[1]),
            _('CloudQuantity.' + matches[0]),
            _('CloudQuantity.' + matches[2])
        ))
        return self._pattern.sub('', code, 1), remark

    def can_parse(self, code: str) -> any:
        return self._pattern.match(code)


class VirgaDirectionCommand(Command):
    regex = r'^VIRGA ([A-Z]{2})'

    def __init__(self):
        self._pattern = re.compile(VirgaDirectionCommand.regex)

    def execute(self, code: str, remark: [str]) -> (str, [str]):
        match = self._pattern.search(code).groups()
        remark.append(_('Remark.Virga.Direction').format(_('Converter.' + match[0])))
        return self._pattern.sub('', code, 1), remark

    def can_parse(self, code: str) -> any:
        return self._pattern.match(code)


class WindPeakCommand(Command):
    regex = r'^PK WND (\d{3})(\d{2,3})/(\d{2})?(\d{2})'

    def __init__(self):
        self._pattern = re.compile(WindPeakCommand.regex)

    def execute(self, code: str, remark: [str]) -> (str, [str]):
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

    def execute(self, code: str, remark: [str]) -> (str, [str]):
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

    def execute(self, code: str, remark: [str]) -> (str, [str]):
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

    def execute(self, code: str, remark: [str]) -> (str, [str]):
        rmk_split = code.split(' ', 1)
        try:
            rem = _('Remark.' + rmk_split[0])
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
                              SnowIncreaseCommand()]

    def get(self, code: str) -> Command:
        for command in self._command_list:
            if command.can_parse(code):
                return command
        return self.default_command
