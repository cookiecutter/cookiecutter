#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
cookiecutter.utils
------------------

Helper functions used throughout Cookiecutter.
"""

from __future__ import unicode_literals
import errno
import logging
import os
import sys
import contextlib


if sys.version_info[:2] < (2, 7):
    import simplejson as json
    from ordereddict import OrderedDict
else:
    import json
    from collections import OrderedDict


PY3 = sys.version > '3'
if PY3:
    pass
else:
    import codecs


def make_sure_path_exists(path):
    """
    Ensures that a directory exists.
    :param path: A directory path.
    """
    logging.debug("Making sure path exists: {0}".format(path))
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            return False
    return True


def unicode_open(filename, *args, **kwargs):
    """
    Opens a file as usual on Python 3, and with UTF-8 encoding on Python 2.
    :param filename: Name of file to open.
    """
    kwargs['encoding'] = "utf-8"
    if PY3:
        return open(filename, *args, **kwargs)
    return codecs.open(filename, *args, **kwargs)


def read_json_file(filename):
    """
    Opens and reads a UTF-8 encoded JSON file.
    :param filename: Name of JSON file to open.
    """
    with unicode_open(filename) as file_handle:
        return json.load(file_handle, encoding='utf-8',
                         object_pairs_hook=OrderedDict)


@contextlib.contextmanager
def work_in(dirname=None):
    """
    Context manager version of os.chdir. When exited, returns to the working
    directory prior to entering.
    """
    curdir = os.getcwd()
    try:
        if dirname is not None:
            os.chdir(dirname)
        yield
    finally:
        os.chdir(curdir)
