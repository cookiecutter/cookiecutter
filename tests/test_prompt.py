#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_prompt
--------------

Tests for `cookiecutter.prompt` module.
"""

import platform
import sys

from cookiecutter.compat import patch, unittest, OrderedDict
from cookiecutter import prompt

if 'windows' in platform.platform().lower():
    old_stdin = sys.stdin

    class X(object):
        def readline(self):
            return '\n'
    sys.stdin = X()


class TestPrompt(unittest.TestCase):

    @patch('cookiecutter.prompt.read_response', lambda x=u'': u'\n')
    def test_unicode_prompt_for_templated_config(self):
        context = {"cookiecutter": OrderedDict([
            ("project_name", u"A New Project"),
            ("pkg_name", u"{{ cookiecutter.project_name|lower|replace(' ', '') }}")
        ])}

        cookiecutter_dict = prompt.prompt_for_config(context)
        self.assertEqual(cookiecutter_dict, {"project_name": u"A New Project",
             "pkg_name": u"anewproject"})
