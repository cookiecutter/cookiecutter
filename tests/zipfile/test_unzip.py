"""Tests for function unzip() from zipfile module."""

from __future__ import annotations

import shutil
import tempfile
from collections.abc import Iterator
from pathlib import Path

import pytest

from cookiecutter import zipfile
from cookiecutter.exceptions import InvalidZipRepository


def mock_download() -> Iterator[bytes]:
    """Fake download function."""
    with Path('tests/files/fake-repo-tmpl.zip').open('rb') as zf:
        chunk = zf.read(1024)
        while chunk:
            yield chunk
            chunk = zf.read(1024)


def mock_download_with_empty_chunks() -> Iterator[None | bytes]:
    """Fake download function."""
    yield None
    with Path('tests/files/fake-repo-tmpl.zip').open('rb') as zf:
        chunk = zf.read(1024)
        while chunk:
            yield chunk
            chunk = zf.read(1024)


def test_unzip_local_file(mocker, clone_dir) -> None:
    """Local file reference can be unzipped."""
    mock_prompt_and_delete = mocker.patch(
        'cookiecutter.zipfile.prompt_and_delete', return_value=True, autospec=True
    )

    output_dir = zipfile.unzip(
        'tests/files/fake-repo-tmpl.zip', is_url=False, clone_to_dir=str(clone_dir)
    )

    assert output_dir.startswith(tempfile.gettempdir())
    assert not mock_prompt_and_delete.called


def test_unzip_protected_local_file_environment_password(mocker, clone_dir) -> None:
    """In `unzip()`, the environment can be used to provide a repo password."""
    mock_prompt_and_delete = mocker.patch(
        'cookiecutter.zipfile.prompt_and_delete', return_value=True, autospec=True
    )

    output_dir = zipfile.unzip(
        'tests/files/protected-fake-repo-tmpl.zip',
        is_url=False,
        clone_to_dir=str(clone_dir),
        password='sekrit',
    )

    assert output_dir.startswith(tempfile.gettempdir())
    assert not mock_prompt_and_delete.called


def test_unzip_protected_local_file_bad_environment_password(mocker, clone_dir) -> None:
    """In `unzip()`, an error occurs if the environment has a bad password."""
    mocker.patch(
        'cookiecutter.zipfile.prompt_and_delete', return_value=True, autospec=True
    )

    with pytest.raises(InvalidZipRepository):
        zipfile.unzip(
            'tests/files/protected-fake-repo-tmpl.zip',
            is_url=False,
            clone_to_dir=str(clone_dir),
            password='not-the-right-password',
        )


def test_unzip_protected_local_file_user_password_with_noinput(
    mocker, clone_dir
) -> None:
    """Can't unpack a password-protected repo in no_input mode."""
    mocker.patch(
        'cookiecutter.zipfile.prompt_and_delete', return_value=True, autospec=True
    )

    with pytest.raises(InvalidZipRepository):
        zipfile.unzip(
            'tests/files/protected-fake-repo-tmpl.zip',
            is_url=False,
            clone_to_dir=str(clone_dir),
            no_input=True,
        )


def test_unzip_protected_local_file_user_password(mocker, clone_dir) -> None:
    """A password-protected local file reference can be unzipped."""
    mock_prompt_and_delete = mocker.patch(
        'cookiecutter.zipfile.prompt_and_delete', return_value=True, autospec=True
    )
    mocker.patch('cookiecutter.zipfile.read_repo_password', return_value='sekrit')

    output_dir = zipfile.unzip(
        'tests/files/protected-fake-repo-tmpl.zip',
        is_url=False,
        clone_to_dir=str(clone_dir),
    )

    assert output_dir.startswith(tempfile.gettempdir())
    assert not mock_prompt_and_delete.called


def test_unzip_protected_local_file_user_bad_password(mocker, clone_dir) -> None:
    """Error in `unzip()`, if user can't provide a valid password."""
    mocker.patch(
        'cookiecutter.zipfile.prompt_and_delete', return_value=True, autospec=True
    )
    mocker.patch(
        'cookiecutter.zipfile.read_repo_password', return_value='not-the-right-password'
    )

    with pytest.raises(InvalidZipRepository):
        zipfile.unzip(
            'tests/files/protected-fake-repo-tmpl.zip',
            is_url=False,
            clone_to_dir=str(clone_dir),
        )


def test_empty_zip_file(mocker, clone_dir) -> None:
    """In `unzip()`, an empty file raises an error."""
    mocker.patch(
        'cookiecutter.zipfile.prompt_and_delete', return_value=True, autospec=True
    )

    with pytest.raises(InvalidZipRepository):
        zipfile.unzip(
            'tests/files/empty.zip', is_url=False, clone_to_dir=str(clone_dir)
        )


def test_non_repo_zip_file(mocker, clone_dir) -> None:
    """In `unzip()`, a repository must have a top level directory."""
    mocker.patch(
        'cookiecutter.zipfile.prompt_and_delete', return_value=True, autospec=True
    )

    with pytest.raises(InvalidZipRepository):
        zipfile.unzip(
            'tests/files/not-a-repo.zip', is_url=False, clone_to_dir=str(clone_dir)
        )


def test_bad_zip_file(mocker, clone_dir) -> None:
    """In `unzip()`, a corrupted zip file raises an error."""
    mocker.patch(
        'cookiecutter.zipfile.prompt_and_delete', return_value=True, autospec=True
    )

    with pytest.raises(InvalidZipRepository):
        zipfile.unzip(
            'tests/files/bad-zip-file.zip', is_url=False, clone_to_dir=str(clone_dir)
        )


def test_unzip_url(mocker, clone_dir) -> None:
    """In `unzip()`, a url will be downloaded and unzipped."""
    mock_prompt_and_delete = mocker.patch(
        'cookiecutter.zipfile.prompt_and_delete', return_value=True, autospec=True
    )

    request = mocker.MagicMock()
    request.iter_content.return_value = mock_download()

    mocker.patch(
        'cookiecutter.zipfile.requests.get',
        return_value=request,
        autospec=True,
    )

    output_dir = zipfile.unzip(
        'https://example.com/path/to/fake-repo-tmpl.zip',
        is_url=True,
        clone_to_dir=str(clone_dir),
    )

    assert output_dir.startswith(tempfile.gettempdir())
    assert not mock_prompt_and_delete.called


def test_unzip_url_with_empty_chunks(mocker, clone_dir) -> None:
    """In `unzip()` empty chunk must be ignored."""
    mock_prompt_and_delete = mocker.patch(
        'cookiecutter.zipfile.prompt_and_delete', return_value=True, autospec=True
    )

    request = mocker.MagicMock()
    request.iter_content.return_value = mock_download_with_empty_chunks()

    mocker.patch(
        'cookiecutter.zipfile.requests.get',
        return_value=request,
        autospec=True,
    )

    output_dir = zipfile.unzip(
        'https://example.com/path/to/fake-repo-tmpl.zip',
        is_url=True,
        clone_to_dir=str(clone_dir),
    )

    assert output_dir.startswith(tempfile.gettempdir())
    assert not mock_prompt_and_delete.called


def test_unzip_url_existing_cache(mocker, clone_dir) -> None:
    """Url should be downloaded and unzipped, old zip file will be removed."""
    mock_prompt_and_delete = mocker.patch(
        'cookiecutter.zipfile.prompt_and_delete', return_value=True, autospec=True
    )

    request = mocker.MagicMock()
    request.iter_content.return_value = mock_download()

    mocker.patch(
        'cookiecutter.zipfile.requests.get',
        return_value=request,
        autospec=True,
    )

    # Create an existing cache of the zipfile
    existing_zip = clone_dir.joinpath('fake-repo-tmpl.zip')
    existing_zip.write_text('This is an existing zipfile')

    output_dir = zipfile.unzip(
        'https://example.com/path/to/fake-repo-tmpl.zip',
        is_url=True,
        clone_to_dir=str(clone_dir),
    )

    assert output_dir.startswith(tempfile.gettempdir())
    assert mock_prompt_and_delete.call_count == 1


def test_unzip_url_existing_cache_no_input(mocker, clone_dir) -> None:
    """If no_input is provided, the existing file should be removed."""
    request = mocker.MagicMock()
    request.iter_content.return_value = mock_download()

    mocker.patch(
        'cookiecutter.zipfile.requests.get',
        return_value=request,
        autospec=True,
    )

    # Create an existing cache of the zipfile
    existing_zip = clone_dir.joinpath('fake-repo-tmpl.zip')
    existing_zip.write_text('This is an existing zipfile')

    output_dir = zipfile.unzip(
        'https://example.com/path/to/fake-repo-tmpl.zip',
        is_url=True,
        clone_to_dir=str(clone_dir),
        no_input=True,
    )

    assert output_dir.startswith(tempfile.gettempdir())


def test_unzip_should_abort_if_no_redownload(mocker, clone_dir) -> None:
    """Should exit without cloning anything If no redownload."""
    mocker.patch(
        'cookiecutter.zipfile.prompt_and_delete', side_effect=SystemExit, autospec=True
    )

    mock_requests_get = mocker.patch(
        'cookiecutter.zipfile.requests.get',
        autospec=True,
    )

    # Create an existing cache of the zipfile
    existing_zip = clone_dir.joinpath('fake-repo-tmpl.zip')
    existing_zip.write_text('This is an existing zipfile')

    zipfile_url = 'https://example.com/path/to/fake-repo-tmpl.zip'

    with pytest.raises(SystemExit):
        zipfile.unzip(zipfile_url, is_url=True, clone_to_dir=str(clone_dir))

    assert not mock_requests_get.called


def test_unzip_is_ok_to_reuse(mocker, clone_dir) -> None:
    """Already downloaded zip should not be downloaded again."""
    mock_prompt_and_delete = mocker.patch(
        'cookiecutter.zipfile.prompt_and_delete', return_value=False, autospec=True
    )

    request = mocker.MagicMock()

    existing_zip = clone_dir.joinpath('fake-repo-tmpl.zip')
    shutil.copy('tests/files/fake-repo-tmpl.zip', existing_zip)

    output_dir = zipfile.unzip(
        'https://example.com/path/to/fake-repo-tmpl.zip',
        is_url=True,
        clone_to_dir=str(clone_dir),
    )

    assert output_dir.startswith(tempfile.gettempdir())
    assert mock_prompt_and_delete.call_count == 1
    assert request.iter_content.call_count == 0


@pytest.mark.parametrize(
    'suffix',
    ['?download=1', '#template', '?token=a/b#section/c'],
)
@pytest.mark.parametrize('reuse_cache', [False, True])
def test_unzip_url_path_cache(mocker, clone_dir, suffix, reuse_cache) -> None:
    """Cache names use the path, while downloads retain the complete URL."""
    archive = Path('tests/files/fake-repo-tmpl.zip').read_bytes()
    cached_zip = clone_dir / 'fake-repo-tmpl.zip'
    if reuse_cache:
        cached_zip.write_bytes(archive)
    prompt = mocker.patch(
        'cookiecutter.zipfile.prompt_and_delete', return_value=False, autospec=True
    )
    response = mocker.Mock()
    response.iter_content.return_value = [archive]
    get = mocker.patch(
        'cookiecutter.zipfile.requests.get', return_value=response, autospec=True
    )
    url = 'https://example.com/path/to/fake-repo-tmpl.zip' + suffix

    output_dir = zipfile.unzip(url, is_url=True, clone_to_dir=clone_dir)
    try:
        assert (Path(output_dir) / 'cookiecutter.json').is_file()
        assert cached_zip.read_bytes() == archive
        assert list(clone_dir.iterdir()) == [cached_zip]
        if reuse_cache:
            prompt.assert_called_once_with(str(cached_zip), no_input=False)
            get.assert_not_called()
        else:
            prompt.assert_not_called()
            get.assert_called_once_with(url, stream=True, timeout=100)
    finally:
        shutil.rmtree(Path(output_dir).parent)
