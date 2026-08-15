"""Global configuration handling."""

from __future__ import annotations

import collections
import copy
import logging
import os
from typing import TYPE_CHECKING, Any

import yaml

from cookiecutter.exceptions import ConfigDoesNotExistException, InvalidConfiguration

if TYPE_CHECKING:
    from pathlib import Path

logger = logging.getLogger(__name__)

USER_CONFIG_PATH = os.path.expanduser('~/.cookiecutterrc')

# The locations Cookiecutter used before it followed the XDG Base Directory
# specification. They are kept only to migrate existing installs; the defaults
# now live under the XDG cache and data directories below.
LEGACY_COOKIECUTTERS_DIR = '~/.cookiecutters'
LEGACY_REPLAY_DIR = '~/.cookiecutter_replay'

BUILTIN_ABBREVIATIONS = {
    'gh': 'https://github.com/{0}.git',
    'gl': 'https://gitlab.com/{0}.git',
    'bb': 'https://bitbucket.org/{0}',
}


def xdg_dir(env_var: str, fallback: str, subdir: str) -> str:
    """Return the path for ``subdir`` under an XDG base directory.

    Honors ``env_var`` (e.g. ``XDG_CACHE_HOME``) when it is set and falls back
    to the default from the XDG Base Directory specification otherwise, e.g.
    ``~/.cache`` for ``XDG_CACHE_HOME``.
    """
    base = os.environ.get(env_var) or os.path.expanduser(fallback)
    return os.path.join(base, subdir)


DEFAULT_CONFIG = {
    'cookiecutters_dir': xdg_dir('XDG_CACHE_HOME', '~/.cache', 'cookiecutter'),
    'replay_dir': xdg_dir('XDG_DATA_HOME', '~/.local/share', 'cookiecutter'),
    'default_context': collections.OrderedDict([]),
    'abbreviations': BUILTIN_ABBREVIATIONS,
}


def _expand_path(path: str) -> str:
    """Expand both environment variables and user home in the given path."""
    path = os.path.expandvars(path)
    return os.path.expanduser(path)


def _migrate_default(path: str, legacy: str, label: str) -> str:
    """Return ``path`` unless a legacy install still holds data there.

    One-way migration from the pre-XDG locations: while the legacy directory
    exists and the new default has not been created yet, keep using the legacy
    directory so existing users are not stranded by the move.
    """
    legacy_path = os.path.expanduser(legacy)
    if os.path.isdir(legacy_path) and not os.path.isdir(path):
        logger.info(
            "Using legacy %s directory %s. Move it to %s or set the %r "
            'setting in your config to migrate to the XDG location.',
            label,
            legacy_path,
            path,
            label,
        )
        return legacy_path
    return path


def _expand_or_migrate(value: str, legacy: str, label: str) -> str:
    """Expand ``value``, migrating from the legacy location when applicable.

    The migration only applies while ``value`` is still the built-in default,
    i.e. the user did not override the setting in their config.
    """
    expanded = _expand_path(value)
    if value == DEFAULT_CONFIG[label]:
        return _migrate_default(expanded, legacy, label)
    return expanded


def _default_config() -> dict[str, Any]:
    """Return a copy of the default config with legacy directories migrated."""
    config_dict = copy.copy(DEFAULT_CONFIG)
    config_dict['replay_dir'] = _migrate_default(
        config_dict['replay_dir'], LEGACY_REPLAY_DIR, 'replay_dir'
    )
    config_dict['cookiecutters_dir'] = _migrate_default(
        config_dict['cookiecutters_dir'],
        LEGACY_COOKIECUTTERS_DIR,
        'cookiecutters_dir',
    )
    return config_dict


def merge_configs(default: dict[str, Any], overwrite: dict[str, Any]) -> dict[str, Any]:
    """Recursively update a dict with the key/value pair of another.

    Dict values that are dictionaries themselves will be updated, whilst
    preserving existing keys.
    """
    new_config = copy.deepcopy(default)

    for k, v in overwrite.items():
        # Make sure to preserve existing items in
        # nested dicts, for example `abbreviations`
        if isinstance(v, dict):
            new_config[k] = merge_configs(default.get(k, {}), v)
        else:
            new_config[k] = v

    return new_config


def get_config(config_path: Path | str) -> dict[str, Any]:
    """Retrieve the config from the specified path, returning a config dict."""
    if not os.path.exists(config_path):
        msg = f'Config file {config_path} does not exist.'
        raise ConfigDoesNotExistException(msg)

    logger.debug('config_path is %s', config_path)
    with open(config_path, encoding='utf-8') as file_handle:
        try:
            yaml_dict = yaml.safe_load(file_handle) or {}
        except yaml.YAMLError as e:
            msg = f'Unable to parse YAML file {config_path}.'
            raise InvalidConfiguration(msg) from e
        if not isinstance(yaml_dict, dict):
            msg = f'Top-level element of YAML file {config_path} should be an object.'
            raise InvalidConfiguration(msg)

    config_dict = merge_configs(DEFAULT_CONFIG, yaml_dict)

    config_dict['replay_dir'] = _expand_or_migrate(
        config_dict['replay_dir'], LEGACY_REPLAY_DIR, 'replay_dir'
    )

    config_dict['cookiecutters_dir'] = _expand_or_migrate(
        config_dict['cookiecutters_dir'],
        LEGACY_COOKIECUTTERS_DIR,
        'cookiecutters_dir',
    )

    return config_dict


def get_user_config(
    config_file: str | None = None,
    default_config: bool | dict[str, Any] = False,
) -> dict[str, Any]:
    """Return the user config as a dict.

    If ``default_config`` is True, ignore ``config_file`` and return default
    values for the config parameters.

    If ``default_config`` is a dict, merge values with default values and return them
    for the config parameters.

    If a path to a ``config_file`` is given, that is different from the default
    location, load the user config from that.

    Otherwise look up the config file path in the ``COOKIECUTTER_CONFIG``
    environment variable. If set, load the config from this path. This will
    raise an error if the specified path is not valid.

    If the environment variable is not set, try the default config file path
    before falling back to the default config values.
    """
    # Do NOT load a config. Merge provided values with defaults and return them instead
    if default_config and isinstance(default_config, dict):
        return merge_configs(DEFAULT_CONFIG, default_config)

    # Do NOT load a config. Return defaults instead.
    if default_config:
        logger.debug("Force ignoring user config with default_config switch.")
        return _default_config()

    # Load the given config file
    if config_file and config_file is not USER_CONFIG_PATH:
        logger.debug("Loading custom config from %s.", config_file)
        return get_config(config_file)

    try:
        # Does the user set up a config environment variable?
        env_config_file = os.environ['COOKIECUTTER_CONFIG']
    except KeyError:
        # Load an optional user config if it exists
        # otherwise return the defaults
        if os.path.exists(USER_CONFIG_PATH):
            logger.debug("Loading config from %s.", USER_CONFIG_PATH)
            return get_config(USER_CONFIG_PATH)
        logger.debug("User config not found. Loading default config.")
        return _default_config()
    else:
        # There is a config environment variable. Try to load it.
        # Do not check for existence, so invalid file paths raise an error.
        logger.debug("User config not found or not specified. Loading default config.")
        return get_config(env_config_file)
