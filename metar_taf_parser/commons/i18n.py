import gettext
import os

from metar_taf_parser.commons.exception import TranslationError


localedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../locale')
t = gettext.translation(domain='messages', localedir=localedir, fallback=True, languages=['en', 'fr', 'pl', 'de'])


def _(message: str) -> str:
    translation = t.gettext(message)
    if message == translation:
        raise TranslationError(translation=message, message='Missing translation')
    return translation
