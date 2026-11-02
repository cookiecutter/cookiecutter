"""Tests for all supported cookiecutter template repository locations."""

import pytest

from cookiecutter.config import BUILTIN_ABBREVIATIONS
from cookiecutter.repository import expand_abbreviations, is_repo_url, is_zip_file


@pytest.fixture(
    params=[
        '/path/to/zipfile.zip',
        'https://example.com/path/to/zipfile.zip',
        'http://example.com/path/to/zipfile.zip',
    ]
)
def zipfile(request):
    """Fixture. Represent possible paths to zip file."""
    return request.param


def test_is_zip_file(zipfile) -> None:
    """Verify is_repo_url works."""
    assert is_zip_file(zipfile) is True


@pytest.mark.parametrize(
    'value, expected',
    [
        ('https://example.com/path/to/zipfile.zip?download=1', True),
        ('https://example.com/path/to/zipfile.zip#template', True),
        ('https://example.com/path/to/zipfile.zip?token=a/b#section/c', True),
        ('https://example.com/repository.git?filename=template.zip', False),
        ('https://example.com/repository.git#template.zip', False),
        ('https://example.com/path/to/zipfile.zip/child', False),
        ('/path/to/zipfile.zip?download=1', False),
        ('/path/to/template?name.zip', True),
        ('/path/to/template#name.zip', True),
    ],
)
def test_is_zip_file_with_query_or_fragment(value: str, expected: bool) -> None:
    """HTTP(S) ZIP URLs are classified by path; local paths are unchanged."""
    assert is_zip_file(value) is expected


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
