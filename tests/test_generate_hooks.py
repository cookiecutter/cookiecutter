#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_generate_hooks
-------------------

Tests formerly known from a unittest residing in test_generate.py named
TestHooks.test_ignore_hooks_dirs
"""

from __future__ import unicode_literals
import os
import pytest

from cookiecutter import generate
from cookiecutter import utils


@pytest.fixture(scope='function')
def remove_additional_folders(request):
    """
    Remove some special folders which are created by the tests.
    """
    def fin_remove_additional_folders():
        if os.path.exists('tests/test-pyhooks/inputpyhooks'):
            utils.rmtree('tests/test-pyhooks/inputpyhooks')
        if os.path.exists('inputpyhooks'):
            utils.rmtree('inputpyhooks')
        if os.path.exists('tests/test-shellhooks'):
            utils.rmtree('tests/test-shellhooks')
    request.addfinalizer(fin_remove_additional_folders)


@pytest.mark.usefixtures('clean_system', 'remove_additional_folders')
def test_ignore_hooks_dirs():
    generate.generate_files(
        context={
            'cookiecutter': {'pyhooks': 'pyhooks'}
        },
        repo_dir='tests/test-pyhooks/',
        output_dir='tests/test-pyhooks/'
    )
    assert not os.path.exists('tests/test-pyhooks/inputpyhooks/hooks')
