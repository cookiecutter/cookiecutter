"""Tests for `cookiecutter.prompt` module."""

from __future__ import annotations

import json
import platform
import sys
from collections import OrderedDict
from pathlib import Path
from typing import Any

import click
import pytest

from cookiecutter import environment, exceptions, prompt


@pytest.fixture(autouse=True)
def patch_readline_on_win(monkeypatch) -> None:
    """Fixture. Overwrite windows end of line to linux standard."""
    if 'windows' in platform.platform().lower():
        monkeypatch.setattr('sys.stdin.readline', lambda: '\n')


class TestRenderVariable:
    """Class to unite simple and complex tests for render_variable function."""

    @pytest.mark.parametrize(
        'raw_var, rendered_var',
        [
            (1, '1'),
            (True, True),
            ('foo', 'foo'),
            ('{{cookiecutter.project}}', 'foobar'),
            (None, None),
        ],
    )
    def test_convert_to_str(self, mocker, raw_var, rendered_var) -> None:
        """Verify simple items correctly rendered to strings."""
        env = environment.StrictEnvironment()
        from_string = mocker.patch(
            'cookiecutter.utils.StrictEnvironment.from_string', wraps=env.from_string
        )
        context = {'project': 'foobar'}

        result = prompt.render_variable(env, raw_var, context)
        assert result == rendered_var

        # Make sure that non None non str variables are converted beforehand
        if raw_var is not None and not isinstance(raw_var, bool):
            if not isinstance(raw_var, str):
                raw_var = str(raw_var)
            from_string.assert_called_once_with(raw_var)
        else:
            assert not from_string.called

    @pytest.mark.parametrize(
        'raw_var, rendered_var',
        [
            ({1: True, 'foo': False}, {'1': True, 'foo': False}),
            (
                {'{{cookiecutter.project}}': ['foo', 1], 'bar': False},
                {'foobar': ['foo', '1'], 'bar': False},
            ),
            (['foo', '{{cookiecutter.project}}', None], ['foo', 'foobar', None]),
        ],
    )
    def test_convert_to_str_complex_variables(self, raw_var, rendered_var) -> None:
        """Verify tree items correctly rendered."""
        env = environment.StrictEnvironment()
        context = {'project': 'foobar'}

        result = prompt.render_variable(env, raw_var, context)
        assert result == rendered_var


class TestPrompt:
    """Class to unite user prompt related tests."""

    @pytest.mark.parametrize(
        'context',
        [
            {'cookiecutter': {'full_name': 'Your Name'}},
            {'cookiecutter': {'full_name': 'Řekni či napiš své jméno'}},
        ],
        ids=['ASCII default prompt/input', 'Unicode default prompt/input'],
    )
    def test_prompt_for_config(self, monkeypatch, context) -> None:
        """Verify `prompt_for_config` call `read_user_variable` on text request."""
        monkeypatch.setattr(
            'cookiecutter.prompt.read_user_variable',
            lambda _var, default, _prompts, _prefix: default,
        )

        cookiecutter_dict = prompt.prompt_for_config(context)
        assert cookiecutter_dict == context['cookiecutter']

    @pytest.mark.parametrize(
        'context',
        [
            {
                'cookiecutter': {
                    'full_name': 'Your Name',
                    'check': ['yes', 'no'],
                    'nothing': 'ok',
                    '__prompts__': {
                        'full_name': 'Name please',
                        'check': 'Checking',
                    },
                }
            },
        ],
        ids=['ASCII default prompt/input'],
    )
    def test_prompt_for_config_with_human_prompts(self, monkeypatch, context) -> None:
        """Verify call `read_user_variable` on request when human-readable prompts."""
        monkeypatch.setattr(
            'cookiecutter.prompt.read_user_variable',
            lambda _var, default, _prompts, _prefix: default,
        )
        monkeypatch.setattr(
            'cookiecutter.prompt.read_user_yes_no',
            lambda _var, default, _prompts, _prefix: default,
        )
        monkeypatch.setattr(
            'cookiecutter.prompt.read_user_choice',
            lambda _var, default, _prompts, _prefix: default,
        )

        cookiecutter_dict = prompt.prompt_for_config(context)
        assert cookiecutter_dict == context['cookiecutter']

    @pytest.mark.parametrize(
        'context',
        [
            {
                'cookiecutter': {
                    'full_name': 'Your Name',
                    'check': ['yes', 'no'],
                    '__prompts__': {
                        'check': 'Checking',
                    },
                }
            },
            {
                'cookiecutter': {
                    'full_name': 'Your Name',
                    'check': ['yes', 'no'],
                    '__prompts__': {
                        'full_name': 'Name please',
                        'check': {'__prompt__': 'Checking', 'yes': 'Yes', 'no': 'No'},
                    },
                }
            },
            {
                'cookiecutter': {
                    'full_name': 'Your Name',
                    'check': ['yes', 'no'],
                    '__prompts__': {
                        'full_name': 'Name please',
                        'check': {'no': 'No'},
                    },
                }
            },
        ],
    )
    def test_prompt_for_config_with_human_choices(self, context) -> None:
        """Test prompts when human-readable labels for user choices."""
        runner = click.testing.CliRunner()
        with runner.isolation(input="\n\n\n"):
            cookiecutter_dict = prompt.prompt_for_config(context)

        assert dict(cookiecutter_dict) == {'full_name': 'Your Name', 'check': 'yes'}

    def test_prompt_for_config_dict(self, monkeypatch) -> None:
        """Verify `prompt_for_config` call `read_user_variable` on dict request."""
        monkeypatch.setattr(
            'cookiecutter.prompt.read_user_dict',
            lambda _var, _default, _prompts, _prefix: {"key": "value", "integer": 37},
        )
        context: dict[str, Any] = {'cookiecutter': {'details': {}}}

        cookiecutter_dict = prompt.prompt_for_config(context)
        assert cookiecutter_dict == {'details': {'key': 'value', 'integer': 37}}

    def test_should_render_dict(self) -> None:
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

    def test_should_render_deep_dict(self) -> None:
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

    def test_should_render_deep_dict_with_human_prompts(self) -> None:
        """Verify dict rendered correctly when human-readable prompts."""
        context = {
            'cookiecutter': {
                'project_name': "Slartibartfast",
                'details': {
                    "key": "value",
                    "integer_key": 37,
                    "other_name": '{{cookiecutter.project_name}}',
                    "dict_key": {
                        "deep_key": "deep_value",
                    },
                },
                '__prompts__': {'project_name': 'Project name'},
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
                },
            },
        }

    def test_internal_use_no_human_prompts(self) -> None:
        """Verify dict rendered correctly when human-readable prompts empty."""
        context = {
            'cookiecutter': {
                'project_name': "Slartibartfast",
                '__prompts__': {},
            }
        }
        cookiecutter_dict = prompt.prompt_for_config(context, no_input=True)
        assert cookiecutter_dict == {
            'project_name': "Slartibartfast",
        }

    def test_prompt_for_templated_config(self, monkeypatch) -> None:
        """Verify Jinja2 templating works in unicode prompts."""
        monkeypatch.setattr(
            'cookiecutter.prompt.read_user_variable',
            lambda _var, default, _prompts, _prefix: default,
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

    def test_dont_prompt_for_private_context_var(self, monkeypatch) -> None:
        """Verify `read_user_variable` not called for private context variables."""
        monkeypatch.setattr(
            'cookiecutter.prompt.read_user_variable',
            lambda _var, _default: pytest.fail(
                'Should not try to read a response for private context var'
            ),
        )
        context = {'cookiecutter': {'_copy_without_render': ['*.html']}}
        cookiecutter_dict = prompt.prompt_for_config(context)
        assert cookiecutter_dict == {'_copy_without_render': ['*.html']}

    def test_should_render_private_variables_with_two_underscores(self) -> None:
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
                    ('rendered_foo', '{{ cookiecutter.foo|lower }}'),
                    ('rendered_bar', 123),
                    ('_hidden_foo', '{{ cookiecutter.foo|lower }}'),
                    ('_hidden_bar', 123),
                    ('__rendered_hidden_foo', '{{ cookiecutter.foo|lower }}'),
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
                ('_hidden_foo', '{{ cookiecutter.foo|lower }}'),
                ('_hidden_bar', 123),
                ('__rendered_hidden_foo', 'hello world'),
                ('__rendered_hidden_bar', '123'),
            ]
        )

    def test_should_not_render_private_variables(self) -> None:
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


DEFAULT_PREFIX = '  [dim][1/1][/] '


class TestReadUserChoice:
    """Class to unite choices prompt related tests."""

    def test_should_invoke_read_user_choice(self, mocker) -> None:
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
        read_user_choice.assert_called_once_with(
            'orientation', choices, {}, DEFAULT_PREFIX
        )
        assert cookiecutter_dict == {'orientation': 'all'}

    def test_should_invoke_read_user_variable(self, mocker) -> None:
        """Verify correct function called for string input variables."""
        read_user_variable = mocker.patch('cookiecutter.prompt.read_user_variable')
        read_user_variable.return_value = 'Audrey Roy'

        prompt_choice = mocker.patch('cookiecutter.prompt.prompt_choice_for_config')

        read_user_choice = mocker.patch('cookiecutter.prompt.read_user_choice')

        context = {'cookiecutter': {'full_name': 'Your Name'}}

        cookiecutter_dict = prompt.prompt_for_config(context)

        assert not prompt_choice.called
        assert not read_user_choice.called
        read_user_variable.assert_called_once_with(
            'full_name', 'Your Name', {}, DEFAULT_PREFIX
        )
        assert cookiecutter_dict == {'full_name': 'Audrey Roy'}

    def test_should_render_choices(self, mocker) -> None:
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

        read_user_variable.assert_called_once_with(
            'project_name', 'A New Project', {}, '  [dim][1/2][/] '
        )
        read_user_choice.assert_called_once_with(
            'pkg_name', rendered_choices, {}, '  [dim][2/2][/] '
        )
        assert cookiecutter_dict == expected


class TestPromptChoiceForConfig:
    """Class to unite choices prompt related tests with config test."""

    @pytest.fixture
    def choices(self):
        """Fixture. Just populate choices variable."""
        return ['landscape', 'portrait', 'all']

    @pytest.fixture
    def context(self, choices):
        """Fixture. Just populate context variable."""
        return {'cookiecutter': {'orientation': choices}}

    def test_should_return_first_option_if_no_input(
        self, mocker, choices, context
    ) -> None:
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

    def test_should_read_user_choice(self, mocker, choices, context) -> None:
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
        read_user_choice.assert_called_once_with('orientation', choices, None, '')
        assert expected_choice == actual_choice


class TestReadUserYesNo:
    """Class to unite boolean prompt related tests."""

    @pytest.mark.parametrize(
        'run_as_docker',
        (
            True,
            False,
        ),
    )
    def test_should_invoke_read_user_yes_no(self, mocker, run_as_docker) -> None:
        """Verify correct function called for boolean variables."""
        read_user_yes_no = mocker.patch('cookiecutter.prompt.read_user_yes_no')
        read_user_yes_no.return_value = run_as_docker

        read_user_variable = mocker.patch('cookiecutter.prompt.read_user_variable')

        context = {'cookiecutter': {'run_as_docker': run_as_docker}}

        cookiecutter_dict = prompt.prompt_for_config(context)

        assert not read_user_variable.called
        read_user_yes_no.assert_called_once_with(
            'run_as_docker', run_as_docker, {}, DEFAULT_PREFIX
        )
        assert cookiecutter_dict == {'run_as_docker': run_as_docker}

    def test_boolean_parameter_no_input(self) -> None:
        """Verify boolean parameter sent to prompt for config with no input."""
        context = {
            'cookiecutter': {
                'run_as_docker': True,
            }
        }
        cookiecutter_dict = prompt.prompt_for_config(context, no_input=True)
        assert cookiecutter_dict == context['cookiecutter']


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
def test_undefined_variable(context) -> None:
    """Verify `prompt.prompt_for_config` raises correct error."""
    with pytest.raises(exceptions.UndefinedVariableInTemplate) as err:
        prompt.prompt_for_config(context, no_input=True)

    error = err.value
    assert error.message == "Unable to render variable 'foo'"
    assert error.context == context


@pytest.mark.parametrize(
    "template_dir,expected",
    [
        ["fake-nested-templates", "fake-project"],
        ["fake-nested-templates-old-style", "fake-package"],
    ],
)
def test_cookiecutter_nested_templates(template_dir: str, expected: Path | str) -> None:
    """Test nested_templates generation."""
    from cookiecutter import prompt

    main_dir = (Path("tests") / template_dir).resolve()
    cookiecuter_context = json.loads((main_dir / "cookiecutter.json").read_text())
    context = {"cookiecutter": cookiecuter_context}
    output_dir = prompt.choose_nested_template(context, main_dir, no_input=True)
    expected = (Path(main_dir) / expected).resolve()
    assert output_dir == f"{expected}"


@pytest.mark.skipif(sys.platform.startswith('win'), reason="Linux / macos test")
@pytest.mark.parametrize(
    "path",
    [
        "",
        "/tmp",
        "/foo",
    ],
)
def test_cookiecutter_nested_templates_invalid_paths(path: str) -> None:
    """Test nested_templates generation."""
    from cookiecutter import prompt

    main_dir = (Path("tests") / "fake-nested-templates").resolve()
    cookiecuter_context = json.loads((main_dir / "cookiecutter.json").read_text())
    cookiecuter_context["templates"]["fake-project"]["path"] = path
    context = {"cookiecutter": cookiecuter_context}
    with pytest.raises(ValueError) as exc:
        prompt.choose_nested_template(context, main_dir, no_input=True)
    assert "Illegal template path" in str(exc)


@pytest.mark.skipif(not sys.platform.startswith('win'), reason="Win only test")
@pytest.mark.parametrize(
    "path",
    [
        "",
        "C:/tmp",
        "D:/tmp",
    ],
)
def test_cookiecutter_nested_templates_invalid_win_paths(path: str) -> None:
    """Test nested_templates generation."""
    from cookiecutter import prompt

    main_dir = (Path("tests") / "fake-nested-templates").resolve()
    cookiecuter_context = json.loads((main_dir / "cookiecutter.json").read_text())
    cookiecuter_context["templates"]["fake-project"]["path"] = path
    context = {"cookiecutter": cookiecuter_context}
    with pytest.raises(ValueError) as exc:
        prompt.choose_nested_template(context, main_dir, no_input=True)
    assert "Illegal template path" in str(exc)


def test_prompt_should_ask_and_rm_repo_dir(mocker, tmp_path) -> None:
    """In `prompt_and_delete()`, if the user agrees to delete/reclone the \
    repo, the repo should be deleted."""
    mock_read_user = mocker.patch(
        'cookiecutter.prompt.read_user_yes_no', return_value=True
    )
    repo_dir = Path(tmp_path, 'repo')
    repo_dir.mkdir()

    deleted = prompt.prompt_and_delete(str(repo_dir))

    assert mock_read_user.called
    assert not repo_dir.exists()
    assert deleted


def test_prompt_should_ask_and_exit_on_user_no_answer(mocker, tmp_path) -> None:
    """In `prompt_and_delete()`, if the user decline to delete/reclone the \
    repo, cookiecutter should exit."""
    mock_read_user = mocker.patch(
        'cookiecutter.prompt.read_user_yes_no',
        return_value=False,
    )
    mock_sys_exit = mocker.patch('sys.exit', return_value=True)
    repo_dir = Path(tmp_path, 'repo')
    repo_dir.mkdir()

    deleted = prompt.prompt_and_delete(str(repo_dir))

    assert mock_read_user.called
    assert repo_dir.exists()
    assert not deleted
    assert mock_sys_exit.called


def test_prompt_should_ask_and_rm_repo_file(mocker, tmp_path) -> None:
    """In `prompt_and_delete()`, if the user agrees to delete/reclone a \
    repo file, the repo should be deleted."""
    mock_read_user = mocker.patch(
        'cookiecutter.prompt.read_user_yes_no', return_value=True, autospec=True
    )

    repo_file = tmp_path.joinpath('repo.zip')
    repo_file.write_text('this is zipfile content')

    deleted = prompt.prompt_and_delete(str(repo_file))

    assert mock_read_user.called
    assert not repo_file.exists()
    assert deleted


def test_prompt_should_ask_and_keep_repo_on_no_reuse(mocker, tmp_path) -> None:
    """In `prompt_and_delete()`, if the user wants to keep their old \
    cloned template repo, it should not be deleted."""
    mock_read_user = mocker.patch(
        'cookiecutter.prompt.read_user_yes_no', return_value=False, autospec=True
    )
    repo_dir = Path(tmp_path, 'repo')
    repo_dir.mkdir()

    with pytest.raises(SystemExit):
        prompt.prompt_and_delete(str(repo_dir))

    assert mock_read_user.called
    assert repo_dir.exists()


def test_prompt_should_ask_and_keep_repo_on_reuse(mocker, tmp_path) -> None:
    """In `prompt_and_delete()`, if the user wants to keep their old \
    cloned template repo, it should not be deleted."""

    def answer(question, _default):
        return 'okay to delete' not in question

    mock_read_user = mocker.patch(
        'cookiecutter.prompt.read_user_yes_no', side_effect=answer, autospec=True
    )
    repo_dir = Path(tmp_path, 'repo')
    repo_dir.mkdir()

    deleted = prompt.prompt_and_delete(str(repo_dir))

    assert mock_read_user.called
    assert repo_dir.exists()
    assert not deleted


def test_prompt_should_not_ask_if_no_input_and_rm_repo_dir(mocker, tmp_path) -> None:
    """Prompt should not ask if no input and rm dir.

    In `prompt_and_delete()`, if `no_input` is True, the call to
    `prompt.read_user_yes_no()` should be suppressed.
    """
    mock_read_user = mocker.patch(
        'cookiecutter.prompt.read_user_yes_no', return_value=True, autospec=True
    )
    repo_dir = Path(tmp_path, 'repo')
    repo_dir.mkdir()

    deleted = prompt.prompt_and_delete(str(repo_dir), no_input=True)

    assert not mock_read_user.called
    assert not repo_dir.exists()
    assert deleted


def test_prompt_should_not_ask_if_no_input_and_rm_repo_file(mocker, tmp_path) -> None:
    """Prompt should not ask if no input and rm file.

    In `prompt_and_delete()`, if `no_input` is True, the call to
    `prompt.read_user_yes_no()` should be suppressed.
    """
    mock_read_user = mocker.patch(
        'cookiecutter.prompt.read_user_yes_no', return_value=True, autospec=True
    )

    repo_file = tmp_path.joinpath('repo.zip')
    repo_file.write_text('this is zipfile content')

    deleted = prompt.prompt_and_delete(str(repo_file), no_input=True)

    assert not mock_read_user.called
    assert not repo_file.exists()
    assert deleted
