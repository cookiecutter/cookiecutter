"""Tests around cloning repositories and detection of errors at it."""
import os
import subprocess

import pytest
from pathlib import Path

from cookiecutter import exceptions, vcs


@pytest.fixture
def clone_dir(tmpdir):
    """Simulate creation of a directory called `clone_dir` inside of `tmpdir`. \
    Returns a str to said directory."""
    return str(tmpdir.mkdir('clone_dir'))


def test_clone_should_raise_if_vcs_not_installed(mocker, clone_dir):
    """In `clone()`, a `VCSNotInstalled` exception should be raised if no VCS \
    is installed."""
    mocker.patch('cookiecutter.vcs.is_vcs_installed', autospec=True, return_value=False)

    repo_url = 'https://github.com/pytest-dev/cookiecutter-pytest-plugin.git'

    with pytest.raises(exceptions.VCSNotInstalled):
        vcs.clone(repo_url, clone_to_dir=clone_dir)


def test_clone_should_rstrip_trailing_slash_in_repo_url(mocker, clone_dir):
    """In `clone()`, repo URL's trailing slash should be stripped if one is \
    present."""
    mocker.patch('cookiecutter.vcs.is_vcs_installed', autospec=True, return_value=True)

    mock_subprocess = mocker.patch(
        'cookiecutter.vcs.subprocess.check_output', autospec=True,
    )

    vcs.clone('https://github.com/foo/bar/', clone_to_dir=clone_dir, no_input=True)

    mock_subprocess.assert_called_once_with(
        ['git', 'clone', 'https://github.com/foo/bar'],
        cwd=clone_dir,
        stderr=subprocess.STDOUT,
    )


def test_clone_should_abort_if_user_does_not_want_to_reclone(mocker, tmpdir):
    """In `clone()`, if user doesn't want to reclone, Cookiecutter should exit \
    without cloning anything."""
    mocker.patch('cookiecutter.vcs.is_vcs_installed', autospec=True, return_value=True)
    mocker.patch(
        'cookiecutter.vcs.prompt_ok_to_delete', side_effect=SystemExit, autospec=True
    )
    mock_subprocess = mocker.patch(
        'cookiecutter.vcs.subprocess.check_output', autospec=True,
    )

    clone_to_dir = tmpdir.mkdir('clone')

    # Create repo_dir to trigger prompt_ok_to_delete
    clone_to_dir.mkdir('cookiecutter-pytest-plugin')

    repo_url = 'https://github.com/pytest-dev/cookiecutter-pytest-plugin.git'

    with pytest.raises(SystemExit):
        vcs.clone(repo_url, clone_to_dir=str(clone_to_dir))
    assert not mock_subprocess.called


@pytest.mark.parametrize(
    'repo_type, repo_url, repo_name',
    [
        ('git', 'https://github.com/hello/world.git', 'world'),
        ('hg', 'https://bitbucket.org/foo/bar', 'bar'),
        ('git', 'git@host:gitoliterepo', 'gitoliterepo'),
        ('git', 'git@gitlab.com:cookiecutter/cookiecutter.git', 'cookiecutter'),
        ('git', 'git@github.com:cookiecutter/cookiecutter.git', 'cookiecutter'),
    ],
)
def test_clone_should_invoke_vcs_command(
    mocker, clone_dir, repo_type, repo_url, repo_name
):
    """When `clone()` is called with a git/hg repo, the corresponding VCS \
    command should be run via `subprocess.check_output()`.

    This should take place:
    * In the correct dir
    * With the correct args.
    """
    mocker.patch('cookiecutter.vcs.is_vcs_installed', autospec=True, return_value=True)

    mock_subprocess = mocker.patch(
        'cookiecutter.vcs.subprocess.check_output', autospec=True,
    )
    expected_repo_dir = os.path.normpath(os.path.join(clone_dir, repo_name))

    branch = 'foobar'

    repo_dir = vcs.clone(
        repo_url, checkout=branch, clone_to_dir=clone_dir, no_input=True
    )

    assert repo_dir == expected_repo_dir

    mock_subprocess.assert_any_call(
        [repo_type, 'clone', repo_url], cwd=clone_dir, stderr=subprocess.STDOUT
    )
    mock_subprocess.assert_any_call(
        [repo_type, 'checkout', branch], cwd=expected_repo_dir, stderr=subprocess.STDOUT
    )


@pytest.mark.parametrize(
    'error_message',
    [
        (
            "fatal: repository 'https://github.com/hackebro/cookiedozer' not found"
        ).encode('utf-8'),
        'hg: abort: HTTP Error 404: Not Found'.encode('utf-8'),
    ],
)
def test_clone_handles_repo_typo(mocker, clone_dir, error_message):
    """In `clone()`, repository not found errors should raise an \
    appropriate exception."""
    # side_effect is set to an iterable here (and below),
    # because of a Python 3.4 unittest.mock regression
    # http://bugs.python.org/issue23661
    mocker.patch(
        'cookiecutter.vcs.subprocess.check_output',
        autospec=True,
        side_effect=[subprocess.CalledProcessError(-1, 'cmd', output=error_message)],
    )

    repository_url = 'https://github.com/hackebro/cookiedozer'
    with pytest.raises(exceptions.RepositoryNotFound) as err:
        vcs.clone(repository_url, clone_to_dir=clone_dir, no_input=True)

    assert str(err.value) == (
        'The repository {} could not be found, have you made a typo?'
    ).format(repository_url)


@pytest.mark.parametrize(
    'error_message',
    [
        (
            "error: pathspec 'unknown_branch' did not match any file(s) known to git"
        ).encode('utf-8'),
        "hg: abort: unknown revision 'unknown_branch'!".encode('utf-8'),
    ],
)
def test_clone_handles_branch_typo(mocker, clone_dir, error_message):
    """In `clone()`, branch not found errors should raise an \
    appropriate exception."""
    mocker.patch(
        'cookiecutter.vcs.subprocess.check_output',
        autospec=True,
        side_effect=[subprocess.CalledProcessError(-1, 'cmd', output=error_message)],
    )

    repository_url = 'https://github.com/pytest-dev/cookiecutter-pytest-plugin'
    with pytest.raises(exceptions.RepositoryCloneFailed) as err:
        vcs.clone(
            repository_url,
            clone_to_dir=clone_dir,
            checkout='unknown_branch',
            no_input=True,
        )

    assert str(err.value) == (
        'The unknown_branch branch of repository '
        '{} could not found, have you made a typo?'
    ).format(repository_url)


def test_clone_unknown_subprocess_error(mocker, clone_dir):
    """In `clone()`, unknown subprocess errors should be raised."""
    mocker.patch(
        'cookiecutter.vcs.subprocess.check_output',
        autospec=True,
        side_effect=[
            subprocess.CalledProcessError(
                -1, 'cmd', output='Something went wrong'.encode('utf-8')
            )
        ],
    )

    with pytest.raises(subprocess.CalledProcessError):
        vcs.clone(
            'https://github.com/pytest-dev/cookiecutter-pytest-plugin',
            clone_to_dir=clone_dir,
            no_input=True,
        )


@pytest.mark.skip(reason='Unable to properly set up mocks')
def test_not_ok_to_delete_not_ok_to_reuse_results_in_system_exit(mocker, clone_dir):
    """In `clone()`, if the user does not download new version,\
    and does not reuse old one, then sys.exit() must be called."""
    mock_ok_to_delete = mocker.patch(
        'cookiecutter.utils.prompt_ok_to_delete', return_value=False,
    )

    mock_ok_to_reuse = mocker.patch(
        'cookiecutter.utils.prompt_ok_to_reuse', return_value=False,
    )

    with pytest.raises(SystemExit):
        vcs.clone(
            'https://github.com/pytest-dev/cookiecutter-pytest-plugin',
            clone_to_dir=clone_dir,
            no_input=True,
        )
    assert mock_ok_to_delete.called_once
    assert mock_ok_to_reuse.called_once


@pytest.mark.skip(reason='Unable to properly set up mocks and reasonable assertions',)
def test_no_ok_to_delete_ok_to_reuse_asked(mocker, clone_dir):
    """In `clone()` normal reuse workflow."""
    mock_ok_to_delete = mocker.patch(
        'cookiecutter.utils.prompt_ok_to_delete', return_value=False,
    )

    mock_ok_to_reuse = mocker.patch(
        'cookiecutter.utils.prompt_ok_to_reuse', return_value=True,
    )

    vcs.clone(
        'https://github.com/pytest-dev/cookiecutter-pytest-plugin',
        clone_to_dir=clone_dir,
        no_input=True,
    )
    assert mock_ok_to_delete.called_once
    assert mock_ok_to_reuse.called_once


def test_backup_and_delete_repo(mocker, tmpdir):
    """Test that backup works correctly."""
    mock_move = mocker.patch('shutil.move', return_value=True)

    repo_dir = tmpdir.mkdir('repo')
    backup_dir = tmpdir.mkdir('backup')

    subdir = repo_dir.mkdir('subdir')
    inner_dir = subdir.mkdir('inner_dir')

    Path(repo_dir / 'cookiecutter.json').touch()
    Path(subdir / 'README.md').touch()
    Path(inner_dir / 'some_file.txt').touch()

    original_files = [
        x.relative_to(repo_dir)
        for x in sorted(Path(repo_dir).glob('**/*'))
        if x.is_file()
    ]

    vcs._backup_and_delete_repo(str(repo_dir), str(backup_dir))
    backed_up_files = [
        x.relative_to(backup_dir / 'repo')
        for x in sorted(Path(backup_dir).glob('**/*'))
        if x.is_file()
    ]
    assert mock_move.called_once
    assert original_files == backed_up_files
    assert not Path(repo_dir).exists()


def test_restore_old_repo_to_existing_directory(mocker, tmpdir):
    """Test that restore works correctly if repo directory exists."""
    mock_rmtree = mocker.patch('cookiecutter.utils.rmtree', return_value=True)

    repo_dir = tmpdir.mkdir('repo')
    backup_dir = tmpdir.mkdir('backup').mkdir('repo')

    subdir = backup_dir.mkdir('subdir')
    inner_dir = subdir.mkdir('inner_dir')

    Path(backup_dir / 'cookiecutter.json').touch()
    Path(subdir / 'README.md').touch()
    Path(inner_dir / 'some_file.txt').touch()

    backed_up_files = [
        x.relative_to(backup_dir)
        for x in sorted(Path(backup_dir).glob('**/*'))
        if x.is_file()
    ]

    vcs._restore_old_repo(str(repo_dir), str(backup_dir))
    restored_files = [
        x.relative_to(repo_dir)
        for x in sorted(Path(repo_dir).glob('**/*'))
        if x.is_file()
    ]
    assert backed_up_files == restored_files
    assert not Path(backup_dir).exists()
    assert mock_rmtree.called_once


def test_restore_old_repo_to_non_existing_directory(mocker, tmpdir):
    """Test that restore works correctly to non-existing directory."""
    mock_rmtree = mocker.patch('cookiecutter.utils.rmtree', return_value=True)

    backup_dir = tmpdir.mkdir('backup').mkdir('repo')

    subdir = backup_dir.mkdir('subdir')
    inner_dir = subdir.mkdir('inner_dir')

    Path(backup_dir / 'cookiecutter.json').touch()
    Path(subdir / 'README.md').touch()
    Path(inner_dir / 'some_file.txt').touch()

    backed_up_files = [
        x.relative_to(backup_dir)
        for x in sorted(Path(backup_dir).glob('**/*'))
        if x.is_file()
    ]

    vcs._restore_old_repo(str(tmpdir / 'repo'), str(backup_dir))
    restored_files = [
        x.relative_to(tmpdir / 'repo')
        for x in sorted(Path(tmpdir / 'repo').glob('**/*'))
        if x.is_file()
    ]
    assert backed_up_files == restored_files
    assert not Path(backup_dir).exists()
    assert mock_rmtree.called_once
