#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pypackage
--------------

Tests formerly known from a unittest residing in test_generate.py named
TestPyPackage.test_cookiecutter_pypackage
"""

from __future__ import unicode_literals
import os
import subprocess
import pytest

from cookiecutter import utils


try:
    travis = os.environ[u'TRAVIS']
except KeyError:
    travis = False

try:
    no_network = os.environ[u'DISABLE_NETWORK_TESTS']
except KeyError:
    no_network = False


@pytest.fixture(scope='function')
def remove_additional_dirs(request):
    """
    Remove special directories which are creating during the tests.
    """
    def fin_remove_additional_dirs():
        if os.path.isdir('cookiecutter-pypackage'):
            utils.rmtree('cookiecutter-pypackage')
        if os.path.isdir('boilerplate'):
            utils.rmtree('boilerplate')
    request.addfinalizer(fin_remove_additional_dirs)


# For some reason pytest incorrectly uses the first reason text regardless of
# which condition matches. Using a unified message for now
# travis_reason = 'Works locally with tox but fails on Travis.'
# no_network_reason = 'Needs a network connection to GitHub.'
reason = 'Fails on Travis or else there is no network connection to GitHub'


@pytest.mark.skipif(travis, reason=reason)
@pytest.mark.skipif(no_network, reason=reason)
@pytest.mark.usefixtures('remove_additional_dirs')
def test_cookiecutter_pypackage():
    """
    Tests that https://github.com/audreyr/cookiecutter-pypackage.git works.
    """

    proc = subprocess.Popen(
        'git clone https://github.com/audreyr/cookiecutter-pypackage.git',
        stdin=subprocess.PIPE,
        shell=True
    )
    proc.wait()

    proc = subprocess.Popen(
        'cookiecutter --no-input cookiecutter-pypackage/',
        stdin=subprocess.PIPE,
        shell=True
    )
    proc.wait()

    assert os.path.isdir('cookiecutter-pypackage')
    assert os.path.isfile('boilerplate/README.rst')
