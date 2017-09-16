# -*- coding: utf-8 -*-
from cookiecutter.prompt import read_repo_password


def test_click_invocation(mocker):
    prompt = mocker.patch('click.prompt')
    prompt.return_value = 'sekrit'

    assert read_repo_password('Password') == 'sekrit'

    prompt.assert_called_once_with('Password', hide_input=True)
