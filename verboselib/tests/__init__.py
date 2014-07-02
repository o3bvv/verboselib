# -*- coding: utf-8 -*-
import os
import unittest
import verboselib


here = os.path.abspath(os.path.dirname(__file__))


class RegistrationTestCase(unittest.TestCase):

    def setUp(self):
        self.root = os.path.join(here, 'lib_foo')

    def test_simple(self):
        path = os.path.join(self.root, 'locale')
        translators = verboselib.register(domain='foo', locale_dir=path)
        self.assertIsNotNone(translators)

    def test_multidomain(self):
        path = os.path.join(self.root, 'locale_extra')
        translators = verboselib.register(['foo', 'bar', ], path)
        self.assertIsNotNone(translators)

    def test_register_many(self):
        path = os.path.join(self.root, 'locale')
        path_extra = os.path.join(self.root, 'locale_extra')
        translators = verboselib.register_many(
            {
                'domain': 'foo',
                'locale_dir': path,
            },
            (['foo', 'bar', ], path_extra),
        )
        self.assertIsNotNone(translators)
