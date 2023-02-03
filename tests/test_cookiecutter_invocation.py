"""
test_cookiecutter_invocation.

Tests to make sure that cookiecutter can be called from the cli without
using the entry point set up for the package.
"""

import os
import subprocess
import sys

import pytest

from cookiecutter import utils


@pytest.fixture
def project_dir():
    """Return test project folder name and remove it after the test."""
    yield 'fake-project-templated'

    if os.path.isdir('fake-project-templated'):
        utils.rmtree('fake-project-templated')


@pytest.mark.usefixtures('clean_system')
def test_should_invoke_main(monkeypatch, project_dir):
    """Should create a project and exit with 0 code on cli invocation."""
    monkeypatch.setenv('PYTHONPATH', '.')

    exit_code = subprocess.check_call(
        [sys.executable, '-m', 'cookiecutter.cli', 'tests/fake-repo-tmpl', '--no-input']
    )
    assert exit_code == 0
    assert os.path.isdir(project_dir)
