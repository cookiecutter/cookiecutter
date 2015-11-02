# -*- coding: utf-8 -*-

import re

VALUE = r"(?P<quotes>['\"]?)(?P<value>.*)(?P=quotes)$"
SIMPLE = r"^(?P<variable>\w+): " + VALUE


def find_simple(config_str):
    """Find all matches for non-nested config variables in config_str.

    Examples:
        cookiecutters_dir: "/home/audreyr/my-custom-cookiecutters-dir/"
        replay_dir: "/home/audreyr/my-custom-replay-dir/"
    """
    matches = re.findall(SIMPLE, config_str, re.MULTILINE)
    return {variable: value for variable, quotes, value in matches}


def loads(config_str):
    """Deserialize the given config_str to a Python dict."""
    config = {}
    return config.update(find_simple(config_str))
