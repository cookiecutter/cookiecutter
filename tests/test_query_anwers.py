#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_query_anwers
-----------------

Tests formerly known from a unittest residing in test_prompt.py named
TestQueryAnswers.test_query_y
"""

import pytest

from cookiecutter import prompt


def test_query_y(monkeypatch):
    monkeypatch.setattr(
        'cookiecutter.prompt.read_response',
        lambda x=u'': u'y'
    )
    answer = prompt.query_yes_no("Blah?")
    assert answer
