#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_prompt
--------------

Tests for `cookiecutter.prompt` module.
"""

import unittest

from cookiecutter import prompt


class TestPrompt(unittest.TestCase):
    def test_prompt_for_config(self):
        context = {"cookiecutter": {"full_name": "Your Name",
                                    "email": "you@example.com"}}

        # TODO: figure out how to mock input with pexpect or something
        # prompt.prompt_for_config(context)
