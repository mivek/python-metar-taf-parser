# Change Log 

## [1.6.4] - 2023-06-TBD

### Fixed

- Parsing of `TAF` with stations starting by `FM`.

## [1.6.3] - 2023-03-12

### Fixed

- Parsing of token `0000KT` no longer causes an error.

## [1.6.2] - 2023-01-29

### Fixed

- Parsing of Runway does not fail if thickness and braking capacity are not in the enum.

### Changed

- RunwayInfo properties `thickness` and `braking_capacity` type is changed to string. Enums `DepositThickness` and `DepositBreakingCapacity` are removed.

## [1.6.1] - 2022-12-20

### Added

- Implement parsing of deposit on a Runway. Properties `indicator`, `deposit_type`, `coverage`, `thickness`, `braking_capacity`.

## [1.6.0] - 2022-12-04

### Added

- Support for unknown height and unknown types in cloud elements. Clouds elements with `///` are no longer ignored.
- `Turbulence` and `Icing` elements are available in `TAF` and `TAFTrend` objects. The new properties are `turbulence` and `icings`.

### Fixed

- WeatherConditions are now added to the list only if the entire token was parsed. This prevents false positive matches.
- Phenomenons in WeatherConditions are now listed in the same order they appear in the token.
- Cloud regex matches the cloud type part only of the height is present. Tokens made of 6 letters do not match the regex anymore.

## [1.5.0] - 2022-07-17

### Added

- Added `flags` property to `AbstractWeatherCode`. This property is a set holding flags: AUTO, AMD, CNL, NIL and COR. Properties `auto`, `amendment`, `nil`, `canceled` and `corrected` are also available.
- Added new translations.

## [1.4.1] - 2022-05-29

### Fixed

- Parsing of visibility in miles having indication: `P` for greater than and `M` for less than.

## [1.4.0] - 2022-04-20

### Added

- Added `WeatherChangeType.INTER` for TAFTrend.
- Added methods to retrieve Taf trends by `WeatherChangeType`: taf.becmgs, taf.fms, taf.inters, taf.probs and taf.tempos
- Turkish translation
- Added `PrecipitationBegCommand` and `PrecipitationEndCommand` in remark parsing.

### Fixed

- Parsing of remarks added Phenomenon.FC to the list of WeatherConditions when the remarks contained `FCST`

## [1.3.0] - 2021-10-05

### Added

- i18n support for simplified Chinese locale
- Completed remarks parsing

## [1.2.0] - 2021-05-04

### Added

- i18n support for Italian locale

## [1.1.1] - 2021-04-20

### Fixed

-   Added packages source directory in `setup.cfg` to fix deployment.   

## [1.1.0] - 2021-03-20

### Added

-   i18n module to support English, French, German and Polish locales.
-   Remarks are now parsed and converted in a readable sentence.
The value is stored in properties `remark` and `remarks`. The `remarks` property contains an element for each remark or
    token. The `remark` property contains the whole decoded remarks in a sentence.

-   Makefile and `pyproject.toml`.
    
-   Coverage measurement.

### Changed

-   The packaging now uses setuptools and build modules instead of `setup.py`.


## [1.0.1] - 2021-02-28

### Changed

-   Removed the regex search from the weatherCondition parsing.
Replaced by a single string search.
  
### Fixed

-   Added `^` (start of string) at the beginning of the wind regex.

## [1.0.0] - 2020-10-18

### Added

-   First version of the MetarParser and the TAFParser.
-   Github actions to handle commits, release and 

### Changed

### Fixed
