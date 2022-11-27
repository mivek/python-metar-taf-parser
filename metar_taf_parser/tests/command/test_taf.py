import unittest

from metar_taf_parser.command.taf import IcingCommand, TurbulenceCommand, TAFCommandSupplier
from metar_taf_parser.model.enum import IcingIntensity, TurbulenceIntensity
from metar_taf_parser.model.model import ITafGroups


class TAFCommandTestCase(unittest.TestCase):

    def test_icing_command_can_parse(self):
        command = IcingCommand()
        self.assertTrue(command.can_parse('620304'))


    def test_icing_command_execute(self):
        code = '620304'
        itaf = ITafGroups()
        command = IcingCommand()

        command.execute(itaf, code)

        self.assertEqual(1, len(itaf.icings))
        self.assertEqual(IcingIntensity.LIGHT_RIME_ICING_CLOUD, itaf.icings[0].intensity)
        self.assertEqual(3000, itaf.icings[0].base_height)
        self.assertEqual(4000, itaf.icings[0].depth)


    def test_turbulence_command_can_parse(self):
        command = TurbulenceCommand()

        self.assertTrue(command.can_parse('520004'))


    def test_turbulence_command_execute(self):
        command = TurbulenceCommand()
        itaf = ITafGroups()

        command.execute(itaf, '520014')
        self.assertEqual(1, len(itaf.turbulence))
        self.assertEqual(TurbulenceIntensity.MODERATE_CLEAR_AIR_OCCASIONAL, itaf.turbulence[0].intensity)
        self.assertEqual(100, itaf.turbulence[0].base_height)
        self.assertEqual(4000, itaf.turbulence[0].depth)

    def test_command_supplier(self):
        command_supplier = TAFCommandSupplier()

        self.assertEqual(2, len(command_supplier._commands))



if __name__ == '__main__':
    unittest.main()
