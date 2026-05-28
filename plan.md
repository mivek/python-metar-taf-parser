# i18n Refactor + Per-Call Locale

## Context

The i18n layer (metar_taf_parser/commons/i18n.py, 24 lines) uses Python's stdlib
gettext over GNU .po/.mo files in metar_taf_parser/locale/<lang>/LC_MESSAGES/.
The foundation is idiomatic, but the implementation has hard limitations and latent bugs:

1. Locale is frozen at import time — locale.getlocale() and the gettext.translation  
   object t are evaluated once as module globals (i18n.py:10,16). No runtime switching.
2. No per-call locale — parse() has no locale parameter; every consumer shares one global.
3. Crashes on partial translations — \_() raises TranslationError whenever a key is  
   absent from the selected language's .mo (i18n.py:21-22). Languages like Spanish (\~492 of  
   \~1112 keys) will raise on valid input, including inside enum \__repr_\_.
4. Non-English non-2-letter locales never load from the system — the old lang = loc\[0\]\[:2\]  
   (i18n.py:13) turns zh_CN→zh and ru_RU→ru, neither of which matches the actual dirs  
   zh-CN / ru-RU, so those silently fall back to English.

This refactor makes locale selectable per-call and dynamically, fixes the two bugs above, and
keeps the public API backward compatible. Decisions confirmed with the user: thread-local +
context manager for lazy enum strings; English fallback chain for missing keys (still raise only
when missing in English too); normalize locale names without renaming dirs.

## Translation pathways (why the design is shaped this way)

- Eager (parse time): remark commands (command/remark.py, 23 \_() calls) and runway  
  deposit strings (command/metar.py:131,135) translate immediately and store strings on the  
  model (metar.remark, metar.remarks, runway.thickness, runway.braking_capacity).
- Lazy (repr time): enum \__repr_\_ (model/enum.py, 12 \_() calls) translate when  
  repr()/str() is called on clouds, phenomena, intensities, etc. — after parse() returns.

A thread-local "current locale" read by \_() covers both: parse(locale=...) sets it for the
whole parse (eager), and a context manager / set_locale lets users control lazy enum output.
This means no changes are needed in enum.py / remark.py / metar.py — they keep calling \_().

## Changes

### 1. Rewrite metar_taf_parser/commons/i18n.py

- Build SUPPORTED_LOCALES once from os.listdir(localedir) (e.g. {'de','en','es','fr','it','pl','ru-RU','tr','zh-CN'}).
- \_resolve(loc) -> str: normalize user input to a real dir name. Try, in order: exact match;  
  hyphen form (zh_CN→zh-CN); 2-letter prefix mapped to a dir (zh→zh-CN, ru→ru-RU,  
  fr_FR→fr). Return DEFAULT_LOCALE ('en') if nothing matches. Build a prefix→dir map at  
  import for the prefix step.
- @functools.lru_cache get_translation(loc) returns  
  gettext.translation('messages', localedir, languages=\[loc, 'en'\], fallback=True) (just  
  \['en'\] for English). The \[loc, 'en'\] list makes gettext chain English as a fallback, so  
  partial languages resolve valid keys to English instead of raising.
- Module-level default locale resolved once from the system locale (replaces old globals lang/t).
- Thread-local state: get_locale(), set_locale(loc) (dynamic global change, per-thread),  
  reset_locale(), and @contextmanager translation_locale(loc) (per-call / scoped; None = no-op).
- \_(message, locale=None) -> str: loc = \_resolve(locale) if locale else get_locale();  
  look up via get_translation(loc); still raise TranslationError only when the result equals  
  the msgid (i.e. missing even in English) — this preserves RemarkParser's control flow.
- Remove now-unused module globals (t, lang, langAvailable). Keep \_ import path stable.

### 2. Thread per-call locale into the parser — metar_taf_parser/parser/parser.py

- Add locale: str = None to MetarParser.parse, TAFParser.parse, RemarkParser.parse.
- Wrap each method body in with translation_locale(locale):. Because parse_remark →  
  RemarkParser().parse runs inside that block, the thread-local already carries the locale; no  
  need to thread it through every execute() / \_() call.
- Import translation_locale from metar_taf_parser.commons.i18n.

No changes required in enum.py, command/remark.py, command/metar.py, command/taf.py,
command/common.py.

### 3. Tests — add metar_taf_parser/tests/commons/test_i18n.py (+ a couple of parser tests)

- parse(locale='fr') yields French remark strings; default stays English.
- translation_locale('de') context manager affects enum repr() (e.g. a Cloud/CloudQuantity),  
  and restores afterward.
- set_locale / reset_locale dynamic switching; verify thread isolation (set in one thread,  
  default in another).
- Partial-language fallback: a key present in English but not in pl/es resolves to English  
  (no TranslationError).
- Unknown token (missing even in English) still raises TranslationError.
- \_resolve: 'zh_CN'/'zh'/'zh-CN' → 'zh-CN'; 'ru_RU'→'ru-RU'; 'fr_FR'→'fr';  
  unknown → 'en'. SUPPORTED_LOCALES contains zh-CN and ru-RU.
- Confirm existing tests/parser/test_parser.py and tests/command/test_metar.py still pass  
  (they compare parsed output against \_() with the same default, so they stay consistent).

### 4. Docs — README.md

Add a short "Locale / i18n" section showing: MetarParser().parse(msg, locale='fr'), the
translation_locale context manager for translated enum output, set_locale/get_locale, and
SUPPORTED_LOCALES. Note English fallback for partial languages.

## Out of scope

- Renaming ru-RU/zh-CN dirs to GNU ru_RU/zh_CN (handled by normalization instead, to avoid  
  touching packaging and Crowdin sync).
- Regenerating/completing .mo files (English fallback covers the gaps).

## Verification

- python -m pytest metar_taf_parser/tests/ -q (full suite green, including new i18n tests).
- Manual smoke check:

  ```python
  from metar_taf_parser.parser.parser import MetarParser
  from metar_taf_parser.commons.i18n import translation_locale, set_locale
  m = MetarParser().parse('KTTN 051853Z 04011KT 9999 VCTS SN FZFG BKN003 OVC010 M02/M02 A3006 RMK AO2 SLP013', locale='fr')
  print(m.remark)                       # French remark text
  with translation_locale('de'):
      print([repr(c) for c in m.clouds])  # German cloud labels
  ```
- Confirm a partial language (e.g. parse(..., locale='es') on a remark whose key is missing in  
  Spanish) returns English text rather than raising.
