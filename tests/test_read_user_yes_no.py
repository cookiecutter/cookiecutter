"""test_read_user_yes_no."""
from cookiecutter.prompt import read_user_yes_no

QUESTION = 'Is it okay to delete and re-clone it?'
DEFAULT = 'y'


def test_click_invocation(mocker):
    """Test click function called correctly by cookiecutter.

    Test for boolean type invocation.
    """
    prompt = mocker.patch('rich.prompt.Confirm.ask')
    prompt.return_value = DEFAULT

    assert read_user_yes_no(QUESTION, DEFAULT) == DEFAULT

    prompt.assert_called_once_with(QUESTION, default=DEFAULT)
