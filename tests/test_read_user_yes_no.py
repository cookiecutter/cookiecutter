"""test_read_user_yes_no."""

import pytest
from rich.prompt import InvalidResponse

from cookiecutter.prompt import YesNoPrompt, read_user_yes_no

QUESTION = 'Is it okay to delete and re-clone it?'
DEFAULT = 'y'


def test_click_invocation(mocker) -> None:
    """Test click function called correctly by cookiecutter.

    Test for boolean type invocation.
    """
    prompt = mocker.patch('cookiecutter.prompt.YesNoPrompt.ask')
    prompt.return_value = DEFAULT

    assert read_user_yes_no(QUESTION, DEFAULT) == DEFAULT

    prompt.assert_called_once_with(QUESTION, default=DEFAULT)


def test_yesno_prompt_process_response() -> None:
    """Test `YesNoPrompt` process_response to convert str to bool."""
    ynp = YesNoPrompt()
    with pytest.raises(InvalidResponse):
        ynp.process_response('wrong')
    assert ynp.process_response('t') is True
    assert ynp.process_response('f') is False
