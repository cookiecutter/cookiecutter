#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_prompt
-----------

Tests for `cookiecutter.prompt` module.
"""

from collections import OrderedDict
import platform

import pytest
from past.builtins import basestring

from cookiecutter import prompt
from jinja2.environment import Environment


@pytest.mark.parametrize('raw_var, rendered_var', [
    (1, '1'),
    (True, 'True'),
    ('foo', 'foo'),
    ('{{cookiecutter.project}}', 'foobar')
])
def test_convert_to_str(mocker, raw_var, rendered_var):
    env = Environment()
    from_string = mocker.patch(
        'cookiecutter.prompt.Environment.from_string',
        wraps=env.from_string
    )
    context = {'project': 'foobar'}

    result = prompt.render_variable(env, raw_var, context)
    assert result == rendered_var

    # Make sure that non str variables are conerted beforehand
    if not isinstance(raw_var, basestring):
        raw_var = str(raw_var)
    from_string.assert_called_once_with(raw_var)


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


class TestReadUserChoice(object):
    def test_should_invoke_read_user_choice(self, mocker):
        prompt_choice = mocker.patch(
            'cookiecutter.prompt.prompt_choice_for_config',
            wraps=prompt.prompt_choice_for_config
        )

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

        assert not read_variable.called
        assert prompt_choice.called
        read_choice.assert_called_once_with('orientation', CHOICES)
        assert cookiecutter_dict == {'orientation': 'all'}

    def test_should_not_invoke_read_user_variable(self, mocker):
        read_variable = mocker.patch('cookiecutter.prompt.read_user_variable')
        read_variable.return_value = u'Audrey Roy'

        prompt_choice = mocker.patch(
            'cookiecutter.prompt.prompt_choice_for_config'
        )

        read_choice = mocker.patch('cookiecutter.prompt.read_user_choice')

        CONTEXT = {'cookiecutter': {'full_name': 'Your Name'}}

        cookiecutter_dict = prompt.prompt_for_config(CONTEXT)

        assert not prompt_choice.called
        assert not read_choice.called
        read_variable.assert_called_once_with('full_name', 'Your Name')
        assert cookiecutter_dict == {'full_name': u'Audrey Roy'}

    def test_should_render_choices(self, mocker):
        read_choice = mocker.patch('cookiecutter.prompt.read_user_choice')
        read_choice.return_value = u'anewproject'

        read_variable = mocker.patch('cookiecutter.prompt.read_user_variable')
        read_variable.return_value = u'A New Project'

        RENDERED_CHOICES = [
            u'foo',
            u'anewproject',
            u'bar'
        ]

        CONTEXT = {'cookiecutter': OrderedDict([
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

        EXP_COOKIECUTTER_DICT = {
            'project_name': u'A New Project', 'pkg_name': u'anewproject'
        }
        cookiecutter_dict = prompt.prompt_for_config(CONTEXT)

        read_variable.assert_called_once_with('project_name', u'A New Project')
        read_choice.assert_called_once_with('pkg_name', RENDERED_CHOICES)
        assert cookiecutter_dict == EXP_COOKIECUTTER_DICT


class TestPromptChoiceForConfig(object):
    @pytest.fixture
    def choices(self):
        return ['landscape', 'portrait', 'all']

    @pytest.fixture
    def context(self, choices):
        return {
            'cookiecutter': {
                'orientation': choices
            }
        }

    def test_should_return_first_option_if_no_input(
            self, mocker, choices, context):
        read_choice = mocker.patch('cookiecutter.prompt.read_user_choice')

        expected_choice = choices[0]

        actual_choice = prompt.prompt_choice_for_config(
            context,
            Environment(),
            'orientation',
            choices,
            True  # Suppress user input
        )
        assert not read_choice.called
        assert expected_choice == actual_choice

    def test_should_read_userchoice(self, mocker, choices, context):
        read_choice = mocker.patch('cookiecutter.prompt.read_user_choice')
        read_choice.return_value = 'all'

        expected_choice = 'all'

        actual_choice = prompt.prompt_choice_for_config(
            context,
            Environment(),
            'orientation',
            choices,
            False  # Ask the user for input
        )
        read_choice.assert_called_once_with('orientation', choices)
        assert expected_choice == actual_choice
