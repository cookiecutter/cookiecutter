"""Regression coverage for cookiecutter issue #2278.

A ZIP template URL that carries a query string or fragment was misclassified:
``is_zip_file`` tested the raw string with ``str.endswith('.zip')``, so
``https://host/t.zip?token=x`` fell through to the git-clone branch, and the
cache filename in ``unzip`` was built from the raw URI, producing a path that
cannot exist on disk. Both are asserted here from the URL *path* instead.
"""

from __future__ import annotations

import pytest

from cookiecutter.repository import is_zip_file

ZIP_URLS_WITH_TRAILING_PARTS = [
    'https://example.com/path/to/zipfile.zip?token=abc123',
    'https://example.com/path/to/zipfile.zip?ref=main&download=1',
    'https://example.com/path/to/zipfile.zip#fragment',
    'https://example.com/path/to/zipfile.zip?token=abc#frag',
    'http://example.com/path/to/zipfile.zip?sig=xyz',
    '/path/to/zipfile.zip?cache=1',
    '/path/to/zipfile.zip#local',
]

PLAIN_ZIP_URLS = [
    '/path/to/zipfile.zip',
    'https://example.com/path/to/zipfile.zip',
    'http://example.com/path/to/zipfile.zip',
]

NOT_ZIP = [
    'https://example.com/path/to/template.tar.gz',
    'https://example.com/path/to/zipfile.zip.bak',
    'https://example.com/zipfile.zip/child',
    'https://example.com/?redirect=zipfile.zip',
    'https://github.com/cookiecutter/cookiecutter.git',
]


@pytest.mark.parametrize('value', PLAIN_ZIP_URLS)
def test_plain_zip_urls_still_classify_as_zip(value: str) -> None:
    """The pre-existing behaviour is unchanged for URLs without a query/fragment."""
    assert is_zip_file(value) is True


@pytest.mark.parametrize('value', ZIP_URLS_WITH_TRAILING_PARTS)
def test_zip_urls_with_query_or_fragment_classify_as_zip(value: str) -> None:
    """A query string or fragment must not hide a ``.zip`` URL path."""
    assert is_zip_file(value) is True


@pytest.mark.parametrize('value', NOT_ZIP)
def test_non_zip_values_are_still_rejected(value: str) -> None:
    """Only the URL path decides, so lookalikes keep returning False."""
    assert is_zip_file(value) is False
