# -*- coding: utf-8 -*-
import unittest

from verboselib._helpers import to_language, to_locale


class HelpersTestCase(unittest.TestCase):

    def test_to_locale(self):
        self.assertEqual(to_locale('en-us'), 'en_US')
        self.assertEqual(to_locale('en-us', to_lower=True), 'en_us')
        self.assertEqual(to_locale('sr-lat'), 'sr_Lat')

    def test_to_language(self):
        self.assertEqual(to_language('en_US'), 'en-us')
        self.assertEqual(to_language('sr_Lat'), 'sr-lat')
