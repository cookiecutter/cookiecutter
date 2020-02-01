# -*- coding: utf-8 -*-

"""Tests around detection whether cookiecutter templates are cached locally."""

import io
import os

import pytest

from cookiecutter import repository


@pytest.fixture
def template():
    return 'cookiecutter-pytest-plugin'


@pytest.fixture
def cloned_cookiecutter_path(user_config_data, template):
    cookiecutters_dir = user_config_data['cookiecutters_dir']

    cloned_template_path = os.path.join(cookiecutters_dir, template)
    os.mkdir(cloned_template_path)

    io.open(os.path.join(cloned_template_path, 'cookiecutter.json'), 'w')

    return cloned_template_path


def test_should_find_existing_cookiecutter(
        template, user_config_data, cloned_cookiecutter_path):
    project_dir, cleanup = repository.determine_repo_dir(
        template,
        abbreviations={},
        clone_to_dir=user_config_data['cookiecutters_dir'],
        checkout=None,
        no_input=True,
    )

    assert cloned_cookiecutter_path == project_dir
    assert not cleanup
