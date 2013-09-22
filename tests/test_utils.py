#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_utils
------------

Tests for `cookiecutter.utils` module.
"""

import os
import shutil
import sys
import unittest

from cookiecutter import utils


class TestUtils(unittest.TestCase):

    def test_make_sure_path_exists(self):
        self.assertTrue(utils.make_sure_path_exists('/usr/'))
        self.assertTrue(utils.make_sure_path_exists('tests/blah'))
        self.assertTrue(utils.make_sure_path_exists('tests/trailingslash/'))
        self.assertFalse(
            utils.make_sure_path_exists(
                '/this-dir-does-not-exist-and-cant-be-created/'.replace("/", os.sep)
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
            if sys.platform.startswith('win'):
                unicode_text = os.linesep.join([s for s in unicode_text.splitlines() if not s.isspace()])
            self.assertEqual(unicode_text, opened_text)

    def test_workin(self):
        cwd = os.getcwd()
        ch_to = 'tests/files'

        class TestException(Exception):
            pass

        def test_work_in():
            with utils.work_in(ch_to):
                test_dir = os.path.join(cwd, ch_to).replace("/", os.sep)
                self.assertEqual(test_dir, os.getcwd())
                raise TestException()

        # Make sure we return to the correct folder
        self.assertEqual(cwd, os.getcwd())

        # Make sure that exceptions are still bubbled up
        self.assertRaises(TestException, test_work_in)


if __name__ == '__main__':
    unittest.main()
