#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_vcs
------------

Tests for `cookiecutter.vcs` module.
"""

import os
import pytest

from cookiecutter import exceptions, vcs


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
    """In `prompt_and_delete_repo()`, if the user agrees to delete/reclone the
    repo, the repo should be deleted.
    """
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
    """In `prompt_and_delete_repo()`, if the user wants to keep their old
    cloned template repo, it should not be deleted.
    """
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
    """In `prompt_and_delete_repo()`, if `no_input` is True, the call to
    `vcs.read_user_yes_no()` should be suppressed.
    """
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
    """Simulates creation of a directory called `clone_dir` inside of `tmpdir`.
    Returns a str to said directory.
    """
    return str(tmpdir.mkdir('clone_dir'))


def test_clone_should_raise_if_vcs_not_installed(mocker, clone_dir):
    """In `clone()`, a `VCSNotInstalled` exception should be raised if no VCS
    is installed.
    """
    mocker.patch(
        'cookiecutter.vcs.is_vcs_installed',
        autospec=True,
        return_value=False
    )

    repo_url = 'https://github.com/pytest-dev/cookiecutter-pytest-plugin.git'

    with pytest.raises(exceptions.VCSNotInstalled):
        vcs.clone(repo_url, clone_to_dir=clone_dir)


@pytest.mark.parametrize('which_return, result', [
    ('', False),
    (None, False),
    (False, False),
    ('/usr/local/bin/git', True),
])
def test_is_vcs_installed(mocker, which_return, result):
    mocker.patch(
        'cookiecutter.vcs.which',
        autospec=True,
        return_value=which_return
    )
    assert vcs.is_vcs_installed('git') == result


@pytest.mark.parametrize('repo_type, repo_url, repo_name', [
    ('git', 'https://github.com/hello/world.git', 'world'),
    ('hg', 'https://bitbucket.org/foo/bar', 'bar'),
])
def test_clone_should_invoke_git(
        mocker, clone_dir, repo_type, repo_url, repo_name):
    """When `clone()` is called with a git/hg repo, the corresponding VCS
    command should be run via `subprocess.check_call()`.

    This should take place:
    * In the correct dir
    * With the correct args.
    """
    mocker.patch(
        'cookiecutter.vcs.is_vcs_installed',
        autospec=True,
        return_value=True
    )

    mock_subprocess = mocker.patch(
        'cookiecutter.vcs.subprocess.check_call',
        autospec=True,
    )
    expected_repo_dir = os.path.normpath(os.path.join(clone_dir, repo_name))

    branch = 'foobar'

    repo_dir = vcs.clone(
        repo_url,
        checkout=branch,
        clone_to_dir=clone_dir,
        no_input=True
    )

    assert repo_dir == expected_repo_dir

    mock_subprocess.assert_any_call(
        [repo_type, 'clone', repo_url], cwd=clone_dir
    )
    mock_subprocess.assert_any_call(
        [repo_type, 'checkout', branch], cwd=expected_repo_dir
    )


def test_clone_should_abort_if_user_does_not_want_to_reclone(mocker, tmpdir):
    """In `clone()`, if user doesn't want to reclone, Cookiecutter should exit
    without cloning anything.
    """
    mocker.patch(
        'cookiecutter.vcs.is_vcs_installed',
        autospec=True,
        return_value=True
    )
    mocker.patch(
        'cookiecutter.vcs.prompt_and_delete_repo',
        side_effect=SystemExit,
        autospec=True
    )
    mock_subprocess = mocker.patch(
        'cookiecutter.vcs.subprocess.check_call',
        autospec=True,
    )

    clone_to_dir = tmpdir.mkdir('clone')

    # Create repo_dir to trigger prompt_and_delete_repo
    clone_to_dir.mkdir('cookiecutter-pytest-plugin')

    repo_url = 'https://github.com/pytest-dev/cookiecutter-pytest-plugin.git'

    with pytest.raises(SystemExit):
        vcs.clone(repo_url, clone_to_dir=str(clone_to_dir))
    assert not mock_subprocess.called


def test_clone_should_rstrip_trailing_slash_in_repo_url(mocker, clone_dir):
    """In `clone()`, repo URL's trailing slash should be stripped if one is
    present.
    """
    mocker.patch(
        'cookiecutter.vcs.is_vcs_installed',
        autospec=True,
        return_value=True
    )

    mock_subprocess = mocker.patch(
        'cookiecutter.vcs.subprocess.check_call',
        autospec=True,
    )

    vcs.clone(
        'https://github.com/foo/bar/',
        clone_to_dir=clone_dir,
        no_input=True
    )

    mock_subprocess.assert_called_once_with(
        ['git', 'clone', 'https://github.com/foo/bar'], cwd=clone_dir
    )
