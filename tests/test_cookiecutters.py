#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_cookiecutters
------------------

Tests formerly known from a unittest residing in test_examples.py named
TestPyPackage.test_cookiecutter_pypackage
TestJQuery.test_cookiecutter_jquery
"""

from __future__ import unicode_literals
import os
import sys
import subprocess
import pytest

from cookiecutter import utils
from tests.skipif_markers import skipif_travis, skipif_no_network


@pytest.fixture(scope='function')
def remove_additional_dirs(request):
    """
    Remove special directories which are creating during the tests.
    """
    def fin_remove_additional_dirs():
        for path in ('cookiecutter-pypackage', 'cookiecutter-jquery',
                     'python_boilerplate', 'boilerplate'):
            if os.path.isdir(path):
                utils.rmtree(path)
    request.addfinalizer(fin_remove_additional_dirs)


def bake_data():
    pypackage_data = (
        'git clone https://github.com/audreyr/cookiecutter-pypackage.git',
        '{0} -m cookiecutter.cli --no-input cookiecutter-pypackage/'.format(
            sys.executable),
        'cookiecutter-pypackage',
        'python_boilerplate/README.rst'
    )

    jquery_data = (
        'git clone https://github.com/audreyr/cookiecutter-jquery.git',
        '{0} -m cookiecutter.cli --no-input cookiecutter-jquery/'.format(
            sys.executable),
        'cookiecutter-jquery',
        'boilerplate/README.md'
    )

    yield pypackage_data

    # TODO: Remove xfail as soon as PR has been accepted
    # https://github.com/audreyr/cookiecutter-jquery/pull/2
    yield pytest.mark.xfail(jquery_data, reason='Undefined variable')


@skipif_travis
@skipif_no_network
@pytest.mark.usefixtures('clean_system', 'remove_additional_dirs')
@pytest.mark.parametrize('git_cmd, bake_cmd, out_dir, readme', bake_data())
def test_cookiecutters(git_cmd, bake_cmd, out_dir, readme):
    """
    Tests that the given cookiecutters work as expected.
    """

    proc = subprocess.Popen(git_cmd, stdin=subprocess.PIPE, shell=True)
    proc.wait()

    proc = subprocess.Popen(bake_cmd, stdin=subprocess.PIPE, shell=True)
    proc.wait()

    assert os.path.isdir(out_dir)
    assert os.path.isfile(readme)
