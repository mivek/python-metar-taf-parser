# METAR TAF Parser

![Python test](https://github.com/mivek/python-metar-taf-parser/workflows/Python%20test/badge.svg)

This project provides METAR and TAF parsers.

## Install

```
pip install metar-taf-parser-mivek
```

## Structure

### Commons package

This package contains the converter module. The module contains helper functions.

### Model package

This package contains multiple modules

- enum: Contains the enumerations for the project
- model: Contains the model classes for the project

### Parser package

This package contains the parser module with the `MetarParser` and `TAFParser` classes.

## Model

### Enumerations:

- CloudQuantity: Represents the quantity in a cloud layer
- CloudType: Represents the type of cloud in a cloud layer
- Intensity: Represents the intensity of a weather phenomenon
- Descriptive: Represents the descriptive part of a weather phenomenon
- Phenomenon: Represents the phenomenon of a weather phenomenon
- TimeIndicator: Indicates the time trend
- WeatherChangeType: Indicate the type of trend


### Objects

#### Wind

Represents the wind part of a metar, taf or trend

- speed: `int`. The speed of the wind
- direction: `str`. The cardinal direction of the wind
- degrees: `int`. The direction in degrees
- gust: `int`. The speed of gust if any, None otherwise
- min_variation: `int`. The minimal degree variation of the wind
- max_variation: `int`. The maximal degree variation of the wind
- unit: `str`. The unit of the speed of the wind.

#### WindShear

Represents a wind shear in TAF message. This class extends Wind.

- height: `int`. The height of the wind shear.

#### Visibility

Represents the visibility part of a METAR, TAF or trend.

- distance: `str`. The distance in meters or nautical miles.
- min_distance: `int`. The minimal distance in meters if any.
- min_direction: `str`. The direction of the minimal distance if any.

#### WeatherCondition

Represents the weather part of a METAR, TAF or trend.

- intensity: `Intensity`. The intensity of the weather condition if any, `None` otherwise.
- descriptive: `Descriptive`. The descriptive of the weather condition if any, `None` otherwise.
- phenomenons: `[Phenomenon]`. Array of phenomenons of the weather condition.

#### TemperatureDated

Represents the temperature part of a TAF. 

- temperature: `int`. The temperature in celsius degrees.
- day: `int`. Day of the occurrence.
- hour: `int`. Hour of the occurrence.

#### RunwayInfo

Contains information on the visibility on a runway

- name: `str`. The name of the runway.
- min_range: `int`. The minimal visibility distance on the runway.
- max_range: `int`. The maximal visibility distance on the runway.
- trend: `str`. The trend of the visibility.

#### Cloud

Represents a cloud layer in METAR, TAF or trend object.

- height: `int`. The height of the layer in feet.
- quantity: `CloudQuantity`. The quantity of clouds.
- type: `CloudType`. The type of cloud in the layer.

#### AbstractWeatherContainer

Abstract class containing the basic fields of METAR, TAF or trend objects.

- wind: `Wind`. The wind. Can be `None` for trends.
- visibility: `Visibility`. The visibility.
- vertical_visibility: `int`. The vertical visibility, can be `None`
- wind_shear: `WindShear`. The wind shear object.
- cavok: `bool`. Indicates whether the message is CAVOK (Ceiling and visibility OK)
- remark: `str`. The remark part of the message.
- remarks: `[str]`. List of remarks. Each element is a different remark or token 
- clouds: `[Cloud]`. Array of clouds elements.
- weather_conditions: `[WeatherCondition]`. Array of weather conditions.

#### AbstractValidity

Abstract class representing the base of a Validity object.

- start_day: `int`. The starting day of the validity.
- start_hour: `int`. The starting hour of the validity.

#### AbstractWeatherCode

Class extending the AbstractWeatherContainer. Abstract parent class of METAR and TAF.

- day: `int`. The delivery day of the METAR or TAF.
- time: `datetime.time`. The delivery time of the METAR/TAF.
- message: `str`. The message of the METAR/TAF.
- station: `str`. The station for which the message was issued.
- trends: `[TAFTrend/MetarTrend]`. Array of trends

#### Metar

Class representing a metar object.

- temperature: `int`. The temperature in celsius.
- dew_point: `int`. The dew_point in celsius.
- altimeter: `float`. The altimeter value in HPa.
- nosig: `bool`. Whether the message is nosig: No significant changes to come.
- auto: `bool`. Whether the message is auto.
- runway_info: `[RunwayInfo]`. Array of runway information.

#### TAF

Class representing a TAF object.

- validity: `Validity`. The validity of the TAF.
- max_temperature: `TemperatureDated`. The maximum temperature during the validity of the TAF.
- min_temperature: `TemperatureDated`. The minimum temperature during the validity of the TAF.
- amendment: `bool`. Whether the TAF is an amendment.

#### AbstractTrend

Abstract base class for trend.

- type: `WeatherChangeType`. The type of change.

#### MetarTrendTime

Class containing the time of the trend.

- time: `datetime.time`. Time of the trend's occurrence.
- type: `TimeIndicator`. Type of time change of the trend.

#### MetarTrend

Represents a trend in a METAR object, this class extends `AbstractTrend`.

- times: `[MetarTrendTime]`. The list of time change of the trend.

#### TAFTrend

Represent a trend in a TAF object, this class extends `AbstractTrend`

- validity: `AbstractValidity`. The validity of the trend either `Validity` or `FMValidity`
- probability: `int`. The probability of a trend, can be `None`.

#### Validity

Represents the validity timespan of a TAF or TAFTrend, this class extends `AbstractValidity`.

- end_day: `int`. The ending day of the validity.
- end_hour: `int` The ending hour of the validity.

#### FMValidity

Represents the validity of a From trend, extends AbstractValidity

- start_minutes: `int`. The starting minute of the trend.


## Example

### Parse a METAR

Use the method `parse(string)` of the `MetarParser` to parse a metar.

```python
from metar_taf_parser.parser.parser import MetarParser

metar = MetarParser().parse('KTTN 051853Z 04011KT 9999 VCTS SN FZFG BKN003 OVC010 M02/M02 A3006')

```


### Parse a TAF 

Use the method `parse(string)` of the TAFParser to parse a TAF message.
The message must start with `TAF` in order to be parsed.


```python
from metar_taf_parser.parser.parser import TAFParser

taf = TAFParser().parse('TAF LFPG 150500Z 1506/1612 17005KT 6000 SCT012 TEMPO 1506/1509 3000 BR BKN006 PROB40 TEMPO 1506/1508 0400 BCFG BKN002 PROB40 TEMPO 1512/1516 4000 -SHRA FEW030TCU BKN040 BECMG 1520/1522 CAVOK TEMPO 1603/1608 3000 BR BKN006 PROB40 TEMPO 1604/1607 0400 BCFG BKN002 TX17/1512Z TN07/1605Z')
```


## Internationalization

The following locales are supported:
- en (default)
- fr
- de
- pl