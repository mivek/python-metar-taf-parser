import functools
import gettext
import locale
import os
import threading
from contextlib import contextmanager

from metar_taf_parser.commons.exception import TranslationError

localedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../locale')

SUPPORTED_LOCALES = {
    name for name in os.listdir(localedir)
    if os.path.isdir(os.path.join(localedir, name))
}

DEFAULT_LOCALE = 'en'

# Map 2-letter prefix -> best-matching dir (exact 2-letter dirs win over hyphenated variants)
_PREFIX_MAP: dict = {}
for _loc_name in SUPPORTED_LOCALES:
    _prefix = _loc_name[:2]
    if _prefix not in _PREFIX_MAP or _loc_name == _prefix:
        _PREFIX_MAP[_prefix] = _loc_name


def _resolve(loc: str) -> str:
    """Normalize a user-supplied locale string to an actual SUPPORTED_LOCALES dir name."""
    if not loc:
        return DEFAULT_LOCALE
    if loc in SUPPORTED_LOCALES:
        return loc
    # zh_CN -> zh-CN
    hyphen = loc.replace('_', '-')
    if hyphen in SUPPORTED_LOCALES:
        return hyphen
    # zh -> zh-CN, fr_FR -> fr (via 2-letter prefix)
    prefix = loc[:2]
    if prefix in _PREFIX_MAP:
        return _PREFIX_MAP[prefix]
    return DEFAULT_LOCALE


@functools.lru_cache(maxsize=None)
def get_translation(loc: str) -> gettext.NullTranslations:
    """Return a cached gettext translation for *loc*, with English as fallback chain."""
    languages = ['en'] if loc == DEFAULT_LOCALE else [loc, 'en']
    return gettext.translation('messages', localedir=localedir, languages=languages, fallback=True)


def _detect_system_locale() -> str:
    try:
        sys_loc = locale.getlocale()
        if sys_loc and sys_loc[0] and len(sys_loc[0]) >= 2:
            return _resolve(sys_loc[0])
    except Exception:
        pass
    return DEFAULT_LOCALE


_default_locale: str = _detect_system_locale()
_thread_local = threading.local()


def get_locale() -> str:
    """Return the active locale for the current thread."""
    return getattr(_thread_local, 'locale', _default_locale)


def set_locale(loc: str) -> None:
    """Set the locale for the current thread."""
    _thread_local.locale = _resolve(loc)


def reset_locale() -> None:
    """Reset the current thread's locale to the module default."""
    if hasattr(_thread_local, 'locale'):
        del _thread_local.locale


@contextmanager
def translation_locale(loc):
    """Context manager: temporarily override the locale for this thread. None is a no-op."""
    if loc is None:
        yield
        return
    resolved = _resolve(loc)
    previous = getattr(_thread_local, 'locale', None)
    _thread_local.locale = resolved
    try:
        yield
    finally:
        if previous is None:
            if hasattr(_thread_local, 'locale'):
                del _thread_local.locale
        else:
            _thread_local.locale = previous


def _(message: str, locale=None) -> str:  # noqa: A002
    """Translate *message* using the active (or explicitly supplied) locale.

    Falls back to English automatically; raises TranslationError only when the
    key is absent from English too.
    """
    loc = _resolve(locale) if locale else get_locale()
    translation = get_translation(loc).gettext(message)
    if translation == message:
        raise TranslationError(translation=message, message='Missing translation')
    return translation
