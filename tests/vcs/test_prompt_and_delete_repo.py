# -*- coding: utf-8 -*-
import pytest

from cookiecutter import vcs


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
