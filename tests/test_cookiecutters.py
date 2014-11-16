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
        if os.path.isdir('cookiecutter-pypackage'):
            utils.rmtree('cookiecutter-pypackage')
        if os.path.isdir('cookiecutter-jquery'):
            utils.rmtree('cookiecutter-jquery')
        if os.path.isdir('boilerplate'):
            utils.rmtree('boilerplate')
    request.addfinalizer(fin_remove_additional_dirs)


def bake_data():
    pypackage_data = (
        'git clone https://github.com/audreyr/cookiecutter-pypackage.git',
        'cookiecutter --no-input cookiecutter-pypackage/',
        'cookiecutter-pypackage',
        'boilerplate/README.rst'
    )

    jquery_data = (
        'git clone https://github.com/audreyr/cookiecutter-jquery.git',
        'cookiecutter --no-input cookiecutter-jquery/',
        'cookiecutter-jquery',
        'boilerplate/README.md'
    )

    yield pypackage_data
    yield jquery_data


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
