#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
cookiecutter.utils
------------------

Helper functions used throughout Cookiecutter.
"""

from __future__ import unicode_literals
import contextlib
import errno
import logging
import os
import stat
import shutil


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

    logging.debug('Making sure path exists: {0}'.format(path))
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


def make_executable(script_path):
    """
    Makes `script_path` executable

    :param script_path: The file to change
    """
    status = os.stat(script_path)
    os.chmod(script_path, status.st_mode | stat.S_IEXEC)
