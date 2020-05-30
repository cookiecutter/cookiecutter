"""Collection of tests around cloning cookiecutter template repositories."""
import os

import pytest

from cookiecutter import exceptions, repository


@pytest.mark.parametrize(
    'template, is_url',
    [
        ('/path/to/zipfile.zip', False),
        ('https://example.com/path/to/zipfile.zip', True),
        ('http://example.com/path/to/zipfile.zip', True),
    ],
)
def test_zipfile_unzip(mocker, template, is_url, user_config_data):
    """Verify zip files correctly handled for different source locations.

    `unzip()` should be called with correct args when `determine_repo_dir()`
    is passed a zipfile, or a URL to a zipfile.
    """
    mock_clone = mocker.patch(
        'cookiecutter.repository.unzip',
        return_value='tests/fake-repo-tmpl',
        autospec=True,
    )

    project_dir, cleanup = repository.determine_repo_dir(
        template,
        abbreviations={},
        clone_to_dir=user_config_data['cookiecutters_dir'],
        checkout=None,
        no_input=True,
        password=None,
    )

    mock_clone.assert_called_once_with(
        zip_uri=template,
        is_url=is_url,
        clone_to_dir=user_config_data['cookiecutters_dir'],
        no_input=True,
        password=None,
    )

    assert os.path.isdir(project_dir)
    assert cleanup
    assert 'tests/fake-repo-tmpl' == project_dir


@pytest.fixture
def template_url():
    """URL to example Cookiecutter template on GitHub.

    Note: when used, git clone is mocked.
    """
    return 'https://github.com/pytest-dev/cookiecutter-pytest-plugin.git'


def test_repository_url_should_clone(mocker, template_url, user_config_data):
    """Verify repository url triggers clone function.

    `clone()` should be called with correct args when `determine_repo_dir()` is
    passed a repository template url.
    """
    mock_clone = mocker.patch(
        'cookiecutter.repository.clone',
        return_value='tests/fake-repo-tmpl',
        autospec=True,
    )

    project_dir, cleanup = repository.determine_repo_dir(
        template_url,
        abbreviations={},
        clone_to_dir=user_config_data['cookiecutters_dir'],
        checkout=None,
        no_input=True,
    )

    mock_clone.assert_called_once_with(
        repo_url=template_url,
        checkout=None,
        clone_to_dir=user_config_data['cookiecutters_dir'],
        no_input=True,
    )

    assert os.path.isdir(project_dir)
    assert not cleanup
    assert 'tests/fake-repo-tmpl' == project_dir


def test_repository_url_with_no_context_file(mocker, template_url, user_config_data):
    """Verify cloned repository without `cookiecutter.json` file raises error."""
    mocker.patch(
        'cookiecutter.repository.clone',
        return_value='tests/fake-repo-bad',
        autospec=True,
    )

    with pytest.raises(exceptions.RepositoryNotFound) as err:
        repository.determine_repo_dir(
            template_url,
            abbreviations={},
            clone_to_dir=None,
            checkout=None,
            no_input=True,
        )

    assert str(err.value) == (
        'A valid repository for "{}" could not be found in the following '
        'locations:\n{}'.format(template_url, 'tests/fake-repo-bad')
    )
