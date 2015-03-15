#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_is_vcs_installed
---------------------
"""

from cookiecutter import vcs


def test_existing_repo_type():
    assert vcs.is_vcs_installed("git")


def test_non_existing_repo_type():
    assert not vcs.is_vcs_installed("stringthatisntashellcommand")
