# -*- coding: utf-8 -*-

"""Tests for `cookiecutter.utils` module."""

import os
import stat
import sys

import pytest

from cookiecutter import utils


def make_readonly(path):
    """Change the access permissions to readonly for a given file."""
    mode = os.stat(path).st_mode
    os.chmod(path, mode & ~stat.S_IWRITE)


def test_rmtree():
    """Verify `utils.rmtree` remove files marked as read-only."""
    os.mkdir('foo')
    with open('foo/bar', "w") as f:
        f.write("Test data")
    make_readonly('foo/bar')
    utils.rmtree('foo')
    assert not os.path.exists('foo')


def test_make_sure_path_exists():
    """Verify correct True/False response from `utils.make_sure_path_exists`.

    Should return True if directory exist or created.
    Should return False if impossible to create directory (for example protected)
    """
    if sys.platform.startswith('win'):
        existing_directory = os.path.abspath(os.curdir)
        uncreatable_directory = 'a*b'
    else:
        existing_directory = '/usr/'
        uncreatable_directory = '/this-doesnt-exist-and-cant-be-created/'

    assert utils.make_sure_path_exists(existing_directory)
    assert utils.make_sure_path_exists('tests/blah')
    assert utils.make_sure_path_exists('tests/trailingslash/')
    assert not utils.make_sure_path_exists(uncreatable_directory)
    utils.rmtree('tests/blah/')
    utils.rmtree('tests/trailingslash/')


def test_workin():
    """Verify returning to original folder after `utils.work_in` use."""
    cwd = os.getcwd()
    ch_to = 'tests/files'

    class TestException(Exception):
        pass

    def test_work_in():
        with utils.work_in(ch_to):
            test_dir = os.path.join(cwd, ch_to).replace("/", os.sep)
            assert test_dir == os.getcwd()
            raise TestException()

    # Make sure we return to the correct folder
    assert cwd == os.getcwd()

    # Make sure that exceptions are still bubbled up
    with pytest.raises(TestException):
        test_work_in()


def test_prompt_should_ask_and_rm_repo_dir(mocker, tmpdir):
    """In `prompt_and_delete()`, if the user agrees to delete/reclone the \
    repo, the repo should be deleted."""
    mock_read_user = mocker.patch(
        'cookiecutter.utils.read_user_yes_no', return_value=True, autospec=True
    )
    repo_dir = tmpdir.mkdir('repo')

    deleted = utils.prompt_and_delete(str(repo_dir))

    assert mock_read_user.called
    assert not repo_dir.exists()
    assert deleted


def test_prompt_should_ask_and_exit_on_user_no_answer(mocker, tmpdir):
    """In `prompt_and_delete()`, if the user decline to delete/reclone the \
    repo, cookiecutter should exit."""
    mock_read_user = mocker.patch(
        'cookiecutter.utils.read_user_yes_no', return_value=False,
    )
    mock_sys_exit = mocker.patch('sys.exit', return_value=True)
    repo_dir = tmpdir.mkdir('repo')

    deleted = utils.prompt_and_delete(str(repo_dir))

    assert mock_read_user.called
    assert repo_dir.exists()
    assert not deleted
    assert mock_sys_exit.called


def test_prompt_should_ask_and_rm_repo_file(mocker, tmpdir):
    """In `prompt_and_delete()`, if the user agrees to delete/reclone a \
    repo file, the repo should be deleted."""
    mock_read_user = mocker.patch(
        'cookiecutter.utils.read_user_yes_no', return_value=True, autospec=True
    )

    repo_file = tmpdir.join('repo.zip')
    repo_file.write('this is zipfile content')

    deleted = utils.prompt_and_delete(str(repo_file))

    assert mock_read_user.called
    assert not repo_file.exists()
    assert deleted


def test_prompt_should_ask_and_keep_repo_on_no_reuse(mocker, tmpdir):
    """In `prompt_and_delete()`, if the user wants to keep their old \
    cloned template repo, it should not be deleted."""
    mock_read_user = mocker.patch(
        'cookiecutter.utils.read_user_yes_no', return_value=False, autospec=True
    )
    repo_dir = tmpdir.mkdir('repo')

    with pytest.raises(SystemExit):
        utils.prompt_and_delete(str(repo_dir))

    assert mock_read_user.called
    assert repo_dir.exists()


def test_prompt_should_ask_and_keep_repo_on_reuse(mocker, tmpdir):
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
    repo_dir = tmpdir.mkdir('repo')

    deleted = utils.prompt_and_delete(str(repo_dir))

    assert mock_read_user.called
    assert repo_dir.exists()
    assert not deleted


def test_prompt_should_not_ask_if_no_input_and_rm_repo_dir(mocker, tmpdir):
    """Prompt should not ask if no input and rm dir.

    In `prompt_and_delete()`, if `no_input` is True, the call to
    `prompt.read_user_yes_no()` should be suppressed.
    """
    mock_read_user = mocker.patch(
        'cookiecutter.prompt.read_user_yes_no', return_value=True, autospec=True
    )
    repo_dir = tmpdir.mkdir('repo')

    deleted = utils.prompt_and_delete(str(repo_dir), no_input=True)

    assert not mock_read_user.called
    assert not repo_dir.exists()
    assert deleted


def test_prompt_should_not_ask_if_no_input_and_rm_repo_file(mocker, tmpdir):
    """Prompt should not ask if no input and rm file.

    In `prompt_and_delete()`, if `no_input` is True, the call to
    `prompt.read_user_yes_no()` should be suppressed.
    """
    mock_read_user = mocker.patch(
        'cookiecutter.prompt.read_user_yes_no', return_value=True, autospec=True
    )

    repo_file = tmpdir.join('repo.zip')
    repo_file.write('this is zipfile content')

    deleted = utils.prompt_and_delete(str(repo_file), no_input=True)

    assert not mock_read_user.called
    assert not repo_file.exists()
    assert deleted
