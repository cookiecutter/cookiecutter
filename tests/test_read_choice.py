#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click
import pytest

from cookiecutter.prompt import read_choice

OPTIONS = ['hello', 'world', 'foo', 'bar']


EXPECTED_PROMPT = """Select varname:
    1 - hello
    2 - world
    3 - foo
    4 - bar
Choose from 1, 2, 3, 4:"""


@pytest.mark.parametrize('user_choice, expected_value', enumerate(OPTIONS, 1))
def test_read_choice(monkeypatch, user_choice, expected_value):
    """Make sure that ``click.prompt`` is being called with the desired prompt
    and choice type. Patch it so that it returns str value of the
    ``user_choice`` fixture.
    """
    def _monkey_prompt(prompt, type=None, default='1'):
        assert prompt == EXPECTED_PROMPT
        assert isinstance(type, click.Choice)
        assert list(type.choices) == ['1', '2', '3', '4']
        return str(user_choice)
    monkeypatch.setattr('click.prompt', _monkey_prompt)

    assert read_choice('varname', OPTIONS) == expected_value


@pytest.fixture(autouse=True)
def patch_readline(monkeypatch):
    monkeypatch.setattr('sys.stdin.readline', lambda: '\n')


def test_default(monkeypatch):
    """Make sure that the default is properly set for click.prompt."""
    assert read_choice('varname', OPTIONS) == OPTIONS[0]
