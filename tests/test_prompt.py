# -*- coding: utf-8 -*-

"""Tests for `cookiecutter.prompt` module."""

import platform
from collections import OrderedDict

import pytest
import six

from cookiecutter import prompt, exceptions, environment


@pytest.mark.parametrize('raw_var, rendered_var', [
    (1, '1'),
    (True, 'True'),
    ('foo', 'foo'),
    ('{{cookiecutter.project}}', 'foobar'),
    (None, None),
])
def test_convert_to_str(mocker, raw_var, rendered_var):
    env = environment.StrictEnvironment()
    from_string = mocker.patch(
        'cookiecutter.prompt.StrictEnvironment.from_string',
        wraps=env.from_string
    )
    context = {'project': 'foobar'}

    result = prompt.render_variable(env, raw_var, context)
    assert result == rendered_var

    # Make sure that non None non str variables are converted beforehand
    if raw_var is not None:
        if not isinstance(raw_var, six.string_types):
            raw_var = str(raw_var)
        from_string.assert_called_once_with(raw_var)
    else:
        assert not from_string.called


@pytest.fixture(autouse=True)
def patch_readline_on_win(monkeypatch):
    if 'windows' in platform.platform().lower():
        monkeypatch.setattr('sys.stdin.readline', lambda: '\n')


class TestPrompt(object):
    """Class to unite user prompt related tests."""

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

    def test_prompt_for_config_empty_dict(self, monkeypatch):
        monkeypatch.setattr(
            'cookiecutter.prompt.read_user_dict',
            lambda var, default: {}
        )
        context = {'cookiecutter': {'details': {}}}

        cookiecutter_dict = prompt.prompt_for_config(context)
        assert cookiecutter_dict == {'details': {}}

    def test_prompt_for_config_dict(self, monkeypatch):
        monkeypatch.setattr(
            'cookiecutter.prompt.read_user_dict',
            lambda var, default: {"key": "value", "integer": 37}
        )
        context = {'cookiecutter': {'details': {}}}

        cookiecutter_dict = prompt.prompt_for_config(context)
        assert cookiecutter_dict == {
            'details': {
                'key': u'value',
                'integer': 37
            }
        }

    def test_prompt_for_config_deep_dict(self, monkeypatch):
        monkeypatch.setattr(
            'cookiecutter.prompt.read_user_dict',
            lambda var, default: {
                "key": "value",
                "integer_key": 37,
                "dict_key": {
                    "deep_key": "deep_value",
                    "deep_integer": 42,
                    "deep_list": [
                        "deep value 1",
                        "deep value 2",
                        "deep value 3",
                    ]
                },
                "list_key": [
                    "value 1",
                    "value 2",
                    "value 3",
                ]
            }
        )
        context = {'cookiecutter': {'details': {}}}

        cookiecutter_dict = prompt.prompt_for_config(context)
        assert cookiecutter_dict == {
            'details': {
                "key": "value",
                "integer_key": 37,
                "dict_key": {
                    "deep_key": "deep_value",
                    "deep_integer": 42,
                    "deep_list": [
                        "deep value 1",
                        "deep value 2",
                        "deep value 3",
                    ]
                },
                "list_key": [
                    "value 1",
                    "value 2",
                    "value 3",
                ]
            }
        }

    def test_should_render_dict(self):
        context = {
            'cookiecutter': {
                'project_name': 'Slartibartfast',
                'details': {
                    'other_name': '{{cookiecutter.project_name}}'
                }
            }
        }

        cookiecutter_dict = prompt.prompt_for_config(context, no_input=True)
        assert cookiecutter_dict == {
            'project_name': 'Slartibartfast',
            'details': {
                'other_name': u'Slartibartfast',
            }
        }

    def test_should_render_deep_dict(self):
        context = {
            'cookiecutter': {
                'project_name': "Slartibartfast",
                'details': {
                    "key": "value",
                    "integer_key": 37,
                    "other_name": '{{cookiecutter.project_name}}',
                    "dict_key": {
                        "deep_key": "deep_value",
                        "deep_integer": 42,
                        "deep_other_name": '{{cookiecutter.project_name}}',
                        "deep_list": [
                            "deep value 1",
                            "{{cookiecutter.project_name}}",
                            "deep value 3",
                        ]
                    },
                    "list_key": [
                        "value 1",
                        "{{cookiecutter.project_name}}",
                        "value 3",
                    ]
                }
            }
        }

        cookiecutter_dict = prompt.prompt_for_config(context, no_input=True)
        assert cookiecutter_dict == {
            'project_name': "Slartibartfast",
            'details': {
                "key": "value",
                "integer_key": "37",
                "other_name": "Slartibartfast",
                "dict_key": {
                    "deep_key": "deep_value",
                    "deep_integer": "42",
                    "deep_other_name": "Slartibartfast",
                    "deep_list": [
                        "deep value 1",
                        "Slartibartfast",
                        "deep value 3",
                    ]
                },
                "list_key": [
                    "value 1",
                    "Slartibartfast",
                    "value 3",
                ]
            }
        }

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
    """Class to unite choices prompt related tests."""

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
    """Class to unite choices prompt related tests with config test."""

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
            environment.StrictEnvironment(),
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
            environment.StrictEnvironment(),
            'orientation',
            choices,
            False  # Ask the user for input
        )
        read_choice.assert_called_once_with('orientation', choices)
        assert expected_choice == actual_choice


def test_undefined_variable_in_cookiecutter_dict():
    context = {
        'cookiecutter': {
            'hello': 'world',
            'foo': '{{cookiecutter.nope}}'
        }
    }
    with pytest.raises(exceptions.UndefinedVariableInTemplate) as err:
        prompt.prompt_for_config(context, no_input=True)

    error = err.value
    assert error.message == "Unable to render variable 'foo'"
    assert error.context == context


def test_undefined_variable_in_cookiecutter_dict_with_choices():
    context = {
        'cookiecutter': {
            'hello': 'world',
            'foo': ['123', '{{cookiecutter.nope}}', '456']
        }
    }
    with pytest.raises(exceptions.UndefinedVariableInTemplate) as err:
        prompt.prompt_for_config(context, no_input=True)

    error = err.value
    assert error.message == "Unable to render variable 'foo'"
    assert error.context == context


def test_undefined_variable_in_cookiecutter_dict_with_dict_key():
    context = {
        'cookiecutter': {
            'hello': 'world',
            'foo': {'{{cookiecutter.nope}}': 'value'}
        }
    }
    with pytest.raises(exceptions.UndefinedVariableInTemplate) as err:
        prompt.prompt_for_config(context, no_input=True)

    error = err.value
    assert error.message == "Unable to render variable 'foo'"
    assert error.context == context


def test_undefined_variable_in_cookiecutter_dict_with_key_value():
    context = {
        'cookiecutter': {
            'hello': 'world',
            'foo': {'key': '{{cookiecutter.nope}}'}
        }
    }
    with pytest.raises(exceptions.UndefinedVariableInTemplate) as err:
        prompt.prompt_for_config(context, no_input=True)

    error = err.value
    assert error.message == "Unable to render variable 'foo'"
    assert error.context == context
