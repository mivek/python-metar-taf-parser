import unittest

from metar_taf_parser.command.common import CloudCommand, WindCommand, CommandSupplier
from metar_taf_parser.model.enum import CloudQuantity, CloudType
from metar_taf_parser.model.model import Metar


class CommonTestCase(unittest.TestCase):
    def test_cloud_command_parse_sky_clear(self):
        command = CloudCommand()
        cloud = command.parse("SKC")
        self.assertIsNotNone(cloud)
        self.assertEqual(CloudQuantity.SKC, cloud.quantity)
        self.assertIsNone(cloud.height)
        self.assertIsNone(cloud.type)

    def test_cloud_command_parse_with_height(self):
        command = CloudCommand()

        cloud = command.parse('SCT016')

        self.assertEqual(CloudQuantity.SCT, cloud.quantity)
        self.assertEqual(1600, cloud.height)
        self.assertIsNone(cloud.type)

    def test_cloud_command_parse_with_type(self):
        command = CloudCommand()

        cloud = command.parse('SCT026CB')

        self.assertEqual(CloudQuantity.SCT, cloud.quantity)
        self.assertEqual(2600, cloud.height)
        self.assertEqual(CloudType.CB, cloud.type)

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


if __name__ == '__main__':
    unittest.main()
