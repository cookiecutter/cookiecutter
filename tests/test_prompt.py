#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_prompt
-----------

Tests for `cookiecutter.prompt` module.
TestPrompt.test_prompt_for_config_simple
TestPrompt.test_prompt_for_config_unicode
TestPrompt.test_unicode_prompt_for_config_unicode
TestPrompt.test_unicode_prompt_for_default_config_unicode
TestPrompt.test_unicode_prompt_for_templated_config

TestQueryAnswers.test_query_y
TestQueryAnswers.test_query_ye
TestQueryAnswers.test_query_yes
TestQueryAnswers.test_query_n

TestQueryDefaults.test_query_y_none_default
TestQueryDefaults.test_query_n_none_default
TestQueryDefaults.test_query_no_default
TestQueryDefaults.test_query_bad_default
"""

from collections import OrderedDict
import platform

import pytest

from cookiecutter import prompt


@pytest.fixture(autouse=True)
def patch_readline_on_win(monkeypatch):
    if 'windows' in platform.platform().lower():
        monkeypatch.setattr('sys.stdin.readline', lambda: '\n')


class TestPrompt(object):
    def test_prompt_for_config_simple(self, monkeypatch):
        monkeypatch.setattr(
            'cookiecutter.prompt.read_user_variable',
            lambda var, default: u'Audrey Roy'
        )
        context = {'cookiecutter': {'full_name': 'Your Name'}}

        cookiecutter_dict = prompt.prompt_for_config(context)
        assert cookiecutter_dict == {'full_name': u'Audrey Roy'}

    def test_prompt_for_config_unicode(self, monkeypatch):
        monkeypatch.setattr(
            'cookiecutter.prompt.read_user_variable',
            lambda var, default: u'Pizzä ïs Gööd'
        )
        context = {'cookiecutter': {'full_name': 'Your Name'}}

        cookiecutter_dict = prompt.prompt_for_config(context)
        assert cookiecutter_dict == {'full_name': u'Pizzä ïs Gööd'}

    def test_unicode_prompt_for_config_unicode(self, monkeypatch):
        monkeypatch.setattr(
            'cookiecutter.prompt.read_user_variable',
            lambda var, default: u'Pizzä ïs Gööd'
        )
        context = {'cookiecutter': {'full_name': u'Řekni či napiš své jméno'}}

        cookiecutter_dict = prompt.prompt_for_config(context)
        assert cookiecutter_dict == {'full_name': u'Pizzä ïs Gööd'}

    def test_unicode_prompt_for_default_config_unicode(self, monkeypatch):
        monkeypatch.setattr(
            'cookiecutter.prompt.read_user_variable',
            lambda var, default: default
        )
        context = {'cookiecutter': {'full_name': u'Řekni či napiš své jméno'}}

        cookiecutter_dict = prompt.prompt_for_config(context)
        assert cookiecutter_dict == {'full_name': u'Řekni či napiš své jméno'}

    def test_unicode_prompt_for_templated_config(self, monkeypatch):
        monkeypatch.setattr(
            'cookiecutter.prompt.read_user_variable',
            lambda var, default: default
        )
        context = {'cookiecutter': OrderedDict([
            (
                'project_name',
                u'A New Project'
            ), (
                'pkg_name',
                u'{{ cookiecutter.project_name|lower|replace(" ", "") }}'
            )
        ])}

        exp_cookiecutter_dict = {
            'project_name': u'A New Project', 'pkg_name': u'anewproject'
        }
        cookiecutter_dict = prompt.prompt_for_config(context)
        assert cookiecutter_dict == exp_cookiecutter_dict

    def test_dont_prompt_for_private_context_var(self, monkeypatch):
        monkeypatch.setattr(
            'cookiecutter.prompt.read_user_variable',
            lambda var, default: pytest.fail(
                'Should not try to read a response for private context var'
            )
        )
        context = {'cookiecutter': {'_copy_without_render': ['*.html']}}
        cookiecutter_dict = prompt.prompt_for_config(context)
        assert cookiecutter_dict == {'_copy_without_render': ['*.html']}


class TestQueryChoice(object):
    def test_should_invoke_read_user_choice(self, mocker):
        read_choice = mocker.patch('cookiecutter.prompt.read_user_choice')
        read_choice.return_value = 'all'

        read_variable = mocker.patch('cookiecutter.prompt.read_user_variable')

        CHOICES = ['landscape', 'portrait', 'all']
        CONTEXT = {
            'cookiecutter': {
                'orientation': CHOICES
            }
        }

        cookiecutter_dict = prompt.prompt_for_config(CONTEXT)
        assert cookiecutter_dict == {'orientation': 'all'}
        assert not read_variable.called

        read_choice.assert_called_once_with('orientation', CHOICES)
