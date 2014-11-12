#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_generate_context
---------------------

Tests formerly known from a unittest residing in test_generate.py named
TestGenerateContext.test_generate_context
"""

from __future__ import unicode_literals
import pytest

from cookiecutter import generate


@pytest.mark.usefixtures("clean_system")
def test_generate_context():
    context = generate.generate_context(
        context_file='tests/test-generate-context/test.json'
    )
    assert context == {"test": {"1": 2, "some_key": "some_val"}}
