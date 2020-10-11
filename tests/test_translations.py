import sys
import unittest

from verboselib import drop_default_language
from verboselib import drop_language
from verboselib import set_language
from verboselib import Translations

from .constants import LOCALE_DOMAIN
from .constants import LOCALE_DIR_PATH


class TranslationsTestCase(unittest.TestCase):

  def setUp(self):
    drop_default_language()
    drop_language()

    self.translations = Translations(LOCALE_DOMAIN, LOCALE_DIR_PATH)

  def test_gettext(self):
    _ = self.translations.gettext

    set_language("en")

    translated = _("verboselib test string")
    self.assertEqual(translated, "verboselib test string in en_US")

    set_language("en-gb")
    self.assertEqual(translated, "verboselib test string in en_US")

  def test_gettext_lazy(self):
    L_ = self.translations.gettext_lazy

    translated = L_("verboselib test string")

    set_language("en")
    self.assertEqual(translated, "verboselib test string in en_US")

    set_language("en-gb")
    self.assertEqual(translated, "verboselib test string in en_GB")

  def test_ngettext(self):
    N_ = self.translations.ngettext

    set_language("uk")

    translated = N_("window", "windows", 1)
    self.assertEqual(translated, "вікно")

    translated = N_("window", "windows", 2)
    self.assertEqual(translated, "вікна")

    translated = N_("window", "windows", 5)
    self.assertEqual(translated, "вікон")

  def test_ngettext_lazy_n(self):
    N_ = self.translations.ngettext

    set_language("uk")

    translated = N_("window", "windows", lambda: 1)
    self.assertEqual(translated, "вікно")

    translated = N_("window", "windows", lambda: 2)
    self.assertEqual(translated, "вікна")

    translated = N_("window", "windows", lambda: 5)
    self.assertEqual(translated, "вікон")

  def test_ngettext_lazy(self):
    LN_ = self.translations.ngettext_lazy

    translated = LN_("window", "windows", 1)

    set_language("en")
    self.assertEqual(translated, "window")

    set_language("uk")
    self.assertEqual(translated, "вікно")

  @unittest.skipIf(
    (sys.version_info.major == 3 and sys.version_info.minor < 8),
    "available since Python 3.8",
  )
  def test_pgettext(self):
    P_ = self.translations.pgettext

    set_language("en")
    translated = P_("abbrev. month", "Jan")
    self.assertEqual(translated, "Jan")

    set_language("uk")
    translated = P_("abbrev. month", "Jan")
    self.assertEqual(translated, "Січ")

  @unittest.skipIf(
    (sys.version_info.major == 3 and sys.version_info.minor < 8),
    "available since Python 3.8",
  )
  def test_pgettext_lazy(self):
    LP_ = self.translations.pgettext_lazy

    translated = LP_("abbrev. month", "Jan")

    set_language("en")
    self.assertEqual(translated, "Jan")

    set_language("uk")
    self.assertEqual(translated, "Січ")

  @unittest.skipIf(
    (sys.version_info.major == 3 and sys.version_info.minor < 8),
    "available since Python 3.8",
  )
  def test_npgettext(self):
    NP_ = self.translations.npgettext

    set_language("uk")
    translated = NP_("noun", "lock", "locks", 1)
    self.assertEqual(translated, "замок")

    translated = NP_("noun", "lock", "locks", 2)
    self.assertEqual(translated, "замки")

    translated = NP_("noun", "lock", "locks", 5)
    self.assertEqual(translated, "замків")

  @unittest.skipIf(
    (sys.version_info.major == 3 and sys.version_info.minor < 8),
    "available since Python 3.8",
  )
  def test_npgettext_lazy_n(self):
    NP_ = self.translations.npgettext

    set_language("uk")
    translated = NP_("noun", "lock", "locks", lambda: 1)
    self.assertEqual(translated, "замок")

    translated = NP_("noun", "lock", "locks", lambda: 2)
    self.assertEqual(translated, "замки")

    translated = NP_("noun", "lock", "locks", lambda: 5)
    self.assertEqual(translated, "замків")

  @unittest.skipIf(
    (sys.version_info.major == 3 and sys.version_info.minor < 8),
    "available since Python 3.8",
  )
  def test_npgettext_lazy(self):
    LNP_ = self.translations.npgettext_lazy

    translated = LNP_("noun", "lock", "locks", 1)

    set_language("en")
    self.assertEqual(translated, "lock")

    set_language("uk")
    self.assertEqual(translated, "замок")
