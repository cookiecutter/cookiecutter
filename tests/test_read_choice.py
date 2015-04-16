#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from cookiecutter.compat import read_choice

OPTIONS = ['hello', 'world', 'foo', 'bar']


EXPECTED_PROMPT = """Select varname:
    1 - hello
    2 - world
    3 - foo
    4 - bar
Choose from 1, 2, 3, 4!"""


@pytest.mark.parametrize('user_choice, expected_value', enumerate(OPTIONS, 1))
def test_read_choice(monkeypatch, user_choice, expected_value):
    def _monkey_prompt(prompt, **kwargs):
        assert prompt == EXPECTED_PROMPT
        return str(user_choice)
    monkeypatch.setattr('click.prompt', _monkey_prompt)

    assert read_choice('varname', OPTIONS) == expected_value
