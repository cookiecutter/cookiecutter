#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_vcs
------------

Tests for `cookiecutter.vcs` module.
"""

import locale
import os
import pytest
import subprocess

from cookiecutter import exceptions, utils, vcs
from tests.skipif_markers import skipif_no_network

ENCODING = locale.getdefaultlocale()[1]


@skipif_no_network
def test_git_clone():
    repo_dir = vcs.clone(
        'https://github.com/audreyr/cookiecutter-pypackage.git'
    )

    assert repo_dir == 'cookiecutter-pypackage'
    assert os.path.isfile('cookiecutter-pypackage/README.rst')

    if os.path.isdir('cookiecutter-pypackage'):
        utils.rmtree('cookiecutter-pypackage')


@skipif_no_network
def test_git_clone_with_trailing_slash():
    repo_dir = vcs.clone(
        'https://github.com/audreyr/cookiecutter-pypackage/'
    )

    assert repo_dir == 'cookiecutter-pypackage'
    assert os.path.isfile('cookiecutter-pypackage/README.rst')

    if os.path.isdir('cookiecutter-pypackage'):
        utils.rmtree('cookiecutter-pypackage')


@skipif_no_network
def test_git_clone_checkout():
    repo_dir = vcs.clone(
        'https://github.com/audreyr/cookiecutter-pypackage.git',
        'console-script'
    )
    git_dir = 'cookiecutter-pypackage'
    assert repo_dir == git_dir
    assert os.path.isfile(os.path.join('cookiecutter-pypackage', 'README.rst'))

    proc = subprocess.Popen(
        ['git', 'symbolic-ref', 'HEAD'],
        cwd=git_dir,
        stdout=subprocess.PIPE
    )
    symbolic_ref = proc.communicate()[0]
    branch = symbolic_ref.decode(ENCODING).strip().split('/')[-1]
    assert 'console-script' == branch

    if os.path.isdir(git_dir):
        utils.rmtree(git_dir)


@skipif_no_network
def test_git_clone_custom_dir():
    os.makedirs('tests/custom_dir1/custom_dir2/')
    repo_dir = vcs.clone(
        repo_url='https://github.com/audreyr/cookiecutter-pypackage.git',
        checkout=None,
        clone_to_dir='tests/custom_dir1/custom_dir2/'
    )
    with utils.work_in('tests/custom_dir1/custom_dir2/'):
        test_dir = 'tests/custom_dir1/custom_dir2/cookiecutter-pypackage'
        assert repo_dir == test_dir.replace('/', os.sep)
        assert os.path.isfile('cookiecutter-pypackage/README.rst')
        if os.path.isdir('cookiecutter-pypackage'):
            utils.rmtree('cookiecutter-pypackage')
    if os.path.isdir('tests/custom_dir1'):
        utils.rmtree('tests/custom_dir1')


@skipif_no_network
def test_hg_clone():
    repo_dir = vcs.clone(
        'https://bitbucket.org/pokoli/cookiecutter-trytonmodule'
    )
    assert repo_dir == 'cookiecutter-trytonmodule'
    assert os.path.isfile('cookiecutter-trytonmodule/README.rst')
    if os.path.isdir('cookiecutter-trytonmodule'):
        utils.rmtree('cookiecutter-trytonmodule')


@skipif_no_network
def test_vcs_not_installed(monkeypatch):
    monkeypatch.setattr(
        'cookiecutter.vcs.identify_repo',
        lambda x: (u'stringthatisntashellcommand', u'anotherstring'),
    )
    with pytest.raises(exceptions.VCSNotInstalled):
        vcs.clone('http://norepotypespecified.com')


@pytest.mark.parametrize('repo_url, exp_repo_type, exp_repo_url', [
    (
        "git+https://github.com/pytest-dev/cookiecutter-pytest-plugin.git",
        "git",
        "https://github.com/pytest-dev/cookiecutter-pytest-plugin.git"
    ), (
        "hg+https://bitbucket.org/foo/bar.hg",
        "hg",
        "https://bitbucket.org/foo/bar.hg"
    ), (
        "https://github.com/pytest-dev/cookiecutter-pytest-plugin.git",
        "git",
        "https://github.com/pytest-dev/cookiecutter-pytest-plugin.git"
    ), (
        "https://bitbucket.org/foo/bar.hg",
        "hg",
        "https://bitbucket.org/foo/bar.hg"
    )
])
def test_identify_known_repo(repo_url, exp_repo_type, exp_repo_url):
    assert vcs.identify_repo(repo_url) == (exp_repo_type, exp_repo_url)


@pytest.fixture(params=[
    "foo+git",  # uses explicit identifier with 'git' in the wrong place
    "foo+hg",  # uses explicit identifier with 'hg' in the wrong place
    "foo+bar",  # uses explicit identifier with neither 'git' nor 'hg'
    "foobar"  # no identifier but neither 'git' nor 'bitbucket' in url
])
def unknown_repo_type_url(request):
    return request.param


def test_identify_raise_on_unknown_repo(unknown_repo_type_url):
    with pytest.raises(exceptions.UnknownRepoType):
        vcs.identify_repo(unknown_repo_type_url)


def test_prompt_should_ask_and_rm_repo_dir(mocker, tmpdir):
    mock_read_user = mocker.patch(
        'cookiecutter.vcs.read_user_yes_no',
        return_value=True,
        autospec=True
    )
    repo_dir = tmpdir.mkdir('repo')

    vcs.prompt_and_delete_repo(str(repo_dir))

    assert mock_read_user.called
    assert not repo_dir.exists()


def test_prompt_should_ask_and_keep_repo_dir(mocker, tmpdir):
    mock_read_user = mocker.patch(
        'cookiecutter.vcs.read_user_yes_no',
        return_value=False,
        autospec=True
    )
    repo_dir = tmpdir.mkdir('repo')

    with pytest.raises(SystemExit):
        vcs.prompt_and_delete_repo(str(repo_dir))

    assert mock_read_user.called
    assert repo_dir.exists()


def test_prompt_should_not_ask_if_no_input_and_rm_repo_dir(mocker, tmpdir):
    mock_read_user = mocker.patch(
        'cookiecutter.vcs.read_user_yes_no',
        return_value=True,
        autospec=True
    )
    repo_dir = tmpdir.mkdir('repo')

    vcs.prompt_and_delete_repo(str(repo_dir), no_input=True)

    assert not mock_read_user.called
    assert not repo_dir.exists()


@pytest.fixture
def clone_dir(tmpdir):
    return str(tmpdir.mkdir('clone_dir'))


def test_clone_should_raise_if_vcs_not_installed(mocker, clone_dir):
    mocker.patch(
        'cookiecutter.vcs.which',
        autospec=True,
        return_value=''
    )

    repo_url = 'https://github.com/pytest-dev/cookiecutter-pytest-plugin.git'

    with pytest.raises(exceptions.VCSNotInstalled):
        vcs.clone(repo_url, clone_to_dir=clone_dir)
