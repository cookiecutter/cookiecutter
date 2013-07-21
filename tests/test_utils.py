#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_utils
------------

Tests for `cookiecutter.utils` module.
"""

import shutil
import unittest

from cookiecutter import utils


class TestUtils(unittest.TestCase):

    def test_make_sure_path_exists(self):
        self.assertTrue(utils.make_sure_path_exists('/usr/'))
        self.assertTrue(utils.make_sure_path_exists('tests/blah'))
        self.assertTrue(utils.make_sure_path_exists('tests/trailingslash/'))
        self.assertFalse(
            utils.make_sure_path_exists(
                '/this-dir-does-not-exist-and-cant-be-created/'
            )
        )
        shutil.rmtree('tests/blah/')
        shutil.rmtree('tests/trailingslash/')

    def test_unicode_open(self):
        """ Test unicode_open(filename, *args, **kwargs). """

        unicode_text = u"""Polish: Ą Ł Ż
Chinese: 倀 倁 倂 倃 倄 倅 倆 倇 倈
Musical Notes: ♬ ♫ ♯"""

        with utils.unicode_open('tests/files/unicode.txt') as f:
            opened_text = f.read()
            self.assertEqual(unicode_text, opened_text)

if __name__ == '__main__':
    unittest.main()
