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

BUILTIN_ABBREVIATIONS = {
    'gh': 'https://github.com/{0}.git',
    'gl': 'https://gitlab.com/{0}.git',
    'bb': 'https://bitbucket.org/{0}',
}

DEFAULT_CONFIG = {
    'cookiecutters_dir': os.path.expanduser('~/.cookiecutters/'),
    'replay_dir': os.path.expanduser('~/.cookiecutter_replay/'),
    'default_context': collections.OrderedDict([]),
    'abbreviations': BUILTIN_ABBREVIATIONS,
}


class CookiecutterConfig:
    """Encapsulates configuration loading and merging logic for Cookiecutter.

    This class is responsible for loading a YAML configuration file,
    validating its contents, merging it with default values, and
    expanding any paths contained within it.
    """

    def __init__(self, config_path: Path | str) -> None:
        """Initialize CookiecutterConfig with a path to a YAML config file.

        :param config_path: Path to the YAML configuration file.
        """
        self.config_path = config_path

    def load(self) -> dict[str, Any]:
        """Load, validate and return config dict from the config file path.

        Reads the YAML config file, merges it with default configuration
        values, and expands any directory paths found in the config.

        :raises ConfigDoesNotExistException: If the config file does not exist.
        :raises InvalidConfiguration: If the YAML file cannot be parsed or
            its top-level element is not a dictionary.
        :returns: dict containing the merged configuration values.
        """
        if not os.path.exists(self.config_path):
            msg = f'Config file {self.config_path} does not exist.'
            raise ConfigDoesNotExistException(msg)

        logger.debug('config_path is %s', self.config_path)
        with open(self.config_path, encoding='utf-8') as file_handle:
            try:
                yaml_dict = yaml.safe_load(file_handle) or {}
            except yaml.YAMLError as e:
                msg = f'Unable to parse YAML file {self.config_path}.'
                raise InvalidConfiguration(msg) from e

            if not isinstance(yaml_dict, dict):
                msg = (
                    f'Top-level element of YAML file {self.config_path} '
                    'should be an object.'
                )
                raise InvalidConfiguration(msg)

        # Merge loaded yaml with default config values
        config_dict = merge_configs(DEFAULT_CONFIG, yaml_dict)

        # Expand paths to handle ~ and environment variables
        config_dict['replay_dir'] = _expand_path(config_dict['replay_dir'])
        config_dict['cookiecutters_dir'] = _expand_path(
            config_dict['cookiecutters_dir']
        )

        return config_dict


def _expand_path(path: str) -> str:
    """Expand both environment variables and user home in the given path."""
    path = os.path.expandvars(path)
    return os.path.expanduser(path)


def merge_configs(
    default: dict[str, Any],
    overwrite: dict[str, Any],
) -> dict[str, Any]:
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
    return CookiecutterConfig(config_path).load()


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
        return copy.copy(DEFAULT_CONFIG)

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
        return copy.copy(DEFAULT_CONFIG)
    else:
        # There is a config environment variable. Try to load it.
        # Do not check for existence, so invalid file paths raise an error.
        logger.debug(
            "User config not found or not specified. Loading default config."
        )
        return get_config(env_config_file)