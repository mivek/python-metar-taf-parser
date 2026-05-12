import unittest

from metar_taf_parser.command.common import (
    CloudCommand,
    CommandSupplier,
    MainVisibilityCommand,
    MainVisibilityNauticalMilesCommand,
    MinimalVisibilityCommand,
    VerticalVisibilityCommand,
    WindCommand,
    WindShearCommand,
)
from metar_taf_parser.model.enum import CloudQuantity, CloudType, LengthUnit
from metar_taf_parser.model.model import TAF, Metar


class CommonTestCase(unittest.TestCase):
    def test_cloud_command_parse_sky_clear(self):
        command = CloudCommand()
        cloud = command.parse("SKC")
        self.assertIsNotNone(cloud)
        self.assertEqual(CloudQuantity.SKC, cloud.quantity)
        self.assertIsNone(cloud.height)
        self.assertIsNone(cloud.type)
        self.assertIsNone(cloud.unit)

    def test_cloud_command_parse_with_height(self):
        command = CloudCommand()

        cloud = command.parse('SCT016')

        self.assertEqual(CloudQuantity.SCT, cloud.quantity)
        self.assertEqual(1600, cloud.height)
        self.assertIsNone(cloud.type)
        self.assertEqual(LengthUnit.FEET, cloud.unit)

    def test_cloud_command_parse_with_type(self):
        command = CloudCommand()

        cloud = command.parse('SCT026CB')

        self.assertEqual(CloudQuantity.SCT, cloud.quantity)
        self.assertEqual(2600, cloud.height)
        self.assertEqual(CloudType.CB, cloud.type)
        self.assertEqual(LengthUnit.FEET, cloud.unit)

    def test_cloud_command_parse_NSC(self):
        command = CloudCommand()

        cloud = command.parse('NSC')

        self.assertEqual(CloudQuantity.NSC, cloud.quantity)

    def test_wind_command_parse_simple(self):
        command = WindCommand()

        wind = command.parse_wind('34008KT')

        self.assertEqual('NNW', wind.direction)
        self.assertEqual(340, wind.degrees)
        self.assertEqual(8, wind.speed)
        self.assertIsNone(wind.gust)
        self.assertEqual('KT', wind.unit)

    def test_wind_command_parse_gusts(self):
        command = WindCommand()

        wind = command.parse_wind('12017G20KT')

        self.assertEqual('ESE', wind.direction)
        self.assertEqual(120, wind.degrees)
        self.assertEqual(17, wind.speed)
        self.assertEqual(20, wind.gust)
        self.assertEqual('KT', wind.unit)

    def test_wind_command_parse_gusts_3_digits(self):
        command = WindCommand()

        wind = command.parse_wind('12017G015KT')
        self.assertEqual('ESE', wind.direction)
        self.assertEqual(120, wind.degrees)
        self.assertEqual(17, wind.speed)
        self.assertEqual(15, wind.gust)
        self.assertEqual('KT', wind.unit)

    def test_parse_wind_command_parse_wind_variable(self):
        command = WindCommand()

        wind = command.parse_wind('VRB08KT')

        self.assertEqual('VRB', wind.direction)
        self.assertEqual(8, wind.speed)
        self.assertIsNone(wind.degrees)

    def test_command_supplier(self):
        supplier = CommandSupplier()

        self.assertEqual(8, len(supplier._commands))

    def test_execute(self):
        command = WindCommand()
        metar = Metar()
        self.assertTrue(command.execute(metar, 'VRB08KT'))

    def test_minimal_visibility_command(self):
        command = MinimalVisibilityCommand()

        for dir in ['N', 'ne', 's', 'SW']:
            with self.subTest(dir):
                vis_str = f'3000{dir}'
                self.assertTrue(command.can_parse(vis_str))

                taf = TAF()
                self.assertTrue(command.execute(taf, vis_str))
                self.assertEqual(taf.visibility.min_distance, 3000)
                self.assertEqual(taf.visibility.min_direction, dir)

    def test_main_visibility_nautical_miles_command_with_greater_than(self):
        command = MainVisibilityNauticalMilesCommand()
        self.assertTrue(command.can_parse('P3SM'))

    def test_main_visibility_nautical_miles_command_with_minus_than(self):
        command = MainVisibilityNauticalMilesCommand()
        self.assertTrue(command.can_parse('M1SM'))

    def test_cloud_command_unknown_type(self):
        command = CloudCommand()
        cloud = command.parse('SCT026///')

        self.assertIsNotNone(cloud)
        self.assertEqual(CloudQuantity.SCT, cloud.quantity)
        self.assertEqual(2600, cloud.height)
        self.assertIsNone(cloud.type)

    def test_cloud_command_unknown_height_and_type(self):
        command = CloudCommand()
        cloud = command.parse('SCT//////')

        self.assertIsNotNone(cloud)
        self.assertEqual(CloudQuantity.SCT, cloud.quantity)
        self.assertIsNone(cloud.height)
        self.assertIsNone(cloud.type)
        self.assertIsNone(cloud.unit)

    def test_main_visibility_command_sets_meters_unit(self):
        command = MainVisibilityCommand()
        metar = Metar()
        command.execute(metar, '5000')
        self.assertEqual('5000', metar.visibility.distance)
        self.assertEqual(LengthUnit.METERS, metar.visibility.unit)

    def test_main_visibility_command_9999(self):
        command = MainVisibilityCommand()
        metar = Metar()
        command.execute(metar, '9999')
        self.assertEqual('>10000', metar.visibility.distance)
        self.assertEqual(LengthUnit.METERS, metar.visibility.unit)

    def test_main_visibility_nautical_miles_command_sets_statute_miles_unit(self):
        command = MainVisibilityNauticalMilesCommand()
        metar = Metar()
        command.execute(metar, '6SM')
        self.assertEqual('6', metar.visibility.distance)
        self.assertEqual(LengthUnit.STATUTE_MILES, metar.visibility.unit)

    def test_main_visibility_nautical_miles_command_fractional(self):
        command = MainVisibilityNauticalMilesCommand()
        metar = Metar()
        command.execute(metar, '1/2SM')
        self.assertEqual('1/2', metar.visibility.distance)
        self.assertEqual(LengthUnit.STATUTE_MILES, metar.visibility.unit)

    def test_minimal_visibility_command_sets_meters_unit(self):
        command = MinimalVisibilityCommand()
        metar = Metar()
        command.execute(metar, '3000NE')
        self.assertEqual(3000, metar.visibility.min_distance)
        self.assertEqual('NE', metar.visibility.min_direction)
        self.assertEqual(LengthUnit.METERS, metar.visibility.unit)

    def test_vertical_visibility_command_sets_feet_unit(self):
        command = VerticalVisibilityCommand()
        metar = Metar()
        command.execute(metar, 'VV002')
        self.assertEqual(200, metar.vertical_visibility)
        self.assertEqual(LengthUnit.FEET, metar.vertical_visibility_unit)

    def test_wind_shear_command_sets_feet_unit(self):
        command = WindShearCommand()
        ws = command.parse_wind_shear('WS020/24045KT')
        self.assertEqual(2000, ws.height)
        self.assertEqual(LengthUnit.FEET, ws.height_unit)
        self.assertEqual(240, ws.degrees)
        self.assertEqual(45, ws.speed)


if __name__ == '__main__':
    unittest.main()
