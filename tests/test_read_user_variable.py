# -*- coding: utf-8 -*-

"""
test_read_user_variable
-----------------------
"""

from __future__ import unicode_literals

import click

from cookiecutter.prompt import read_user_variable

VARIABLE = 'project_name'
DEFAULT = 'Kivy Project'


def test_click_invocation(mocker):
    prompt = mocker.patch('click.prompt')
    prompt.return_value = DEFAULT

    assert read_user_variable(VARIABLE, DEFAULT) == DEFAULT

    click.prompt.assert_called_once_with(VARIABLE, default=DEFAULT)
