import unittest

from metar_taf_parser.command.remark import CeilingHeightCommand, DefaultCommand, RemarkCommandSupplier


class RemarkCommandTestCase(unittest.TestCase):
    def test_ceiling_height(self):
        code = 'CIG 005V010'
        command = CeilingHeightCommand()
        (res, remarks) = command.execute(code, [])
        self.assertEqual('', res)
        self.assertEqual(1, len(remarks))

    def test_default_command(self):
        self.assertTrue(DefaultCommand().can_parse(''))

    def test_supplier_commands_list(self):
        self.assertEqual(25, len(RemarkCommandSupplier()._command_list))


if __name__ == '__main__':
    unittest.main()
