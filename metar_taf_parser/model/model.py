import abc
from datetime import time

from metar_taf_parser.model.enum import Descriptive, Flag, WeatherChangeType, TimeIndicator, IcingIntensity, TurbulenceIntensity


class Country:

    def __init__(self, name):
        self._name = name

    def _get_name(self):
        """ Return the name of the country """
        return self._name

    def _set_name(self, value):
        """ Setter for the name """
        self._name = value

    def __repr__(self):
        return f'Country[name={self.name}]'

    name = property(_get_name, _set_name)


class Wind:
    def __init__(self):
        self._speed = None
        self._direction = None
        self._degrees = None
        self._gust = None
        self._min_variation = None
        self._max_variation = None
        self._unit = None

    def _get_speed(self):
        return self._speed

    def _set_speed(self, value):
        self._speed = value

    def _get_direction(self):
        return self._direction

    def _set_direction(self, value):
        self._direction = value

    def _get_degrees(self):
        return self._degrees

    def _set_degrees(self, value):
        self._degrees = value

    def _get_gust(self):
        return self._gust

    def _set_gust(self, value):
        self._gust = value

    def _get_min_variation(self):
        return self._min_variation

    def _set_min_variation(self, value):
        self._min_variation = value

    def _get_max_variation(self):
        return self._max_variation

    def _set_max_variation(self, value):
        self._max_variation = value

    def _get_unit(self):
        return self._unit

    def _set_unit(self, value):
        self._unit = value

    def __repr__(self):
        return f'Wind[speed={self.speed}, direction={self.direction}, gust={self.gust}, degrees={self.degrees}, '\
            f'unit={self.unit}, min_variation={self.min_variation}, max_variation={self.max_variation}]'

    speed = property(_get_speed, _set_speed)
    direction = property(_get_direction, _set_direction)
    gust = property(_get_gust, _set_gust)
    degrees = property(_get_degrees, _set_degrees)
    unit = property(_get_unit, _set_unit)
    min_variation = property(_get_min_variation, _set_min_variation)
    max_variation = property(_get_max_variation, _set_max_variation)


class WindShear(Wind):
    def __init__(self):
        super().__init__()
        self._height = None

    def _get_height(self):
        return self._height

    def _set_height(self, value):
        self._height = value

    def __repr__(self):
        return f'WindShear[height={self.height}' + super().__repr__() + ']'

    height = property(_get_height, _set_height)


class Visibility:
    def __init__(self):
        self._distance = None
        self._min_distance = None
        self._min_direction = None

    def _get_distance(self):
        return self._distance

    def _set_distance(self, value):
        self._distance = value

    def _get_min_distance(self):
        return self._min_distance

    def _set_min_distance(self, value):
        self._min_distance = value

    def _get_min_direction(self):
        return self._min_direction

    def _set_min_direction(self, value):
        self._min_direction = value

    def __repr__(self):
        return f'Visibility[distance={self.distance}, min_distance={self.min_distance}, '\
            f'min_direction={self.min_direction}]'

    distance = property(_get_distance, _set_distance)
    min_distance = property(_get_min_distance, _set_min_distance)
    min_direction = property(_get_min_direction, _set_min_direction)


class WeatherCondition:
    def __init__(self):
        self._intensity = None
        self._descriptive = None
        self._phenomenons = []

    def _get_intensity(self):
        return self._intensity

    def _set_intensity(self, value):
        self._intensity = value

    def _get_descriptive(self):
        return self._descriptive

    def _set_descriptive(self, value):
        self._descriptive = value

    def _get_phenomenons(self):
        return self._phenomenons

    def add_phenomenon(self, phenomenon):
        self._phenomenons.append(phenomenon)

    def is_valid(self):
        return len(self._phenomenons) != 0 or self._descriptive == Descriptive.THUNDERSTORM

    def __repr__(self):
        return f'WeatherCondition[intensity={self.intensity}, descriptive={self.descriptive}, phenomenons={self.phenomenons}]'

    intensity = property(_get_intensity, _set_intensity)
    descriptive = property(_get_descriptive, _set_descriptive)
    phenomenons = property(_get_phenomenons)


class TemperatureDated:
    def __init__(self):
        self._temperature = None
        self._day = None
        self._hour = None

    def _get_temperature(self):
        return self._temperature

    def _set_temperature(self, value):
        self._temperature = value

    def _get_day(self):
        return self._day

    def _set_day(self, value):
        self._day = value

    def _get_hour(self):
        return self._hour

    def _set_hour(self, value):
        self._hour = value

    def __repr__(self):
        return f'TemperatureDated[temperature={self.temperature}, day={self.day}, hour={self.hour}]'

    temperature = property(_get_temperature, _set_temperature)
    day = property(_get_day, _set_day)
    hour = property(_get_hour, _set_hour)


class RunwayInfo:

    def __init__(self):
        self._name = None
        self._min_range = None
        self._max_range = None
        self._trend = None
        self._indicator = None
        self._deposit_type = None
        self._coverage = None
        self._thickness = None
        self._braking_capacity = None

    def _get_name(self):
        return self._name

    def _set_name(self, value):
        self._name = value

    def _get_min_range(self):
        return self._min_range

    def _set_min_range(self, value):
        self._min_range = value

    def _get_max_range(self):
        return self._max_range

    def _set_max_range(self, value):
        self._max_range = value

    def _get_trend(self):
        return self._trend

    def _set_trend(self, value):
        self._trend = value

    def _get_indicator(self):
        return self._indicator

    def _set_indicator(self, value: str):
        self._indicator = value

    def _get_deposit_type(self):
        return self._deposit_type

    def _set_deposit_type(self, value):
        self._deposit_type = value

    def _get_coverage(self):
        return self._coverage

    def _set_coverage(self, value):
        self._coverage = value

    def _get_thickness(self):
        return self._thickness

    def _set_thickness(self, value):
        self._thickness = value

    def _get_braking_capacity(self):
        return self._braking_capacity

    def _set_braking_capacity(self, value):
        self._braking_capacity = value

    def __repr__(self):
        return f'RunwayInfo[name={self.name}, min_range={self.min_range}, max_range={self.max_range}, '\
            f'trend={self.trend}, indicator={self.indicator}, deposit_type={self.deposit_type}, '\
            f'coverage={self.coverage}, thickness={self.thickness}, braking_capacity={self.braking_capacity}]'\

    name = property(_get_name, _set_name)
    min_range = property(_get_min_range, _set_min_range)
    max_range = property(_get_max_range, _set_max_range)
    trend = property(_get_trend, _set_trend)
    indicator = property(_get_indicator, _set_indicator)
    deposit_type = property(_get_deposit_type, _set_deposit_type)
    coverage = property(_get_coverage, _set_coverage)
    thickness = property(_get_thickness, _set_thickness)
    braking_capacity = property(_get_braking_capacity, _set_braking_capacity)


class Cloud:

    def __init__(self):
        self._height = None
        self._quantity = None
        self._type = None

    def _get_height(self):
        return self._height

    def _set_height(self, value):
        self._height = value

    def _get_quantity(self):
        return self._quantity

    def _set_quantity(self, value):
        self._quantity = value

    def _set_type(self, value):
        self._type = value

    def _get_type(self):
        return self._type

    def __repr__(self):
        return f'Cloud[height={self.height}, quantity={self.quantity}, type={self.type}]'

    height = property(_get_height, _set_height)
    quantity = property(_get_quantity, _set_quantity)
    type = property(_get_type, _set_type)


class Icing:
    def __init__(self):
        self._intensity: IcingIntensity = None
        self._base_height = 0
        self._depth = 0

    def _get_intensity(self):
        return self._intensity

    def _set_intensity(self, intensity: IcingIntensity):
        self._intensity = intensity

    def _get_base_height(self):
        return self._base_height

    def _set_base_height(self, base_height: int):
        self._base_height = base_height

    def _get_depth(self):
        return self._depth

    def _set_depth(self, depth: int):
        self._depth = depth

    def __repr__(self):
        return f'Icing[intensity={self.intensity}, base_height={self.base_height}, depth={self.depth}]'

    intensity = property(_get_intensity, _set_intensity)
    base_height = property(_get_base_height, _set_base_height)
    depth = property(_get_depth, _set_depth)


class Turbulence:

    def __init__(self):
        self._intensity: TurbulenceIntensity = None
        self._base_height = 0
        self._depth = 0

    def _get_intensity(self):
        return self._intensity

    def _set_intensity(self, intensity: TurbulenceIntensity):
        self._intensity = intensity

    def _get_base_height(self):
        return self._base_height

    def _set_base_height(self, base_height: int):
        self._base_height = base_height

    def _get_depth(self):
        return self._depth

    def _set_depth(self, depth: int):
        self._depth = depth

    def __repr__(self):
        return f'Turbulence[intensity={self.intensity}, base_height={self.base_height}, depth={self.depth}]'

    intensity = property(_get_intensity, _set_intensity)
    base_height = property(_get_base_height, _set_base_height)
    depth = property(_get_depth, _set_depth)


class ITafGroups:
    def __init__(self):
        self._turbulence = []
        self._icings = []

    def _get_turbulence(self):
        return self._turbulence

    def _get_icings(self):
        return self._icings

    def add_turbulence(self, turbulence: Turbulence):
        self._turbulence.append(turbulence)

    def add_icing(self, icing: Icing):
        self._icings.append(icing)

    def __repr__(self):
        return f'turbulence={self.turbulence}, icings={self.icings}'

    turbulence = property(_get_turbulence)
    icings = property(_get_icings)


class AbstractWeatherContainer(abc.ABC):

    def __init__(self):
        self._wind = None
        self._visibility = None
        self._vertical_visibility = None
        self._wind_shear = None
        self._cavok = None
        self._remark = None
        self._remarks = []
        self._clouds = []
        self._weather_conditions = []

    def _get_wind(self):
        return self._wind

    def _set_wind(self, value: Wind):
        self._wind = value

    def _get_visibility(self):
        return self._visibility

    def _set_visibility(self, value: Visibility):
        self._visibility = value

    def _get_vertical_visibility(self):
        return self._vertical_visibility

    def _set_vertical_visibility(self, value: int):
        self._vertical_visibility = value

    def _get_wind_shear(self):
        return self._wind_shear

    def _set_wind_shear(self, value: WindShear):
        self._wind_shear = value

    def _get_cavok(self):
        return self._cavok

    def _set_cavok(self, value: bool):
        self._cavok = value

    def _get_remark(self):
        return self._remark

    def _set_remark(self, value: str):
        self._remark = value

    def _get_remarks(self):
        return self._remarks

    def _set_remarks(self, remarks: list):
        self._remarks = remarks

    def _get_clouds(self):
        return self._clouds

    def add_cloud(self, cloud: Cloud):
        if cloud:
            self._clouds.append(cloud)

    def _get_weather_conditions(self):
        return self._weather_conditions

    def add_weather_condition(self, wc: WeatherCondition):
        if wc:
            self._weather_conditions.append(wc)
            return True

    def __repr__(self):
        return f'wind={self.wind}, visibility={self.visibility}, vertical_visibility={self.vertical_visibility}, '\
            f'wind_shear={self.wind_shear}, cavok={self.cavok}, remark={self.remark}, '\
            f'clouds={self.clouds}, weather_conditions={self.weather_conditions}'

    wind = property(_get_wind, _set_wind)
    visibility = property(_get_visibility, _set_visibility)
    vertical_visibility = property(_get_vertical_visibility, _set_vertical_visibility)
    wind_shear = property(_get_wind_shear, _set_wind_shear)
    cavok = property(_get_cavok, _set_cavok)
    remark = property(_get_remark, _set_remark)
    remarks = property(_get_remarks, _set_remarks)
    clouds = property(_get_clouds)
    weather_conditions = property(_get_weather_conditions)


class AbstractValidity(abc.ABC):

    def _get_start_day(self):
        return self._start_day

    def _set_start_day(self, value: int):
        self._start_day = value

    def _get_start_hour(self):
        return self._start_hour

    def _set_start_hour(self, value: int):
        self._start_hour = value

    def __repr__(self):
        return f'start_day={self.start_day}, start_hour={self.start_hour}'

    start_day = property(_get_start_day, _set_start_day)
    start_hour = property(_get_start_hour, _set_start_hour)


class AbstractWeatherCode(AbstractWeatherContainer):

    def __init__(self):
        super().__init__()
        self._day = None
        self._time = None
        self._message = None
        self._station = None
        self._flags = set()
        self._trends = []

    def _get_day(self):
        return self._day

    def _set_day(self, value: int):
        self._day = value

    def _get_time(self):
        return self._time

    def _set_time(self, value: time):
        self._time = value

    def _get_message(self):
        return self._message

    def _set_message(self, value: str):
        self._message = value

    def _get_station(self):
        return self._station

    def _set_station(self, value: str):
        self._station = value

    def _get_trends(self):
        return self._trends

    def add_trend(self, value):
        self._trends.append(value)

    def _get_flags(self):
        return self._flags

    def _is_auto(self):
        return Flag.AUTO in self._flags

    def _is_amendment(self):
        return Flag.AMD in self._flags

    def _is_canceled(self):
        return Flag.CNL in self._flags

    def _is_corrected(self):
        return Flag.COR in self._flags

    def _is_nil(self):
        return Flag.NIL in self._flags

    def __repr__(self):
        return (f'day={self.day}, time={self.time}, message={self.message}, station={self.station}, '
                f'trends={self.trends}, flags={self.flags}, ' + super().__repr__())

    day = property(_get_day, _set_day)
    time = property(_get_time, _set_time)
    message = property(_get_message, _set_message)
    station = property(_get_station, _set_station)
    trends = property(_get_trends)
    flags = property(_get_flags)
    amendment = property(_is_amendment)
    auto = property(_is_auto)
    canceled = property(_is_canceled)
    corrected = property(_is_corrected)
    nil = property(_is_nil)


class Metar(AbstractWeatherCode):

    def __init__(self):
        super().__init__()
        self._temperature = None
        self._dew_point = None
        self._altimeter = None
        self._nosig = False
        self._runways_info = []

    def _get_temperature(self):
        return self._temperature

    def _set_temperature(self, input: int):
        self._temperature = input

    def _get_dew_point(self):
        return self._dew_point

    def _set_dew_point(self, value: int):
        self._dew_point = value

    def _get_altimeter(self):
        return self._altimeter

    def _set_altimeter(self, value: int):
        self._altimeter = value

    def _is_nosig(self):
        return self._nosig

    def _set_nosig(self, value: bool):
        self._nosig = value

    def _get_runways_info(self):
        return self._runways_info

    def add_runway_info(self, runway_info: RunwayInfo):
        self._runways_info.append(runway_info)

    def __repr__(self):
        return 'Metar[' + super().__repr__() + f', temperature={self.temperature}, dew_point={self.dew_point}, altimeter={self.altimeter}, nosig={self.nosig}, runways_info={self.runways_info}]'

    temperature = property(_get_temperature, _set_temperature)
    dew_point = property(_get_dew_point, _set_dew_point)
    altimeter = property(_get_altimeter, _set_altimeter)
    nosig = property(_is_nosig, _set_nosig)
    runways_info = property(_get_runways_info)


class TAF(ITafGroups, AbstractWeatherCode):

    def __init__(self):
        ITafGroups.__init__(self)
        AbstractWeatherCode.__init__(self)
        self._validity = None
        self._max_temperature = None
        self._min_temperature = None

    def _get_validity(self):
        return self._validity

    def _set_validity(self, value: AbstractValidity):
        self._validity = value

    def _get_min_temperature(self):
        return self._min_temperature

    def _set_min_temperature(self, value: TemperatureDated):
        self._min_temperature = value

    def _get_max_temperature(self):
        return self._max_temperature

    def _set_max_temperature(self, value: TemperatureDated):
        self._max_temperature = value

    def becmgs(self):
        return list(filter(lambda trend: trend.type == WeatherChangeType.BECMG, self.trends))

    def probs(self):
        return list(filter(lambda trend: trend.type == WeatherChangeType.PROB, self.trends))

    def tempos(self):
        return list(filter(lambda trend: trend.type == WeatherChangeType.TEMPO, self.trends))

    def inters(self):
        return list(filter(lambda trend: trend.type == WeatherChangeType.INTER, self.trends))

    def fms(self):
        return list(filter(lambda trend: trend.type == WeatherChangeType.FM, self.trends))

    def __repr__(self):
        return 'TAF[' + AbstractWeatherCode.__repr__(self) + ITafGroups.__repr__(self) + f', validity={self.validity}, max_temperature={self.max_temperature}, min_temperature={self.min_temperature}]'

    validity = property(_get_validity, _set_validity)
    max_temperature = property(_get_max_temperature, _set_max_temperature)
    min_temperature = property(_get_min_temperature, _set_min_temperature)


class AbstractTrend(AbstractWeatherContainer):
    def __init__(self, weather_change_type: WeatherChangeType):
        super().__init__()
        self._type = weather_change_type

    def _get_type(self):
        return self._type

    def __repr__(self):
        return super().__repr__() + f', type={self.type}'

    type = property(_get_type)


class MetarTrendTime:
    def __init__(self, time_indicator: TimeIndicator):
        self._type = time_indicator

    def _get_type(self):
        return self._type

    def _get_time(self):
        return self._time

    def _set_time(self, value: time):
        self._time = value

    def __repr__(self):
        return f'MetarTrendTime[type={self.type}, time={self.time}]'

    type = property(_get_type)
    time = property(_get_time, _set_time)


class MetarTrend(AbstractTrend):

    def __init__(self, weather_change_type: WeatherChangeType):
        super().__init__(weather_change_type)
        self._times = []

    def _get_times(self):
        return self._times

    def add_time(self, value: MetarTrendTime):
        self._times.append(value)

    def __repr__(self):
        return 'MetarTrend[' + super().__repr__() + f', times={self.times}'

    times = property(_get_times)


class TAFTrend(AbstractTrend, ITafGroups):
    def __init__(self, weather_change_type: WeatherChangeType):
        ITafGroups.__init__(self)
        AbstractTrend.__init__(self, weather_change_type)
        self._probability = None

    def _get_validity(self):
        return self._validity

    def _set_validity(self, value: AbstractValidity):
        self._validity = value

    def _get_probability(self):
        return self._probability

    def _set_probability(self, prob: int):
        self._probability = prob

    def __repr__(self):
        return 'TAFTrend[' + ITafGroups.__repr__(self) + ', ' + AbstractTrend.__repr__(self) + f', validity={self.validity}, probability={self.probability}'

    probability = property(_get_probability, _set_probability)
    validity = property(_get_validity, _set_validity)


class Validity(AbstractValidity):

    def __init__(self):
        super().__init__()
        self._end_hour = None

    def _get_end_hour(self):
        return self._end_hour

    def _set_end_hour(self, value: int):
        self._end_hour = value

    def _get_end_day(self):
        return self._end_day

    def _set_end_day(self, value: int):
        self._end_day = value

    def __repr__(self):
        return 'Validity[' + super().__repr__() + ', end_day={end_day}, end_hour={end_hour}]'.format(end_hour=self.end_hour, end_day=self.end_day)

    end_hour = property(_get_end_hour, _set_end_hour)
    end_day = property(_get_end_day, _set_end_day)


class FMValidity(AbstractValidity):

    def __init__(self):
        super().__init__()
        self._start_minutes = None

    def _get_start_minutes(self):
        return self._start_minutes

    def _set_start_minutes(self, value: int):
        self._start_minutes = value

    def __repr__(self):
        return 'FMValidity[' + super().__repr__() + f', strart_minutes={self.start_minutes}]'

    start_minutes = property(_get_start_minutes, _set_start_minutes)
