# -*- coding: utf-8 -*-

"""Collection of tests around repository type identification."""

import pytest

from cookiecutter import exceptions, vcs


@pytest.mark.parametrize(
    'repo_url, exp_repo_type, exp_repo_url',
    [
        (
            'git+https://github.com/pytest-dev/cookiecutter-pytest-plugin.git',
            'git',
            'https://github.com/pytest-dev/cookiecutter-pytest-plugin.git',
        ),
        (
            'hg+https://bitbucket.org/foo/bar.hg',
            'hg',
            'https://bitbucket.org/foo/bar.hg',
        ),
        (
            'https://github.com/pytest-dev/cookiecutter-pytest-plugin.git',
            'git',
            'https://github.com/pytest-dev/cookiecutter-pytest-plugin.git',
        ),
        ('https://bitbucket.org/foo/bar.hg', 'hg', 'https://bitbucket.org/foo/bar.hg'),
        (
            'https://github.com/audreyr/cookiecutter-pypackage.git',
            'git',
            'https://github.com/audreyr/cookiecutter-pypackage.git',
        ),
        (
            'https://github.com/audreyr/cookiecutter-pypackage',
            'git',
            'https://github.com/audreyr/cookiecutter-pypackage',
        ),
        (
            'git@gitorious.org:cookiecutter-gitorious/cookiecutter-gitorious.git',
            'git',
            'git@gitorious.org:cookiecutter-gitorious/cookiecutter-gitorious.git',
        ),
        (
            'https://audreyr@bitbucket.org/audreyr/cookiecutter-bitbucket',
            'hg',
            'https://audreyr@bitbucket.org/audreyr/cookiecutter-bitbucket',
        ),
    ],
)
def test_identify_known_repo(repo_url, exp_repo_type, exp_repo_url):
    """Verify different correct repositories url syntax is correctly transformed."""
    assert vcs.identify_repo(repo_url) == (exp_repo_type, exp_repo_url)


@pytest.fixture(
    params=[
        'foo+git',  # uses explicit identifier with 'git' in the wrong place
        'foo+hg',  # uses explicit identifier with 'hg' in the wrong place
        'foo+bar',  # uses explicit identifier with neither 'git' nor 'hg'
        'foobar',  # no identifier but neither 'git' nor 'bitbucket' in url
        'http://norepotypespecified.com',
    ]
)
def unknown_repo_type_url(request):
    """Fixture. Return wrong formatted repository url."""
    return request.param


def test_identify_raise_on_unknown_repo(unknown_repo_type_url):
    """Verify different incorrect repositories url syntax trigger error raising."""
    with pytest.raises(exceptions.UnknownRepoType):
        vcs.identify_repo(unknown_repo_type_url)
