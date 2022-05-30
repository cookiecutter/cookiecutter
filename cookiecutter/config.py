"""Global configuration handling."""
import collections
import copy
import logging
import os

import yaml

from cookiecutter.exceptions import ConfigDoesNotExistException, InvalidConfiguration

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


def _expand_path(path):
    """Expand both environment variables and user home in the given path."""
    path = os.path.expandvars(path)
    path = os.path.expanduser(path)
    return path


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
            new_config[k] = merge_configs(default.get(k, {}), v)
        else:
            new_config[k] = v

    return new_config


def get_config(config_path):
    """Retrieve the config from the specified path, returning a config dict."""
    if not os.path.exists(config_path):
        raise ConfigDoesNotExistException(f'Config file {config_path} does not exist.')

    logger.debug('config_path is %s', config_path)
    with open(config_path, encoding='utf-8') as file_handle:
        try:
            yaml_dict = yaml.safe_load(file_handle)
        except yaml.YAMLError as e:
            raise InvalidConfiguration(
                f'Unable to parse YAML file {config_path}.'
            ) from e

    config_dict = merge_configs(DEFAULT_CONFIG, yaml_dict)

    raw_replay_dir = config_dict['replay_dir']
    config_dict['replay_dir'] = _expand_path(raw_replay_dir)

    raw_cookies_dir = config_dict['cookiecutters_dir']
    config_dict['cookiecutters_dir'] = _expand_path(raw_cookies_dir)

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
        else:
            logger.debug("User config not found. Loading default config.")
            return copy.copy(DEFAULT_CONFIG)
    else:
        # There is a config environment variable. Try to load it.
        # Do not check for existence, so invalid file paths raise an error.
        logger.debug("User config not found or not specified. Loading default config.")
        return get_config(env_config_file)
