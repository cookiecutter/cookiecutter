#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_read_response
------------------
"""

from __future__ import unicode_literals

from cookiecutter.prompt import read_response

PROMPT = 'project_name (default is "Kivy Project")?'


def _monkey_prompt(prompt, **kwargs):
    expected_kwargs = {
        'default': '',
        'prompt_suffix': '',
        'show_default': False
    }
    assert prompt == PROMPT
    assert kwargs == expected_kwargs
    return 'Hello World'


def test_click_invocation(capsys, monkeypatch):
    monkeypatch.setattr('click.prompt', _monkey_prompt)
    assert read_response(PROMPT) == 'Hello World'
