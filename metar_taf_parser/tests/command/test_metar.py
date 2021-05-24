import unittest

from metar_taf_parser.command.metar import RunwayCommand, CommandSupplier
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

    def test_command_supplier(self):
        command_supplier = CommandSupplier()

        self.assertEqual(4, len(command_supplier._commands))


if __name__ == '__main__':
    unittest.main()
