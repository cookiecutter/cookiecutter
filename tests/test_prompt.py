#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_prompt
--------------

Tests for `cookiecutter.prompt` module.
"""

import sys
import platform
import unittest

from cookiecutter import prompt

PY3 = sys.version > '3'
if PY3:
    from unittest.mock import patch
    input_str = 'builtins.input'
else:
    import __builtin__
    from mock import patch
    input_str = '__builtin__.raw_input'
    from cStringIO import StringIO

if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest

if 'windows' in platform.platform().lower():

    old_stdin = sys.stdin

    class X(object):
        def readline(self):
            return '\n'
    sys.stdin = X()


class TestPrompt(unittest.TestCase):

    @patch(input_str, lambda x: 'Audrey Roy')
    def test_prompt_for_config_simple(self):
        context = {"cookiecutter": {"full_name": "Your Name"}}

        if not PY3:
            sys.stdin = StringIO("Audrey Roy")

        cookiecutter_dict = prompt.prompt_for_config(context)
        self.assertEqual(cookiecutter_dict, {"full_name": "Audrey Roy"})

    @patch(input_str, lambda x: 'Pizzä ïs Gööd')
    def test_prompt_for_config_unicode(self):
        context = {"cookiecutter": {"full_name": "Your Name"}}

        if not PY3:
            sys.stdin = StringIO("Pizzä ïs Gööd")

        cookiecutter_dict = prompt.prompt_for_config(context)

        if PY3:
            self.assertEqual(cookiecutter_dict, {"full_name": "Pizzä ïs Gööd"})
        else:
            self.assertEqual(cookiecutter_dict, {"full_name": u"Pizzä ïs Gööd"})

    @patch(input_str, lambda x: 'Pizzä ïs Gööd')
    def test_unicode_prompt_for_config_unicode(self):
        context = {"cookiecutter": {"full_name": u"Řekni či napiš své jméno"}}

        if not PY3:
            sys.stdin = StringIO("Pizzä ïs Gööd")

        cookiecutter_dict = prompt.prompt_for_config(context)

        if PY3:
            self.assertEqual(cookiecutter_dict, {"full_name": "Pizzä ïs Gööd"})
        else:
            self.assertEqual(cookiecutter_dict, {"full_name": u"Pizzä ïs Gööd"})

    @patch(input_str, lambda x: '\n')
    def test_unicode_prompt_for_default_config_unicode(self):
        context = {"cookiecutter": {"full_name": u"Řekni či napiš své jméno"}}

        if not PY3:
            sys.stdin = StringIO("\n")

        cookiecutter_dict = prompt.prompt_for_config(context)

        if PY3:
            self.assertEqual(cookiecutter_dict, {"full_name": "Řekni či napiš své jméno"})
        else:
            self.assertEqual(cookiecutter_dict, {"full_name": u"Řekni či napiš své jméno"})


class TestQueryAnswers(unittest.TestCase):

    @patch(input_str, lambda: 'y')
    def test_query_y(self):
        if not PY3:
            sys.stdin = StringIO('y')
        answer = prompt.query_yes_no("Blah?")
        self.assertTrue(answer)

    @patch(input_str, lambda: 'ye')
    def test_query_ye(self):
        if not PY3:
            sys.stdin = StringIO('ye')
        answer = prompt.query_yes_no("Blah?")
        self.assertTrue(answer)

    @patch(input_str, lambda: 'yes')
    def test_query_yes(self):
        if not PY3:
            sys.stdin = StringIO('yes')
        answer = prompt.query_yes_no("Blah?")
        self.assertTrue(answer)

    @patch(input_str, lambda: 'n')
    def test_query_n(self):
        if not PY3:
            sys.stdin = StringIO('n')
        answer = prompt.query_yes_no("Blah?")
        self.assertFalse(answer)

    @patch(input_str, lambda: 'no')
    def test_query_n(self):
        if not PY3:
            sys.stdin = StringIO('no')
        answer = prompt.query_yes_no("Blah?")
        self.assertFalse(answer)


class TestQueryDefaults(unittest.TestCase):

    @patch(input_str, lambda: 'y')
    def test_query_y_none_default(self):
        if not PY3:
            sys.stdin = StringIO('y')
        answer = prompt.query_yes_no("Blah?", default=None)
        self.assertTrue(answer)

    @patch(input_str, lambda: 'n')
    def test_query_n_none_default(self):
        if not PY3:
            sys.stdin = StringIO('n')
        answer = prompt.query_yes_no("Blah?", default=None)
        self.assertFalse(answer)

    @patch(input_str, lambda: '')
    def test_query_no_default(self):
        if not PY3:
            sys.stdin = StringIO('\n')
        answer = prompt.query_yes_no("Blah?", default='no')
        self.assertFalse(answer)

    @patch(input_str, lambda: 'junk')
    def test_query_bad_default(self):
        if not PY3:
            sys.stdin = StringIO('junk')
        self.assertRaises(ValueError, prompt.query_yes_no, "Blah?", default='yn')
