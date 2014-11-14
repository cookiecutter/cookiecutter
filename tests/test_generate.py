#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_generate
--------------

Tests for `cookiecutter.generate` module.
"""
from __future__ import unicode_literals
import logging
import os
import io
import sys
import stat
import unittest

from jinja2 import FileSystemLoader
from jinja2.environment import Environment
from jinja2.exceptions import TemplateSyntaxError

from cookiecutter import generate
from cookiecutter import exceptions
from cookiecutter import utils
from tests import CookiecutterCleanSystemTestCase

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)


class TestGenerateFile(unittest.TestCase):

    def test_generate_file(self):
        env = Environment()
        env.loader = FileSystemLoader('.')
        infile = 'tests/files/{{generate_file}}.txt'
        generate.generate_file(
            project_dir=".",
            infile=infile,
            context={'generate_file': 'cheese'},
            env=env
        )
        self.assertTrue(os.path.isfile('tests/files/cheese.txt'))
        with open('tests/files/cheese.txt', 'rt') as f:
            generated_text = f.read()
            self.assertEqual(generated_text, 'Testing cheese')

    def test_generate_file_verbose_template_syntax_error(self):
        env = Environment()
        env.loader = FileSystemLoader('.')
        try:
            generate.generate_file(
                project_dir=".",
                infile='tests/files/syntax_error.txt',
                context={'syntax_error': 'syntax_error'},
                env=env
            )
        except TemplateSyntaxError as exception:
            expected = (
                'Missing end of comment tag\n'
                '  File "./tests/files/syntax_error.txt", line 1\n'
                '    I eat {{ syntax_error }} {# this comment is not closed}'
            )
            expected = expected.replace("/", os.sep)
            self.assertEquals(str(exception), expected)
        except exception:
            self.fail('Unexpected exception thrown:', exception)
        else:
            self.fail('TemplateSyntaxError not thrown')

    def tearDown(self):
        if os.path.exists('tests/files/cheese.txt'):
            os.remove('tests/files/cheese.txt')


if __name__ == '__main__':
    unittest.main()
