import unittest

from parameterized import parameterized
from metar_taf_parser.commons import converter


class ConverterTest(unittest.TestCase):

    def test_converter(self):
        self.assertEqual('VRB', converter.degrees_to_cardinal('VRB'))

    @parameterized.expand([
        ("80", "E"),
        ("30", "NNE"),
        ("200", "SSW"),
        ("280", "W"),
        ("300", "WNW"),
        ("130", "SE"),
        ("230", "SW"),
        ("2", "N"),
        ("345", "NNW"),
        ("anything", "VRB"),
    ])
    def test_floor(self, input, expected):
        self.assertEqual(expected, converter.degrees_to_cardinal(input))

    def test_convert_visibility_10_km(self):
        self.assertEqual('> 10km', converter.convert_visibility('9999'))

    def test_convert_visibility(self):
        self.assertEqual('4512m', converter.convert_visibility('4512'))

    def test_convert_temperature_minus(self):
        self.assertEqual(-12, converter.convert_temperature('M12'))

    def test_convert_temperature(self):
        self.assertEqual(5, converter.convert_temperature('05'))

    def test_convert_inches_mercury_to_pascal(self):
        self.assertAlmostEqual(1013.20, converter.convert_inches_mercury_to_pascal(29.92), None, None, 0.01)


if __name__ == '__main__':
    unittest.main()
