# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import unittest

from verboselib import (
    use_language, use_language_bypass, drop_language, set_default_language,
)
from verboselib.factory import TranslationsFactory


here = os.path.abspath(os.path.dirname(__file__))


class PackageTestCase(unittest.TestCase):

    def setUp(self):
        set_default_language(None)
        drop_language()

        path = os.path.join(here, 'locale')
        self.translations = TranslationsFactory('tests', path)

    def tearDown(self):
        del self.translations

        set_default_language(None)
        drop_language()

    def test_bypass(self):
        _ = self.translations.ugettext
        source = "verboselib test string"

        translated = _("verboselib test string")
        self.assertEqual(translated, source)

        use_language('en')
        translated = _("verboselib test string")
        self.assertNotEqual(translated, source)

        use_language_bypass()
        translated = _("verboselib test string")
        self.assertEqual(translated, source)

    def test_default_language(self):
        _ = self.translations.ugettext

        translated = _("verboselib test string")
        self.assertEqual(translated, "verboselib test string")

        set_default_language('ru')
        translated = _("verboselib test string")
        self.assertEqual(translated, "verboselib test string in ru")

        set_default_language('uk')
        translated = _("verboselib test string")
        self.assertEqual(translated, "verboselib test string in uk")

        set_default_language('en')
        translated = _("verboselib test string")
        self.assertEqual(translated, "verboselib test string in en_US")

        set_default_language('en-gb')
        translated = _("verboselib test string")
        self.assertEqual(translated, "verboselib test string in en_GB")

    def test_use_n_drop_language(self):
        _ = self.translations.ugettext

        translated = _("verboselib test string")
        self.assertEqual(translated, "verboselib test string")

        set_default_language('en')

        use_language('ru')
        translated = _("verboselib test string")
        self.assertEqual(translated, "verboselib test string in ru")

        drop_language()
        translated = _("verboselib test string")
        self.assertEqual(translated, "verboselib test string in en_US")

    def test_lazy(self):
        L_ = self.translations.ugettext_lazy

        use_language('uk')
        translated = L_("verboselib test string")

        use_language('ru')
        self.assertEqual(translated, "verboselib test string in ru")
        use_language('en-gb')
        self.assertEqual(translated, "verboselib test string in en_GB")
        use_language_bypass()
        self.assertEqual(translated, "verboselib test string")

        translated = L_("Good morning, {:}!")
        use_language('ru')

        self.assertEqual(translated.format("Иван"), "Доброе утро, Иван!")
        use_language('uk')
        self.assertEqual(translated.format("Іван"), "Доброго ранку, Іван!")
