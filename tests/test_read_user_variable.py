"""test_read_user_variable."""

import pytest

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
