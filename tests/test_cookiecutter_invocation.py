"""
test_cookiecutter_invocation.

Tests to make sure that cookiecutter can be called from the cli without
using the entry point set up for the package.
"""

import subprocess
import sys
from pathlib import Path
from typing import Iterator

import pytest

from cookiecutter import utils


@pytest.fixture
def project_dir() -> Iterator[Path]:
    """Return test project folder name and remove it after the test."""
    project_dir = Path('fake-project-templated')
    yield project_dir

    if project_dir.is_dir():
        utils.rmtree(project_dir)


@pytest.mark.usefixtures('clean_system')
def test_should_invoke_main(monkeypatch, project_dir) -> None:
    """Should create a project and exit with 0 code on cli invocation."""
    monkeypatch.setenv('PYTHONPATH', '.')

    exit_code = subprocess.check_call(
        [
            sys.executable,
            '-m',
            'cookiecutter.cli',
            'tests/fake-repo-tmpl',
            '--no-input',
        ]
    )
    assert exit_code == 0
    assert project_dir.is_dir()
