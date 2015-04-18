#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_prompt_choice
------------------

Tests for `cookiecutter.prompt` module related to the *choice* feature.
"""

from collections import OrderedDict
import platform

import pytest
from jinja2.environment import Environment

from cookiecutter import prompt


@pytest.fixture(autouse=True)
def patch_readline_on_win(monkeypatch):
    if 'windows' in platform.platform().lower():
        monkeypatch.setattr('sys.stdin.readline', lambda: '\n')


def test_should_not_invoke_read_response(monkeypatch):
    """Test that ``read_response`` is not called when running
    ``prompt_for_config`` and the context only holds a list variable.
    """
    monkeypatch.setattr(
        'cookiecutter.prompt.read_response',
        lambda _: pytest.fail(
            'Should not call read_response to query a choice'
        )
    )
    monkeypatch.setattr(
        'cookiecutter.prompt.read_choice',
        lambda prompt, options: 'all'
    )
    context = {
        'cookiecutter': {
            'orientation': ['landscape', 'portrait', 'all']
        }
    }

    cookiecutter_dict = prompt.prompt_for_config(context)
    assert cookiecutter_dict == {'orientation': 'all'}


def test_should_not_invoke_read_choice(monkeypatch):
    """Test that ``read_choice`` is not called when running
    ``prompt_for_config`` and the context does not hold a list variable.
    """
    monkeypatch.setattr(
        'cookiecutter.prompt.read_choice',
        lambda p, o: pytest.fail(
            'Should not call read_choice to query non list variable'
        )
    )
    monkeypatch.setattr(
        'cookiecutter.prompt.read_response',
        lambda x=u'': u'Audrey Roy'
    )
    context = {'cookiecutter': {'full_name': 'Your Name'}}

    cookiecutter_dict = prompt.prompt_for_config(context)
    assert cookiecutter_dict == {'full_name': u'Audrey Roy'}


def test_should_render_choices(monkeypatch):
    """Test that templated variable are still being rendered as we go even
    when they are part of a choice variable. The ``monkeypatch`` version of
    ``read_choice`` simply returns the second option so we can verify that it
    has been rendered just as we do with regular variables.
    """
    monkeypatch.setattr(
        'cookiecutter.prompt.read_choice',
        lambda prompt, options: options[1]
    )
    monkeypatch.setattr(
        'cookiecutter.prompt.read_response',
        lambda x=u'': u'\n'
    )
    context = {'cookiecutter': OrderedDict([
        (
            'project_name',
            u'A New Project'
        ), (
            'pkg_name',
            [
                u'foo',
                u'{{ cookiecutter.project_name|lower|replace(" ", "") }}',
                u'bar'
            ]
        )
    ])}

    exp_cookiecutter_dict = {
        'project_name': u'A New Project', 'pkg_name': u'anewproject'
    }
    cookiecutter_dict = prompt.prompt_for_config(context)
    assert cookiecutter_dict == exp_cookiecutter_dict


def test_should_return_first_option_if_no_input(monkeypatch):
    """Test that ``prompt_choice_for_config`` returns the very first option
    when ``no_input`` is True. This pretty much mimics the behaviour of
    the default value in ``read_choice``.
    """
    env = Environment()
    key = 'orientation'
    options = ['landscape', 'portrait', 'all']
    cookiecutter_dict = {key: options}

    val = prompt.prompt_choice_for_config(
        cookiecutter_dict, env, key, options, no_input=True
    )
    assert val == 'landscape'
