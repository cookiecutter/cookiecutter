"""Collection of tests around loading cookiecutter config."""

import os

import pytest
import yaml

from cookiecutter import config
from cookiecutter.exceptions import ConfigDoesNotExistException, InvalidConfiguration


def test_merge_configs() -> None:
    """Verify default and user config merged in expected way."""
    default = {
        'cookiecutters_dir': '/home/example/some-path-to-templates',
        'replay_dir': '/home/example/some-path-to-replay-files',
        'default_context': {},
        'abbreviations': {
            'gh': 'https://github.com/{0}.git',
            'gl': 'https://gitlab.com/{0}.git',
            'bb': 'https://bitbucket.org/{0}',
        },
    }

    user_config = {
        'default_context': {
            'full_name': 'Raphael Pierzina',
            'github_username': 'hackebrot',
        },
        'abbreviations': {
            'gl': 'https://gitlab.com/hackebrot/{0}.git',
            'pytest-plugin': 'https://github.com/pytest-dev/pytest-plugin.git',
        },
    }

    expected_config = {
        'cookiecutters_dir': '/home/example/some-path-to-templates',
        'replay_dir': '/home/example/some-path-to-replay-files',
        'default_context': {
            'full_name': 'Raphael Pierzina',
            'github_username': 'hackebrot',
        },
        'abbreviations': {
            'gh': 'https://github.com/{0}.git',
            'gl': 'https://gitlab.com/hackebrot/{0}.git',
            'bb': 'https://bitbucket.org/{0}',
            'pytest-plugin': 'https://github.com/pytest-dev/pytest-plugin.git',
        },
    }

    assert config.merge_configs(default, user_config) == expected_config


def test_get_config() -> None:
    """Verify valid config opened and rendered correctly."""
    conf = config.get_config('tests/test-config/valid-config.yaml')
    expected_conf = {
        'cookiecutters_dir': '/home/example/some-path-to-templates',
        'replay_dir': '/home/example/some-path-to-replay-files',
        'default_context': {
            'full_name': 'Firstname Lastname',
            'email': 'firstname.lastname@gmail.com',
            'github_username': 'example',
            'project': {
                'description': 'description',
                'tags': [
                    'first',
                    'second',
                    'third',
                ],
            },
        },
        'abbreviations': {
            'gh': 'https://github.com/{0}.git',
            'gl': 'https://gitlab.com/{0}.git',
            'bb': 'https://bitbucket.org/{0}',
            'helloworld': 'https://github.com/hackebrot/helloworld',
        },
    }
    assert conf == expected_conf


def test_get_config_does_not_exist() -> None:
    """Check that `exceptions.ConfigDoesNotExistException` is raised when \
    attempting to get a non-existent config file."""
    expected_error_msg = 'Config file tests/not-exist.yaml does not exist.'
    with pytest.raises(ConfigDoesNotExistException) as exc_info:
        config.get_config('tests/not-exist.yaml')
    assert str(exc_info.value) == expected_error_msg


def test_invalid_config() -> None:
    """An invalid config file should raise an `InvalidConfiguration` \
    exception."""
    expected_error_msg = (
        'Unable to parse YAML file tests/test-config/invalid-config.yaml.'
    )
    with pytest.raises(InvalidConfiguration) as exc_info:
        config.get_config('tests/test-config/invalid-config.yaml')
        assert expected_error_msg in str(exc_info.value)
        assert isinstance(exc_info.value.__cause__, yaml.YAMLError)


def test_get_config_with_defaults() -> None:
    """A config file that overrides 1 of 3 defaults."""
    conf = config.get_config('tests/test-config/valid-partial-config.yaml')
    expected_conf = {
        'cookiecutters_dir': config.DEFAULT_CONFIG['cookiecutters_dir'],
        'replay_dir': config.DEFAULT_CONFIG['replay_dir'],
        'default_context': {
            'full_name': 'Firstname Lastname',
            'email': 'firstname.lastname@gmail.com',
            'github_username': 'example',
        },
        'abbreviations': {
            'gh': 'https://github.com/{0}.git',
            'gl': 'https://gitlab.com/{0}.git',
            'bb': 'https://bitbucket.org/{0}',
        },
    }
    assert conf == expected_conf


def test_get_config_empty_config_file() -> None:
    """An empty config file results in the default config."""
    conf = config.get_config('tests/test-config/empty-config.yaml')
    assert conf == config.DEFAULT_CONFIG


def test_xdg_dir_uses_env_variable_when_set(monkeypatch) -> None:
    """XDG base directory environment variables are honored when set."""
    monkeypatch.setenv('XDG_CACHE_HOME', '/custom/cache')
    monkeypatch.setenv('XDG_DATA_HOME', '/custom/data')

    cache_dir = config.xdg_dir('XDG_CACHE_HOME', '~/.cache', 'cookiecutter')
    data_dir = config.xdg_dir('XDG_DATA_HOME', '~/.local/share', 'cookiecutter')
    assert cache_dir == os.path.join('/custom/cache', 'cookiecutter')
    assert data_dir == os.path.join('/custom/data', 'cookiecutter')


def test_xdg_dir_uses_spec_default_when_env_var_unset(monkeypatch) -> None:
    """XDG base directory defaults are used when the env var is not set."""
    monkeypatch.delenv('XDG_CACHE_HOME', raising=False)
    monkeypatch.delenv('XDG_DATA_HOME', raising=False)
    monkeypatch.setenv('HOME', '/custom/home')

    cache_dir = config.xdg_dir('XDG_CACHE_HOME', '~/.cache', 'cookiecutter')
    data_dir = config.xdg_dir('XDG_DATA_HOME', '~/.local/share', 'cookiecutter')
    assert cache_dir == os.path.join('/custom/home', '.cache', 'cookiecutter')
    assert data_dir == os.path.join('/custom/home', '.local', 'share', 'cookiecutter')


def test_get_config_invalid_file_with_array_as_top_level_element() -> None:
    """An exception should be raised if top-level element is array."""
    expected_error_msg = (
        'Top-level element of YAML file '
        'tests/test-config/invalid-config-w-array.yaml should be an object.'
    )
    with pytest.raises(InvalidConfiguration) as exc_info:
        config.get_config('tests/test-config/invalid-config-w-array.yaml')
    assert expected_error_msg in str(exc_info.value)


def test_get_config_invalid_file_with_multiple_docs() -> None:
    """An exception should be raised if config file contains multiple docs."""
    expected_error_msg = (
        'Unable to parse YAML file '
        'tests/test-config/invalid-config-w-multiple-docs.yaml.'
    )
    with pytest.raises(InvalidConfiguration) as exc_info:
        config.get_config('tests/test-config/invalid-config-w-multiple-docs.yaml')
    assert expected_error_msg in str(exc_info.value)
