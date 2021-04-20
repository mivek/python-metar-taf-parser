# Change Log 

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
