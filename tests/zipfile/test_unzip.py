# -*- coding: utf-8 -*-
import os

import pytest

from cookiecutter import zipfile


def mock_download():
    with open('tests/files/fake-repo-tmpl.zip', 'rb') as zf:
        chunk = zf.read(1024)
        while chunk:
            yield chunk
            chunk = zf.read(1024)


def test_unzip_local_file(mocker, tmpdir):
    """In `unzip()`, a local file reference is just unzipped where it is.
    """
    mock_prompt_and_delete = mocker.patch(
        'cookiecutter.zipfile.prompt_and_delete',
        return_value=True,
        autospec=True
    )

    clone_to_dir = tmpdir.mkdir('clone')

    output_dir = zipfile.unzip(
        'tests/files/fake-repo-tmpl.zip',
        is_url=False,
        clone_to_dir=str(clone_to_dir)
    )

    assert output_dir == os.path.join(str(clone_to_dir), 'fake-repo-tmpl')
    assert not mock_prompt_and_delete.called


def test_unzip_should_abort_not_overwrite_template(mocker, tmpdir):
    """In `unzip()`, if user doesn't want to overwrite an existing cached
    template, Cookiecutter should exit.
    """
    mocker.patch(
        'cookiecutter.zipfile.prompt_and_delete',
        side_effect=SystemExit,
        autospec=True
    )

    clone_to_dir = tmpdir.mkdir('clone')
    clone_to_dir.mkdir('fake-repo-tmpl')

    with pytest.raises(SystemExit):
        zipfile.unzip(
            'tests/files/fake-repo-tmpl.zip',
            is_url=False,
            clone_to_dir=str(clone_to_dir)
        )


def test_unzip_url(mocker, tmpdir):
    """In `unzip()`, a url will be downloaded and unzipped
    """
    mock_prompt_and_delete = mocker.patch(
        'cookiecutter.zipfile.prompt_and_delete',
        return_value=True,
        autospec=True
    )

    request = mocker.MagicMock()
    request.iter_content.return_value = mock_download()

    mocker.patch(
        'cookiecutter.zipfile.requests.get',
        return_value=request,
        autospec=True,
    )

    clone_to_dir = tmpdir.mkdir('clone')

    output_dir = zipfile.unzip(
        'https://example.com/path/to/fake-repo-tmpl.zip',
        is_url=True,
        clone_to_dir=str(clone_to_dir)
    )

    assert output_dir == os.path.join(str(clone_to_dir), 'fake-repo-tmpl')
    assert not mock_prompt_and_delete.called


def test_unzip_url_existing_cache(mocker, tmpdir):
    """In `unzip()`, a url will be downloaded and unzipped; an existing zip file
    will be removed.
    """
    mock_prompt_and_delete = mocker.patch(
        'cookiecutter.zipfile.prompt_and_delete',
        return_value=True,
        autospec=True
    )

    request = mocker.MagicMock()
    request.iter_content.return_value = mock_download()

    mocker.patch(
        'cookiecutter.zipfile.requests.get',
        return_value=request,
        autospec=True,
    )

    clone_to_dir = tmpdir.mkdir('clone')

    # Create an existing cache of the zipfile
    existing_zip = clone_to_dir.join('fake-repo-tmpl.zip')
    existing_zip.write('This is an existing zipfile')

    output_dir = zipfile.unzip(
        'https://example.com/path/to/fake-repo-tmpl.zip',
        is_url=True,
        clone_to_dir=str(clone_to_dir)
    )

    assert output_dir == os.path.join(str(clone_to_dir), 'fake-repo-tmpl')
    assert mock_prompt_and_delete.call_count == 1


def test_unzip_url_existing_template(mocker, tmpdir):
    """In `unzip()`, a url will be downloaded and unzipped; an existing
    template directory will be removed
    """
    mock_prompt_and_delete = mocker.patch(
        'cookiecutter.zipfile.prompt_and_delete',
        return_value=True,
        autospec=True
    )

    request = mocker.MagicMock()
    request.iter_content.return_value = mock_download()

    mocker.patch(
        'cookiecutter.zipfile.requests.get',
        return_value=request,
        autospec=True,
    )

    clone_to_dir = tmpdir.mkdir('clone')

    # Create an existing rolled out template directory
    clone_to_dir.mkdir('fake-repo-tmpl')

    output_dir = zipfile.unzip(
        'https://example.com/path/to/fake-repo-tmpl.zip',
        is_url=True,
        clone_to_dir=str(clone_to_dir)
    )

    assert output_dir == os.path.join(str(clone_to_dir), 'fake-repo-tmpl')
    assert mock_prompt_and_delete.call_count == 1


def test_unzip_url_existing_cache_and_template(mocker, tmpdir):
    """In `unzip()`, a url will be downloaded and unzipped; an existing
    zipfile cache and template directory will both be removed
    """
    mock_prompt_and_delete = mocker.patch(
        'cookiecutter.zipfile.prompt_and_delete',
        return_value=True,
        autospec=True
    )

    def mock_download():
        with open('tests/files/fake-repo-tmpl.zip', 'rb') as zipfile:
            chunk = zipfile.read(1024)
            while chunk:
                yield chunk
                chunk = zipfile.read(1024)

    request = mocker.MagicMock()
    request.iter_content.return_value = mock_download()

    mocker.patch(
        'cookiecutter.zipfile.requests.get',
        return_value=request,
        autospec=True,
    )

    clone_to_dir = tmpdir.mkdir('clone')

    # Create an existing cache of the zipfile
    existing_zip = clone_to_dir.join('fake-repo-tmpl.zip')
    existing_zip.write('This is an existing zipfile')

    # Create an existing rolled out template directory
    clone_to_dir.mkdir('fake-repo-tmpl')

    output_dir = zipfile.unzip(
        'https://example.com/path/to/fake-repo-tmpl.zip',
        is_url=True,
        clone_to_dir=str(clone_to_dir)
    )

    assert output_dir == os.path.join(str(clone_to_dir), 'fake-repo-tmpl')
    assert mock_prompt_and_delete.call_count == 1


def test_unzip_should_abort_if_no_redownload(mocker, tmpdir):
    """In `unzip()`, if user doesn't want to download, Cookiecutter should exit
    without cloning anything.
    """
    mocker.patch(
        'cookiecutter.zipfile.prompt_and_delete',
        side_effect=SystemExit,
        autospec=True
    )

    mock_requests_get = mocker.patch(
        'cookiecutter.zipfile.requests.get',
        autospec=True,
    )

    clone_to_dir = tmpdir.mkdir('clone')

    # Create an existing cache of the zipfile
    existing_zip = clone_to_dir.join('fake-repo-tmpl.zip')
    existing_zip.write('This is an existing zipfile')

    zipfile_url = 'https://example.com/path/to/fake-repo-tmpl.zip'

    with pytest.raises(SystemExit):
        zipfile.unzip(zipfile_url, is_url=True, clone_to_dir=str(clone_to_dir))

    assert not mock_requests_get.called
