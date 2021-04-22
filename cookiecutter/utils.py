"""Helper functions used throughout Cookiecutter."""
import contextlib
import errno
import logging
import os
import shutil
import stat
import sys

from cookiecutter.prompt import read_user_yes_no

logger = logging.getLogger(__name__)


def force_delete(func, path, exc_info):
    """Error handler for `shutil.rmtree()` equivalent to `rm -rf`.

    Usage: `shutil.rmtree(path, onerror=force_delete)`
    From https://docs.python.org/3/library/shutil.html#rmtree-example
    """
    os.chmod(path, stat.S_IWRITE)
    func(path)


def rmtree(path):
    """Remove a directory and all its contents. Like rm -rf on Unix.

    :param path: A directory path.
    """
    shutil.rmtree(path, onerror=force_delete)


def make_sure_path_exists(path):
    """Ensure that a directory exists.

    :param path: A directory path.
    """
    logger.debug('Making sure path exists: %s', path)
    try:
        os.makedirs(path)
        logger.debug('Created directory at: %s', path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            return False
    return True


@contextlib.contextmanager
def work_in(dirname=None):
    """Context manager version of os.chdir.

    When exited, returns to the working directory prior to entering.
    """
    curdir = os.getcwd()
    try:
        if dirname is not None:
            os.chdir(dirname)
        yield
    finally:
        os.chdir(curdir)


def make_executable(script_path):
    """Make `script_path` executable.

    :param script_path: The file to change
    """
    status = os.stat(script_path)
    os.chmod(script_path, status.st_mode | stat.S_IEXEC)


def prompt_and_delete(path, no_input=False):
    """
    Ask user if it's okay to delete the previously-downloaded file/directory.

    If yes, delete it. If no, checks to see if the old version should be
    reused. If yes, it's reused; otherwise, Cookiecutter exits.

    :param path: Previously downloaded zipfile.
    :param no_input: Suppress prompt to delete repo and just delete it.
    :return: True if the content was deleted
    """
    # Suppress prompt if called via API
    if no_input:
        ok_to_delete = True
    else:
        question = (
            "You've downloaded {} before. Is it okay to delete and re-download it?"
        ).format(path)

        ok_to_delete = read_user_yes_no(question, 'yes')

    if ok_to_delete:
        if os.path.isdir(path):
            rmtree(path)
        else:
            os.remove(path)
        return True
    else:
        ok_to_reuse = read_user_yes_no(
            "Do you want to re-use the existing version?", 'yes'
        )

        if ok_to_reuse:
            return False

        sys.exit()
