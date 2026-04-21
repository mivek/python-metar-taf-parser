# Copilot Instructions for python-metar-taf-parser

## Build, Test, and Lint Commands

### Installation and Setup
```bash
make install              # Install dependencies and development tools
make clean                # Clean up build artifacts and coverage reports
```

### Testing
```bash
make test                 # Run all unit tests with coverage
make report               # Run tests and generate coverage reports (HTML, XML, JSON)
```

### Code Quality
```bash
flake8                    # Run linting with configured rules
```

### Build and Deployment
```bash
make install_deploy       # Install build/deployment dependencies
python -m build           # Build distribution packages
```

**Note**: The project uses `pipenv` for dependency management. Tests are executed with the built-in `unittest` framework.

---

## High-Level Architecture

### Core Structure
The project is organized into distinct packages that follow a pipeline architecture for parsing METAR and TAF aviation weather messages:

1. **Parser Package** (`metar_taf_parser/parser/`)
   - Entry point: `MetarParser` and `TAFParser` classes
   - Tokenizes input messages and orchestrates the parsing workflow
   - Delegates specific token parsing to command handlers

2. **Command Package** (`metar_taf_parser/command/`)
   - Implements the **Command Pattern** for parsing individual tokens
   - Each command class handles a specific token type (e.g., wind, visibility, altimeter)
   - Commands are grouped by supplier: `MetarCommandSupplier`, `TAFCommandSupplier`, `CommandSupplier` (common), `RemarkCommandSupplier`
   - Each command has:
     - `regex` class attribute for pattern matching
     - `can_parse(input: str)` method to check if it matches
     - `execute(weather_obj, input: str)` method to update the model

3. **Model Package** (`metar_taf_parser/model/`)
   - **enum.py**: Enumerations for all weather concepts (CloudQuantity, Intensity, Phenomenon, TimeIndicator, etc.)
   - **model.py**: Core data classes representing METAR/TAF concepts
   - Class hierarchy:
     - `AbstractWeatherContainer`: Base for common weather data (wind, visibility, clouds, weather conditions)
     - `AbstractWeatherCode`: Extends container; parent to `Metar` and `TAF`
     - `Metar` and `TAF`: Specific implementations with their own fields
     - Supporting classes: `Wind`, `WindShear`, `Visibility`, `Cloud`, `RunwayInfo`, `WeatherCondition`, etc.

4. **Commons Package** (`metar_taf_parser/commons/`)
   - **converter.py**: Helper functions for unit conversions and data transformations
   - **i18n.py**: Internationalization support (en, fr, de, pl, it, ru)
   - **exception.py**: Custom exceptions (`ParseError`, `TranslationError`)

5. **Service Package** (`metar_taf_parser/service/`)
   - High-level service layer (abstraction over parsers)

### Parsing Flow
1. User calls `MetarParser().parse(metar_string)` or `TAFParser().parse(taf_string)`
2. Parser tokenizes the input string
3. Parser iterates through tokens and finds matching commands via regex patterns
4. Commands execute and populate the model object
5. Model object is returned with all parsed data

---

## Key Conventions

### Command Pattern Implementation
- Commands are stateless and reusable
- Regex patterns use `^...$` anchors (exact match required)
- The `can_parse()` method is called before `execute()` for all commands
- Multiple suppliers (Metar, TAF, Common) allow different parsing rules for different message types

### Naming Conventions
- **Enum classes**: PascalCase describing a concept (e.g., `CloudQuantity`, `IcingIntensity`)
- **Model classes**: PascalCase (e.g., `Wind`, `Metar`, `AbstractWeatherContainer`)
- **Command classes**: Describe the functionality with "Command" suffix (e.g., `AltimeterCommand`, `WindCommand`)
- **Suppliers**: Named with "Supplier" suffix (e.g., `MetarCommandSupplier`)

### Commit Messages
Follow [Conventional Commits](https://www.conventionalcommits.org/):
```
<type>(<scope>): <subject>

Examples:
  feat(parser): add support for new weather condition
  fix(translation): correct French translation for 'clear sky'
  docs(contributing): add commit message guidelines
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`

### Internationalization
- Locales stored in `metar_taf_parser/locale/` as `.po` and `.mo` files
- Use the `_()` function from `commons.i18n` for translatable strings
- New languages added via [Crowdin](https://crwd.in/metarParser) and require 100% completion

### Test Organization
- Test files mirror source structure: `metar_taf_parser/tests/`
- Test modules grouped by parsing phase: `command/`, `parser/`, `common/`
- Tests use Python's `unittest` framework
- Each test file typically tests one command or command group

### Flake8 Configuration
- Max line length: unlimited (E501 ignored)
- Max complexity: 10
- Ignored rules: E501 (line too long), W605 (invalid escape), W503 (line break before operator)

---

## Project Details

- **Language**: Python 3.9+
- **License**: MIT
- **Package Name**: `metar-taf-parser-mivek`
- **Main Classes**: `MetarParser`, `TAFParser` (in `metar_taf_parser.parser.parser`)
- **Build System**: setuptools (pyproject.toml)
