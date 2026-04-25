"""
Tests for features ported from MetarParser Java since commit bce66046:
- ReportType enum (METAR/SPECI prefix)
- NCD (No Cloud Detected)
- NSW (No Significant Weather) handling
- Solidus placeholder handling (wind, visibility, altimeter, temperature)
- P99KT support (winds >= 100kt)
- LengthUnit fields on Cloud, Visibility, WindShear, Icing, Turbulence, AbstractWeatherContainer
- STATUTE_MILES LengthUnit
- AbstractWeatherLayer base class for Icing/Turbulence
"""
import unittest

from metar_taf_parser.command.common import (
    CloudCommand,
    MainVisibilityCommand,
    MainVisibilityNauticalMilesCommand,
    MinimalVisibilityCommand,
    VerticalVisibilityCommand,
    WindCommand,
    WindShearCommand,
)
from metar_taf_parser.command.metar import AltimeterCommand, AltimeterMercuryCommand, TemperatureCommand
from metar_taf_parser.command.taf import IcingCommand, TurbulenceCommand
from metar_taf_parser.model.enum import (
    CloudQuantity,
    IcingIntensity,
    LengthUnit,
    ReportType,
    TurbulenceIntensity,
)
from metar_taf_parser.model.model import (
    AbstractWeatherLayer,
    Icing,
    Metar,
    TAF,
    Turbulence,
    Visibility,
)
from metar_taf_parser.parser.parser import MetarParser, TAFParser


class ReportTypeEnumTest(unittest.TestCase):

    def test_metar_value(self):
        self.assertEqual('METAR', ReportType.METAR.value)

    def test_speci_value(self):
        self.assertEqual('SPECI', ReportType.SPECI.value)


class NCDCloudQuantityTest(unittest.TestCase):

    def test_ncd_in_cloud_quantity(self):
        self.assertEqual('NCD', CloudQuantity.NCD.value)

    def test_cloud_command_parse_ncd(self):
        command = CloudCommand()
        cloud = command.parse('NCD')
        self.assertIsNotNone(cloud)
        self.assertEqual(CloudQuantity.NCD, cloud.quantity)


class ReportTypeParsingTest(unittest.TestCase):

    def test_metar_prefix_sets_report_type(self):
        metar = MetarParser().parse('METAR KTTN 051853Z 04011KT 9999 BKN003 02/01 Q1013')
        self.assertEqual(ReportType.METAR, metar.report_type)
        self.assertEqual('KTTN', metar.station)

    def test_speci_prefix_sets_report_type(self):
        metar = MetarParser().parse('SPECI KTTN 051853Z 04011KT 9999 BKN003 02/01 Q1013')
        self.assertEqual(ReportType.SPECI, metar.report_type)
        self.assertEqual('KTTN', metar.station)

    def test_no_prefix_report_type_is_none(self):
        metar = MetarParser().parse('KTTN 051853Z 04011KT 9999 BKN003 02/01 Q1013')
        self.assertIsNone(metar.report_type)
        self.assertEqual('KTTN', metar.station)


class NSWHandlingTest(unittest.TestCase):

    def test_metar_trend_nsw_clears_weather_conditions(self):
        metar = MetarParser().parse('EGLL 211020Z 25015KT 9999 -RA FEW020 15/09 Q1022 TEMPO NSW')
        self.assertEqual(1, len(metar.trends))
        trend = metar.trends[0]
        self.assertTrue(trend.nsw)
        self.assertEqual(0, len(trend.weather_conditions))

    def test_taf_trend_nsw(self):
        taf = TAFParser().parse(
            'TAF EGLL 211100Z 2112/2218 24012KT 9999 BKN020\n'
            'TEMPO 2115/2118 NSW'
        )
        self.assertEqual(1, len(taf.trends))
        self.assertTrue(taf.trends[0].nsw)


class SolidusWindHandlingTest(unittest.TestCase):

    def test_wind_command_solidus_speed_not_set(self):
        command = WindCommand()
        self.assertTrue(command.can_parse('000////KT'))
        wind = command.parse_wind('000////KT')
        self.assertIsNone(wind.speed)
        self.assertIsNone(wind.gust)

    def test_wind_command_p99_support(self):
        command = WindCommand()
        self.assertTrue(command.can_parse('270P99KT'))
        wind = command.parse_wind('270P99KT')
        self.assertEqual(100, wind.speed)
        self.assertEqual('KT', wind.unit)

    def test_wind_command_p99_gust(self):
        command = WindCommand()
        self.assertTrue(command.can_parse('28050GP99KT'))
        wind = command.parse_wind('28050GP99KT')
        self.assertEqual(50, wind.speed)
        self.assertEqual(100, wind.gust)


class SolidusVisibilityHandlingTest(unittest.TestCase):

    def test_main_visibility_solidus_not_set(self):
        command = MainVisibilityCommand()
        container = Metar()
        self.assertTrue(command.can_parse('////'))
        command.execute(container, '////')
        self.assertIsNone(container.visibility.distance)

    def test_main_visibility_solidus_creates_visibility_object(self):
        command = MainVisibilityCommand()
        container = Metar()
        command.execute(container, '////')
        self.assertIsNotNone(container.visibility)

    def test_main_visibility_sets_unit_meters(self):
        command = MainVisibilityCommand()
        container = Metar()
        command.execute(container, '9999')
        self.assertEqual(LengthUnit.METERS, container.visibility.unit)


class SolidusAltimeterHandlingTest(unittest.TestCase):

    def test_altimeter_solidus_not_set(self):
        command = AltimeterCommand()
        metar = Metar()
        self.assertTrue(command.can_parse('Q////'))
        command.execute(metar, 'Q////')
        self.assertIsNone(metar.altimeter)

    def test_altimeter_normal(self):
        command = AltimeterCommand()
        metar = Metar()
        command.execute(metar, 'Q1013')
        self.assertEqual(1013, metar.altimeter)

    def test_altimeter_mercury_solidus_not_set(self):
        command = AltimeterMercuryCommand()
        metar = Metar()
        self.assertTrue(command.can_parse('A////'))
        command.execute(metar, 'A////')
        self.assertIsNone(metar.altimeter)

    def test_altimeter_mercury_normal(self):
        command = AltimeterMercuryCommand()
        metar = Metar()
        command.execute(metar, 'A2992')
        self.assertIsNotNone(metar.altimeter)


class PartialMissingTemperatureTest(unittest.TestCase):

    def test_temperature_solidus_both_missing(self):
        command = TemperatureCommand()
        metar = Metar()
        self.assertTrue(command.can_parse('///////'))
        command.execute(metar, '///////')
        self.assertIsNone(metar.temperature)
        self.assertIsNone(metar.dew_point)

    def test_temperature_solidus_temp_missing(self):
        command = TemperatureCommand()
        metar = Metar()
        self.assertTrue(command.can_parse('////10'))
        command.execute(metar, '////10')
        self.assertIsNone(metar.temperature)
        self.assertEqual(10, metar.dew_point)

    def test_temperature_solidus_dew_missing(self):
        command = TemperatureCommand()
        metar = Metar()
        self.assertTrue(command.can_parse('25////'))
        command.execute(metar, '25////')
        self.assertEqual(25, metar.temperature)
        self.assertIsNone(metar.dew_point)

    def test_temperature_full_solidus_both_null(self):
        command = TemperatureCommand()
        metar = Metar()
        self.assertTrue(command.can_parse('///////'))
        command.execute(metar, '///////')
        self.assertIsNone(metar.temperature)
        self.assertIsNone(metar.dew_point)

    def test_temperature_normal(self):
        command = TemperatureCommand()
        metar = Metar()
        command.execute(metar, '20/15')
        self.assertEqual(20, metar.temperature)
        self.assertEqual(15, metar.dew_point)


class LengthUnitStatuteMilesTest(unittest.TestCase):

    def test_statute_miles_value(self):
        self.assertEqual('SM', LengthUnit.STATUTE_MILES.value)

    def test_sm_visibility_sets_statute_miles_unit(self):
        command = MainVisibilityNauticalMilesCommand()
        container = Metar()
        command.execute(container, '5SM')
        self.assertEqual(LengthUnit.STATUTE_MILES, container.visibility.unit)
        self.assertEqual('5', container.visibility.distance)

    def test_sm_visibility_strips_sm_suffix(self):
        command = MainVisibilityNauticalMilesCommand()
        container = Metar()
        command.execute(container, 'P6SM')
        self.assertEqual('P6', container.visibility.distance)
        self.assertEqual(LengthUnit.STATUTE_MILES, container.visibility.unit)

    def test_sm_fraction_visibility_strips_suffix(self):
        command = MainVisibilityNauticalMilesCommand()
        container = Metar()
        command.execute(container, '1/2SM')
        self.assertEqual('1/2', container.visibility.distance)


class LengthUnitOnModelsTest(unittest.TestCase):

    def test_cloud_unit_set_to_feet(self):
        command = CloudCommand()
        cloud = command.parse('SCT016')
        self.assertEqual(LengthUnit.FEET, cloud.unit)

    def test_cloud_unit_none_when_no_height(self):
        command = CloudCommand()
        cloud = command.parse('SKC')
        self.assertIsNone(cloud.unit)

    def test_vertical_visibility_unit_set_to_feet(self):
        command = VerticalVisibilityCommand()
        container = Metar()
        command.execute(container, 'VV005')
        self.assertEqual(500, container.vertical_visibility)
        self.assertEqual(LengthUnit.FEET, container.vertical_visibility_unit)

    def test_wind_shear_height_unit_set_to_feet(self):
        command = WindShearCommand()
        container = Metar()
        command.execute(container, 'WS020/24045KT')
        self.assertEqual(LengthUnit.FEET, container.wind_shear.height_unit)

    def test_minimal_visibility_sets_unit_meters(self):
        command = MinimalVisibilityCommand()
        container = Metar()
        container.visibility = Visibility()
        command.execute(container, '1500NE')
        self.assertEqual(LengthUnit.METERS, container.visibility.unit)

    def test_icing_unit_set_to_feet(self):
        command = IcingCommand()
        taf = TAF()
        command.execute(taf, '620304')
        self.assertEqual(1, len(taf.icings))
        self.assertEqual(LengthUnit.FEET, taf.icings[0].unit)

    def test_turbulence_unit_set_to_feet(self):
        command = TurbulenceCommand()
        taf = TAF()
        command.execute(taf, '520304')
        self.assertEqual(1, len(taf.turbulence))
        self.assertEqual(LengthUnit.FEET, taf.turbulence[0].unit)

    def test_cavok_sets_unit_meters(self):
        metar = MetarParser().parse('KTTN 051853Z 04011KT CAVOK 02/01 Q1013')
        self.assertEqual(LengthUnit.METERS, metar.visibility.unit)


class AbstractWeatherLayerTest(unittest.TestCase):

    def test_icing_is_abstract_weather_layer(self):
        icing = Icing()
        self.assertIsInstance(icing, AbstractWeatherLayer)

    def test_turbulence_is_abstract_weather_layer(self):
        turbulence = Turbulence()
        self.assertIsInstance(turbulence, AbstractWeatherLayer)

    def test_icing_inherits_base_height(self):
        icing = Icing()
        icing.base_height = 3000
        self.assertEqual(3000, icing.base_height)

    def test_icing_inherits_depth(self):
        icing = Icing()
        icing.depth = 4000
        self.assertEqual(4000, icing.depth)

    def test_icing_inherits_unit(self):
        icing = Icing()
        icing.unit = LengthUnit.FEET
        self.assertEqual(LengthUnit.FEET, icing.unit)

    def test_turbulence_inherits_unit(self):
        turbulence = Turbulence()
        turbulence.unit = LengthUnit.FEET
        self.assertEqual(LengthUnit.FEET, turbulence.unit)

    def test_icing_intensity_still_works(self):
        icing = Icing()
        icing.intensity = IcingIntensity.LIGHT
        self.assertEqual(IcingIntensity.LIGHT, icing.intensity)

    def test_turbulence_intensity_still_works(self):
        turbulence = Turbulence()
        turbulence.intensity = TurbulenceIntensity.LIGHT
        self.assertEqual(TurbulenceIntensity.LIGHT, turbulence.intensity)


class IntegrationTest(unittest.TestCase):

    def test_metar_with_speci_prefix(self):
        metar = MetarParser().parse(
            'SPECI CYQB 211933Z 25023G35KT 1SM -RASN BR BKN007 OVC013 02/01 A2988'
        )
        self.assertEqual(ReportType.SPECI, metar.report_type)
        self.assertEqual('CYQB', metar.station)
        self.assertEqual(23, metar.wind.speed)

    def test_metar_with_solidus_wind(self):
        metar = MetarParser().parse('KTTN 051853Z 000////KT 9999 BKN003 02/01 Q1013')
        self.assertIsNotNone(metar.wind)
        self.assertIsNone(metar.wind.speed)

    def test_metar_with_p99_wind(self):
        metar = MetarParser().parse('KJFK 121151Z 280P99KT 10SM 25/10 Q1012')
        self.assertIsNotNone(metar.wind)
        self.assertEqual(100, metar.wind.speed)

    def test_metar_with_solidus_visibility(self):
        metar = MetarParser().parse('KTTN 051853Z 04011KT //// BKN003 02/01 Q1013')
        self.assertIsNotNone(metar.visibility)
        self.assertIsNone(metar.visibility.distance)

    def test_metar_with_solidus_altimeter(self):
        metar = MetarParser().parse('KTTN 051853Z 04011KT 9999 BKN003 02/01 Q////')
        self.assertIsNone(metar.altimeter)

    def test_metar_with_partial_missing_temperature(self):
        metar = MetarParser().parse('KTTN 051853Z 04011KT 9999 BKN003 ////M02 Q1013')
        self.assertIsNone(metar.temperature)
        self.assertEqual(-2, metar.dew_point)

    def test_taf_with_icing_unit(self):
        taf = TAFParser().parse(
            'TAF EGLL 211100Z 2112/2218 24012KT 9999 BKN020 620304'
        )
        self.assertEqual(1, len(taf.icings))
        self.assertEqual(LengthUnit.FEET, taf.icings[0].unit)

    def test_taf_with_turbulence_unit(self):
        taf = TAFParser().parse(
            'TAF EGLL 211100Z 2112/2218 24012KT 9999 BKN020 520304'
        )
        self.assertEqual(1, len(taf.turbulence))
        self.assertEqual(LengthUnit.FEET, taf.turbulence[0].unit)

    def test_metar_clouds_have_feet_unit(self):
        metar = MetarParser().parse('KTTN 051853Z 04011KT 9999 BKN003 02/01 Q1013')
        self.assertEqual(1, len(metar.clouds))
        self.assertEqual(LengthUnit.FEET, metar.clouds[0].unit)


if __name__ == '__main__':
    unittest.main()
