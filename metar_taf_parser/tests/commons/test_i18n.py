import threading
import unittest

from metar_taf_parser.commons.exception import TranslationError
from metar_taf_parser.commons.i18n import (
    SUPPORTED_LOCALES,
    _,
    _resolve,
    get_locale,
    reset_locale,
    set_locale,
    translation_locale,
)
from metar_taf_parser.model.enum import CloudQuantity
from metar_taf_parser.parser.parser import MetarParser


METAR_WITH_REMARKS = (
    'KTTN 051853Z 04011KT 9999 VCTS SN FZFG BKN003 OVC010 M02/M02 A3006 '
    'RMK AO2 SLP013'
)


class TestSupportedLocales(unittest.TestCase):
    def test_contains_standard_locales(self):
        for loc in ('en', 'fr', 'de', 'pl', 'it'):
            self.assertIn(loc, SUPPORTED_LOCALES)

    def test_contains_hyphenated_locales(self):
        self.assertIn('zh-CN', SUPPORTED_LOCALES)
        self.assertIn('ru-RU', SUPPORTED_LOCALES)


class TestResolve(unittest.TestCase):
    def test_exact_match(self):
        self.assertEqual(_resolve('fr'), 'fr')
        self.assertEqual(_resolve('en'), 'en')
        self.assertEqual(_resolve('zh-CN'), 'zh-CN')
        self.assertEqual(_resolve('ru-RU'), 'ru-RU')

    def test_underscore_to_hyphen(self):
        self.assertEqual(_resolve('zh_CN'), 'zh-CN')
        self.assertEqual(_resolve('ru_RU'), 'ru-RU')

    def test_two_letter_prefix(self):
        self.assertEqual(_resolve('zh'), 'zh-CN')
        self.assertEqual(_resolve('ru'), 'ru-RU')

    def test_underscore_two_letter_country(self):
        self.assertEqual(_resolve('fr_FR'), 'fr')

    def test_unknown_falls_back_to_en(self):
        self.assertEqual(_resolve('xx'), 'en')
        self.assertEqual(_resolve(''), 'en')
        self.assertEqual(_resolve(None), 'en')


class TestTranslationFallback(unittest.TestCase):
    """English fallback: partial languages resolve missing keys to English."""

    def test_pl_key_missing_in_pl_returns_english(self):
        # Remark.AO1 is present in English but not in Polish
        with translation_locale('pl'):
            result = _('Remark.AO1')
        self.assertEqual(result, 'automated stations without a precipitation discriminator')

    def test_unknown_key_raises_translation_error(self):
        # Remark.SLP is missing even in English
        with self.assertRaises(TranslationError):
            _('Remark.SLP')

    def test_missing_key_in_any_locale_raises_translation_error(self):
        with translation_locale('fr'):
            with self.assertRaises(TranslationError):
                _('Remark.SLP')


class TestTranslationLocaleContextManager(unittest.TestCase):
    def test_french_translation_active_inside_block(self):
        with translation_locale('fr'):
            result = _('CloudQuantity.BKN')
        self.assertEqual(result, 'nuages fragmentés')

    def test_german_translation_active_inside_block(self):
        with translation_locale('de'):
            result = _('CloudQuantity.OVC')
        self.assertEqual(result, 'bedeckt')

    def test_locale_restored_after_block(self):
        locale_before = get_locale()
        with translation_locale('de'):
            pass
        self.assertEqual(get_locale(), locale_before)

    def test_none_is_noop(self):
        locale_before = get_locale()
        with translation_locale(None):
            locale_after = get_locale()
        self.assertEqual(locale_before, locale_after)

    def test_enum_repr_uses_active_locale(self):
        with translation_locale('fr'):
            result = repr(CloudQuantity.BKN)
        self.assertEqual(result, 'nuages fragmentés')

    def test_enum_repr_uses_german(self):
        with translation_locale('de'):
            result = repr(CloudQuantity.OVC)
        self.assertEqual(result, 'bedeckt')

    def test_nested_context_managers(self):
        with translation_locale('fr'):
            with translation_locale('de'):
                de_result = _('CloudQuantity.BKN')
            fr_result = _('CloudQuantity.BKN')
        self.assertEqual(de_result, 'stark bewölkt')
        self.assertEqual(fr_result, 'nuages fragmentés')


class TestSetResetLocale(unittest.TestCase):
    def setUp(self):
        reset_locale()

    def tearDown(self):
        reset_locale()

    def test_set_and_get_locale(self):
        set_locale('fr')
        self.assertEqual(get_locale(), 'fr')

    def test_reset_locale_restores_default(self):
        set_locale('de')
        reset_locale()
        # After reset, locale should be the module default (typically 'en')
        self.assertNotEqual(get_locale(), 'de')

    def test_set_locale_normalizes(self):
        set_locale('zh_CN')
        self.assertEqual(get_locale(), 'zh-CN')


class TestThreadIsolation(unittest.TestCase):
    def test_set_in_one_thread_does_not_affect_another(self):
        results = {}

        def worker_set():
            set_locale('fr')
            results['set_thread'] = get_locale()

        def worker_check():
            import time
            time.sleep(0.05)
            results['check_thread'] = get_locale()

        t1 = threading.Thread(target=worker_set)
        t2 = threading.Thread(target=worker_check)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        self.assertEqual(results['set_thread'], 'fr')
        # The other thread should use the module default, not 'fr'
        self.assertNotEqual(results['check_thread'], 'fr')


class TestParserLocaleParameter(unittest.TestCase):
    def test_metar_parse_with_french_locale(self):
        metar = MetarParser().parse(METAR_WITH_REMARKS, locale='fr')
        # AO2 remark should be in French
        self.assertIn('stations automatisées avec discriminateur de précipitation', metar.remarks)

    def test_metar_parse_default_is_english(self):
        metar = MetarParser().parse(METAR_WITH_REMARKS)
        self.assertIn('automated station with a precipitation discriminator', metar.remarks)

    def test_metar_parse_locale_does_not_leak(self):
        MetarParser().parse(METAR_WITH_REMARKS, locale='fr')
        # After parsing with French, the default should still be English
        metar = MetarParser().parse(METAR_WITH_REMARKS)
        self.assertIn('automated station with a precipitation discriminator', metar.remarks)

    def test_partial_locale_falls_back_to_english(self):
        # Polish lacks Remark.AO2; it should fall back to English without raising
        metar = MetarParser().parse(METAR_WITH_REMARKS, locale='pl')
        self.assertIn('automated station with a precipitation discriminator', metar.remarks)


if __name__ == '__main__':
    unittest.main()
