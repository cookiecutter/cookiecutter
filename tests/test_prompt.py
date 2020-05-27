"""Tests for `cookiecutter.prompt` module."""
import platform
from collections import OrderedDict

import pytest

from cookiecutter import prompt, exceptions, environment


@pytest.fixture(autouse=True)
def patch_readline_on_win(monkeypatch):
    """Fixture. Overwrite windows end of line to linux standard."""
    if 'windows' in platform.platform().lower():
        monkeypatch.setattr('sys.stdin.readline', lambda: '\n')


class TestRenderVariable:
    """Class to unite simple and complex tests for render_variable function."""

    @pytest.mark.parametrize(
        'raw_var, rendered_var',
        [
            (1, '1'),
            (True, 'True'),
            ('foo', 'foo'),
            ('{{cookiecutter.project}}', 'foobar'),
            (None, None),
        ],
    )
    def test_convert_to_str(self, mocker, raw_var, rendered_var):
        """Verify simple items correctly rendered to strings."""
        env = environment.StrictEnvironment()
        from_string = mocker.patch(
            'cookiecutter.prompt.StrictEnvironment.from_string', wraps=env.from_string
        )
        context = {'project': 'foobar'}

        result = prompt.render_variable(env, raw_var, context)
        assert result == rendered_var

        # Make sure that non None non str variables are converted beforehand
        if raw_var is not None:
            if not isinstance(raw_var, str):
                raw_var = str(raw_var)
            from_string.assert_called_once_with(raw_var)
        else:
            assert not from_string.called

    @pytest.mark.parametrize(
        'raw_var, rendered_var',
        [
            ({1: True, 'foo': False}, {'1': 'True', 'foo': 'False'}),
            (
                {'{{cookiecutter.project}}': ['foo', 1], 'bar': False},
                {'foobar': ['foo', '1'], 'bar': 'False'},
            ),
            (['foo', '{{cookiecutter.project}}', None], ['foo', 'foobar', None]),
        ],
    )
    def test_convert_to_str_complex_variables(self, raw_var, rendered_var):
        """Verify tree items correctly rendered."""
        env = environment.StrictEnvironment()
        context = {'project': 'foobar'}

        result = prompt.render_variable(env, raw_var, context)
        assert result == rendered_var


class TestPrompt(object):
    """Class to unite user prompt related tests."""

    @pytest.mark.parametrize(
        'context',
        [
            {'cookiecutter': {'full_name': 'Your Name'}},
            {'cookiecutter': {'full_name': 'Řekni či napiš své jméno'}},
        ],
        ids=['ASCII default prompt/input', 'Unicode default prompt/input'],
    )
    def test_prompt_for_config(self, monkeypatch, context):
        """Verify `prompt_for_config` call `read_user_variable` on text request."""
        monkeypatch.setattr(
            'cookiecutter.prompt.read_user_variable', lambda var, default: default,
        )

        cookiecutter_dict = prompt.prompt_for_config(context)
        assert cookiecutter_dict == context['cookiecutter']

    def test_prompt_for_config_dict(self, monkeypatch):
        """Verify `prompt_for_config` call `read_user_variable` on dict request."""
        monkeypatch.setattr(
            'cookiecutter.prompt.read_user_dict',
            lambda var, default: {"key": "value", "integer": 37},
        )
        context = {'cookiecutter': {'details': {}}}

        cookiecutter_dict = prompt.prompt_for_config(context)
        assert cookiecutter_dict == {'details': {'key': 'value', 'integer': 37}}

    def test_should_render_dict(self):
        """Verify template inside dictionary variable rendered."""
        context = {
            'cookiecutter': {
                'project_name': 'Slartibartfast',
                'details': {
                    '{{cookiecutter.project_name}}': '{{cookiecutter.project_name}}'
                },
            }
        }

        cookiecutter_dict = prompt.prompt_for_config(context, no_input=True)
        assert cookiecutter_dict == {
            'project_name': 'Slartibartfast',
            'details': {'Slartibartfast': 'Slartibartfast'},
        }

    def test_should_render_deep_dict(self):
        """Verify nested structures like dict in dict, rendered correctly."""
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
                        ],
                    },
                    "list_key": [
                        "value 1",
                        "{{cookiecutter.project_name}}",
                        "value 3",
                    ],
                },
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
                    "deep_list": ["deep value 1", "Slartibartfast", "deep value 3"],
                },
                "list_key": ["value 1", "Slartibartfast", "value 3"],
            },
        }

    def test_prompt_for_templated_config(self, monkeypatch):
        """Verify Jinja2 templating works in unicode prompts."""
        monkeypatch.setattr(
            'cookiecutter.prompt.read_user_variable', lambda var, default: default
        )
        context = {
            'cookiecutter': OrderedDict(
                [
                    ('project_name', 'A New Project'),
                    (
                        'pkg_name',
                        '{{ cookiecutter.project_name|lower|replace(" ", "") }}',
                    ),
                ]
            )
        }

        exp_cookiecutter_dict = {
            'project_name': 'A New Project',
            'pkg_name': 'anewproject',
        }
        cookiecutter_dict = prompt.prompt_for_config(context)
        assert cookiecutter_dict == exp_cookiecutter_dict

    def test_dont_prompt_for_private_context_var(self, monkeypatch):
        """Verify `read_user_variable` not called for private context variables."""
        monkeypatch.setattr(
            'cookiecutter.prompt.read_user_variable',
            lambda var, default: pytest.fail(
                'Should not try to read a response for private context var'
            ),
        )
        context = {'cookiecutter': {'_copy_without_render': ['*.html']}}
        cookiecutter_dict = prompt.prompt_for_config(context)
        assert cookiecutter_dict == {'_copy_without_render': ['*.html']}

    def test_should_render_private_variables_with_two_underscores(self):
        """Test rendering of private variables with two underscores.

        There are three cases:
        1. Variables beginning with a single underscore are private and not rendered.
        2. Variables beginning with a double underscore are private and are rendered.
        3. Variables beginning with anything other than underscores are not private and
           are rendered.
        """
        context = {
            'cookiecutter': OrderedDict(
                [
                    ('foo', 'Hello world'),
                    ('bar', 123),
                    ('rendered_foo', u'{{ cookiecutter.foo|lower }}'),
                    ('rendered_bar', 123),
                    ('_hidden_foo', u'{{ cookiecutter.foo|lower }}'),
                    ('_hidden_bar', 123),
                    ('__rendered_hidden_foo', u'{{ cookiecutter.foo|lower }}'),
                    ('__rendered_hidden_bar', 123),
                ]
            )
        }
        cookiecutter_dict = prompt.prompt_for_config(context, no_input=True)
        assert cookiecutter_dict == OrderedDict(
            [
                ('foo', 'Hello world'),
                ('bar', '123'),
                ('rendered_foo', 'hello world'),
                ('rendered_bar', '123'),
                ('_hidden_foo', u'{{ cookiecutter.foo|lower }}'),
                ('_hidden_bar', 123),
                ('__rendered_hidden_foo', 'hello world'),
                ('__rendered_hidden_bar', '123'),
            ]
        )

    def test_should_not_render_private_variables(self):
        """Verify private(underscored) variables not rendered by `prompt_for_config`.

        Private variables designed to be raw, same as context input.
        """
        context = {
            'cookiecutter': {
                'project_name': 'Skip render',
                '_skip_jinja_template': '{{cookiecutter.project_name}}',
                '_skip_float': 123.25,
                '_skip_integer': 123,
                '_skip_boolean': True,
                '_skip_nested': True,
            }
        }
        cookiecutter_dict = prompt.prompt_for_config(context, no_input=True)
        assert cookiecutter_dict == context['cookiecutter']


class TestReadUserChoice(object):
    """Class to unite choices prompt related tests."""

    def test_should_invoke_read_user_choice(self, mocker):
        """Verify correct function called for select(list) variables."""
        prompt_choice = mocker.patch(
            'cookiecutter.prompt.prompt_choice_for_config',
            wraps=prompt.prompt_choice_for_config,
        )

        read_user_choice = mocker.patch('cookiecutter.prompt.read_user_choice')
        read_user_choice.return_value = 'all'

        read_user_variable = mocker.patch('cookiecutter.prompt.read_user_variable')

        choices = ['landscape', 'portrait', 'all']
        context = {'cookiecutter': {'orientation': choices}}

        cookiecutter_dict = prompt.prompt_for_config(context)

        assert not read_user_variable.called
        assert prompt_choice.called
        read_user_choice.assert_called_once_with('orientation', choices)
        assert cookiecutter_dict == {'orientation': 'all'}

    def test_should_invoke_read_user_variable(self, mocker):
        """Verify correct function called for string input variables."""
        read_user_variable = mocker.patch('cookiecutter.prompt.read_user_variable')
        read_user_variable.return_value = 'Audrey Roy'

        prompt_choice = mocker.patch('cookiecutter.prompt.prompt_choice_for_config')

        read_user_choice = mocker.patch('cookiecutter.prompt.read_user_choice')

        context = {'cookiecutter': {'full_name': 'Your Name'}}

        cookiecutter_dict = prompt.prompt_for_config(context)

        assert not prompt_choice.called
        assert not read_user_choice.called
        read_user_variable.assert_called_once_with('full_name', 'Your Name')
        assert cookiecutter_dict == {'full_name': 'Audrey Roy'}

    def test_should_render_choices(self, mocker):
        """Verify Jinja2 templating engine works inside choices variables."""
        read_user_choice = mocker.patch('cookiecutter.prompt.read_user_choice')
        read_user_choice.return_value = 'anewproject'

        read_user_variable = mocker.patch('cookiecutter.prompt.read_user_variable')
        read_user_variable.return_value = 'A New Project'

        rendered_choices = ['foo', 'anewproject', 'bar']

        context = {
            'cookiecutter': OrderedDict(
                [
                    ('project_name', 'A New Project'),
                    (
                        'pkg_name',
                        [
                            'foo',
                            '{{ cookiecutter.project_name|lower|replace(" ", "") }}',
                            'bar',
                        ],
                    ),
                ]
            )
        }

        expected = {
            'project_name': 'A New Project',
            'pkg_name': 'anewproject',
        }
        cookiecutter_dict = prompt.prompt_for_config(context)

        read_user_variable.assert_called_once_with('project_name', 'A New Project')
        read_user_choice.assert_called_once_with('pkg_name', rendered_choices)
        assert cookiecutter_dict == expected


class TestPromptChoiceForConfig(object):
    """Class to unite choices prompt related tests with config test."""

    @pytest.fixture
    def choices(self):
        """Fixture. Just populate choices variable."""
        return ['landscape', 'portrait', 'all']

    @pytest.fixture
    def context(self, choices):
        """Fixture. Just populate context variable."""
        return {'cookiecutter': {'orientation': choices}}

    def test_should_return_first_option_if_no_input(self, mocker, choices, context):
        """Verify prompt_choice_for_config return first list option on no_input=True."""
        read_user_choice = mocker.patch('cookiecutter.prompt.read_user_choice')

        expected_choice = choices[0]

        actual_choice = prompt.prompt_choice_for_config(
            cookiecutter_dict=context,
            env=environment.StrictEnvironment(),
            key='orientation',
            options=choices,
            no_input=True,  # Suppress user input
        )

        assert not read_user_choice.called
        assert expected_choice == actual_choice

    def test_should_read_user_choice(self, mocker, choices, context):
        """Verify prompt_choice_for_config return user selection on no_input=False."""
        read_user_choice = mocker.patch('cookiecutter.prompt.read_user_choice')
        read_user_choice.return_value = 'all'

        expected_choice = 'all'

        actual_choice = prompt.prompt_choice_for_config(
            cookiecutter_dict=context,
            env=environment.StrictEnvironment(),
            key='orientation',
            options=choices,
            no_input=False,  # Ask the user for input
        )
        read_user_choice.assert_called_once_with('orientation', choices)
        assert expected_choice == actual_choice


@pytest.mark.parametrize(
    'context',
    (
        {'cookiecutter': {'foo': '{{cookiecutter.nope}}'}},
        {'cookiecutter': {'foo': ['123', '{{cookiecutter.nope}}', '456']}},
        {'cookiecutter': {'foo': {'{{cookiecutter.nope}}': 'value'}}},
        {'cookiecutter': {'foo': {'key': '{{cookiecutter.nope}}'}}},
    ),
    ids=[
        'Undefined variable in cookiecutter dict',
        'Undefined variable in cookiecutter dict with choices',
        'Undefined variable in cookiecutter dict with dict_key',
        'Undefined variable in cookiecutter dict with key_value',
    ],
)
def test_undefined_variable(context):
    """Verify `prompt.prompt_for_config` raises correct error."""
    with pytest.raises(exceptions.UndefinedVariableInTemplate) as err:
        prompt.prompt_for_config(context, no_input=True)

    error = err.value
    assert error.message == "Unable to render variable 'foo'"
    assert error.context == context
