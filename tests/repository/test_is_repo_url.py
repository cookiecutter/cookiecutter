"""Tests for all supported cookiecutter template repository locations."""

import pytest

from cookiecutter.config import BUILTIN_ABBREVIATIONS
from cookiecutter.repository import expand_abbreviations, is_repo_url, is_zip_file


@pytest.fixture(
    params=[
        '/path/to/zipfile.zip',
        'https://example.com/path/to/zipfile.zip',
        'http://example.com/path/to/zipfile.zip',
        # Query strings and fragments must not hide the .zip extension
        # (e.g. presigned download URLs).
        'https://example.com/path/to/zipfile.zip?download=1',
        'https://example.com/path/to/zipfile.zip#template',
        '/path/to/zipfile.zip?token=abc',
    ]
)
def zipfile(request):
    """Fixture. Represent possible paths to zip file."""
    return request.param


def test_is_zip_file(zipfile) -> None:
    """Verify is_repo_url works."""
    assert is_zip_file(zipfile) is True


def test_is_zip_file_git_with_query_is_not_zip() -> None:
    """A .git URL carrying a query is not classified as a zip file."""
    url = 'https://example.com/repository.git?filename=template.zip'
    assert is_zip_file(url) is False


@pytest.fixture(
    params=[
        'gitolite@server:team/repo',
        'git@github.com:audreyfeldroy/cookiecutter.git',
        'https://github.com/cookiecutter/cookiecutter.git',
        'git+https://private.com/gitrepo',
        'hg+https://private.com/mercurialrepo',
        'https://bitbucket.org/pokoli/cookiecutter.hg',
        'file://server/path/to/repo.git',
    ]
)
def remote_repo_url(request):
    """Fixture. Represent possible URI to different repositories types."""
    return request.param


def test_is_repo_url_for_remote_urls(remote_repo_url) -> None:
    """Verify is_repo_url works."""
    assert is_repo_url(remote_repo_url) is True


@pytest.fixture(
    params=[
        '/audreyr/cookiecutter.git',
        '/home/audreyr/cookiecutter',
        (
            'c:\\users\\foo\\appdata\\local\\temp\\1\\pytest-0\\'
            'test_default_output_dir0\\template'
        ),
    ]
)
def local_repo_url(request):
    """Fixture. Represent possible paths to local resources."""
    return request.param


def test_is_repo_url_for_local_urls(local_repo_url) -> None:
    """Verify is_repo_url works."""
    assert is_repo_url(local_repo_url) is False


def test_expand_abbreviations() -> None:
    """Validate `repository.expand_abbreviations` correctly translate url."""
    template = 'gh:audreyfeldroy/cookiecutter-pypackage'

    # This is not a valid repo url just yet!
    # First `repository.expand_abbreviations` needs to translate it
    assert is_repo_url(template) is False

    expanded_template = expand_abbreviations(template, BUILTIN_ABBREVIATIONS)
    assert is_repo_url(expanded_template) is True
