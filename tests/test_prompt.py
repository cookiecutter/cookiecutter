#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_prompt
--------------

Tests for `cookiecutter.prompt` module.
"""

import unittest
from unittest.mock import patch

from cookiecutter import prompt


# class TestPrompt(unittest.TestCase):
#     def test_prompt_for_config(self):
#         context = {"cookiecutter": {"full_name": "Your Name",
#                                     "email": "you@example.com"}}

        # TODO: figure out how to mock input with pexpect or something
        # prompt.prompt_for_config(context)

class TestQueryAnswers(unittest.TestCase):

    @patch('builtins.input', lambda: 'y')
    def test_query_y(self):
        answer = prompt.query_yes_no("Blah?")
        self.assertTrue(answer)

    @patch('builtins.input', lambda: 'ye')
    def test_query_ye(self):
        answer = prompt.query_yes_no("Blah?")
        self.assertTrue(answer)

    @patch('builtins.input', lambda: 'yes')
    def test_query_yes(self):
        answer = prompt.query_yes_no("Blah?")
        self.assertTrue(answer)

    @patch('builtins.input', lambda: 'n')
    def test_query_n(self):
        answer = prompt.query_yes_no("Blah?")
        self.assertFalse(answer)

    @patch('builtins.input', lambda: 'no')
    def test_query_n(self):
        answer = prompt.query_yes_no("Blah?")
        self.assertFalse(answer)

    # @patch('builtins.input', lambda: 'junk')
    # def test_query_junk(self):
    #     answer = prompt.query_yes_no("Blah?")
    #     self.assertTrue(answer)

class TestQueryDefaults(unittest.TestCase):

    @patch('builtins.input', lambda: 'y')
    def test_query_y_none_default(self):
        answer = prompt.query_yes_no("Blah?", default=None)
        self.assertTrue(answer)

    @patch('builtins.input', lambda: 'n')
    def test_query_n_none_default(self):
        answer = prompt.query_yes_no("Blah?", default=None)
        self.assertFalse(answer)

    @patch('builtins.input', lambda: '')
    def test_query_no_default(self):
        answer = prompt.query_yes_no("Blah?", default='no')
        self.assertFalse(answer)

    @patch('builtins.input', lambda: 'junk')
    def test_query_bad_default(self):
        self.assertRaises(ValueError, prompt.query_yes_no, "Blah?", default='yn')
