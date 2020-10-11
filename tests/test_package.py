import unittest

from pathlib import Path

from verboselib import drop_default_language
from verboselib import drop_language
from verboselib import get_default_language
from verboselib import set_default_language
from verboselib import set_language
from verboselib import set_language_bypass
from verboselib import Translations

from .constants import LOCALE_DOMAIN
from .constants import LOCALE_DIR_PATH


class PackageTestCase(unittest.TestCase):

  def setUp(self):
    drop_default_language()
    drop_language()

    self.translations = Translations(LOCALE_DOMAIN, LOCALE_DIR_PATH)

  def tearDown(self):
    del self.translations

    drop_default_language()
    drop_language()

  def test_bypass(self):
    _ = self.translations.gettext
    source = "verboselib test string"

    translated = _("verboselib test string")
    self.assertEqual(translated, source)

    set_language("en")
    translated = _("verboselib test string")
    self.assertNotEqual(translated, source)

    set_language_bypass()
    translated = _("verboselib test string")
    self.assertEqual(translated, source)

  def test_set_default_language(self):
    _ = self.translations.gettext

    translated = _("verboselib test string")
    self.assertEqual(translated, "verboselib test string")

    set_default_language("ru")
    translated = _("verboselib test string")
    self.assertEqual(translated, "verboselib test string in ru")

    set_default_language("uk")
    translated = _("verboselib test string")
    self.assertEqual(translated, "verboselib test string in uk")

    set_default_language("en")
    translated = _("verboselib test string")
    self.assertEqual(translated, "verboselib test string in en_US")

    set_default_language("en-gb")
    translated = _("verboselib test string")
    self.assertEqual(translated, "verboselib test string in en_GB")

  def test_get_default_language(self):
    self.assertEqual(get_default_language(), None)
    set_default_language("en")
    self.assertEqual(get_default_language(), "en")

  def test_use_n_drop_language(self):
    _ = self.translations.gettext

    translated = _("verboselib test string")
    self.assertEqual(translated, "verboselib test string")

    set_default_language("en")

    set_language("ru")
    translated = _("verboselib test string")
    self.assertEqual(translated, "verboselib test string in ru")

    drop_language()
    translated = _("verboselib test string")
    self.assertEqual(translated, "verboselib test string in en_US")

  def test_lazy(self):
    L_ = self.translations.gettext_lazy

    set_language("uk")

    translated = L_("verboselib test string")

    set_language("ru")
    self.assertEqual(translated, "verboselib test string in ru")

    set_language("en-gb")
    self.assertEqual(translated, "verboselib test string in en_GB")

    set_language_bypass()
    self.assertEqual(translated, "verboselib test string")

    translated = L_("Good morning, {:}!")

    set_language("ru")
    self.assertEqual(translated.format("Иван"), "Доброе утро, Иван!")

    set_language("uk")
    self.assertEqual(translated.format("Іване"), "Доброго ранку, Іване!")
