#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_main
---------

Tests for `cookiecutter.main` module.
"""

import logging
import unittest

from cookiecutter import main

# Log debug and above to console
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)


class TestAbbreviationExpansion(unittest.TestCase):

    def test_abbreviation_expansion(self):
        template = main.expand_abbreviations('foo', {'abbreviations': {'foo': 'bar'}})
        self.assertEqual(template, 'bar')

    def test_abbreviation_expansion_not_an_abbreviation(self):
        template = main.expand_abbreviations('baz', {'abbreviations': {'foo': 'bar'}})
        self.assertEqual(template, 'baz')

    def test_abbreviation_expansion_prefix(self):
        template = main.expand_abbreviations('xx:a', {'abbreviations': {'xx': '<{0}>'}})
        self.assertEqual(template, '<a>')

    def test_abbreviation_expansion_builtin(self):
        template = main.expand_abbreviations('gh:a', {})
        self.assertEqual(template, 'https://github.com/a.git')

    def test_abbreviation_expansion_override_builtin(self):
        template = main.expand_abbreviations('gh:a', {'abbreviations': {'gh': '<{0}>'}})
        self.assertEqual(template, '<a>')

    def test_abbreviation_expansion_prefix_ignores_suffix(self):
        template = main.expand_abbreviations('xx:a', {'abbreviations': {'xx': '<>'}})
        self.assertEqual(template, '<>')

    def test_abbreviation_expansion_prefix_not_0_in_braces(self):
        self.assertRaises(
            IndexError,
            main.expand_abbreviations,
            'xx:a',
            {'abbreviations': {'xx': '{1}'}}
        )


if __name__ == '__main__':
    unittest.main()
