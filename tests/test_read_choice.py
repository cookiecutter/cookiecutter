#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click
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
    """Make sure that ``click.prompt`` is being called with the desired prompt
    and choice type. Patch it so that it returns str value of the
    ``user_choice`` fixture.
    """
    def _monkey_prompt(prompt, type=None):
        assert prompt == EXPECTED_PROMPT
        assert isinstance(type, click.Choice)
        assert type.choices == ['1', '2', '3', '4']
        return str(user_choice)
    monkeypatch.setattr('click.prompt', _monkey_prompt)

    assert read_choice('varname', OPTIONS) == expected_value
