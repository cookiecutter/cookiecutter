#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_utils
------------

Tests for `cookiecutter.utils` module.
"""

import os
import io
import sys
import stat
import unittest

from cookiecutter import utils

def make_readonly(path):
    mode = os.stat(path).st_mode
    os.chmod(path, mode & ~stat.S_IWRITE)

class TestUtils(unittest.TestCase):

    def test_rmtree(self):
        os.mkdir('foo')
        with open('foo/bar', "w") as f:
            f.write("Test data")
        make_readonly('foo/bar')
        utils.rmtree('foo')
        self.assertFalse(os.path.exists('foo'))

    def test_make_sure_path_exists(self):
        if sys.platform.startswith('win'):
            existing_directory = os.path.abspath(os.curdir)
            uncreatable_directory = 'a*b'
        else:
            existing_directory = '/usr/'
            uncreatable_directory = '/this-dir-does-not-exist-and-cant-be-created/'

        self.assertTrue(utils.make_sure_path_exists(existing_directory))
        self.assertTrue(utils.make_sure_path_exists('tests/blah'))
        self.assertTrue(utils.make_sure_path_exists('tests/trailingslash/'))
        self.assertFalse(utils.make_sure_path_exists(uncreatable_directory))
        utils.rmtree('tests/blah/')
        utils.rmtree('tests/trailingslash/')

    def test_unicode_open(self):
        """ Test that io.open(filename, mode, encoding='utf-8') works as we expect. """

        unicode_text = u"""Polish: Ą Ł Ż
Chinese: 倀 倁 倂 倃 倄 倅 倆 倇 倈
Musical Notes: ♬ ♫ ♯"""

        with io.open('tests/files/unicode.txt', encoding='utf-8') as f:
            opened_text = f.read()
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
