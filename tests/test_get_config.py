# -*- coding: utf-8 -*-
import os

import pytest

from cookiecutter import config
from cookiecutter.exceptions import (InvalidConfiguration,
                                     ConfigDoesNotExistException)


def test_find_user_config_envvar_is_valid_path(monkeypatch, tmpdir):
    """If COOKIECUTTER_CONFIG is set and valid, use it"""
    # .ensure makes the path exist so it passes os.path.isfile
    path = tmpdir.mkdir('spoofdir').join('spoofrc').ensure()
    monkeypatch.setenv('COOKIECUTTER_CONFIG', str(path))
    assert config._find_user_config() == str(path)


def test_find_user_config_raises_for_invalid_envvar(monkeypatch, tmpdir):
    """If COOKIECUTTER_CONFIG is set but not a file,
    raise ConfigDoesNotExistException
    """
    # path doesn't actually exist unless we call ensure
    path = tmpdir.mkdir('spoofdir').join('spoofrc')
    monkeypatch.setenv('COOKIECUTTER_CONFIG', str(path))
    with pytest.raises(ConfigDoesNotExistException):
        config._find_user_config()


def test_find_user_config_gets_existing_default(monkeypatch, tmpdir):
    """
    If COOKIECUTTER_CONFIG is unset but ~/.cookiecutterrc exists, return it
    """
    base_path = tmpdir.mkdir('spoofdir')
    # we can't just patch cookiecutter.config.expanduser; the value of
    # USER_CONFIG_FALLBACK_PATH is set at import time, which is prior to when
    # we can patch - so patch the computed constant directly against the
    # imported module
    monkeypatch.setattr(config,
                        'USER_CONFIG_FALLBACK_PATH',
                        str(base_path.join('.cookiecutterrc')))
    default_conf_path = str(base_path.join('.cookiecutterrc').ensure())
    monkeypatch.delenv('COOKIECUTTER_CONFIG', raising=False)
    assert config._find_user_config() == default_conf_path


@pytest.mark.parametrize("platform", ['XDG', 'NIX', 'OSX', 'WIN', None])
def test_find_user_config_platform_dir_search_path(monkeypatch,
                                                   tmpdir,
                                                   platform):
    r"""
    If COOKIECUTTER_CONFIG is unset and ~/.cookiecutterrc does not exist, then
    search the following:
        $XDG_CONFIG_HOME/cookiecutter/config
        %APPDATA%\cookiecutter\config
        ~/.config/cookiecutter/config
        ~/Library/Application\ Support/cookiecutter/config
    And the return the first match that exists
    """
    base_path = tmpdir.mkdir('spoofdir')
    # patch this in this test so we can assert it isn't a file (since nothing
    # below is supposed to run if it is)
    monkeypatch.setattr(config,
                        'USER_CONFIG_FALLBACK_PATH',
                        str(base_path.join('.cookiecutterrc')))
    # preconditions of searching for a platform-specific dir
    monkeypatch.delenv('COOKIECUTTER_CONFIG', raising=False)
    assert not os.path.isfile(config.USER_CONFIG_FALLBACK_PATH)

    search_path = {
        # make them unique - they're just envvars, so they could be anything
        'XDG': base_path.join('XDG'),
        'WIN': base_path.join('WIN'),
        # these two are a little more concrete - they have to match what's
        # hardcoded in the join in cookiecutter/config.py
        'NIX': base_path.join('.config'),
        'OSX': base_path.join('Library', 'Application Support')
    }
    monkeypatch.setenv('XDG_CONFIG_HOME', str(search_path['XDG']))
    monkeypatch.setenv('APPDATA', str(search_path['WIN']))
    monkeypatch.setattr(config, 'HOME_DIR', str(base_path))

    if platform is None:
        assert config._find_user_config() is None
        return

    path = search_path.pop(platform)
    path = path.join('cookiecutter', 'config').ensure()

    assert config._find_user_config() == str(path)
    for _, other_path in search_path.items():
        assert config._find_user_config() != str(other_path)


@pytest.mark.parametrize('kind', ['cookiecutters_dir', 'cookiecutter_replay'])
def test_find_user_data_dir_valid_envvar(monkeypatch, tmpdir, kind):
    tmpdatadir = tmpdir.mkdir('spoof').join('temprc').ensure(dir=True)
    monkeypatch.setenv(kind.upper(), str(tmpdatadir))
    assert config._find_user_data_dir(kind) == str(tmpdatadir)


@pytest.mark.parametrize('kind', ['cookiecutters_dir', 'cookiecutter_replay'])
def test_find_user_data_dir_preexisting_dotdir(monkeypatch, tmpdir, kind):
    tmphome = tmpdir.mkdir('phonyhome')
    monkeypatch.setattr(config, 'HOME_DIR', str(tmphome))
    tmpdatadir = tmphome.join('.{}'.format(kind.lower())).ensure(dir=True)
    assert config._find_user_data_dir(kind) == str(tmpdatadir)


@pytest.mark.parametrize('kind', ['cookiecutters_dir', 'cookiecutter_replay'])
def test_find_user_data_dir_falls_back_to_user_home(monkeypatch, tmpdir, kind):
    monkeypatch.delenv(kind.upper(), raising=False)
    monkeypatch.delenv('XDG_DATA_HOME', raising=False)
    monkeypatch.delenv('APPDATA', raising=False)
    mockdir = tmpdir.mkdir('mock')
    monkeypatch.setattr(config, 'HOME_DIR', str(mockdir))
    expected = os.path.normpath('{}/.{}'.format(str(mockdir), kind.lower()))
    assert config._find_user_data_dir(kind) == expected


def test_merge_configs():
    default = {
        'cookiecutters_dir': '/home/example/some-path-to-templates',
        'replay_dir': '/home/example/some-path-to-replay-files',
        'default_context': {},
        'abbreviations': {
            'gh': 'https://github.com/{0}.git',
            'gl': 'https://gitlab.com/{0}.git',
            'bb': 'https://bitbucket.org/{0}',
        }
    }

    user_config = {
        'default_context': {
            'full_name': 'Raphael Pierzina',
            'github_username': 'hackebrot',
        },
        'abbreviations': {
            'gl': 'https://gitlab.com/hackebrot/{0}.git',
            'pytest-plugin': 'https://github.com/pytest-dev/pytest-plugin.git',
        }
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
        }
    }

    assert config.merge_configs(default, user_config) == expected_config


def test_get_config():
    """
    Opening and reading config file
    """
    conf = config.get_config('tests/test-config/valid-config.yaml')
    expected_conf = {
        'cookiecutters_dir': '/home/example/some-path-to-templates',
        'replay_dir': '/home/example/some-path-to-replay-files',
        'default_context': {
            'full_name': 'Firstname Lastname',
            'email': 'firstname.lastname@gmail.com',
            'github_username': 'example'
        },
        'abbreviations': {
            'gh': 'https://github.com/{0}.git',
            'gl': 'https://gitlab.com/{0}.git',
            'bb': 'https://bitbucket.org/{0}',
            'helloworld': 'https://github.com/hackebrot/helloworld'
        }
    }
    assert conf == expected_conf


def test_get_config_does_not_exist():
    """
    Check that `exceptions.ConfigDoesNotExistException` is raised when
    attempting to get a non-existent config file.
    """
    with pytest.raises(ConfigDoesNotExistException):
        config.get_config('tests/test-config/this-does-not-exist.yaml')


def test_invalid_config():
    """
    An invalid config file should raise an `InvalidConfiguration` exception.
    """
    with pytest.raises(InvalidConfiguration) as excinfo:
        config.get_config('tests/test-config/invalid-config.yaml')

    expected_error_msg = (
        'Unable to parse YAML file '
        'tests/test-config/invalid-config.yaml. '
        'Error: '
    )
    assert expected_error_msg in str(excinfo.value)


def test_get_config_with_defaults():
    """
    A config file that overrides 1 of 3 defaults
    """
    conf = config.get_config('tests/test-config/valid-partial-config.yaml')
    # use the defaults directly rather than invoke config._find_user_data_dir;
    # _find_user_data_dir should be an implementation detail
    default_cookiecutters_dir = config.DEFAULT_CONFIG['cookiecutters_dir']
    default_replay_dir = config.DEFAULT_CONFIG['replay_dir']
    expected_conf = {
        'cookiecutters_dir': default_cookiecutters_dir,
        'replay_dir': default_replay_dir,
        'default_context': {
            'full_name': 'Firstname Lastname',
            'email': 'firstname.lastname@gmail.com',
            'github_username': 'example'
        },
        'abbreviations': {
            'gh': 'https://github.com/{0}.git',
            'gl': 'https://gitlab.com/{0}.git',
            'bb': 'https://bitbucket.org/{0}',
        }
    }
    assert conf == expected_conf
