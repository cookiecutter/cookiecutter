# -*- coding: utf-8 -*-

"""
conftest.

--------
"""

import pytest


@pytest.fixture
def context():
    """Fixture to return a valid context as known from a cookiecutter.json."""
    return {
        u"cookiecutter": {
            u"email": u"raphael@hackebrot.de",
            u"full_name": u"Raphael Pierzina",
            u"github_username": u"hackebrot",
            u"version": u"0.1.0",
        }
    }


@pytest.fixture
def replay_test_dir():
    """Fixture to test directory."""
    return "tests/test-replay/"


@pytest.fixture
def mock_user_config(mocker):
    """Fixture to mock user config."""
    return mocker.patch("cookiecutter.main.get_user_config")
