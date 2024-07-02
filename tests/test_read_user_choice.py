"""Tests around prompting for and handling of choice variables."""

import pytest

from cookiecutter.prompt import read_user_choice

OPTIONS = ['hello', 'world', 'foo', 'bar']
OPTIONS_INDEX = ['1', '2', '3', '4']

EXPECTED_PROMPT = """Select varname
    [bold magenta]1[/] - [bold]hello[/]
    [bold magenta]2[/] - [bold]world[/]
    [bold magenta]3[/] - [bold]foo[/]
    [bold magenta]4[/] - [bold]bar[/]
    Choose from"""


@pytest.mark.parametrize('user_choice, expected_value', enumerate(OPTIONS, 1))
def test_click_invocation(mocker, user_choice, expected_value) -> None:
    """Test click function called correctly by cookiecutter.

    Test for choice type invocation.
    """
    prompt = mocker.patch('rich.prompt.Prompt.ask')
    prompt.return_value = f'{user_choice}'

    assert read_user_choice('varname', OPTIONS) == expected_value

    prompt.assert_called_once_with(EXPECTED_PROMPT, choices=OPTIONS_INDEX, default='1')


def test_raise_if_options_is_not_a_non_empty_list() -> None:
    """Test function called by cookiecutter raise expected errors.

    Test for choice type invocation.
    """
    with pytest.raises(ValueError):
        read_user_choice('foo', [])
