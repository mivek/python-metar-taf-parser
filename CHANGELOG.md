# Change Log 

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
