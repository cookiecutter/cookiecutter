# -*- coding: utf-8 -*-

"""Helper functions for working with version control systems."""

from __future__ import unicode_literals
import logging
import os
import subprocess

try:
    from shutil import which
except ImportError:
    from whichcraft import which

from cookiecutter.exceptions import (
    RepositoryNotFound,
    RepositoryCloneFailed,
    UnknownRepoType,
    VCSNotInstalled,
)
from cookiecutter.utils import make_sure_path_exists, prompt_and_delete

logger = logging.getLogger(__name__)


BRANCH_ERRORS = [
    'error: pathspec',
    'unknown revision',
]


def identify_repo(repo_url):
    """Determine if `repo_url` should be treated as a URL to a git or hg repo.

    Repos can be identified by prepending "hg+" or "git+" to the repo URL.

    :param repo_url: Repo URL of unknown type.
    :returns: ('git', repo_url), ('hg', repo_url), or None.
    """
    repo_url_values = repo_url.split('+')
    if len(repo_url_values) == 2:
        repo_type = repo_url_values[0]
        if repo_type in ["git", "hg"]:
            return repo_type, repo_url_values[1]
        else:
            raise UnknownRepoType
    else:
        if 'git' in repo_url:
            return 'git', repo_url
        elif 'bitbucket' in repo_url:
            return 'hg', repo_url
        else:
            raise UnknownRepoType


def is_vcs_installed(repo_type):
    """
    Check if the version control system for a repo type is installed.

    :param repo_type:
    """
    return bool(which(repo_type))


def clone(repo_url, checkout=None, clone_to_dir='.', no_input=False):
    """Clone a repo to the current directory.

    :param repo_url: Repo URL of unknown type.
    :param checkout: The branch, tag or commit ID to checkout after clone.
    :param clone_to_dir: The directory to clone to.
                         Defaults to the current directory.
    :param no_input: Suppress all user prompts when calling via API.
    :returns: str with path to the new directory of the repository.
    """
    # Ensure that clone_to_dir exists
    clone_to_dir = os.path.expanduser(clone_to_dir)
    make_sure_path_exists(clone_to_dir)

    # identify the repo_type
    repo_type, repo_url = identify_repo(repo_url)

    # check that the appropriate VCS for the repo_type is installed
    if not is_vcs_installed(repo_type):
        msg = "'{0}' is not installed.".format(repo_type)
        raise VCSNotInstalled(msg)

    repo_url = repo_url.rstrip('/')
    repo_name = os.path.split(repo_url)[1]
    if repo_type == 'git':
        repo_name = repo_name.split(':')[-1].rsplit('.git')[0]
        repo_dir = os.path.normpath(os.path.join(clone_to_dir, repo_name))
    elif repo_type == 'hg':
        repo_dir = os.path.normpath(os.path.join(clone_to_dir, repo_name))
    logger.debug('repo_dir is {0}'.format(repo_dir))

    if os.path.isdir(repo_dir):
        clone = prompt_and_delete(repo_dir, no_input=no_input)
    else:
        clone = True

    if clone:
        try:
            subprocess.check_output(
                [repo_type, 'clone', repo_url],
                cwd=clone_to_dir,
                stderr=subprocess.STDOUT,
            )
            if checkout is not None:
                subprocess.check_output(
                    [repo_type, 'checkout', checkout],
                    cwd=repo_dir,
                    stderr=subprocess.STDOUT,
                )
        except subprocess.CalledProcessError as clone_error:
            output = clone_error.output.decode('utf-8')
            if 'not found' in output.lower():
                raise RepositoryNotFound(
                    'The repository {} could not be found, '
                    'have you made a typo?'.format(repo_url)
                )
            if any(error in output for error in BRANCH_ERRORS):
                raise RepositoryCloneFailed(
                    'The {} branch of repository {} could not found, '
                    'have you made a typo?'.format(checkout, repo_url)
                )
            raise

    return repo_dir
