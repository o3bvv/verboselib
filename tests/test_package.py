# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import gettext
import os
import unittest

from verboselib import (
    use_language, use_language_bypass, drop_language, set_default_language,
    get_default_language,
)
from verboselib.factory import TranslationsFactory, VerboselibTranslation
from verboselib._compatibility import PY2, PY3


here = os.path.abspath(os.path.dirname(__file__))


class PackageTestCase(unittest.TestCase):

    def setUp(self):
        set_default_language(None)
        drop_language()

        path = os.path.join(here, "locale")
        self.translations = TranslationsFactory("tests", path)

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

    def test_set_default_language(self):
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

    def test_get_default_language(self):
        self.assertEqual(get_default_language(), None)
        set_default_language('en')
        self.assertEqual(get_default_language(), 'en')

    def test_use_n_drop_language(self):
        _ = self.translations.gettext
        U_ = self.translations.ugettext

        translated = _("verboselib test string")
        self.assertEqual(translated, "verboselib test string")

        translated = U_("verboselib test string")
        self.assertEqual(translated, "verboselib test string")

        set_default_language('en')

        use_language('ru')
        translated = U_("verboselib test string")
        self.assertEqual(translated, "verboselib test string in ru")

        drop_language()
        translated = U_("verboselib test string")
        self.assertEqual(translated, "verboselib test string in en_US")

    def test_lazy(self):
        L_ = self.translations.gettext_lazy
        UL_ = self.translations.ugettext_lazy

        use_language('uk')

        if PY2:
            self.assertEqual(str(L_("Hello")), "Вітаю".encode('utf-8'))

        translated = UL_("verboselib test string")

        use_language('ru')
        self.assertEqual(translated, "verboselib test string in ru")
        use_language('en-gb')
        self.assertEqual(translated, "verboselib test string in en_GB")
        use_language_bypass()
        self.assertEqual(translated, "verboselib test string")

        translated = UL_("Good morning, {:}!")
        use_language('ru')

        self.assertEqual(translated.format("Иван"), "Доброе утро, Иван!")
        use_language('uk')
        self.assertEqual(translated.format("Іван"), "Доброго ранку, Іван!")


class VerboselibTranslationTestCase(unittest.TestCase):

    def setUp(self):
        self.method_name = 'gettext' if PY3 else 'ugettext'
        self.path = os.path.join(here, "locale")

    def test_merge(self):

        def _translation(domain):
            class_ = VerboselibTranslation
            t = gettext.translation(domain, self.path, ['uk'], class_)
            t.set_language('uk')
            return t

        t1 = _translation("tests")
        method1 = getattr(t1, self.method_name)
        self.assertEqual(method1("Hello"), "Вітаю")
        self.assertEqual(method1("Good bye"), "Good bye")

        t2 = _translation("extra")
        method2 = getattr(t2, self.method_name)
        self.assertEqual(method2("Hello"), "Hello")
        self.assertEqual(method2("Good bye"), "До зустрічі")

        t1.merge(t2)
        self.assertEqual(method1("Hello"), "Вітаю")
        self.assertEqual(method1("Good bye"), "До зустрічі")

    def test_language(self):
        class_ = VerboselibTranslation
        t = gettext.translation('tests', self.path, ['en_US'], class_)
        t.set_language('en_US')
        self.assertEqual(t.language(), 'en_US')

    def test_to_language(self):
        class_ = VerboselibTranslation
        t = gettext.translation('tests', self.path, ['en_US'], class_)
        t.set_language('en_US')
        self.assertEqual(t.to_language(), 'en-us')

    def test_repr(self):
        class_ = VerboselibTranslation
        t = gettext.translation('tests', self.path, ['en_US'], class_)
        t.set_language('en_US')
        self.assertEqual(repr(t), '<VerboselibTranslation lang:en_US>')
