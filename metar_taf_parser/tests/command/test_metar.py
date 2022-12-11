import unittest

from metar_taf_parser.command.metar import RunwayCommand, CommandSupplier
from metar_taf_parser.model.enum import DepositType, DepositCoverage, DepositThickness, DepositBrakingCapacity
from metar_taf_parser.model.model import Metar


class MetarCommandTestCase(unittest.TestCase):

    def test_runway_command_execute(self):
        metar = Metar()
        command = RunwayCommand()

        command.execute(metar, 'R26/0600U')

        self.assertEqual(1, len(metar.runways_info))
        runway_info = metar.runways_info[0]
        self.assertEqual('26', runway_info.name)
        self.assertEqual(600, runway_info.min_range)
        self.assertEqual('U', runway_info.trend)

    def test_runway_command_execute_runway(self):
        metar = Metar()
        command = RunwayCommand()

        command.execute(metar, 'R26L/0550V700U')

        self.assertEqual(1, len(metar.runways_info))
        runway_info = metar.runways_info[0]

        self.assertEqual('26L', runway_info.name)
        self.assertEqual(550, runway_info.min_range)
        self.assertEqual(700, runway_info.max_range)
        self.assertEqual('U', runway_info.trend)

    def test_runway_command_execute_wrong_runway(self):
        metar = Metar()
        command = RunwayCommand()

        command.execute(metar, 'R26R/AZEAZEDS')

        self.assertEqual(0, len(metar.runways_info))

    def test_parse_runwway_visual_range_feet_variable(self):
        metar = Metar()

        command = RunwayCommand()

        command.execute(metar, 'R01L/0600V1000FT')
        self.assertEqual(1, len(metar.runways_info))
        self.assertEqual('01L', metar.runways_info[0].name)
        self.assertEqual(600, metar.runways_info[0].min_range)
        self.assertEqual(1000, metar.runways_info[0].max_range)
        self.assertEqual('', metar.runways_info[0].trend)

    def test_parse_runway_visual_range_feet_simple(self):
        metar = Metar()

        command = RunwayCommand()

        command.execute(metar, 'R01L/0800FT')
        self.assertEqual(1, len(metar.runways_info))
        self.assertEqual('01L', metar.runways_info[0].name)
        self.assertEqual(800, metar.runways_info[0].min_range)
        self.assertEqual('', metar.runways_info[0].trend)

    def test_parse_runway_deposit(self):
        metar = Metar()
        RunwayCommand().execute(metar, 'R05/629294')

        self.assertEqual(1, len(metar.runways_info))
        self.assertEqual('05', metar.runways_info[0].name)
        self.assertEqual(DepositType.SLUSH, metar.runways_info[0].deposit_type)
        self.assertEqual(DepositCoverage.FROM_11_TO_25, metar.runways_info[0].coverage)
        self.assertEqual(DepositThickness.THICKNESS_10, metar.runways_info[0].thickness)
        self.assertEqual(DepositBrakingCapacity.MEDIUM_GOOD, metar.runways_info[0].braking_capacity)

    def test_parse_runway_deposit_with_not_reported_type(self):
        metar = Metar()

        RunwayCommand().execute(metar, 'R05//29294')

        self.assertEqual(1, len(metar.runways_info))
        self.assertEqual('05', metar.runways_info[0].name)
        self.assertEqual(DepositType.NOT_REPORTED, metar.runways_info[0].deposit_type)
        self.assertEqual(DepositCoverage.FROM_11_TO_25, metar.runways_info[0].coverage)
        self.assertEqual(DepositThickness.THICKNESS_10, metar.runways_info[0].thickness)
        self.assertEqual(DepositBrakingCapacity.MEDIUM_GOOD, metar.runways_info[0].braking_capacity)

    def test_parse_runway_deposit_with_invalid_deposit(self):
        metar = Metar()

        RunwayCommand().execute(metar, 'R05/6292/4')
        self.assertEqual(0, len(metar.runways_info))

    def test_parse_runway_with_less_than_indicator_and_unit(self):
        metar = Metar()
        RunwayCommand().execute(metar, 'R01L/M0600FT')
        self.assertEqual('01L', metar.runways_info[0].name)
        self.assertEqual('M', metar.runways_info[0].indicator)
        self.assertEqual(600, metar.runways_info[0].min_range)

    def test_parse_runway_with_greater_than_indicator(self):
        metar = Metar()
        RunwayCommand().execute(metar, 'R01L/P0600FT')
        self.assertEqual('01L', metar.runways_info[0].name)
        self.assertEqual('P', metar.runways_info[0].indicator)
        self.assertEqual(600, metar.runways_info[0].min_range)

    def test_command_supplier(self):
        command_supplier = CommandSupplier()

        self.assertEqual(4, len(command_supplier._commands))


if __name__ == '__main__':
    unittest.main()
