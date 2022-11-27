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


class Flag(enum.Enum):
    AMD = 'AMD'
    AUTO = 'AUTO'
    CNL = 'CNL'
    COR = 'COR'
    NIL = 'NIL'

    def __str__(self):
        return _('Flag.' + self.value)


class IcingIntensity(enum.Enum):
    NONE = '0'
    LIGHT = '1'
    LIGHT_RIME_ICING_CLOUD = '2'
    LIGHT_CLEAR_ICING_PRECIPITATION = '3'
    MODERATE_MIXED_ICING = '4'
    MODERATE_RIME_ICING_CLOUD = '5'
    MODERATE_CLEAR_ICING_PRECIPITATION = '6'
    SEVERE_MIXED_ICING = '7'
    SEVERE_RIME_ICING_CLOUD = '8'
    SEVERE_CLEAR_ICING_PRECIPITATION = '9'
    
    def __str__(self) -> str:
        return _('IcingIntensity.' + self.value)


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


class TurbulenceIntensity(enum.Enum):
    NONE = '0'
    LIGHT = '1'
    MODERATE_CLEAR_AIR_OCCASIONAL = '2'
    MODERATE_CLEAR_AIR_FREQUENT = '3'
    MODERATE_CLOUD_OCCASIONAL = '4'
    MODERATE_CLOUD_FREQUENT = '5'
    SEVERE_CLEAR_AIR_OCCASIONAL = '6'
    SEVERE_CLEAR_AIR_FREQUENT = '7'
    SEVERE_CLOUD_OCCASIONAL = '8'
    SEVERE_CLOUD_FREQUENT = '9'
    EXTREME = 'X'

    def __str__(self) -> str:
        return _('TurbuleneIntensity.' + self.value)

class WeatherChangeType(enum.Enum):
    FM = 'FM'
    BECMG = 'BECMG'
    TEMPO = 'TEMPO'
    PROB = 'PROB'
    INTER = 'INTER'

    def __str__(self):
        return _('WeatherChangeType.' + self.value)
