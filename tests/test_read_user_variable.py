"""test_read_user_variable."""
import click

from cookiecutter.prompt import read_user_variable

VARIABLE = 'project_name'
DEFAULT = 'Kivy Project'


def test_click_invocation(mocker):
    """Test click function called correctly by cookiecutter.

    Test for string type invocation.
    """
    prompt = mocker.patch('click.prompt')
    prompt.return_value = DEFAULT

    assert read_user_variable(VARIABLE, DEFAULT) == DEFAULT

    click.prompt.assert_called_once_with(VARIABLE, default=DEFAULT)
