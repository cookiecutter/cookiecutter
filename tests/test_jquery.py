#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_jquery
-----------

Tests formerly known from a unittest residing in test_generate.py named
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
        if os.path.isdir('cookiecutter-jquery'):
            utils.rmtree('cookiecutter-jquery')
        if os.path.isdir('boilerplate'):
            utils.rmtree('boilerplate')
    request.addfinalizer(fin_remove_additional_dirs)


@skipif_travis
@skipif_no_network
@pytest.mark.usefixtures('clean_system', 'remove_additional_dirs')
def test_cookiecutter_jquery():
    """
    Tests that https://github.com/audreyr/cookiecutter-jquery.git works.
    """

    proc = subprocess.Popen(
        'git clone https://github.com/audreyr/cookiecutter-jquery.git',
        stdin=subprocess.PIPE,
        shell=True
    )
    proc.wait()

    proc = subprocess.Popen(
        'cookiecutter --no-input cookiecutter-jquery/',
        stdin=subprocess.PIPE,
        shell=True
    )
    proc.wait()

    assert os.path.isdir('cookiecutter-jquery')
    assert os.path.isfile('boilerplate/README.md')
