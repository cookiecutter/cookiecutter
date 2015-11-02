# -*- coding: utf-8 -*-

import re

VALUE = r"(?P<quotes>['\"]?)(?P<value>.*)(?P=quotes)$"
SIMPLE = r"^(?P<variable>\w+): " + VALUE

NESTED = r"^(?P<variable>\w+):\s((?:^\s.+$\n)+)"
NESTED_VAR = r"^\s+(?P<variable>\w+): " + VALUE


def find_simple(config_str):
    """Find all matches for non-nested config variables in config_str.

    Examples:
        cookiecutters_dir: "/home/audreyr/my-custom-cookiecutters-dir/"
        replay_dir: "/home/audreyr/my-custom-replay-dir/"
    """
    matches = re.findall(SIMPLE, config_str, re.MULTILINE)
    return {variable: value for variable, quotes, value in matches}


def find_nested(config_str):
    """Find all matches for nested config variables in config_str.

    Examples:
        default_context:
            full_name: "Audrey Roy"
            email: "audreyr@gmail.com"
            github_username: "audreyr"
        abbreviations:
            pp: https://github.com/audreyr/cookiecutter-pypackage.git
            gh: https://github.com/{0}.git
            bb: https://bitbucket.org/{0}
    """
    config = {}
    nested_variables = re.findall(NESTED, config_str, re.MULTILINE)

    for variable, text in nested_variables:
        matches = re.findall(NESTED_VAR, text, re.MULTILINE)
        config[variable] = {key: value for key, quotes, value in matches}

    return config


def loads(config_str):
    """Deserialize the given config_str to a Python dict."""
    config = {}
    config.update(find_simple(config_str))
    config.update(find_nested(config_str))
    return config
