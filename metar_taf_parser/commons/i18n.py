import gettext
import locale
import os

from metar_taf_parser.commons.exception import TranslationError


localedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../locale')
langAvailable = os.listdir(localedir)
lang = locale.getdefaultlocale()[0][:2]
if lang not in langAvailable:
    lang = 'en'
t = gettext.translation(domain='messages', localedir=localedir, fallback=True, languages=[lang])


def _(message: str) -> str:
    translation = t.gettext(message)
    if message == translation:
        raise TranslationError(translation=message, message='Missing translation')
    return translation
