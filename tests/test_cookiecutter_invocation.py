# -*- coding: utf-8 -*-

"""
test_cookiecutter_invocation
----------------------------

Tests to make sure that cookiecutter can be called from the cli without
using the entry point set up for the package.
"""

import os
import pytest
import subprocess
import sys

from cookiecutter import utils


def test_should_raise_error_without_template_arg(capfd):
    with pytest.raises(subprocess.CalledProcessError):
        subprocess.check_call(['python', '-m', 'cookiecutter.cli'])

    _, err = capfd.readouterr()
    exp_message = 'Error: Missing argument "template".'
    assert exp_message in err


@pytest.fixture
def project_dir(request):
    """Remove the rendered project directory created by the test."""
    rendered_dir = 'fake-project-templated'

    def remove_generated_project():
        if os.path.isdir(rendered_dir):
            utils.rmtree(rendered_dir)
    request.addfinalizer(remove_generated_project)

    return rendered_dir


@pytest.mark.usefixtures('clean_system')
def test_should_invoke_main(monkeypatch, project_dir):
    monkeypatch.setenv('PYTHONPATH', '.')

    subprocess.check_call([
        sys.executable,
        '-m',
        'cookiecutter.cli',
        'tests/fake-repo-tmpl',
        '--no-input'
    ])

    assert os.path.isdir(project_dir)
