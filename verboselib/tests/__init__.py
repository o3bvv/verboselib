# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import unittest

from verboselib.core import (
    TranslationsFactory, use, drop, use_bypass, set_default_language,
)


here = os.path.abspath(os.path.dirname(__file__))


class VerboselibTestCase(unittest.TestCase):

    def setUp(self):
        set_default_language(None)
        drop()

        path = os.path.join(here, 'locale')
        self.translations = TranslationsFactory('tests', path)

    def tearDown(self):
        del self.translations

        set_default_language(None)
        drop()

    def test_bypass(self):
        _ = self.translations.ugettext
        source = "verboselib test string"

        translated = _("verboselib test string")
        self.assertEqual(translated, source)

        use('en')
        translated = _("verboselib test string")
        self.assertNotEqual(translated, source)

        use_bypass()
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

    def test_use_n_drop(self):
        _ = self.translations.ugettext

        translated = _("verboselib test string")
        self.assertEqual(translated, "verboselib test string")

        set_default_language('en')

        use('ru')
        translated = _("verboselib test string")
        self.assertEqual(translated, "verboselib test string in ru")

        drop()
        translated = _("verboselib test string")
        self.assertEqual(translated, "verboselib test string in en_US")
