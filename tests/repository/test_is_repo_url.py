# -*- coding: utf-8 -*-

"""Tests for all supported cookiecutter template repository locations."""

import pytest

from cookiecutter.config import BUILTIN_ABBREVIATIONS
from cookiecutter.repository import (
    is_zip_file, is_repo_url, expand_abbreviations
)


@pytest.fixture(params=[
    '/path/to/zipfile.zip',
    'https://example.com/path/to/zipfile.zip',
    'http://example.com/path/to/zipfile.zip',
])
def zipfile(request):
    return request.param


def test_is_zip_file(zipfile):
    """Verify is_repo_url works."""
    assert is_zip_file(zipfile) is True


@pytest.fixture(params=[
    'gitolite@server:team/repo',
    'git@github.com:audreyr/cookiecutter.git',
    'https://github.com/audreyr/cookiecutter.git',
    'git+https://private.com/gitrepo',
    'hg+https://private.com/mercurialrepo',
    'https://bitbucket.org/pokoli/cookiecutter.hg',
    'file://server/path/to/repo.git',
])
def remote_repo_url(request):
    return request.param


def test_is_repo_url_for_remote_urls(remote_repo_url):
    """Verify is_repo_url works."""
    assert is_repo_url(remote_repo_url) is True


@pytest.fixture(params=[
    '/audreyr/cookiecutter.git',
    '/home/audreyr/cookiecutter',
    (
        'c:\\users\\appveyor\\appdata\\local\\temp\\1\\pytest-0\\'
        'test_default_output_dir0\\template'
    ),
])
def local_repo_url(request):
    return request.param


def test_is_repo_url_for_local_urls(local_repo_url):
    """Verify is_repo_url works."""
    assert is_repo_url(local_repo_url) is False


def test_expand_abbreviations():
    template = 'gh:audreyr/cookiecutter-pypackage'

    # This is not a valid repo url just yet!
    # First `repository.expand_abbreviations` needs to translate it
    assert is_repo_url(template) is False

    expanded_template = expand_abbreviations(template, BUILTIN_ABBREVIATIONS)
    assert is_repo_url(expanded_template) is True
