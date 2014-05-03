#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_prompt
--------------

Tests for `cookiecutter.prompt` module.
"""

import sys
import unittest

from cookiecutter import prompt

PY3 = sys.version > '3'
if PY3:
    from unittest.mock import patch
    input_str = 'cookiecutter.prompt.get_input'
else:
    import __builtin__
    from mock import patch
    input_str = 'cookiecutter.prompt.get_input'
    from cStringIO import StringIO

if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest


class TestPrompt(unittest.TestCase):

    @patch(input_str, lambda x: 'Audrey Roy')
    def test_prompt_for_config_simple(self):
        context = {"cookiecutter": {"full_name": "Your Name"}}

        cookiecutter_dict = prompt.prompt_for_config(context)
        self.assertEqual(cookiecutter_dict, {"full_name": "Audrey Roy"})

    @patch(input_str, lambda x: 'Pizzä ïs Gööd')
    def test_prompt_for_config_unicode(self):
        context = {"cookiecutter": {"full_name": "Your Name"}}

        cookiecutter_dict = prompt.prompt_for_config(context)

        if PY3:
            self.assertEqual(cookiecutter_dict, {"full_name": "Pizzä ïs Gööd"})
        else:
            self.assertEqual(cookiecutter_dict, {"full_name": u"Pizzä ïs Gööd"})

    @patch(input_str, lambda x: 'Pizzä ïs Gööd')
    def test_unicode_prompt_for_config_unicode(self):
        context = {"cookiecutter": {"full_name": u"Řekni či napiš své jméno"}}

        cookiecutter_dict = prompt.prompt_for_config(context)

        if PY3:
            self.assertEqual(cookiecutter_dict, {"full_name": "Pizzä ïs Gööd"})
        else:
            self.assertEqual(cookiecutter_dict, {"full_name": u"Pizzä ïs Gööd"})

    @patch(input_str, lambda x: '\n')
    def test_unicode_prompt_for_default_config_unicode(self):
        context = {"cookiecutter": {"full_name": u"Řekni či napiš své jméno"}}

        cookiecutter_dict = prompt.prompt_for_config(context)

        if PY3:
            self.assertEqual(cookiecutter_dict, {"full_name": "Řekni či napiš své jméno"})
        else:
            self.assertEqual(cookiecutter_dict, {"full_name": u"Řekni či napiš své jméno"})


    def test_custom_prompt(self):
        context = {"cookiecutter": {"full_name": {"default": u"Pizzä ïs Gööd",
                                                  "prompt": u"Prompt"}}}

        def _check_prompt(x):
            if PY3:
                self.assertEqual(x, "Prompt (default is \"Pizzä ïs Gööd\")? ")
            else:
                self.assertEqual(unicode(x), u"Prompt (default is \"Pizzä ïs Gööd\")? ")
            return '_check_prompt\n'

        with patch(input_str, _check_prompt):
            cookiecutter_dict = prompt.prompt_for_config(context)

        if PY3:
            self.assertEqual(cookiecutter_dict, {"full_name": "_check_prompt"})
        else:
            self.assertEqual(cookiecutter_dict, {"full_name": u"_check_prompt"})

    @patch(input_str, lambda x: '200\n')
    def test_extended_prompt_type_int(self):
        context = {"cookiecutter": {"value": {"type": "int"}}}

        cookiecutter_dict = prompt.prompt_for_config(context)
        self.assertEqual(cookiecutter_dict, {"value": 200})

    @patch(input_str, lambda x: '0\n')
    def test_extended_prompt_type_bool_0(self):
        context = {"cookiecutter": {"logic": {"type": "bool"}}}

        if not PY3:
            sys.stdin = StringIO("0\n")

        cookiecutter_dict = prompt.prompt_for_config(context)
        self.assertEqual(cookiecutter_dict, {"logic": False})

    @patch(input_str, lambda x: 'n\n')
    def test_extended_prompt_type_bool_n(self):
        context = {"cookiecutter": {"logic": {"type": "bool"}}}

        if not PY3:
            sys.stdin = StringIO("n\n")

        cookiecutter_dict = prompt.prompt_for_config(context)
        self.assertEqual(cookiecutter_dict, {"logic": False})

    @patch(input_str, lambda x: 'y\n')
    def test_extended_prompt_type_bool_y(self):
        context = {"cookiecutter": {"logic": {"type": "bool"}}}

        if not PY3:
            sys.stdin = StringIO("y\n")

        cookiecutter_dict = prompt.prompt_for_config(context)
        self.assertEqual(cookiecutter_dict, {"logic": True})

    @patch(input_str, lambda x: '\n')
    def test_extended_prompt_type_bool_default(self):
        context = {"cookiecutter": {"logic": {"type": "bool", "default":  "Y"}}}

        if not PY3:
            sys.stdin = StringIO("\n")

        cookiecutter_dict = prompt.prompt_for_config(context)
        self.assertEqual(cookiecutter_dict, {"logic": True})

class TestQueryAnswers(unittest.TestCase):

    @patch(input_str, lambda: 'y')
    def test_query_y(self):
        answer = prompt.query_yes_no("Blah?")
        self.assertTrue(answer)

    @patch(input_str, lambda: 'ye')
    def test_query_ye(self):
        answer = prompt.query_yes_no("Blah?")
        self.assertTrue(answer)

    @patch(input_str, lambda: 'yes')
    def test_query_yes(self):
        answer = prompt.query_yes_no("Blah?")
        self.assertTrue(answer)

    @patch(input_str, lambda: 'n')
    def test_query_n(self):
        answer = prompt.query_yes_no("Blah?")
        self.assertFalse(answer)

    @patch(input_str, lambda: 'no')
    def test_query_n(self):
        answer = prompt.query_yes_no("Blah?")
        self.assertFalse(answer)


class TestQueryDefaults(unittest.TestCase):

    @patch(input_str, lambda: 'y')
    def test_query_y_none_default(self):
        answer = prompt.query_yes_no("Blah?", default=None)
        self.assertTrue(answer)

    @patch(input_str, lambda: 'n')
    def test_query_n_none_default(self):
        answer = prompt.query_yes_no("Blah?", default=None)
        self.assertFalse(answer)

    @patch(input_str, lambda: '')
    def test_query_no_default(self):
        answer = prompt.query_yes_no("Blah?", default='no')
        self.assertFalse(answer)

    @patch(input_str, lambda: 'junk')
    def test_query_bad_default(self):
        self.assertRaises(ValueError, prompt.query_yes_no, "Blah?", default='yn')
