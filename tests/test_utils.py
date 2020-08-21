"""Tests for `cookiecutter.utils` module."""
import stat
import sys
from pathlib import Path

import pytest

from cookiecutter import utils


def make_readonly(path):
    """Change the access permissions to readonly for a given file."""
    mode = Path.stat(path).st_mode
    Path.chmod(path, mode & ~stat.S_IWRITE)


@pytest.mark.skipif(
    sys.version_info[0] == 3 and sys.version_info[1] == 6 and sys.version_info[2] == 1,
    reason="Outdated pypy3 version on Travis CI/CD",
)
def test_rmtree(tmp_path):
    """Verify `utils.rmtree` remove files marked as read-only."""
    with open(Path(tmp_path, 'bar'), "w") as f:
        f.write("Test data")
    make_readonly(Path(tmp_path, 'bar'))

    utils.rmtree(tmp_path)

    assert not Path(tmp_path).exists()


@pytest.mark.skipif(
    sys.version_info[0] == 3 and sys.version_info[1] == 6 and sys.version_info[2] == 1,
    reason="Outdated pypy3 version on Travis CI/CD",
)
def test_make_sure_path_exists(tmp_path):
    """Verify correct True/False response from `utils.make_sure_path_exists`.

    Should return True if directory exist or created.
    Should return False if impossible to create directory (for example protected)
    """
    existing_directory = tmp_path
    directory_to_create = Path(tmp_path, "not_yet_created")

    assert utils.make_sure_path_exists(existing_directory)
    assert utils.make_sure_path_exists(directory_to_create)

    # Ensure by base system methods.
    assert existing_directory.is_dir()
    assert existing_directory.exists()
    assert directory_to_create.is_dir()
    assert directory_to_create.exists()


def test_make_sure_path_exists_correctly_handle_os_error(mocker):
    """Verify correct True/False response from `utils.make_sure_path_exists`.

    Should return True if directory exist or created.
    Should return False if impossible to create directory (for example protected)
    """

    def raiser(*args, **kwargs):
        raise OSError()

    mocker.patch("os.makedirs", raiser)
    uncreatable_directory = Path('protected_path')

    assert not utils.make_sure_path_exists(uncreatable_directory)


@pytest.mark.skipif(
    sys.version_info[0] == 3 and sys.version_info[1] == 6 and sys.version_info[2] == 1,
    reason="Outdated pypy3 version on Travis CI/CD",
)
def test_work_in(tmp_path):
    """Verify returning to original folder after `utils.work_in` use."""
    cwd = Path.cwd()
    ch_to = tmp_path

    assert ch_to != Path.cwd()

    # Under context manager we should work in tmp_path.
    with utils.work_in(ch_to):
        assert ch_to == Path.cwd()

    # Make sure we return to the correct folder
    assert cwd == Path.cwd()


def test_prompt_ok_to_delete_reads_user_yes(mocker):
    """In `prompt_ok_to_delete()` the user answers yes."""
    mock_read_user = mocker.patch(
        'cookiecutter.utils.read_user_yes_no', return_value=True
    )
    ok_to_delete = utils.prompt_ok_to_delete('path/to/repo')

    assert mock_read_user.called_once
    assert ok_to_delete


def test_prompt_ok_to_delete_reads_user_no(mocker):
    """In `prompt_ok_to_delete()` the user answers no."""
    mock_read_user = mocker.patch(
        'cookiecutter.utils.read_user_yes_no', return_value=False
    )
    ok_to_delete = utils.prompt_ok_to_delete('path/to/repo')

    assert mock_read_user.called_once
    assert not ok_to_delete


def test_prompt_ok_to_delete_no_user_input(mocker):
    """In `prompt_ok_to_delete()` no user input means yes."""
    mock_read_user = mocker.patch(
        'cookiecutter.utils.read_user_yes_no', return_value=False
    )
    ok_to_delete = utils.prompt_ok_to_delete('path/to/repo', no_input=True)

    assert not mock_read_user.called
    assert ok_to_delete


def test_prompt_ok_to_reuse(mocker):
    """In `prompt_ok_to_reuse()` check that the user Yes is read."""
    mock_read_user = mocker.patch(
        'cookiecutter.utils.read_user_yes_no', return_value=True,
    )
    ok_to_reuse = utils.prompt_ok_to_reuse('any_path')

    assert mock_read_user.called_once
    assert ok_to_reuse


def test_prompt_not_ok_to_reuse(mocker):
    """In `prompt_ok_to_reuse()` check that the user No is read."""
    mock_read_user = mocker.patch(
        'cookiecutter.utils.read_user_yes_no', return_value=False,
    )
    ok_to_reuse = utils.prompt_ok_to_reuse('any_path')

    assert mock_read_user.called_once
    assert not ok_to_reuse
