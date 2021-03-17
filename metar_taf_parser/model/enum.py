import enum

from metar_taf_parser.commons.i18n import _


class CloudQuantity(enum.Enum):
    SKC = 'SKC'   # Sky clear
    FEW = 'FEW'   # Few
    BKN = 'BKN'  # Broken
    SCT = 'SCT'  # Scattered
    OVC = 'OVC'  # Overcast
    NSC = 'NSC'  # No significant cloud

    def __str__(self):
        return _('CloudQuantity.' + self.value)


class CloudType(enum.Enum):
    CB = 'CB'  # Cumulonimbus
    TCU = 'TCU'  # Towering cumulus, cumulus congestus
    CI = 'CI'  # Cirrus
    CC = 'CC'  # Cirrocumulus
    CS = 'CS'  # Cirrostratus
    AC = 'AC'  # Altocumulus
    ST = 'ST'  # Stratus
    CU = 'CU'  # Cumulus
    AS = 'AS'  # Astrostratus
    NS = 'NS'  # Nimbostratus
    SC = 'SC'  # Stratocumulus

    def __str__(self):
        return _('CloudType.' + self.value)


class Intensity(enum.Enum):
    LIGHT = '-'
    HEAVY = '+'
    IN_VICINITY = 'VC'

    def __str__(self):
        return _('Intensity.' + self.value)


class Descriptive(enum.Enum):
    SHOWERS = 'SH'
    SHALLOW = 'MI'
    PATCHES = 'BC'
    PARTIAL = 'PR'
    DRIFTING = 'DR'
    THUNDERSTORM = 'TS'
    BLOWING = 'BL'
    FREEZING = 'FZ'

    def __str__(self):
        return _('Descriptive.' + self.value)


class Phenomenon(enum.Enum):
    RAIN = 'RA'
    DRIZZLE = 'DZ'
    SNOW = 'SN'
    SNOW_GRAINS = 'SG'
    ICE_PELLETS = 'PL'
    ICE_CRYSTALS = 'IC'
    HAIL = 'GR'
    SMALL_HAIL = 'GS'
    UNKNOW_PRECIPITATION = 'UP'
    FOG = 'FG'
    VOLCANIC_ASH = 'VA'
    MIST = 'BR'
    HAZE = 'HZ'
    WIDESPREAD_DUST = 'DU'
    SMOKE = 'FU'
    SAND = 'SA'
    SPRAY = 'PY'
    SQUALL = 'SQ'
    SAND_WHIRLS = 'PO'
    DUSTSTORM = 'DS'
    SANDSTORM = 'SS'
    FUNNEL_CLOUD = 'FC'

    def __str__(self):
        return _('Phenomenon.' + self.value)


class TimeIndicator(enum.Enum):
    AT = 'AT'
    FM = 'FM'
    TL = 'TL'

    def __str__(self):
        return _('TimeIndicator.' + self.value)


class WeatherChangeType(enum.Enum):
    FM = 'FM'
    BECMG = 'BECMG'
    TEMPO = 'TEMPO'
    PROB = 'PROB'

    def __str__(self):
        return _('WeatherChangeType.' + self.value)
