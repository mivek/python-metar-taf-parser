# Change Log 

## [TBD] - TBD

### Added

-   i18n module to support English, French, German and Polish locales.
-   Remarks are now parsed and converted in readable sentence.
The value is stored in properties `remark` and `remarks`. The `remarks` property contains an element for each remark or
    token. The `remark` property contains the whole decoded remarks in a sentence.

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
