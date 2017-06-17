# -*- coding: utf-8 -*-
import pytest

from cookiecutter import zipfile


def test_prompt_should_ask_and_rm_dir(mocker, tmpdir):
    """In `prompt_and_delete()`, if the user agrees to delete/reclone the
    repo, the repo should be deleted.
    """
    mock_read_user = mocker.patch(
        'cookiecutter.zipfile.read_user_yes_no',
        return_value=True,
        autospec=True
    )
    dir = tmpdir.mkdir('repo')

    zipfile.prompt_and_delete(str(dir))

    assert mock_read_user.called
    assert not dir.exists()


def test_prompt_should_ask_and_keep_dir(mocker, tmpdir):
    """In `prompt_and_delete()`, if the user wants to keep their old
    cloned template repo, it should not be deleted.
    """
    mock_read_user = mocker.patch(
        'cookiecutter.zipfile.read_user_yes_no',
        return_value=False,
        autospec=True
    )
    dir = tmpdir.mkdir('repo')

    with pytest.raises(SystemExit):
        zipfile.prompt_and_delete(str(dir))

    assert mock_read_user.called
    assert dir.exists()


def test_prompt_should_not_ask_if_no_input_and_rm_dir(mocker, tmpdir):
    """In `prompt_and_delete()`, if `no_input` is True, the call to
    `zipfile.read_user_yes_no()` should be suppressed.
    """
    mock_read_user = mocker.patch(
        'cookiecutter.zipfile.read_user_yes_no',
        return_value=True,
        autospec=True
    )
    dir = tmpdir.mkdir('repo')

    zipfile.prompt_and_delete(str(dir), no_input=True)

    assert not mock_read_user.called
    assert not dir.exists()


def test_prompt_should_ask_and_rm_file(mocker, tmpdir):
    """In `prompt_and_delete()`, if the user agrees to delete/reclone the
    template zipfile, the zipfile should be deleted.
    """
    mock_read_user = mocker.patch(
        'cookiecutter.zipfile.read_user_yes_no',
        return_value=True,
        autospec=True
    )
    file = tmpdir.join('repo.zip')
    file.write('this is zipfile content')

    zipfile.prompt_and_delete(str(file))

    assert mock_read_user.called
    assert not file.exists()


def test_prompt_should_ask_and_keep_file(mocker, tmpdir):
    """In `prompt_and_delete()`, if the user wants to keep their old
    downloaded template zipfile, it should not be deleted.
    """
    mock_read_user = mocker.patch(
        'cookiecutter.zipfile.read_user_yes_no',
        return_value=False,
        autospec=True
    )
    file = tmpdir.join('repo.zip')
    file.write('this is zipfile content')

    with pytest.raises(SystemExit):
        zipfile.prompt_and_delete(str(file))

    assert mock_read_user.called
    assert file.exists()


def test_prompt_should_not_ask_if_no_input_and_rm_file(mocker, tmpdir):
    """In `prompt_and_delete()`, if `no_input` is True, the call to
    `zipfile.read_user_yes_no()` should be suppressed.
    """
    mock_read_user = mocker.patch(
        'cookiecutter.zipfile.read_user_yes_no',
        return_value=True,
        autospec=True
    )
    file = tmpdir.join('repo.zip')
    file.write('this is zipfile content')

    zipfile.prompt_and_delete(str(file), no_input=True)

    assert not mock_read_user.called
    assert not file.exists()
