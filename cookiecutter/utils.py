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
import stat
import shutil
import contextlib
import io

import yaml

from .exceptions import InvalidConfiguration

if sys.version_info[:2] < (2, 7):
    import simplejson as json
    from ordereddict import OrderedDict
else:
    import json
    from collections import OrderedDict


def force_delete(func, path, exc_info):
    """
    Error handler for `shutil.rmtree()` equivalent to `rm -rf`
    Usage: `shutil.rmtree(path, onerror=force_delete)`
    From stackoverflow.com/questions/1889597
    """

    os.chmod(path, stat.S_IWRITE)
    func(path)


def rmtree(path):
    """
    Removes a directory and all its contents. Like rm -rf on Unix.

    :param path: A directory path.
    """

    shutil.rmtree(path, onerror=force_delete)


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


def read_file(filename, encoding='utf-8', mode='r'):
    """
    Read and return the contents of a file

    :param filename: Path to the file to read
    :param encoding: The encoding of the file.
    """
    with io.open(filename, mode=mode, encoding=encoding) as stream:
        return stream.read()


def read_json_file(filename, encoding='utf-8', with_order=False):
    hook = OrderedDict if with_order else None
    return json.loads(
        read_file(filename, encoding=encoding),
        object_pairs_hook=hook
    )


def read_yaml_file(filename, encoding='utf-8'):
    try:
        return yaml.safe_load(read_file(filename, encoding=encoding))
    except yaml.scanner.ScannerError:
        raise InvalidConfiguration(
            "%s is not a valid YAML file" % filename)


def write_file(filename, contents, encoding='utf-8'):
    with io.open(filename, 'w', encoding=encoding) as stream:
        stream.write(contents)
