# -*- coding: utf-8 -*-
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
