#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
conftest
--------

Contains pytest fixtures which are globally available throughout the suite.
"""

import os
import pytest


@pytest.fixture(scope='function', autouse=True)
def test_setup(tmpdir, monkeypatch):
    home = tmpdir.mkdir('home')
    monkeypatch.setenv('HOME', home)


@pytest.fixture(scope='function', autouse=True)
def change_directory(tmpdir):
    os.chdir(str(tmpdir))
