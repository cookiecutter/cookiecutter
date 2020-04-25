# -*- coding: utf-8 -*-

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


def test_should_raise_error_without_template_arg(monkeypatch, capfd):
    """Verify expected error in command line on invocation without arguments."""
    monkeypatch.setenv('PYTHONPATH', '.')

    with pytest.raises(subprocess.CalledProcessError):
        subprocess.check_call([sys.executable, '-m', 'cookiecutter.cli'])

    _, err = capfd.readouterr()
    exp_message = "Error: Missing argument"
    assert exp_message in err and "TEMPLATE" in err


@pytest.mark.usefixtures('clean_system')
def test_should_invoke_main(monkeypatch, project_dir):
    """Should create a project and exit with 0 code on cli invocation."""
    monkeypatch.setenv('PYTHONPATH', '.')

    exit_code = subprocess.check_call(
        [sys.executable, '-m', 'cookiecutter.cli', 'tests/fake-repo-tmpl', '--no-input']
    )
    assert exit_code == 0
    assert os.path.isdir(project_dir)
