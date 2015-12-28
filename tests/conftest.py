#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
conftest
--------

Contains pytest fixtures which are globally available throughout the suite.
"""
import functools
import os

import pytest
from imp import reload

from tests.utils import dir_tests



@pytest.fixture(scope='function', autouse=True)
def test_setup(tmpdir, monkeypatch):
    home = tmpdir.mkdir('home')
    monkeypatch.setenv('HOME', home)




@pytest.fixture(scope='function', autouse=True)
def change_directory(request, tmpdir):
    os.chdir(str(tmpdir))

    cleanup = functools.partial(os.chdir, dir_tests('..'))
    request.addfinalizer(cleanup)