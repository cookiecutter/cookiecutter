#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_query_anwers
-----------------

Tests formerly known from a unittest residing in test_prompt.py named
TestQueryAnswers.test_query_y
TestQueryAnswers.test_query_ye
TestQueryAnswers.test_query_yes
"""

import pytest

from cookiecutter import prompt


@pytest.fixture(params=[u'y', u'ye', u'yes'])
def patch_read_response(request, monkeypatch):
    monkeypatch.setattr(
        'cookiecutter.prompt.read_response',
        lambda x=u'': request.param
    )


@pytest.mark.usefixtures('patch_read_response')
def test_query():
    assert prompt.query_yes_no("Blah?")
