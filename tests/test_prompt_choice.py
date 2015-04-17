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

from cookiecutter import prompt


@pytest.fixture(autouse=True)
def patch_readline_on_win(monkeypatch):
    if 'windows' in platform.platform().lower():
        monkeypatch.setattr('sys.stdin.readline', lambda: '\n')


def test_should_invoke_read_choice(monkeypatch):
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


def test_should_not_invoke_read_response(monkeypatch):
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
    monkeypatch.setattr(
        'cookiecutter.prompt.read_choice',
        lambda p, o: u'anewproject'
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
