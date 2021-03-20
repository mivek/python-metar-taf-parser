import abc
from datetime import time

from metar_taf_parser.model.enum import Descriptive, WeatherChangeType, TimeIndicator


class Country:

    def __init__(self, name):
        self._name = name

    def _get_name(self):
        """ Return the name of the country """
        return self._name

    def _set_name(self, value):
        """ Setter for the name """
        self._name = value

    name = property(_get_name, _set_name)


class Airport:
    def __init__(self):
        """ Initiate the attributes """
        self._name = None
        self._city = None
        self._country = None
        self._iata = None
        self._icao = None
        self._latitude = None
        self._longitude = None
        self._altitude = None
        self._timezone = None
        self._dst = None
        self._tz_database = None

    def _get_name(self):
        return self._name

    def _set_name(self, value):
        self._name = value

    def _get_city(self):
        return self._city

    def _set_city(self, value):
        self._city = value

    def _get_country(self):
        return self._country

    def _set_country(self, value):
        self._country = value

    def _get_iata(self):
        return self._iata

    def _set_iata(self, value):
        self._iata = value

    def _get_icao(self):
        return self._icao

    def _set_icao(self, value):
        self._icao = value

    def _get_latitude(self):
        return self._latitude

    def _set_latitude(self, value):
        self._latitude = value

    def _get_longitude(self):
        return self._longitude

    def _set_longitude(self, value):
        self._longitude = value

    def _set_altitude(self, value):
        self._altitude = value

    def _get_altitude(self):
        return self._altitude

    def _get_timezone(self):
        return self._timezone

    def _set_timezone(self, value):
        self._timezone = value

    def _get_dst(self):
        return self._dst

    def _set_dst(self, value):
        self._dst = value

    def _get_tz_database(self):
        return self._tz_database

    def _set_tz_database(self, value):
        self._tz_database = value

    name = property(_get_name, _set_name)
    city = property(_get_city, _set_city)
    country = property(_get_country, _set_country)
    iata = property(_get_iata, _set_iata)
    icao = property(_get_icao, _set_icao)
    latitude = property(_get_latitude, _set_latitude)
    longitude = property(_get_longitude, _set_longitude)
    altitude = property(_get_altitude, _set_altitude)
    timezone = property(_get_timezone, _set_timezone)
    dst = property(_get_dst, _set_dst)
    tz_database = property(_get_tz_database, _set_tz_database)


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

    temperature = property(_get_temperature, _set_temperature)
    day = property(_get_day, _set_day)
    hour = property(_get_hour, _set_hour)


class RunwayInfo:

    def __init__(self):
        self._name = None
        self._min_range = None
        self._max_range = None
        self._trend = None

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

    name = property(_get_name, _set_name)
    min_range = property(_get_min_range, _set_min_range)
    max_range = property(_get_max_range, _set_max_range)
    trend = property(_get_trend, _set_trend)


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

    height = property(_get_height, _set_height)
    quantity = property(_get_quantity, _set_quantity)
    type = property(_get_type, _set_type)


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

    def _set_remarks(self, remarks: [str]):
        self._remarks = remarks

    def _get_clouds(self):
        return self._clouds

    def add_cloud(self, cloud: Cloud):
        if cloud:
            self._clouds.append(cloud)

    def _get_weather_conditions(self):
        return self._weather_conditions

    def add_weather_condition(self, wc: WeatherCondition):
        if wc.is_valid():
            self._weather_conditions.append(wc)
            return True

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

    start_day = property(_get_start_day, _set_start_day)
    start_hour = property(_get_start_hour, _set_start_hour)


class AbstractWeatherCode(AbstractWeatherContainer):

    def __init__(self):
        super().__init__()
        self._day = None
        self._time = None
        self._airport = None
        self._message = None
        self._station = None
        self._trends = []

    def _get_day(self):
        return self._day

    def _set_day(self, value: int):
        self._day = value

    def _get_time(self):
        return self._time

    def _set_time(self, value: time):
        self._time = value

    def _get_airport(self):
        return self._airport

    def _set_airport(self, value: Airport):
        self._airport = value

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

    day = property(_get_day, _set_day)
    time = property(_get_time, _set_time)
    airport = property(_get_airport, _set_airport)
    message = property(_get_message, _set_message)
    station = property(_get_station, _set_station)
    trends = property(_get_trends)


class Metar(AbstractWeatherCode):

    def __init__(self):
        super().__init__()
        self._temperature = None
        self._dew_point = None
        self._altimeter = None
        self._nosig = False
        self._auto = False
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

    def _is_auto(self):
        return self._auto

    def _set_auto(self, value: bool):
        self._auto = value

    def _get_runways_info(self):
        return self._runways_info

    def add_runway_info(self, runway_info: RunwayInfo):
        self._runways_info.append(runway_info)

    temperature = property(_get_temperature, _set_temperature)
    dew_point = property(_get_dew_point, _set_dew_point)
    altimeter = property(_get_altimeter, _set_altimeter)
    nosig = property(_is_nosig, _set_nosig)
    auto = property(_is_auto, _set_auto)
    runways_info = property(_get_runways_info)


class TAF(AbstractWeatherCode):

    def __init__(self):
        super().__init__()
        self._validity = None
        self._max_temperature = None
        self._min_temperature = None
        self._amendment = False

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

    def _is_amendment(self):
        return self._amendment

    def _set_amendment(self, value: bool):
        self._amendment = value

    validity = property(_get_validity, _set_validity)
    max_temperature = property(_get_max_temperature, _set_max_temperature)
    min_temperature = property(_get_min_temperature, _set_min_temperature)
    amendment = property(_is_amendment, _set_amendment)


class AbstractTrend(AbstractWeatherContainer):
    def __init__(self, weather_change_type: WeatherChangeType):
        super().__init__()
        self._type = weather_change_type

    def _get_type(self):
        return self._type

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

    times = property(_get_times)


class TAFTrend(AbstractTrend):
    def __init__(self, weather_change_type: WeatherChangeType):
        super().__init__(weather_change_type)
        self._probability = None

    def _get_validity(self):
        return self._validity

    def _set_validity(self, value: AbstractValidity):
        self._validity = value

    def _get_probability(self):
        return self._probability

    def _set_probability(self, prob: int):
        self._probability = prob

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

    start_minutes = property(_get_start_minutes, _set_start_minutes)
