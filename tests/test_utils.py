"""Tests for `cookiecutter.utils` module."""

import stat
import sys
from pathlib import Path

import pytest

from cookiecutter import utils


def make_readonly(path) -> None:
    """Change the access permissions to readonly for a given file."""
    mode = Path.stat(path).st_mode
    Path.chmod(path, mode & ~stat.S_IWRITE)


def test_force_delete(mocker, tmp_path) -> None:
    """Verify `utils.force_delete` makes files writable."""
    ro_file = Path(tmp_path, 'bar')
    ro_file.write_text("Test data")
    make_readonly(ro_file)

    rmtree = mocker.Mock()
    utils.force_delete(rmtree, ro_file, sys.exc_info())

    assert (ro_file.stat().st_mode & stat.S_IWRITE) == stat.S_IWRITE
    rmtree.assert_called_once_with(ro_file)

    utils.rmtree(tmp_path)


def test_rmtree(tmp_path) -> None:
    """Verify `utils.rmtree` remove files marked as read-only."""
    file_path = Path(tmp_path, "bar")
    file_path.write_text("Test data")
    make_readonly(file_path)

    utils.rmtree(tmp_path)

    assert not Path(tmp_path).exists()


def test_make_sure_path_exists(tmp_path) -> None:
    """Verify correct True/False response from `utils.make_sure_path_exists`.

    Should return True if directory exist or created.
    Should return False if impossible to create directory (for example protected)
    """
    existing_directory = tmp_path
    directory_to_create = Path(tmp_path, "not_yet_created")

    utils.make_sure_path_exists(existing_directory)
    utils.make_sure_path_exists(directory_to_create)

    # Ensure by base system methods.
    assert existing_directory.is_dir()
    assert existing_directory.exists()
    assert directory_to_create.is_dir()
    assert directory_to_create.exists()


def test_make_sure_path_exists_correctly_handle_os_error(mocker) -> None:
    """Verify correct True/False response from `utils.make_sure_path_exists`.

    Should return True if directory exist or created.
    Should return False if impossible to create directory (for example protected)
    """
    mocker.patch("pathlib.Path.mkdir", side_effect=OSError)
    with pytest.raises(OSError) as err:
        utils.make_sure_path_exists(Path('protected_path'))
    assert str(err.value) == "Unable to create directory at protected_path"


def test_work_in(tmp_path) -> None:
    """Verify returning to original folder after `utils.work_in` use."""
    cwd = Path.cwd()
    ch_to = tmp_path

    assert ch_to != Path.cwd()

    # Under context manager we should work in tmp_path.
    with utils.work_in(ch_to):
        assert ch_to == Path.cwd()

    # Make sure we return to the correct folder
    assert cwd == Path.cwd()


def test_work_in_without_path() -> None:
    """Folder is not changed if no path provided."""
    cwd = Path.cwd()

    with utils.work_in():
        assert cwd == Path.cwd()

    assert cwd == Path.cwd()


def test_create_tmp_repo_dir(tmp_path) -> None:
    """Verify `utils.create_tmp_repo_dir` creates a copy."""
    repo_dir = Path(tmp_path) / 'bar'
    repo_dir.mkdir()
    subdirs = ('foo', 'bar', 'foobar')
    for name in subdirs:
        (repo_dir / name).mkdir()

    new_repo_dir = utils.create_tmp_repo_dir(repo_dir)

    assert new_repo_dir.exists()
    assert new_repo_dir.glob('*')
