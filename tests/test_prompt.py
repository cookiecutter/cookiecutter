#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_prompt
--------------

Tests for `cookiecutter.prompt` module.
"""

from collections import OrderedDict
import platform
import sys
import unittest

from cookiecutter.compat import patch
from cookiecutter import prompt

if 'windows' in platform.platform().lower():
    old_stdin = sys.stdin

    class X(object):
        def readline(self):
            return '\n'
    sys.stdin = X()


class TestPrompt(unittest.TestCase):

    @patch('cookiecutter.prompt.read_response', lambda x=u'': u'Audrey Roy')
    def test_prompt_for_config_simple(self):
        context = {"cookiecutter": {"full_name": "Your Name"}}

        cookiecutter_dict = prompt.prompt_for_config(context)
        self.assertEqual(cookiecutter_dict, {"full_name": u"Audrey Roy"})

    @patch('cookiecutter.prompt.read_response', lambda x=u'': u'Pizzä ïs Gööd')
    def test_prompt_for_config_unicode(self):
        context = {"cookiecutter": {"full_name": "Your Name"}}

        cookiecutter_dict = prompt.prompt_for_config(context)
        self.assertEqual(cookiecutter_dict, {"full_name": u"Pizzä ïs Gööd"})

    @patch('cookiecutter.prompt.read_response', lambda x=u'': u'Pizzä ïs Gööd')
    def test_unicode_prompt_for_config_unicode(self):
        context = {"cookiecutter": {"full_name": u"Řekni či napiš své jméno"}}

        cookiecutter_dict = prompt.prompt_for_config(context)
        self.assertEqual(cookiecutter_dict, {"full_name": u"Pizzä ïs Gööd"})

    @patch('cookiecutter.prompt.read_response', lambda x=u'': u'\n')
    def test_unicode_prompt_for_default_config_unicode(self):
        context = {"cookiecutter": {"full_name": u"Řekni či napiš své jméno"}}

        cookiecutter_dict = prompt.prompt_for_config(context)
        self.assertEqual(cookiecutter_dict, {"full_name": u"Řekni či napiš své jméno"})

    @patch('cookiecutter.prompt.read_response', lambda x=u'': u'\n')
    def test_unicode_prompt_for_templated_config(self):
        context = {"cookiecutter": OrderedDict([
            ("project_name", u"A New Project"),
            ("pkg_name", u"{{ cookiecutter.project_name|lower|replace(' ', '') }}")
        ])}

        cookiecutter_dict = prompt.prompt_for_config(context)
        self.assertEqual(cookiecutter_dict, {"project_name": u"A New Project",
             "pkg_name": u"anewproject"})

    @patch('cookiecutter.prompt.read_response', lambda x=u'': u'Audrey Roy')
    def test_prompt_for_config_nonstring(self):
        context = {"cookiecutter": {"python_major_version": 3}}

        cookiecutter_dict = prompt.prompt_for_config(context)
        self.assertEqual(cookiecutter_dict, {"python_major_version": u"3"})


class TestQueryAnswers(unittest.TestCase):

    @patch('cookiecutter.prompt.read_response', lambda x=u'': u'y')
    def test_query_y(self):
        answer = prompt.query_yes_no("Blah?")
        self.assertTrue(answer)

    @patch('cookiecutter.prompt.read_response', lambda x=u'': u'ye')
    def test_query_ye(self):
        answer = prompt.query_yes_no("Blah?")
        self.assertTrue(answer)

    @patch('cookiecutter.prompt.read_response', lambda x=u'': u'yes')
    def test_query_yes(self):
        answer = prompt.query_yes_no("Blah?")
        self.assertTrue(answer)

    @patch('cookiecutter.prompt.read_response', lambda x=u'': u'n')
    def test_query_n(self):
        answer = prompt.query_yes_no("Blah?")
        self.assertFalse(answer)


class TestQueryDefaults(unittest.TestCase):

    @patch('cookiecutter.prompt.read_response', lambda x=u'': u'y')
    def test_query_y_none_default(self):
        answer = prompt.query_yes_no("Blah?", default=None)
        self.assertTrue(answer)

    @patch('cookiecutter.prompt.read_response', lambda x=u'': u'n')
    def test_query_n_none_default(self):
        answer = prompt.query_yes_no("Blah?", default=None)
        self.assertFalse(answer)

    @patch('cookiecutter.prompt.read_response', lambda x=u'': u'')
    def test_query_no_default(self):
        answer = prompt.query_yes_no("Blah?", default='no')
        self.assertFalse(answer)

    @patch('cookiecutter.prompt.read_response', lambda x=u'': u'junk')
    def test_query_bad_default(self):
        self.assertRaises(ValueError, prompt.query_yes_no, "Blah?", default='yn')
