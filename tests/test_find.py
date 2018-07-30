# -*- coding: utf-8 -*-

"""
test_find
---------

Tests for `cookiecutter.find` module.
"""

import os
import pytest

from cookiecutter import find, environment


@pytest.fixture(params=['fake-repo-pre', 'fake-repo-pre2'])
def repo_dir(request):
    return os.path.join('tests', request.param)


def test_find_template(repo_dir):
    env = environment.StrictEnvironment()
    template = find.find_template(repo_dir=repo_dir, env=env)

    test_dir = os.path.join(repo_dir, '{{cookiecutter.repo_name}}')
    assert template == test_dir
