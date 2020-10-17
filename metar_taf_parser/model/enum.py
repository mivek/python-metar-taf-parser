import enum


class CloudQuantity(enum.Enum):
    SKC = 'SKC'   # Sky clear
    FEW = 'FEW'   # Few
    BKN = 'BKN'  # Broken
    SCT = 'SCT'  # Scattered
    OVC = 'OVC'  # Overcast
    NSC = 'NSC'  # No significant cloud


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


class Intensity(enum.Enum):
    LIGHT = '-'
    HEAVY = '+'
    IN_VICINITY = 'VC'


class Descriptive(enum.Enum):
    SHOWERS = 'SH'
    SHALLOW = 'MI'
    PATCHES = 'BC'
    PARTIAL = 'PR'
    DRIFTING = 'DR'
    THUNDERSTORM = 'TS'
    BLOWING = 'BL'
    FREEZING = 'FZ'


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


class TimeIndicator(enum.Enum):
    AT = 'AT'
    FM = 'FM'
    TL = 'TL'


class WeatherChangeType(enum.Enum):
    FM = 'FM'
    BECMG = 'BECMG'
    TEMPO = 'TEMPO'
    PROB = 'PROB'
