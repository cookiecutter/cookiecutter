# -*- coding: utf-8 -*-

"""Global configuration handling."""

from __future__ import unicode_literals
import copy
import logging
from os.path import (
    abspath, expandvars, expanduser, isfile, isdir, join
)
import io

import poyo

from .exceptions import ConfigDoesNotExistException
from .exceptions import InvalidConfiguration


logger = logging.getLogger(__name__)

USER_CONFIG_FALLBACK_PATH = expanduser('~/.cookiecutterrc')


def _find_user_config():
    # user override gets returned immediately
    if isfile(expandvars('$COOKIECUTTER_CONFIG')):
        return expandvars('$COOKIECUTTER_CONFIG')

    # give priority to existing cookie cutter rc's
    if isfile(USER_CONFIG_FALLBACK_PATH):
        return USER_CONFIG_FALLBACK_PATH

    paths = [
        expandvars('$XDG_CONFIG_HOME'),         # *nix
        expandvars('%APPDATA%'),                # Windows
        expanduser('~/.config'),                # lazy Linux (not all set XDG)
        expanduser('~/Library/Application\ Support/'),  # OS X
    ]
    for _path in paths:
        path = abspath(join(_path, 'cookiecutter', 'config'))
        if isfile(path):
            return path
    # if we reach this point then either the config file does not exist or we
    # have not properly been told where to look via env vars
    raise ConfigDoesNotExistException


def _find_user_data_dir(kind):
    envvar = '${}'.format(kind.upper())
    dotdir = '~/.{}'.format(kind.lower())

    # only two types of data dir in the cookiecutter project at the moment
    assert kind.lower() in ('cookiecutters_dir', 'cookiecutter_replay')

    # user override via $COOKIECUTTERS_DIR
    if isdir(expandvars(envvar)):
        return expandvars(envvar)

    # respect existing COOKIECUTTERS_DIR
    fallback = expanduser(dotdir)
    if isdir(fallback):
        return fallback

    # data dir search path
    paths = [
        expandvars('$XDG_DATA_HOME'),           # *nix
        expandvars('%APPDATA%'),                # Windows
        expanduser('~/.local/share'),           # lazy Linux (not all set XDG)
        expanduser('~/Library/Application\ Support/'),  # OS X
    ]

    # search for an existing, appropriate location
    for _path in paths:
        if isdir(_path):
            return abspath(join(_path, 'cookiecutter', kind))
    # No appropriate location exists; use the fallback
    return fallback


BUILTIN_ABBREVIATIONS = {
    'gh': 'https://github.com/{0}.git',
    'gl': 'https://gitlab.com/{0}.git',
    'bb': 'https://bitbucket.org/{0}',
}

DEFAULT_CONFIG = {
    'cookiecutters_dir': _find_user_data_dir('cookiecutters_dir'),
    'replay_dir': _find_user_data_dir('cookiecutter_replay'),
    'default_context': {},
    'abbreviations': BUILTIN_ABBREVIATIONS,
}


def merge_configs(default, overwrite):
    """Recursively update a dict with the key/value pair of another.

    Dict values that are dictionaries themselves will be updated, whilst
    preserving existing keys.
    """
    new_config = copy.deepcopy(default)

    for k, v in overwrite.items():
        # Make sure to preserve existing items in
        # nested dicts, for example `abbreviations`
        if isinstance(v, dict):
            new_config[k] = merge_configs(default[k], v)
        else:
            new_config[k] = v

    return new_config


def get_config(config_path):
    """Retrieve the config from the specified path, returning a config dict."""
    if not isfile(config_path):
        raise ConfigDoesNotExistException

    logger.debug('config_path is {0}'.format(config_path))
    with io.open(config_path, encoding='utf-8') as file_handle:
        try:
            yaml_dict = poyo.parse_string(file_handle.read())
        except poyo.exceptions.PoyoException as e:
            raise InvalidConfiguration(
                'Unable to parse YAML file {}. Error: {}'
                ''.format(config_path, e)
            )

    config_dict = merge_configs(DEFAULT_CONFIG, yaml_dict)

    # the calls to expanduser/expandvars are only necessary if the User
    # overrides the default location using envvars or '~'
    raw_replay_dir = config_dict['replay_dir']
    config_dict['replay_dir'] = expanduser(expandvars(raw_replay_dir))

    raw_cookies_dir = config_dict['cookiecutters_dir']
    config_dict['cookiecutters_dir'] = expanduser(expandvars(raw_cookies_dir))

    return config_dict


def get_user_config(config_file=None, default_config=False):
    """Return the user config as a dict.

    If ``default_config`` is True, ignore ``config_file`` and return default
    values for the config parameters.

    If a path to a ``config_file`` is given, that is different from the default
    location, load the user config from that.

    Otherwise look up the config file path in the ``COOKIECUTTER_CONFIG``
    environment variable. If set, load the config from this path. This will
    raise an error if the specified path is not valid.

    If the environment variable is not set, try the default config file path
    before falling back to the default config values.
    """
    # Do NOT load a config. Return defaults instead.
    if default_config:
        return copy.copy(DEFAULT_CONFIG)

    # Load the given config file
    if config_file is not None:
        return get_config(config_file)

    try:
        # If the user has a valid COOKIECUTTER_CONFIG set or has placed a
        # config file in a platform appropriate location (defaulting to HOME),
        # this should find it
        found_config_file = _find_user_config()
    except ConfigDoesNotExistException:
        # Otherwise, return the defaults
        return copy.copy(DEFAULT_CONFIG)
    else:
        # There IS a config file. Try to load it
        return get_config(found_config_file)
