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


def test_force_delete(mocker, tmp_path):
    """Verify `utils.force_delete` makes files writable."""
    ro_file = Path(tmp_path, 'bar')

    with open(ro_file, "w") as f:
        f.write("Test data")
    make_readonly(ro_file)

    rmtree = mocker.Mock()
    utils.force_delete(rmtree, ro_file, sys.exc_info())

    assert (ro_file.stat().st_mode & stat.S_IWRITE) == stat.S_IWRITE
    rmtree.assert_called_once_with(ro_file)

    utils.rmtree(tmp_path)


def test_rmtree(tmp_path):
    """Verify `utils.rmtree` remove files marked as read-only."""
    with open(Path(tmp_path, 'bar'), "w") as f:
        f.write("Test data")
    make_readonly(Path(tmp_path, 'bar'))

    utils.rmtree(tmp_path)

    assert not Path(tmp_path).exists()


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


def test_prompt_should_ask_and_rm_repo_dir(mocker, tmp_path):
    """In `prompt_and_delete()`, if the user agrees to delete/reclone the \
    repo, the repo should be deleted."""
    mock_read_user = mocker.patch(
        'cookiecutter.utils.read_user_yes_no', return_value=True
    )
    repo_dir = Path(tmp_path, 'repo')
    repo_dir.mkdir()

    deleted = utils.prompt_and_delete(str(repo_dir))

    assert mock_read_user.called
    assert not repo_dir.exists()
    assert deleted


def test_prompt_should_ask_and_exit_on_user_no_answer(mocker, tmp_path):
    """In `prompt_and_delete()`, if the user decline to delete/reclone the \
    repo, cookiecutter should exit."""
    mock_read_user = mocker.patch(
        'cookiecutter.utils.read_user_yes_no', return_value=False,
    )
    mock_sys_exit = mocker.patch('sys.exit', return_value=True)
    repo_dir = Path(tmp_path, 'repo')
    repo_dir.mkdir()

    deleted = utils.prompt_and_delete(str(repo_dir))

    assert mock_read_user.called
    assert repo_dir.exists()
    assert not deleted
    assert mock_sys_exit.called


def test_prompt_should_ask_and_rm_repo_file(mocker, tmp_path):
    """In `prompt_and_delete()`, if the user agrees to delete/reclone a \
    repo file, the repo should be deleted."""
    mock_read_user = mocker.patch(
        'cookiecutter.utils.read_user_yes_no', return_value=True, autospec=True
    )

    repo_file = tmp_path.joinpath('repo.zip')
    repo_file.write_text('this is zipfile content')

    deleted = utils.prompt_and_delete(str(repo_file))

    assert mock_read_user.called
    assert not repo_file.exists()
    assert deleted


def test_prompt_should_ask_and_keep_repo_on_no_reuse(mocker, tmp_path):
    """In `prompt_and_delete()`, if the user wants to keep their old \
    cloned template repo, it should not be deleted."""
    mock_read_user = mocker.patch(
        'cookiecutter.utils.read_user_yes_no', return_value=False, autospec=True
    )
    repo_dir = Path(tmp_path, 'repo')
    repo_dir.mkdir()

    with pytest.raises(SystemExit):
        utils.prompt_and_delete(str(repo_dir))

    assert mock_read_user.called
    assert repo_dir.exists()


def test_prompt_should_ask_and_keep_repo_on_reuse(mocker, tmp_path):
    """In `prompt_and_delete()`, if the user wants to keep their old \
    cloned template repo, it should not be deleted."""

    def answer(question, default):
        if 'okay to delete' in question:
            return False
        else:
            return True

    mock_read_user = mocker.patch(
        'cookiecutter.utils.read_user_yes_no', side_effect=answer, autospec=True
    )
    repo_dir = Path(tmp_path, 'repo')
    repo_dir.mkdir()

    deleted = utils.prompt_and_delete(str(repo_dir))

    assert mock_read_user.called
    assert repo_dir.exists()
    assert not deleted


def test_prompt_should_not_ask_if_no_input_and_rm_repo_dir(mocker, tmp_path):
    """Prompt should not ask if no input and rm dir.

    In `prompt_and_delete()`, if `no_input` is True, the call to
    `prompt.read_user_yes_no()` should be suppressed.
    """
    mock_read_user = mocker.patch(
        'cookiecutter.prompt.read_user_yes_no', return_value=True, autospec=True
    )
    repo_dir = Path(tmp_path, 'repo')
    repo_dir.mkdir()

    deleted = utils.prompt_and_delete(str(repo_dir), no_input=True)

    assert not mock_read_user.called
    assert not repo_dir.exists()
    assert deleted


def test_prompt_should_not_ask_if_no_input_and_rm_repo_file(mocker, tmp_path):
    """Prompt should not ask if no input and rm file.

    In `prompt_and_delete()`, if `no_input` is True, the call to
    `prompt.read_user_yes_no()` should be suppressed.
    """
    mock_read_user = mocker.patch(
        'cookiecutter.prompt.read_user_yes_no', return_value=True, autospec=True
    )

    repo_file = tmp_path.joinpath('repo.zip')
    repo_file.write_text('this is zipfile content')

    deleted = utils.prompt_and_delete(str(repo_file), no_input=True)

    assert not mock_read_user.called
    assert not repo_file.exists()
    assert deleted
