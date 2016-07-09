# -*- coding: utf-8 -*-
import os
import pytest

from cookiecutter import exceptions, vcs


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
