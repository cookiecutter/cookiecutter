# -*- coding: utf-8 -*-

"""
test_cookiecutter_invocation
----------------------------

Tests to make sure that cookiecutter can be called from the cli without
using the entry point set up for the package.
"""

import pytest
import subprocess


def test_should_raise_error_without_template_arg(capfd):
    with pytest.raises(subprocess.CalledProcessError):
        subprocess.check_call(['python', '-m', 'cookiecutter.cli'])

    _, err = capfd.readouterr()
    exp_message = 'Error: Missing argument "template".'
    assert exp_message in err
