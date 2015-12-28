#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_cookiecutter_repo_arg
--------------------------

Tests formerly known from a unittest residing in test_main.py named
TestCookiecutterRepoArg.test_cookiecutter_git
TestCookiecutterRepoArg.test_cookiecutter_mercurial
"""

from __future__ import unicode_literals
import os


from tests.skipif_markers import skipif_no_network, skipif_no_hg


@skipif_no_network
def test_cookiecutter_git():
    from cookiecutter import main
    main.cookiecutter(
        'https://github.com/audreyr/cookiecutter-pypackage.git',
        no_input=True
    )
    clone_dir = os.path.join(
        os.path.expanduser('~/.cookiecutters'),
        'cookiecutter-pypackage'
    )
    assert os.path.exists(clone_dir)
    assert os.path.isdir('python_boilerplate')
    assert os.path.isfile('python_boilerplate/README.rst')
    assert os.path.exists('python_boilerplate/setup.py')


@skipif_no_hg
@skipif_no_network
def test_cookiecutter_mercurial(monkeypatch):
    from cookiecutter import main
    monkeypatch.setattr(
        'cookiecutter.prompt.read_user_variable',
        lambda var, default: default
    )

    main.cookiecutter('https://bitbucket.org/pokoli/cookiecutter-trytonmodule')
    clone_dir = os.path.join(
        os.path.expanduser('~/.cookiecutters'),
        'cookiecutter-trytonmodule'
    )
    assert os.path.exists(clone_dir)
    assert os.path.isdir('module_name')
    assert os.path.isfile('module_name/README')
    assert os.path.exists('module_name/setup.py')
