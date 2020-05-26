# -*- coding: utf-8 -*-

"""Tests for function unzip() from zipfile module."""

import tempfile

import pytest

from cookiecutter import zipfile

from cookiecutter.exceptions import InvalidZipRepository


def mock_download():
    """Fake download function."""
    with open('tests/files/fake-repo-tmpl.zip', 'rb') as zf:
        chunk = zf.read(1024)
        while chunk:
            yield chunk
            chunk = zf.read(1024)


def test_unzip_local_file(mocker, tmpdir):
    """Local file reference can be unzipped."""
    mock_prompt_and_delete = mocker.patch(
        'cookiecutter.zipfile.prompt_and_delete', return_value=True, autospec=True
    )

    clone_to_dir = tmpdir.mkdir('clone')

    output_dir = zipfile.unzip(
        'tests/files/fake-repo-tmpl.zip', is_url=False, clone_to_dir=str(clone_to_dir)
    )

    assert output_dir.startswith(tempfile.gettempdir())
    assert not mock_prompt_and_delete.called


def test_unzip_protected_local_file_environment_password(mocker, tmpdir):
    """In `unzip()`, the environment can be used to provide a repo password."""
    mock_prompt_and_delete = mocker.patch(
        'cookiecutter.zipfile.prompt_and_delete', return_value=True, autospec=True
    )

    clone_to_dir = tmpdir.mkdir('clone')

    output_dir = zipfile.unzip(
        'tests/files/protected-fake-repo-tmpl.zip',
        is_url=False,
        clone_to_dir=str(clone_to_dir),
        password='sekrit',
    )

    assert output_dir.startswith(tempfile.gettempdir())
    assert not mock_prompt_and_delete.called


def test_unzip_protected_local_file_bad_environment_password(mocker, tmpdir):
    """In `unzip()`, an error occurs if the environment has a bad password."""
    mocker.patch(
        'cookiecutter.zipfile.prompt_and_delete', return_value=True, autospec=True
    )

    clone_to_dir = tmpdir.mkdir('clone')

    with pytest.raises(InvalidZipRepository):
        zipfile.unzip(
            'tests/files/protected-fake-repo-tmpl.zip',
            is_url=False,
            clone_to_dir=str(clone_to_dir),
            password='not-the-right-password',
        )


def test_unzip_protected_local_file_user_password_with_noinput(mocker, tmpdir):
    """Can't unpack a password-protected repo in no_input mode."""
    mocker.patch(
        'cookiecutter.zipfile.prompt_and_delete', return_value=True, autospec=True
    )

    clone_to_dir = tmpdir.mkdir('clone')

    with pytest.raises(InvalidZipRepository):
        zipfile.unzip(
            'tests/files/protected-fake-repo-tmpl.zip',
            is_url=False,
            clone_to_dir=str(clone_to_dir),
            no_input=True,
        )


def test_unzip_protected_local_file_user_password(mocker, tmpdir):
    """A password-protected local file reference can be unzipped."""
    mock_prompt_and_delete = mocker.patch(
        'cookiecutter.zipfile.prompt_and_delete', return_value=True, autospec=True
    )
    mocker.patch('cookiecutter.zipfile.read_repo_password', return_value='sekrit')

    clone_to_dir = tmpdir.mkdir('clone')

    output_dir = zipfile.unzip(
        'tests/files/protected-fake-repo-tmpl.zip',
        is_url=False,
        clone_to_dir=str(clone_to_dir),
    )

    assert output_dir.startswith(tempfile.gettempdir())
    assert not mock_prompt_and_delete.called


def test_unzip_protected_local_file_user_bad_password(mocker, tmpdir):
    """Error in `unzip()`, if user can't provide a valid password."""
    mocker.patch(
        'cookiecutter.zipfile.prompt_and_delete', return_value=True, autospec=True
    )
    mocker.patch(
        'cookiecutter.zipfile.read_repo_password', return_value='not-the-right-password'
    )

    clone_to_dir = tmpdir.mkdir('clone')

    with pytest.raises(InvalidZipRepository):
        zipfile.unzip(
            'tests/files/protected-fake-repo-tmpl.zip',
            is_url=False,
            clone_to_dir=str(clone_to_dir),
        )


def test_empty_zip_file(mocker, tmpdir):
    """In `unzip()`, an empty file raises an error."""
    mocker.patch(
        'cookiecutter.zipfile.prompt_and_delete', return_value=True, autospec=True
    )

    clone_to_dir = tmpdir.mkdir('clone')

    with pytest.raises(InvalidZipRepository):
        zipfile.unzip(
            'tests/files/empty.zip', is_url=False, clone_to_dir=str(clone_to_dir)
        )


def test_non_repo_zip_file(mocker, tmpdir):
    """In `unzip()`, a repository must have a top level directory."""
    mocker.patch(
        'cookiecutter.zipfile.prompt_and_delete', return_value=True, autospec=True
    )

    clone_to_dir = tmpdir.mkdir('clone')

    with pytest.raises(InvalidZipRepository):
        zipfile.unzip(
            'tests/files/not-a-repo.zip', is_url=False, clone_to_dir=str(clone_to_dir)
        )


def test_bad_zip_file(mocker, tmpdir):
    """In `unzip()`, a corrupted zip file raises an error."""
    mocker.patch(
        'cookiecutter.zipfile.prompt_and_delete', return_value=True, autospec=True
    )

    clone_to_dir = tmpdir.mkdir('clone')

    with pytest.raises(InvalidZipRepository):
        zipfile.unzip(
            'tests/files/bad-zip-file.zip', is_url=False, clone_to_dir=str(clone_to_dir)
        )


def test_unzip_url(mocker, tmpdir):
    """In `unzip()`, a url will be downloaded and unzipped."""
    mock_prompt_and_delete = mocker.patch(
        'cookiecutter.zipfile.prompt_and_delete', return_value=True, autospec=True
    )

    request = mocker.MagicMock()
    request.iter_content.return_value = mock_download()

    mocker.patch(
        'cookiecutter.zipfile.requests.get', return_value=request, autospec=True,
    )

    clone_to_dir = tmpdir.mkdir('clone')

    output_dir = zipfile.unzip(
        'https://example.com/path/to/fake-repo-tmpl.zip',
        is_url=True,
        clone_to_dir=str(clone_to_dir),
    )

    assert output_dir.startswith(tempfile.gettempdir())
    assert not mock_prompt_and_delete.called


def test_unzip_url_existing_cache(mocker, tmpdir):
    """Url should be downloaded and unzipped, old zip file will be removed."""
    mock_prompt_and_delete = mocker.patch(
        'cookiecutter.zipfile.prompt_and_delete', return_value=True, autospec=True
    )

    request = mocker.MagicMock()
    request.iter_content.return_value = mock_download()

    mocker.patch(
        'cookiecutter.zipfile.requests.get', return_value=request, autospec=True,
    )

    clone_to_dir = tmpdir.mkdir('clone')

    # Create an existing cache of the zipfile
    existing_zip = clone_to_dir.join('fake-repo-tmpl.zip')
    existing_zip.write('This is an existing zipfile')

    output_dir = zipfile.unzip(
        'https://example.com/path/to/fake-repo-tmpl.zip',
        is_url=True,
        clone_to_dir=str(clone_to_dir),
    )

    assert output_dir.startswith(tempfile.gettempdir())
    assert mock_prompt_and_delete.call_count == 1


def test_unzip_url_existing_cache_no_input(mocker, tmpdir):
    """If no_input is provided, the existing file should be removed."""
    request = mocker.MagicMock()
    request.iter_content.return_value = mock_download()

    mocker.patch(
        'cookiecutter.zipfile.requests.get', return_value=request, autospec=True,
    )

    clone_to_dir = tmpdir.mkdir('clone')

    # Create an existing cache of the zipfile
    existing_zip = clone_to_dir.join('fake-repo-tmpl.zip')
    existing_zip.write('This is an existing zipfile')

    output_dir = zipfile.unzip(
        'https://example.com/path/to/fake-repo-tmpl.zip',
        is_url=True,
        clone_to_dir=str(clone_to_dir),
        no_input=True,
    )

    assert output_dir.startswith(tempfile.gettempdir())


def test_unzip_should_abort_if_no_redownload(mocker, tmpdir):
    """Should exit without cloning anything If no redownload."""
    mocker.patch(
        'cookiecutter.zipfile.prompt_and_delete', side_effect=SystemExit, autospec=True
    )

    mock_requests_get = mocker.patch(
        'cookiecutter.zipfile.requests.get', autospec=True,
    )

    clone_to_dir = tmpdir.mkdir('clone')

    # Create an existing cache of the zipfile
    existing_zip = clone_to_dir.join('fake-repo-tmpl.zip')
    existing_zip.write('This is an existing zipfile')

    zipfile_url = 'https://example.com/path/to/fake-repo-tmpl.zip'

    with pytest.raises(SystemExit):
        zipfile.unzip(zipfile_url, is_url=True, clone_to_dir=str(clone_to_dir))

    assert not mock_requests_get.called
