import unittest

from parameterized import parameterized

from metar_taf_parser.model.enum import Intensity, Phenomenon, Descriptive, DepositType, DepositCoverage, WeatherChangeType, CloudQuantity, CloudType, \
    TimeIndicator, TurbulenceIntensity, IcingIntensity
from metar_taf_parser.model.model import AbstractWeatherContainer, Visibility, Wind
from metar_taf_parser.parser.parser import AbstractParser, MetarParser, _parse_validity, _parse_temperature, TAFParser, \
    RemarkParser
from metar_taf_parser.commons.i18n import _


CLOUD_QUANTITY_BROKEN = 'CloudQuantity.BKN'
CONVERTER_NE = 'Converter.NE'
REMARK_AO1 = 'Remark.AO1'
REMARK_PRECIPITATION_BEG_END = 'Remark.Precipitation.Beg.End'
REMARK_SEA_LEVEL_PRESSURE = 'Remark.Sea.Level.Pressure'
TEN_KM = '> 10km'


class AbstractParserTestCase(unittest.TestCase):

    def test_parse_weather_condition(self):
        weather_condition = StubParser()._parse_weather_condition('-DZ')

        self.assertEqual(Intensity.LIGHT, weather_condition.intensity)
        self.assertIsNone(weather_condition.descriptive)
        self.assertEqual(1, len(weather_condition.phenomenons))
        self.assertEqual(Phenomenon.DRIZZLE, weather_condition.phenomenons[0])

    def test_parse_weather_condition_multiple_phenomenons(self):
        weather_condition = StubParser()._parse_weather_condition('SHRAGR')

        self.assertIsNone(weather_condition.intensity)
        self.assertEqual(Descriptive.SHOWERS, weather_condition.descriptive)
        self.assertListEqual([Phenomenon.RAIN, Phenomenon.HAIL], weather_condition.phenomenons)

    def test_parse_weather_condition_order(self):
        weather_condition = StubParser()._parse_weather_condition('-SNRA')

        self.assertEqual(Intensity.LIGHT, weather_condition.intensity)
        self.assertIsNone(weather_condition.descriptive)
        self.assertEqual(Phenomenon.SNOW, weather_condition.phenomenons[0])
        self.assertEqual(Phenomenon.RAIN, weather_condition.phenomenons[1])

    def test_tokenize(self):
        code = 'METAR KTTN 051853Z 04011KT 1 1/2SM VCTS SN FZFG BKN003 OVC010 M02/M02 A3006 RMK AO2 TSB40 SLP176 P0002 T10171017='
        expected = ['METAR', 'KTTN', '051853Z', '04011KT', '1 1/2SM', 'VCTS', 'SN', 'FZFG', 'BKN003', 'OVC010',
                    'M02/M02', 'A3006', 'RMK', 'AO2', 'TSB40', 'SLP176', 'P0002', 'T10171017']

        res = StubParser().tokenize(code)

        self.assertListEqual(expected, res)

    @parameterized.expand([
        ('05009KT', True),
        ('030V113', True),
        ('9999', True),
        ('6 1/2SM', True),
        ('1100w', True),
        ('VV002', True),
        ('CAVOK', True),
        ('SCT026CB', True),
        ('ZZZ026CV', None),
        ('+SHGSRA', True),
        ('+VFDR', None),
    ])
    def test_general_parse(self, input, expected):
        self.assertEqual(expected, StubParser().general_parse(StubWeatherContainer(), input))


class MetarParserTestCase(unittest.TestCase):

    def test_parse(self):
        input = 'LFPG 170830Z 00000KT 0350 R27L/0375N R09R/0175N R26R/0500D R08L/0400N R26L/0275D R08R/0250N R27R/0300N R09L/0200N FG SCT000 M01/M01 Q1026 NOSIG'

        metar = MetarParser().parse(input)

        self.assertEqual('LFPG', metar.station)
        self.assertEqual(17, metar.day)
        self.assertEqual(8, metar.time.hour)
        self.assertEqual(30, metar.time.minute)
        self.assertIsNotNone(metar.wind)
        self.assertEqual(0, metar.wind.speed)
        self.assertEqual('N', metar.wind.direction)
        self.assertEqual('KT', metar.wind.unit)
        self.assertIsNotNone(metar.visibility)
        self.assertEqual('350m', metar.visibility.distance)
        self.assertEqual(8, len(metar.runways_info))
        self.assertEqual('27L', metar.runways_info[0].name)
        self.assertEqual(375, metar.runways_info[0].min_range)
        self.assertEqual('N', metar.runways_info[0].trend)

    def test_parse_with_tempo(self):
        metar = MetarParser().parse(
            'LFBG 081130Z AUTO 23012KT 9999 SCT022 BKN072 BKN090 22/16 Q1011 TEMPO 26015G25KT 3000 TSRA SCT025CB BKN050')

        self.assertTrue(metar._is_auto)
        self.assertEqual(3, len(metar.clouds))
        self.assertEqual(1, len(metar.trends))

        trend = metar.trends[0]

        self.assertEqual(WeatherChangeType.TEMPO, trend.type)
        self.assertIsNotNone(trend.wind)
        self.assertEqual(260, trend.wind.degrees)
        self.assertEqual(15, trend.wind.speed)
        self.assertEqual(25, trend.wind.gust)
        self.assertEqual(0, len(trend.times))
        self.assertEqual('3000m', trend.visibility.distance)
        self.assertEqual(1, len(trend.weather_conditions))

        wc = trend.weather_conditions[0]

        self.assertEqual(Phenomenon.RAIN, wc.phenomenons[0])
        self.assertEqual(2, len(trend.clouds))
        self.assertEqual(CloudQuantity.SCT, trend.clouds[0].quantity)
        self.assertEqual(2500, trend.clouds[0].height)
        self.assertEqual(CloudType.CB, trend.clouds[0].type)
        self.assertEqual(CloudQuantity.BKN, trend.clouds[1].quantity)
        self.assertEqual(5000, trend.clouds[1].height)
        self.assertIsNone(trend.clouds[1].type)

    def test_parse_with_tempo_becmg(self):
        metar = MetarParser().parse('LFRM 081630Z AUTO 30007KT 260V360 9999 24/15 Q1008 TEMPO SHRA BECMG SKC')

        self.assertEqual(2, len(metar.trends))
        self.assertEqual(WeatherChangeType.TEMPO, metar.trends[0].type)
        self.assertEqual(1, len(metar.trends[0].weather_conditions))
        self.assertEqual(Descriptive.SHOWERS, metar.trends[0].weather_conditions[0].descriptive)
        self.assertEqual(Phenomenon.RAIN, metar.trends[0].weather_conditions[0].phenomenons[0])
        self.assertEqual(WeatherChangeType.BECMG, metar.trends[1].type)
        self.assertEqual(1, len(metar.trends[1].clouds))

    def test_parse_with_tempo_fm(self):
        metar = MetarParser().parse('LFRM 081630Z AUTO 30007KT 260V360 9999 24/15 Q1008 TEMPO FM1830 SHRA')

        self.assertEqual(1, len(metar.trends))
        self.assertEqual(WeatherChangeType.TEMPO, metar.trends[0].type)
        self.assertEqual(1, len(metar.trends[0].weather_conditions))

        trend = metar.trends[0]

        self.assertEqual(Descriptive.SHOWERS, trend.weather_conditions[0].descriptive)
        self.assertEqual(1, len(trend.weather_conditions[0].phenomenons))
        self.assertEqual(TimeIndicator.FM, trend.times[0].type)
        self.assertEqual(18, trend.times[0].time.hour)
        self.assertEqual(30, trend.times[0].time.minute)

    def test_parse_with_tempo_tl(self):
        metar = MetarParser().parse('LFRM 081630Z AUTO 30007KT 260V360 9999 24/15 Q1008 TEMPO FM1700 TL1830 SHRA')

        self.assertEqual(1, len(metar.trends))
        self.assertEqual(WeatherChangeType.TEMPO, metar.trends[0].type)
        self.assertEqual(1, len(metar.trends[0].weather_conditions))
        trend = metar.trends[0]

        self.assertEqual(Descriptive.SHOWERS, trend.weather_conditions[0].descriptive)
        self.assertEqual(1, len(trend.weather_conditions[0].phenomenons))
        self.assertEqual(Phenomenon.RAIN, trend.weather_conditions[0].phenomenons[0])
        self.assertEqual(TimeIndicator.FM, trend.times[0].type)
        self.assertEqual(17, trend.times[0].time.hour)
        self.assertEqual(0, trend.times[0].time.minute)
        self.assertEqual(TimeIndicator.TL, trend.times[1].type)
        self.assertEqual(18, trend.times[1].time.hour)
        self.assertEqual(30, trend.times[1].time.minute)
        self.assertEqual(TEN_KM, metar.visibility.distance)

    def test_parse_with_min_visibility(self):
        metar = MetarParser().parse('LFPG 161430Z 24015G25KT 5000 1100w')

        self.assertEqual(16, metar.day)
        self.assertEqual(14, metar.time.hour)
        self.assertEqual(30, metar.time.minute)

        self.assertEqual(240, metar.wind.degrees)
        self.assertEqual(15, metar.wind.speed)
        self.assertEqual(25, metar.wind.gust)
        self.assertEqual('5000m', metar.visibility.distance)
        self.assertEqual(1100, metar.visibility.min_distance)
        self.assertEqual('w', metar.visibility.min_direction)

    def test_parse_variation_wind(self):
        metar = MetarParser().parse('LFPG 161430Z 24015G25KT 180V300')

        self.assertEqual(240, metar.wind.degrees)
        self.assertEqual(15, metar.wind.speed)
        self.assertEqual(25, metar.wind.gust)
        self.assertEqual('KT', metar.wind.unit)
        self.assertEqual(180, metar.wind.min_variation)
        self.assertEqual(300, metar.wind.max_variation)

    def test_parse_with_vertical_visibility(self):
        metar = MetarParser().parse('LFLL 160730Z 28002KT 0350 FG VV002')

        self.assertEqual(16, metar.day)
        self.assertEqual(7, metar.time.hour)
        self.assertEqual(30, metar.time.minute)
        self.assertEqual(280, metar.wind.degrees)
        self.assertEqual(2, metar.wind.speed)
        self.assertEqual('350m', metar.visibility.distance)
        self.assertEqual(200, metar.vertical_visibility)
        self.assertEqual(Phenomenon.FOG, metar.weather_conditions[0].phenomenons[0])

    def test_parse_visibility_Ndv(self):
        metar = MetarParser().parse('LSZL 300320Z AUTO 00000KT 9999NDV BKN060 OVC074 00/M04 Q1001\n RMK=')

        self.assertEqual(TEN_KM, metar.visibility.distance)

    def test_parse_with_cavok(self):
        metar = MetarParser().parse('LFPG 212030Z 03003KT CAVOK 09/06 Q1031 NOSIG')

        self.assertTrue(metar.cavok)
        self.assertEqual(TEN_KM, metar.visibility.distance)
        self.assertEqual(9, metar.temperature)
        self.assertEqual(6, metar.dew_point)
        self.assertEqual(1031, metar.altimeter)
        self.assertTrue(metar.nosig)

    def test_parse_altimeter_mercury(self):
        metar = MetarParser().parse('KTTN 051853Z 04011KT 9999 VCTS SN FZFG BKN003 OVC010 M02/M02 A3006')

        self.assertEqual(1017, metar.altimeter)
        self.assertEqual(3, len(metar.weather_conditions))

    def test_parse_wind_alternative_form(self):
        metar = MetarParser().parse('ENLK 081350Z 26026G40 240V300 9999 VCSH FEW025 BKN030 02/M01 Q0996')

        self.assertEqual(260, metar.wind.degrees)
        self.assertEqual(26, metar.wind.speed)
        self.assertEqual(40, metar.wind.gust)
        self.assertEqual('KT', metar.wind.unit)
        self.assertEqual(240, metar.wind.min_variation)
        self.assertEqual(300, metar.wind.max_variation)

    def test_parse_with_descriptive_only(self):
        metar = MetarParser().parse('AGGH 140340Z 05010KT 9999 TS FEW020 SCT021CB BKN300 32/26 Q1010')

        self.assertEqual(1, len(metar.weather_conditions))
        self.assertEqual(Descriptive.THUNDERSTORM, metar.weather_conditions[0].descriptive)

    def test_parse_with_runway_deposit(self):
        metar = MetarParser().parse('UNAA 240830Z 34002MPS CAVOK M14/M18 Q1019 NOSIG RMK QFE741')

        self.assertEqual('UNAA', metar.station)
        self.assertEqual(340, metar.wind.degrees)
        self.assertEqual(2, metar.wind.speed)
        self.assertEqual('MPS', metar.wind.unit)
        self.assertTrue(metar.cavok)
        self.assertTrue(metar.nosig)
        self.assertEqual('QFE741', metar.remark)
        self.assertEqual(1, len(metar.remarks))

    def test_parse_with_nil(self):
        metar = MetarParser().parse('SVMC 211703Z AUTO NIL')

        self.assertTrue(metar.nil)

    def test_parse_with_unknown_cloudtype(self):
        metar = MetarParser().parse('EKVG 291550Z AUTO 13009KT 9999 BKN037/// BKN048/// 07/06 Q1009 RMK FEW011/// FEW035/// WIND SKEID 13020KT')

        self.assertIsNotNone(metar)
        self.assertEqual('EKVG', metar.station)
        self.assertEqual(2, len(metar.clouds))

    def test_parseVC(self):

        metar = MetarParser().parse('CYVM 282100Z 36028G36KT 1SM -SN DRSN VCBLSN OVC008 M03/M04 A2935 RMK SN2ST8 LAST STFFD OBS/NXT 291200UTC SLP940')

        self.assertEqual(3, len(metar.weather_conditions))
        self.assertEqual(Intensity.LIGHT, metar.weather_conditions[0].intensity)
        self.assertEqual(Phenomenon.SNOW, metar.weather_conditions[0].phenomenons[0])
        self.assertEqual(Descriptive.DRIFTING, metar.weather_conditions[1].descriptive)
        self.assertEqual(Phenomenon.SNOW, metar.weather_conditions[1].phenomenons[0])
        self.assertEqual(Intensity.IN_VICINITY, metar.weather_conditions[2].intensity)
        self.assertEqual(Descriptive.BLOWING, metar.weather_conditions[2].descriptive)
        self.assertEqual(Phenomenon.SNOW, metar.weather_conditions[2].phenomenons[0])

    def test_parse_runway_deposit(self):

        metar = MetarParser().parse('UUDD 212100Z 20005MPS 8000 -FZRA SCT005 M01/M02 Q1010 R14R/590335 NOSIG')

        self.assertEqual('UUDD', metar.station)
        self.assertEqual(1, len(metar.runways_info))
        self.assertEqual('14R', metar.runways_info[0].name)
        self.assertEqual(DepositType.WET_SNOW, metar.runways_info[0].deposit_type)
        self.assertEqual(DepositCoverage.FROM_51_TO_100, metar.runways_info[0].coverage)
        self.assertEqual('03 mm', metar.runways_info[0].thickness)
        self.assertEqual(_('DepositBrakingCapacity.default').format(0.35), metar.runways_info[0].braking_capacity)


class FunctionTestCase(unittest.TestCase):

    def test_parse_visibility(self):
        validity = _parse_validity('3118/0124')

        self.assertEqual(31, validity.start_day)
        self.assertEqual(18, validity.start_hour)
        self.assertEqual(1, validity.end_day)
        self.assertEqual(24, validity.end_hour)

    def test_parse_temperature_max(self):
        temperature = _parse_temperature('TX15/0612Z')
        self.assertEqual(15, temperature.temperature)
        self.assertEqual(6, temperature.day)
        self.assertEqual(12, temperature.hour)

    def test_parse_temperature_min(self):
        temperature = _parse_temperature('TNM02/0612Z')

        self.assertEqual(-2, temperature.temperature)
        self.assertEqual(6, temperature.day)
        self.assertEqual(12, temperature.hour)


class TAFParserTestCase(unittest.TestCase):

    def test_parse_with_invalid_line_breaks(self):
        code = 'TAF LFPG 150500Z 1506/1612 17005KT 6000 SCT012 \n' + 'TEMPO 1506/1509 3000 BR BKN006 PROB40 \n' + 'TEMPO 1506/1508 0400 BCFG BKN002 PROB40 \n' + 'TEMPO 1512/1516 4000 -SHRA FEW030TCU BKN040 \n' + 'BECMG 1520/1522 CAVOK \n' + 'TEMPO 1603/1608 3000 BR BKN006 PROB40 \n TEMPO 1604/1607 0400 BCFG BKN002 TX17/1512Z TN07/1605Z'

        taf = TAFParser().parse(code)

        self.assertEqual('LFPG', taf.station)
        self.assertEqual(15, taf.day)
        self.assertEqual(5, taf.time.hour)
        self.assertEqual(0, taf.time.minute)

        self.assertEqual(15, taf.validity.start_day)
        self.assertEqual(6, taf.validity.start_hour)
        self.assertEqual(16, taf.validity.end_day)
        self.assertEqual(12, taf.validity.end_hour)

        self.assertEqual(170, taf.wind.degrees)
        self.assertEqual(5, taf.wind.speed)
        self.assertEqual(None, taf.wind.gust)
        self.assertEqual('KT', taf.wind.unit)

        self.assertEqual('6000m', taf.visibility.distance)

        self.assertEqual(1, len(taf.clouds))
        self.assertEqual(CloudQuantity.SCT, taf.clouds[0].quantity)
        self.assertIsNone(taf.clouds[0].type)
        self.assertEqual(1200, taf.clouds[0].height)

        self.assertEqual(0, len(taf.weather_conditions))

        self.assertEqual(6, len(taf.trends))

        # First trend
        trend0 = taf.trends[0]

        self.assertEqual(WeatherChangeType.TEMPO, trend0.type)
        self.assertEqual(15, trend0.validity.start_day)
        self.assertEqual(6, trend0.validity.start_hour)
        self.assertEqual(15, trend0.validity.end_day)
        self.assertEqual(9, trend0.validity.end_hour)
        self.assertEqual('3000m', trend0.visibility.distance)
        self.assertEqual(1, len(trend0.weather_conditions))
        self.assertIsNone(trend0.weather_conditions[0].intensity)
        self.assertIsNone(trend0.weather_conditions[0].descriptive)
        self.assertEqual(Phenomenon.MIST, trend0.weather_conditions[0].phenomenons[0])
        self.assertEqual(1, len(trend0.clouds))
        self.assertEqual(CloudQuantity.BKN, trend0.clouds[0].quantity)
        self.assertIsNone(trend0.clouds[0].type)

        # Second trend
        trend_1 = taf.trends[1]
        self.assertEqual(WeatherChangeType.TEMPO, trend_1.type)
        self.assertEqual(15, trend_1.validity.start_day)
        self.assertEqual(6, trend_1.validity.start_hour)
        self.assertEqual(15, trend_1.validity.end_day)
        self.assertEqual(8, trend_1.validity.end_hour)
        self.assertIsNone(trend_1.wind)
        self.assertEqual('400m', trend_1.visibility.distance)
        self.assertEqual(1, len(trend_1.weather_conditions))
        self.assertIsNone(trend_1.weather_conditions[0].intensity)
        self.assertEqual(Descriptive.PATCHES, trend_1.weather_conditions[0].descriptive)
        self.assertEqual(1, len(trend_1.weather_conditions[0].phenomenons))
        self.assertEqual(Phenomenon.FOG, trend_1.weather_conditions[0].phenomenons[0])
        self.assertEqual(1, len(trend_1.clouds))
        self.assertEqual(CloudQuantity.BKN, trend_1.clouds[0].quantity)
        self.assertEqual(200, trend_1.clouds[0].height)
        self.assertEqual(40, trend_1.probability)

        trend_2 = taf.trends[2]
        self.assertEqual(WeatherChangeType.TEMPO, trend_2.type)
        self.assertEqual(15, trend_2.validity.start_day)
        self.assertEqual(12, trend_2.validity.start_hour)
        self.assertEqual(15, trend_2.validity.end_day)
        self.assertEqual(16, trend_2.validity.end_hour)
        self.assertEqual('4000m', trend_2.visibility.distance)
        self.assertEqual(1, len(trend_2.weather_conditions))
        self.assertEqual(Intensity.LIGHT, trend_2.weather_conditions[0].intensity)
        self.assertEqual(Descriptive.SHOWERS, trend_2.weather_conditions[0].descriptive)
        self.assertEqual(1, len(trend_2.weather_conditions[0].phenomenons))
        self.assertEqual(Phenomenon.RAIN, trend_2.weather_conditions[0].phenomenons[0])
        self.assertEqual(2, len(trend_2.clouds))
        self.assertEqual(CloudQuantity.FEW, trend_2.clouds[0].quantity)
        self.assertEqual(CloudType.TCU, trend_2.clouds[0].type)
        self.assertEqual(CloudQuantity.BKN, trend_2.clouds[1].quantity)
        self.assertIsNone(trend_2.clouds[1].type)
        self.assertEqual(40, trend_2.probability)

        trend_3 = taf.trends[3]
        self.assertEqual(WeatherChangeType.BECMG, trend_3.type)
        self.assertEqual(15, trend_3.validity.start_day)
        self.assertEqual(20, trend_3.validity.start_hour)
        self.assertEqual(15, trend_3.validity.end_day)
        self.assertEqual(22, trend_3.validity.end_hour)

        # Fourth Tempo
        trend_4 = taf.trends[4]
        self.assertEqual(16, trend_4.validity.start_day)
        self.assertEqual(3, trend_4.validity.start_hour)
        self.assertEqual(16, trend_4.validity.end_day)
        self.assertEqual(8, trend_4.validity.end_hour)
        self.assertEqual("3000m", trend_4.visibility.distance)
        self.assertEqual(1, len(trend_4.weather_conditions))
        self.assertIsNone(trend_4.weather_conditions[0].intensity)
        self.assertIsNone(trend_4.weather_conditions[0].descriptive)
        self.assertEqual(1, len(trend_4.weather_conditions[0].phenomenons))
        self.assertEqual(Phenomenon.MIST, trend_4.weather_conditions[0].phenomenons[0])
        self.assertEqual(1, len(trend_4.clouds))
        self.assertEqual(CloudQuantity.BKN, trend_4.clouds[0].quantity)
        self.assertIsNone(trend_4.clouds[0].type)
        self.assertIsNone(trend_4.probability)

        # Fifth Tempo
        trend_5 = taf.trends[5]
        self.assertEqual(16, trend_5.validity.start_day)
        self.assertEqual(4, trend_5.validity.start_hour)
        self.assertEqual(16, trend_5.validity.end_day)
        self.assertEqual(7, trend_5.validity.end_hour)
        self.assertEqual("400m", trend_5.visibility.distance)
        self.assertEqual(1, len(trend_5.weather_conditions))
        self.assertIsNone(trend_5.weather_conditions[0].intensity)
        self.assertEqual(Descriptive.PATCHES, trend_5.weather_conditions[0].descriptive)
        self.assertEqual(1, len(trend_5.weather_conditions[0].phenomenons))
        self.assertEqual(Phenomenon.FOG, trend_5.weather_conditions[0].phenomenons[0])
        self.assertEqual(1, len(trend_5.clouds))
        self.assertEqual(CloudQuantity.BKN, trend_5.clouds[0].quantity)
        self.assertIsNone(trend_5.clouds[0].type)
        self.assertEqual(40, trend_5.probability)

    def test_parse_without_line_breaks(self):
        taf = TAFParser().parse(
            'TAF LSZH 292025Z 2921/3103 VRB03KT 9999 FEW020 BKN080 TX20/3014Z TN06/3003Z PROB30 TEMPO 2921/2923 SHRA BECMG 3001/3004 4000 MIFG NSC PROB40 3003/3007 1500 BCFG SCT004 PROB30 3004/3007 0800 FG VV003 BECMG 3006/3009 9999 FEW030 PROB40 TEMPO 3012/3017 30008KT')

        # Check on time delivery.
        self.assertEqual(29, taf.day)
        self.assertEqual(20, taf.time.hour)
        self.assertEqual(25, taf.time.minute)
        # Checks on validity.
        self.assertEqual(29, taf.validity.start_day)
        self.assertEqual(21, taf.validity.start_hour)
        self.assertEqual(31, taf.validity.end_day)
        self.assertEqual(3, taf.validity.end_hour)
        # Checks on wind.
        self.assertIsNone(taf.wind.degrees)
        self.assertEqual("VRB", taf.wind.direction)
        self.assertEqual(3, taf.wind.speed)
        self.assertIsNone(taf.wind.gust)
        self.assertEqual("KT", taf.wind.unit)
        # Checks on visibility.
        self.assertEqual(TEN_KM, taf.visibility.distance)
        # Check on clouds.
        self.assertEqual(2, len(taf.clouds))
        self.assertEqual(CloudQuantity.FEW, taf.clouds[0].quantity)
        self.assertEqual(2000, taf.clouds[0].height)
        self.assertIsNone(taf.clouds[0].type)

        self.assertEqual(CloudQuantity.BKN, taf.clouds[1].quantity)
        self.assertEqual(8000, taf.clouds[1].height)
        self.assertIsNone(taf.clouds[1].type)
        # Check that no weatherCondition
        self.assertEqual(0, len(taf.weather_conditions))
        # Check max temperature
        self.assertEqual(30, taf.max_temperature.day)
        self.assertEqual(14, taf.max_temperature.hour)
        self.assertEqual(20, taf.max_temperature.temperature)
        # Check min temperature
        self.assertEqual(30, taf.min_temperature.day)
        self.assertEqual(3, taf.min_temperature.hour)
        self.assertEqual(6, taf.min_temperature.temperature)

        self.assertEqual(2, len(taf.tempos()))
        self.assertEqual(2, len(taf.becmgs()))
        self.assertEqual(2, len(taf.probs()))
        self.assertEqual(0, len(taf.fms()))

        # First TEMPO
        tempo0 = taf.trends[0]
        self.assertEqual(29, tempo0.validity.start_day)
        self.assertEqual(21, tempo0.validity.start_hour)
        self.assertEqual(29, tempo0.validity.end_day)
        self.assertEqual(23, tempo0.validity.end_hour)
        self.assertEqual(1, len(tempo0.weather_conditions))
        self.assertIsNone(tempo0.weather_conditions[0].intensity)
        self.assertEqual(Descriptive.SHOWERS, tempo0.weather_conditions[0].descriptive)
        self.assertEqual(1, len(tempo0.weather_conditions[0].phenomenons))
        self.assertEqual(Phenomenon.RAIN, tempo0.weather_conditions[0].phenomenons[0])
        self.assertEqual(30, tempo0.probability)

        # First BECOMG
        becmg0 = taf.trends[1]
        self.assertEqual(30, becmg0.validity.start_day)
        self.assertEqual(1, becmg0.validity.start_hour)
        self.assertEqual(30, becmg0.validity.end_day)
        self.assertEqual(4, becmg0.validity.end_hour)
        self.assertEqual("4000m", becmg0.visibility.distance)
        self.assertIsNone(becmg0.weather_conditions[0].intensity)
        self.assertEqual(Descriptive.SHALLOW, becmg0.weather_conditions[0].descriptive)
        self.assertEqual(1, len(becmg0.weather_conditions[0].phenomenons))
        self.assertEqual(Phenomenon.FOG, becmg0.weather_conditions[0].phenomenons[0])
        self.assertEqual(CloudQuantity.NSC, becmg0.clouds[0].quantity)

        # First PROB
        prob0 = taf.trends[2]
        self.assertEqual(30, prob0.validity.start_day)
        self.assertEqual(3, prob0.validity.start_hour)
        self.assertEqual(30, prob0.validity.end_day)
        self.assertEqual(7, prob0.validity.end_hour)
        self.assertEqual("1500m", prob0.visibility.distance)
        self.assertIsNone(prob0.weather_conditions[0].intensity)
        self.assertEqual(Descriptive.PATCHES, prob0.weather_conditions[0].descriptive)
        self.assertEqual(1, len(prob0.weather_conditions[0].phenomenons))
        self.assertEqual(Phenomenon.FOG, prob0.weather_conditions[0].phenomenons[0])
        self.assertEqual(1, len(prob0.clouds))
        self.assertEqual(CloudQuantity.SCT, prob0.clouds[0].quantity)
        self.assertEqual(400, prob0.clouds[0].height)
        self.assertIsNone(prob0.clouds[0].type)
        self.assertEqual(40, prob0.probability)

        # Second PROB
        prob1 = taf.trends[3]
        self.assertEqual(30, prob1.validity.start_day)
        self.assertEqual(4, prob1.validity.start_hour)
        self.assertEqual(30, prob1.validity.end_day)
        self.assertEqual(7, prob1.validity.end_hour)
        self.assertEqual("800m", prob1.visibility.distance)
        self.assertIsNone(prob1.weather_conditions[0].intensity)
        self.assertIsNone(prob1.weather_conditions[0].descriptive)
        self.assertEqual(1, len(prob1.weather_conditions[0].phenomenons))
        self.assertEqual(Phenomenon.FOG, prob1.weather_conditions[0].phenomenons[0])
        self.assertEqual(300, prob1.vertical_visibility)
        self.assertEqual(0, len(prob1.clouds))
        self.assertEqual(30, prob1.probability)

        # Second BECOMG
        becmg1 = taf.trends[4]
        self.assertEqual(30, becmg1.validity.start_day)
        self.assertEqual(6, becmg1.validity.start_hour)
        self.assertEqual(30, becmg1.validity.end_day)
        self.assertEqual(9, becmg1.validity.end_hour)
        self.assertEqual(TEN_KM, becmg1.visibility.distance)
        self.assertEqual(0, len(becmg1.weather_conditions))
        self.assertEqual(1, len(becmg1.clouds))
        self.assertEqual(CloudQuantity.FEW, becmg1.clouds[0].quantity)
        self.assertEqual(3000, becmg1.clouds[0].height)
        self.assertIsNone(becmg1.clouds[0].type)

        # Second TEMPO
        tempo1 = taf.trends[5]
        self.assertEqual(30, tempo1.validity.start_day)
        self.assertEqual(12, tempo1.validity.start_hour)
        self.assertEqual(30, tempo1.validity.end_day)
        self.assertEqual(17, tempo1.validity.end_hour)
        self.assertEqual(0, len(tempo1.weather_conditions))
        self.assertEqual(300, tempo1.wind.degrees)
        self.assertEqual(8, tempo1.wind.speed)
        self.assertIsNone(tempo1.wind.gust)
        self.assertEqual("KT", tempo1.wind.unit)
        self.assertEqual(40, tempo1.probability)

    def test_parse_without_line_breaks_and_ending_temperature(self):
        taf = TAFParser().parse(
            'TAF KLSV 120700Z 1207/1313 VRB06KT 9999 SCT250 QNH2992INS BECMG 1217/1218 10010G15KT 9999 SCT250 QNH2980INS BECMG 1303/1304 VRB06KT 9999 FEW250 QNH2979INS TX42/1223Z TN24/1213Z')

        # Check on time delivery.
        self.assertEqual(12, taf.day)
        self.assertEqual(7, taf.time.hour)
        self.assertEqual(0, taf.time.minute)
        # Checks on validity.
        self.assertEqual(12, taf.validity.start_day)
        self.assertEqual(7, taf.validity.start_hour)
        self.assertEqual(13, taf.validity.end_day)
        self.assertEqual(13, taf.validity.end_hour)
        # Checks on wind.
        self.assertIsNone(taf.wind.degrees)
        self.assertEqual("VRB", taf.wind.direction)
        self.assertEqual(6, taf.wind.speed)
        self.assertIsNone(taf.wind.gust)
        self.assertEqual("KT", taf.wind.unit)
        # Checks on visibility.
        self.assertEqual(TEN_KM, taf.visibility.distance)
        # Check on clouds.
        self.assertEqual(1, len(taf.clouds))
        self.assertEqual(CloudQuantity.SCT, taf.clouds[0].quantity)
        self.assertEqual(25000, taf.clouds[0].height)
        self.assertIsNone(taf.clouds[0].type)

        # Check that no weatherCondition
        self.assertEqual(0, len(taf.weather_conditions))
        # Check max temperature
        self.assertEqual(12, taf.max_temperature.day)
        self.assertEqual(23, taf.max_temperature.hour)
        self.assertEqual(42, taf.max_temperature.temperature)
        # Check min temperature
        self.assertEqual(12, taf.min_temperature.day)
        self.assertEqual(13, taf.min_temperature.hour)
        self.assertEqual(24, taf.min_temperature.temperature)

        # Checks on BECOMGs.
        self.assertEqual(2, len(taf.trends))
        self.assertEqual(2, len(taf.becmgs()))

        # First BECOMG
        becmg0 = taf.trends[0]
        self.assertEqual(12, becmg0.validity.start_day)
        self.assertEqual(17, becmg0.validity.start_hour)
        self.assertEqual(12, becmg0.validity.end_day)
        self.assertEqual(18, becmg0.validity.end_hour)
        self.assertEqual(TEN_KM, becmg0.visibility.distance)
        self.assertEqual(0, len(becmg0.weather_conditions))
        self.assertEqual(CloudQuantity.SCT, becmg0.clouds[0].quantity)
        self.assertEqual(25000, becmg0.clouds[0].height)
        self.assertEqual(100, becmg0.wind.degrees)
        self.assertEqual(10, becmg0.wind.speed)
        self.assertEqual(15, becmg0.wind.gust)
        self.assertEqual("KT", becmg0.wind.unit)

        # Second BECOMG
        becmg1 = taf.trends[1]
        self.assertEqual(13, becmg1.validity.start_day)
        self.assertEqual(3, becmg1.validity.start_hour)
        self.assertEqual(13, becmg1.validity.end_day)
        self.assertEqual(4, becmg1.validity.end_hour)
        self.assertEqual(TEN_KM, becmg1.visibility.distance)
        self.assertIsNone(becmg1.wind.degrees)
        self.assertEqual("VRB", becmg1.wind.direction)
        self.assertEqual(6, becmg1.wind.speed)
        self.assertIsNone(becmg1.wind.gust)
        self.assertEqual("KT", becmg1.wind.unit)
        self.assertEqual(0, len(becmg1.weather_conditions))
        self.assertEqual(1, len(becmg1.clouds))
        self.assertEqual(CloudQuantity.FEW, becmg1.clouds[0].quantity)
        self.assertEqual(25000, becmg1.clouds[0].height)
        self.assertIsNone(becmg1.clouds[0].type)

    def test_parse_with_2_taf(self):
        taf = TAFParser().parse('TAF TAF LFPG 191100Z 1912/2018 02010KT 9999 FEW040 PROB30')

        self.assertIsNotNone(taf)
        self.assertEqual(1, len(taf.trends))
        self.assertEqual(30, taf.trends[0].probability)

    def test_parse_with_wind_shear(self):
        taf = TAFParser().parse('TAF KMKE 011530 0116/0218 WS020/24045KT FM010200 17005KT P6SM SKC WS020/23055KT')

        # THEN the windshear of the principle part is decoded
        self.assertEqual(2000, taf.wind_shear.height)
        self.assertEqual(240, taf.wind_shear.degrees)
        self.assertEqual(45, taf.wind_shear.speed)

        # Checks on the from part.
        fm = taf.trends[0]
        self.assertIsNotNone(fm)
        # Checks on the wind of the FM
        self.assertIsNotNone(fm.wind)
        self.assertEqual(170, fm.wind.degrees)
        self.assertEqual(5, fm.wind.speed)
        # Checks on the wind shear of the fm
        self.assertIsNotNone(fm.wind_shear)
        self.assertEqual(2000, fm.wind_shear.height)
        self.assertEqual(230, fm.wind_shear.degrees)
        self.assertEqual(55, fm.wind_shear.speed)

    def test_parse_with_nautical_miles_visibility(self):
        taf = TAFParser().parse(
            'TAF AMD CZBF 300939Z 3010/3022 VRB03KT 6SM -SN OVC015 TEMPO 3010/3012 11/2SM -SN OVC009 \nFM301200 10008KT 2SM -SN OVC010 TEMPO 3012/3022 3/4SM -SN VV007 RMK FCST BASED ON AUTO OBS. NXT FCST BY 301400Z')

        # THEN the visibility of the main event is 6 SM
        self.assertEqual("6SM", taf.visibility.distance)
        # THEN the visibility of the first tempo is 11/2 SM
        self.assertEqual("11/2SM", taf.trends[0].visibility.distance)
        # THEN the visibility of the second tempo is 3/4 SM
        self.assertEqual("3/4SM", taf.trends[2].visibility.distance)
        # Then the visibility of the FROM part is 2SN
        self.assertEqual("2SM", taf.trends[1].visibility.distance)
        self.assertTrue(taf.amendment)

    def test_parse_with_remark(self):
        taf = TAFParser().parse(
            'TAF CZBF 300939Z 3010/3022 VRB03KT 6SM -SN OVC015 RMK FCST BASED ON AUTO OBS. NXT FCST BY 301400Z\n TEMPO 3010/3012 11/2SM -SN OVC009 FM301200 10008KT 2SM -SN OVC010 \nTEMPO 3012/3022 3/4SM -SN VV007')

        self.assertIsNotNone(taf)
        self.assertIsNotNone(taf.remark)
        self.assertEqual(9, len(taf.remarks))

    def test_parse_with_trend_remark(self):
        taf = TAFParser().parse(
            'TAF CZBF 300939Z 3010/3022 VRB03KT 6SM -SN OVC015\n TEMPO 3010/3012 11/2SM -SN OVC009 FM301200 10008KT 2SM -SN OVC010 TEMPO 3012/3022 3/4SM -SN VV007 RMK FCST BASED ON AUTO OBS. NXT FCST BY 301400Z')

        self.assertEqual(3, len(taf.trends))
        self.assertIsNotNone(taf.trends[2].remark)
        self.assertEqual(9, len(taf.trends[2].remarks))

    def test_parse_with_remarks_forecast(self):
        taf = TAFParser().parse(
            """TAF CYTL 121940Z 1220/1308
              TEMPO 1303/1308 2SM -SN RMK FCST BASED ON AUTO OBS. FCST BASED ON OBS BY OTHER SRCS. WIND SENSOR INOP. NXT FCST BY 130200Z"""
        )

        self.assertEqual(1, len(taf.tempos()))
        self.assertEqual(1, len(taf.tempos()[0].weather_conditions))
        self.assertEqual(Intensity.LIGHT, taf.tempos()[0].weather_conditions[0].intensity)
        self.assertEqual(1, len(taf.tempos()[0].weather_conditions[0].phenomenons))
        self.assertEqual(Phenomenon.SNOW, taf.tempos()[0].weather_conditions[0].phenomenons[0])

    def test_parse_trend_visibility(self):
        taf = TAFParser().parse(
            """TAF AMD KEWR 191303Z 1913/2018 09006KT 5SM -RA BR BKN007 OVC025
            FM191600 17007KT P6SM BKN020
            FM192100 26008KT P3SM SCT030 SCT050
            FM200000 29005KT P4SM SCT050
            FM200600 VRB03KT P9SM SCT050
            """
        )

        self.assertEqual('KEWR', taf.station)
        self.assertIsNotNone(taf.visibility)
        self.assertEqual('5SM', taf.visibility.distance)
        self.assertEqual(4, len(taf.fms()))
        self.assertEqual('P6SM', taf.fms()[0].visibility.distance)
        self.assertEqual('P3SM', taf.fms()[1].visibility.distance)
        self.assertEqual('P4SM', taf.fms()[2].visibility.distance)
        self.assertEqual('P9SM', taf.fms()[3].visibility.distance)

    def test_parse_canceled(self):
        taf = TAFParser().parse('TAF VTBD 281000Z 2812/2912 CNL=')
        self.assertTrue(taf.canceled)

    def test_parse_corrected(self):
        taf = TAFParser().parse('TAF COR EDDS 201148Z 2012/2112 31010KT CAVOK BECMG 2018/2021 33004KT BECMG 2106/2109 07005KT')
        self.assertTrue(taf.corrected)

    def test_parse_with_turbulence_and_icing(self):
        taf = TAFParser().parse(
            """TAF KLSV 222300Z 2223/2405 21020G35KT 8000 BLDU BKN160 530009 630009 QNH2941INS
              TEMPO 2223/2302 23035G52KT BKN150 560009
              BECMG 2305/2306 35015G25KT 9999 VCSH BKN140 520009 QNH2948INS
              BECMG 2316/2317 34010G18KT 9999 NSW SCT170 QNH2969INS TX28/2323Z TN12/2314Z
            """
        )

        self.assertEqual('KLSV', taf.station)
        self.assertEqual(210, taf.wind.degrees)
        self.assertEqual(20, taf.wind.speed)
        self.assertEqual(35, taf.wind.gust)
        self.assertEqual('KT', taf.wind.unit)

        self.assertEqual(TurbulenceIntensity.MODERATE_CLEAR_AIR_FREQUENT, taf.turbulence[0].intensity)
        self.assertEqual(0, taf.turbulence[0].base_height)
        self.assertEqual(9000, taf.turbulence[0].depth)

        self.assertEqual(IcingIntensity.LIGHT_CLEAR_ICING_PRECIPITATION, taf.icings[0].intensity)
        self.assertEqual(0, taf.icings[0].base_height)
        self.assertEqual(9000, taf.icings[0].depth)

    def test_parse_with_icings_turbulence_trends(self):
        taf = TAFParser().parse(
            """TAF AMD KNID 222300Z 0115/0215 21006KT 9999 SCT250 QNH2981INS
              BECMG 0116/0118 19014G22KT 9999 FEW120 SCT250 520009 520909 QNH2978INS WND 160V230
              BECMG 0118/0120 19018G26KT 9000 BLDU FEW003 FEW120 SCT250 530009 530909 QNH2972INS
              BECMG 0120/0122 19022G35KT 9000 BLDU FEW003 SCT120 BKN250 560009 560906 531509 QNH2967INS
              TEMPO 0122/0202 19030G40KT 1600 BLDUSA BKN002 SCT120 BKN250
              BECMG 0202/0204 20018G30KT 9999 NSW SCT120 BKN220 530008 530909 QNH2972INS
              BECMG 0208/0210 21015G25KT 9999 BKN120 BKN220 611208 530009 540909 QNH2974INS
              BECMG 0214/0215 22012G25KT 9999 BKN120 BKN220 611208 520009 540909 QNH2980INS
            """
        )

        self.assertIsNotNone(taf)
        self.assertEqual(6, len(taf.becmgs()))
        self.assertEqual(1, len(taf.tempos()))
        self.assertEqual(2, len(taf.becmgs()[0].turbulence))
        self.assertEqual(2, len(taf.becmgs()[1].turbulence))
        self.assertEqual(3, len(taf.becmgs()[2].turbulence))
        self.assertEqual(2, len(taf.becmgs()[3].turbulence))
        self.assertEqual(2, len(taf.becmgs()[4].turbulence))
        self.assertEqual(1, len(taf.becmgs()[4].icings))
        self.assertEqual(1, len(taf.becmgs()[5].icings))
        self.assertEqual(2, len(taf.becmgs()[5].turbulence))


class RemarkParserTestCase(unittest.TestCase):

    def test_parse_AO1(self):
        remarks = RemarkParser().parse('Token AO1 End of remark')

        self.assertEqual(5, len(remarks))
        self.assertEqual(_(REMARK_AO1), remarks[1])

    def test_parse_AO2(self):
        remarks = RemarkParser().parse('Token AO2 End of remark')

        self.assertEqual(5, len(remarks))
        self.assertEqual(_('Remark.AO2'), remarks[1])

    def test_parse_peak_wind_hour(self):
        remarks = RemarkParser().parse('AO1 PK WND 28045/15')

        self.assertEqual(2, len(remarks))
        self.assertEqual(_(REMARK_AO1), remarks[0])
        self.assertEqual(_('Remark.PeakWind').format('280', '45', '', '15'), remarks[1])

    def test_parse_peak_wind_another_hour(self):
        remarks = RemarkParser().parse('AO1 PK WND 28045/1515')

        self.assertEqual(2, len(remarks))
        self.assertEqual(_(REMARK_AO1), remarks[0])
        self.assertEqual(_('Remark.PeakWind').format('280', '45', '15', '15'), remarks[1])

    def test_parse_wind_shift_hour(self):
        remarks = RemarkParser().parse('AO1 WSHFT 30')

        self.assertEqual(2, len(remarks))
        self.assertEqual(_('Remark.WindShift').format('', 30), remarks[1])

    def test_parse_wind_shift(self):
        remarks = RemarkParser().parse('AO1 WSHFT 1530')

        self.assertEqual(2, len(remarks))
        self.assertEqual(_('Remark.WindShift').format(15, 30), remarks[1])

    def test_parse_wind_shift_frontal(self):
        remarks = RemarkParser().parse('AO1 WSHFT 1530 FROPA')

        self.assertEqual(2, len(remarks))
        self.assertEqual(_('Remark.WindShift.FROPA').format(15, 30), remarks[1])

    def test_parse_wind_shift_frontal_at_hour(self):
        remarks = RemarkParser().parse('AO1 WSHFT 30 FROPA')

        self.assertEqual(2, len(remarks))
        self.assertEqual(_('Remark.WindShift.FROPA').format('', 30), remarks[1])

    def test_parse_tower_visibility(self):
        remarks = RemarkParser().parse('AO1 TWR VIS 16 1/2')

        self.assertEqual(2, len(remarks))
        self.assertEqual(_('Remark.Tower.Visibility').format('16 1/2'), remarks[1])

    def test_parse_surface_visibility(self):
        remarks = RemarkParser().parse('AO1 SFC VIS 16 1/2')

        self.assertEqual(2, len(remarks))
        self.assertEqual(_('Remark.Surface.Visibility').format('16 1/2'), remarks[1])

    def test_parse_prevailing_visibility(self):
        remarks = RemarkParser().parse('AO1 VIS 1/2V2')

        self.assertEqual(2, len(remarks))
        self.assertEqual(_('Remark.Variable.Prevailing.Visibility').format('1/2', '2'), remarks[1])

    def test_parse_sector_visibility(self):
        remarks = RemarkParser().parse('AO1 VIS NE 2 1/2')

        self.assertEqual(2, len(remarks))
        self.assertEqual(_('Remark.Sector.Visibility').format(_(CONVERTER_NE), '2 1/2'), remarks[1])

    def test_parse_second_location_visibility(self):
        remarks = RemarkParser().parse('AO1 VIS 2 1/2 RWY11')

        self.assertEqual(2, len(remarks))
        self.assertEqual(_('Remark.Second.Location.Visibility').format('2 1/2', 'RWY11'), remarks[1])

    def test_parse_tornadic_activity_tornado(self):
        remarks = RemarkParser().parse('AO1 TORNADO B13 6 NE')

        self.assertEqual(2, len(remarks))
        self.assertEqual(
            _('Remark.Tornadic.Activity.Beginning').format(_('Remark.TORNADO'), '', 13, 6, _(CONVERTER_NE)),
            remarks[1])

    def test_parse_tornadic_activity_tornado_hour(self):
        remarks = RemarkParser().parse('AO1 TORNADO B1513 6 NE')

        self.assertEqual(2, len(remarks))
        self.assertEqual(
            _('Remark.Tornadic.Activity.Beginning').format(_('Remark.TORNADO'), 15, 13, 6, _(CONVERTER_NE)),
            remarks[1])

    def test_parse_tornadic_activity_funnel_cloud(self):
        remarks = RemarkParser().parse('AO1 FUNNEL CLOUD B1513E1630 6 NE')

        self.assertEqual(2, len(remarks))
        self.assertEqual(
            _('Remark.Tornadic.Activity.BegEnd').format(_('Remark.FUNNELCLOUD'), 15, 13, 16, 30, 6, _(CONVERTER_NE)),
            remarks[1])

    def test_parse_tornadic_activity_water_sprout_ending_time_minutes(self):
        remarks = RemarkParser().parse('AO1 WATERSPOUT E16 12 NE')

        self.assertEqual(2, len(remarks))
        self.assertEqual(
            _('Remark.Tornadic.Activity.Ending').format(_('Remark.WATERSPOUT'), '', 16, 12, _(CONVERTER_NE)),
            remarks[1])

    def test_parse_tornadic_activity_watersprout_ending_time(self):
        remarks = RemarkParser().parse('AO1 WATERSPOUT E1516 12 NE')

        self.assertEqual(2, len(remarks))
        self.assertEqual(
            _('Remark.Tornadic.Activity.Ending').format(_('Remark.WATERSPOUT'), 15, 16, 12, _(CONVERTER_NE)),
            remarks[1])

    def test_parse_precipitation_start_end(self):
        remarks = RemarkParser().parse('AO1 RAB05E30SNB1520E1655')

        self.assertEqual(3, len(remarks))
        self.assertEqual(_(REMARK_PRECIPITATION_BEG_END).format('', _('Phenomenon.RA'), '', '05', '', 30), remarks[1])
        self.assertEqual(_(REMARK_PRECIPITATION_BEG_END).format('', _('Phenomenon.SN'), 15, 20, 16, 55), remarks[2])

    def test_parse_precipitation_start_end_descriptive(self):
        remarks = RemarkParser().parse('AO1 SHRAB05E30SHSNB20E55')

        self.assertEqual(3, len(remarks))
        self.assertEqual(
            _(REMARK_PRECIPITATION_BEG_END).format(_('Descriptive.SH'), _('Phenomenon.RA'), '', '05', '', 30),
            remarks[1])
        self.assertEqual(
            _(REMARK_PRECIPITATION_BEG_END).format(_('Descriptive.SH'), _('Phenomenon.SN'), '', 20, '', 55),
            remarks[2])

    def test_parse_thunderstorm_start(self):
        remarks = RemarkParser().parse('AO1 TSB0159E30')

        self.assertEqual(2, len(remarks))
        self.assertEqual(_(REMARK_PRECIPITATION_BEG_END).format('', _('Phenomenon.TS'), '01', 59, '', 30), remarks[1])

    def test_parse_thunderstorm_location(self):
        remarks = RemarkParser().parse('AO1 TS SE')

        self.assertEqual(2, len(remarks))
        self.assertEqual(_('Remark.Thunderstorm.Location').format(_('Converter.SE')), remarks[1])

    def test_parse_thunderstorm_location_moving(self):
        remarks = RemarkParser().parse('AO1 TS SE MOV NE')

        self.assertEqual(2, len(remarks))
        self.assertEqual(_('Remark.Thunderstorm.Location.Moving').format(_('Converter.SE'), _(CONVERTER_NE)),
                         remarks[1])

    def test_parse_hail_size(self):
        remarks = RemarkParser().parse('AO1 GR 1 3/4')

        self.assertEqual(2, len(remarks))
        self.assertEqual(_('Remark.Hail').format('1 3/4'), remarks[1])

    def test_parse_hail_size_less_than(self):
        remarks = RemarkParser().parse('AO1 GR LESS THAN 1/4')

        self.assertEqual(2, len(remarks))
        self.assertEqual(_('Remark.Hail.LesserThan').format('1/4'), remarks[1])

    def test_parse_snow_pellets(self):
        remarks = RemarkParser().parse('AO1 GS MOD')

        self.assertEqual(2, len(remarks))
        self.assertEqual(_('Remark.Snow.Pellets').format(_('Remark.MOD')), remarks[1])

    def test_parse_virga_direction(self):
        remarks = RemarkParser().parse('AO1 VIRGA SW')

        self.assertEqual(2, len(remarks))
        self.assertEqual(_('Remark.Virga.Direction').format(_('Converter.SW')), remarks[1])

    def test_parse_virga(self):
        remarks = RemarkParser().parse('AO1 VIRGA')

        self.assertEqual(2, len(remarks))
        self.assertEqual(_('Remark.VIRGA'), remarks[1])

    def test_parse_ceiling_height(self):
        remarks = RemarkParser().parse('AO1 CIG 005V010')

        self.assertEqual(2, len(remarks))
        self.assertEqual(_('Remark.Ceiling.Height').format(500, 1000), remarks[1])

    def test_parse_obscurations(self):
        remarks = RemarkParser().parse('AO1 FU BKN020')

        self.assertEqual(2, len(remarks))
        self.assertEqual(_('Remark.Obscuration').format(_(CLOUD_QUANTITY_BROKEN), 2000, _('Phenomenon.FU')), remarks[1])

    def test_parse_variable_sky_condition_without_layer(self):
        remarks = RemarkParser().parse('BKN V OVC')

        self.assertEqual(_('Remark.Variable.Sky.Condition').format(_(CLOUD_QUANTITY_BROKEN), _('CloudQuantity.OVC')),
                         remarks[0])

    def test_parse_variable_sky_conditions(self):
        remarks = RemarkParser().parse('BKN014 V OVC')
        self.assertEqual(
            _('Remark.Variable.Sky.Condition.Height').format(1400, _(CLOUD_QUANTITY_BROKEN), _('CloudQuantity.OVC')),
            remarks[0])

    def test_parse_ceiling_second_location(self):
        remarks = RemarkParser().parse('CIG 002 RWY11')

        self.assertEqual(_('Remark.Ceiling.Second.Location').format(200, 'RWY11'), remarks[0])

    def test_parse_sea_level_pressure(self):
        remarks = RemarkParser().parse('AO1 SLP134')

        self.assertEqual(_(REMARK_SEA_LEVEL_PRESSURE).format('1013.4'), remarks[1])

    def test_parse_sea_level_pressure_lower(self):
        remarks = RemarkParser().parse('AO1 SLP982')

        self.assertEqual(_(REMARK_SEA_LEVEL_PRESSURE).format('998.2'), remarks[1])

    def test_parse_snow_increasing_rapidly(self):
        remarks = RemarkParser().parse('AO1 SNINCR 2/10')
        self.assertEqual(_('Remark.Snow.Increasing.Rapidly').format(2, 10), remarks[1])

    def test_parse_rmk_slp(self):
        remarks = RemarkParser().parse('CF1AC8 CF TR SLP091 DENSITY ALT 200FT')
        self.assertEqual(_(REMARK_SEA_LEVEL_PRESSURE).format('1009.1'), remarks[3])

    def test_parse_hourly_maximum_minimum_temperature_command(self):
        remarks = RemarkParser().parse('401001015 AO1')
        self.assertEqual('24-hour maximum temperature of 10.0°C and 24-hour minimum temperature of -1.5°C', remarks[0])

    def test_parse_hourly_maximum_temperature_below_zero(self):
        remarks = RemarkParser().parse('11021 AO1')
        self.assertEqual('6-hourly maximum temperature of -2.1°C', remarks[0])

    def test_parse_hourly_maximum_temperature_above_zero(self):
        remarks = RemarkParser().parse('10142')
        self.assertEqual('6-hourly maximum temperature of 14.2°C', remarks[0])

    def test_parse_hourly_minimum_temperature_negative(self):
        remarks = RemarkParser().parse('21001')
        self.assertEqual('6-hourly minimum temperature of -0.1°C', remarks[0])

    def test_parse_hourly_minimum_temperature_positive(self):
        remarks = RemarkParser().parse('20012')
        self.assertEqual('6-hourly minimum temperature of 1.2°C', remarks[0])

    def test_parse_hourly_pressure(self):
        remarks = RemarkParser().parse('52032')
        self.assertEqual('steady or unsteady increase of 3.2 hectopascals in the past 3 hours', remarks[0])

    def test_parse_hourly_precipitation_amount(self):
        remarks = RemarkParser().parse('P0009')
        self.assertEqual('9/100 of an inch of precipitation fell in the last hour', remarks[0])

    def test_parse_precipitation_amount_24_hour(self):
        remarks = RemarkParser().parse('70125')
        self.assertEqual('1.25 inches of precipitation fell in the last 24 hours', remarks[0])

    def test_parse_snow_depth(self):
        remarks = RemarkParser().parse('4/021')
        self.assertEqual('snow depth of 21 inches', remarks[0])

    def test_parse_sunshine_duration(self):
        remarks = RemarkParser().parse('98096')
        self.assertEqual('96 minutes of sunshine', remarks[0])

    def test_parse_water_equivalent_snow(self):
        remarks = RemarkParser().parse('933036')
        self.assertEqual('water equivalent of 3.6 inches of snow', remarks[0])

    def test_parse_ice_accretion(self):
        remarks = RemarkParser().parse('l1004 AO1')
        self.assertEqual('4/100 of an inch of ice accretion in the past 1 hour(s)', remarks[0])

    def test_parse_hourly_temperature(self):
        remarks = RemarkParser().parse('T0026 AO1')
        self.assertEqual('hourly temperature of 2.6°C', remarks[0])

    def test_parse_hourly_temperature_dew_point(self):
        remarks = RemarkParser().parse('T00261015 AO1')
        self.assertEqual('hourly temperature of 2.6°C and dew point of -1.5°C', remarks[0])

    def test_parse_precipitation_amount_3_hours(self):
        remarks = RemarkParser().parse('30217')
        self.assertEqual('2.17 inches of precipitation fell in the last 3 hours', remarks[0])

    def test_parse_precipitation_amount_6_hours(self):
        remarks = RemarkParser().parse('60217')
        self.assertEqual('2.17 inches of precipitation fell in the last 6 hours', remarks[0])

    def test_parse_precipitation_beg(self):
        remarks = RemarkParser().parse('RAB45 AO1')
        self.assertEqual(' rain beginning at :45', remarks[0])

    def test_parse_precipitation_beg_with_descriptive(self):
        remarks = RemarkParser().parse('SHRAB45')
        self.assertEqual('showers of rain beginning at :45', remarks[0])

    def test_parse_precipitation_end(self):
        remarks = RemarkParser().parse('RAE45 AO1')
        self.assertEqual(' rain ending at :45', remarks[0])

    def test_parse_precipitation_end_with_descriptive(self):
        remarks = RemarkParser().parse('SHRAE0545 AO1')
        self.assertEqual('showers of rain ending at 05:45', remarks[0])


class StubParser(AbstractParser):
    def __init__(self):
        super().__init__()

    def parse(self, input):
        """
        Does nothing for the stub
        :param input:
        :return:
        """
        pass


class StubWeatherContainer(AbstractWeatherContainer):
    def __init__(self):
        super().__init__()
        self.wind = Wind
        self.visibility = Visibility


if __name__ == '__main__':
    unittest.main()
