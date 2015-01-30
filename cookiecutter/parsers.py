# -*- coding: utf-8 -*-

import logging
import yaml
import json
import os.path

from collections import OrderedDict

from .utils import work_in
from .exceptions import ParsingError, ContextDecodingException


DEFAULT_CONFIG_BASE = 'cookiecutter'


def ordered_load(stream, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
    class OrderedLoader(Loader):
        pass

    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))
    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)
    return yaml.load(stream, OrderedLoader)


def load_from_yaml(fh):
    try:
        obj = ordered_load(fh, yaml.SafeLoader)
    except yaml.scanner.ScannerError as e:
        # YAML parsing error.  Let's throw a normalized exception
        # to be catched upwards.
        raise ParsingError(
            'line {0}: {1}'.format(
                e.problem_mark.line,
                e.problem))
    if "context" in obj and isinstance(obj["context"], dict):
        return {"__meta__": obj["context"]}
    return obj


def load_from_json(fh):
    try:
        obj = json.load(fh, object_pairs_hook=OrderedDict)
    except ValueError as e:
        # JSON parsing error.  Let's throw a normalized exception
        # to be catched upwards.
        raise ParsingError(str(e))
    return obj


PARSERS = [
    ('yml', ("YAML", load_from_yaml)),
    ('json', ("JSON", load_from_json)),
]


def find_cfg_file(repo_dir):
    with work_in(repo_dir):
        for ext, _ in PARSERS:
            fname = "%s.%s" % (DEFAULT_CONFIG_BASE, ext)
            if os.path.exists(fname):
                logging.debug('Found %s.', fname)
                return os.path.abspath(fname)
    return False


def load_context_from_file(context_file):
    """Load given file"""

    ext = context_file.rsplit(".", 1)[-1]
    parsers = dict(PARSERS)
    if ext not in parsers:
        raise ValueError(
            "Unknown file extension %r for config file."
            % ext)
    fmt_identifier, parser = parsers[ext]

    try:
        with open(context_file) as fh:
            return parser(fh)
    except ParsingError as e:
        # JSON decoding error.  Let's throw a new exception that is more
        # friendly for the developer or user.
        full_fpath = os.path.abspath(context_file)
        exc_message = str(e)
        our_exc_message = (
            '{0} Decoding error while loading "{1}".  Decoding'
            ' error details: "{2}"'.format(
                fmt_identifier, full_fpath, exc_message))
        raise ContextDecodingException(our_exc_message)
