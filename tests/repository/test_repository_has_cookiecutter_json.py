# -*- coding: utf-8 -*-

"""Tests around validation if a given repository contains a (valid) config."""

import pytest

from cookiecutter.repository import repository_has_cookiecutter_json


def test_valid_repository():
    assert repository_has_cookiecutter_json('tests/fake-repo')


@pytest.fixture(params=[
    'tests/fake-repo-bad',
    'tests/unknown-repo',
])
def invalid_repository(request):
    return request.param


def test_invalid_repository(invalid_repository):
    assert not repository_has_cookiecutter_json(invalid_repository)
