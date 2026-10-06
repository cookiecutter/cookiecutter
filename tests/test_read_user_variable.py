"""test_read_user_variable."""

import pytest
from rich.text import Text

from cookiecutter.prompt import read_user_variable

VARIABLE = 'project_name'
DEFAULT = 'Kivy Project'


@pytest.fixture
def mock_prompt(mocker):
    """Return a mocked version of the 'Prompt.ask' function."""
    return mocker.patch('rich.prompt.Prompt.ask')


def test_click_invocation(mock_prompt) -> None:
    """Test click function called correctly by cookiecutter.

    Test for string type invocation.
    """
    mock_prompt.return_value = DEFAULT

    assert read_user_variable(VARIABLE, DEFAULT) == DEFAULT

    mock_prompt.assert_called_once_with(VARIABLE, default=DEFAULT)


def test_input_loop_with_null_default_value(mock_prompt) -> None:
    """Test `Prompt.ask` is run repeatedly until a valid answer is provided.

    Test for `default_value` parameter equal to None.
    """
    # Simulate user providing None input initially and then a valid input
    mock_prompt.side_effect = [None, DEFAULT]

    assert read_user_variable(VARIABLE, None) == DEFAULT
    assert mock_prompt.call_count == 2


def test_prompts_show_literal_square_brackets(mock_prompt) -> None:
    """``__prompts__`` text must show square brackets, not Rich markup.

    Regression for https://github.com/cookiecutter/cookiecutter/issues/1958.
    """
    mock_prompt.return_value = 'kept'
    prompts = {'entry': 'prefix [bracket content] suffix'}
    prefix = '  [dim][1/1][/] '

    assert read_user_variable('entry', None, prompts, prefix) == 'kept'

    visible = Text.from_markup(mock_prompt.call_args.args[0]).plain
    assert visible == '  [1/1] prefix [bracket content] suffix'
