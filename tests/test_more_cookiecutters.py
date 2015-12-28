#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_more_cookiecutters
-----------------------

Test formerly known from a unittest residing in test_examples.py named
TestGitBranch.test_branch
TestExamplesRepoArg.test_cookiecutter_pypackage_git
"""

from __future__ import unicode_literals

import subprocess
import sys

import os

from tests.skipif_markers import skipif_travis, skipif_no_network


@skipif_travis
@skipif_no_network
def test_git_branch():
    pypackage_git = 'https://github.com/audreyr/cookiecutter-pypackage.git'
    proc = subprocess.Popen(
        '{0} -m cookiecutter.cli -c console-script {1}'.format(sys.executable,
                                                               pypackage_git),
        stdin=subprocess.PIPE,
        shell=True
    )

    # Just skip all the prompts
    proc.communicate(input=b'\n\n\n\n\n\n\n\n\n\n\n\n')

    assert os.path.isfile('boilerplate/README.rst')
    assert os.path.isfile('boilerplate/boilerplate/main.py')


@skipif_travis
@skipif_no_network
def test_cookiecutter_pypackage_git():
    proc = subprocess.Popen(
        '{0} -m cookiecutter.cli https://github.com/audreyr/'
        'cookiecutter-pypackage.git'.format(sys.executable),
        stdin=subprocess.PIPE,
        shell=True
    )

    # Just skip all the prompts
    proc.communicate(input=b'\n\n\n\n\n\n\n\n\n\n\n\n')

    assert os.path.isfile('python_boilerplate/README.rst')
