# -*- coding: utf-8 -*-
from cookiecutter.repository import valid_repository

import pytest


def test_valid_repository():
    assert valid_repository('tests/fake-repo')


@pytest.fixture(params=[
    'tests/fake-repo-bad',
    'tests/unknown-repo',
])
def invalid_repository(request):
    return request.param


def test_invalid_repository(invalid_repository):
    assert not valid_repository(invalid_repository)
