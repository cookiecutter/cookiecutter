# -*- coding: utf-8 -*-
from cookiecutter.repository import repository_has_cookiecutter_json

import pytest


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
