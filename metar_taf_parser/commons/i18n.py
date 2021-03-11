import gettext
import os

localedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../locale')
t = gettext.translation(domain='messages', localedir=localedir, fallback=True, languages=['en', 'fr', 'pl', 'de'])
_ = t.gettext
