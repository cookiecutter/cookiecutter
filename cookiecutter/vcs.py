"""Helper functions for working with version control systems."""
import logging
import os
import subprocess
from shutil import (
    which,
    move,
)
import sys
import tempfile

from cookiecutter.exceptions import (
    RepositoryCloneFailed,
    RepositoryNotFound,
    UnknownRepoType,
    VCSNotInstalled,
)
from cookiecutter.utils import (
    make_sure_path_exists,
    prompt_ok_to_delete,
    prompt_ok_to_reuse,
    rmtree,
)

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

    if _need_to_clone(repo_dir, no_input):
        _delete_old_and_clone_new(
            repo_dir, repo_url, repo_type, clone_to_dir, checkout,
        )
    return repo_dir


def _need_to_clone(repo_dir, no_input):
    ok_to_delete = prompt_ok_to_delete(repo_dir, no_input=no_input)

    if ok_to_delete:
        ok_to_reuse = False
    else:
        ok_to_reuse = prompt_ok_to_reuse(repo_dir, no_input=no_input)

    if not ok_to_delete and not ok_to_reuse:
        sys.exit()

    need_to_clone = ok_to_delete and not ok_to_reuse
    return need_to_clone


def _delete_old_and_clone_new(repo_dir, repo_url, repo_type, clone_to_dir, checkout):
    with tempfile.TemporaryDirectory() as tmp_dir:
        backup_performed = os.path.exists(repo_dir)
        if backup_performed:
            backup_dir = os.path.join(tmp_dir, os.path.basename(repo_dir))
            _backup_and_delete_repo(repo_dir, backup_dir)

        try:
            _clone_repo(repo_dir, repo_url, repo_type, clone_to_dir, checkout)
        except subprocess.CalledProcessError as clone_error:
            if backup_performed:
                _restore_old_repo(repo_dir, backup_dir)
            _handle_clone_error(clone_error, repo_url, checkout)


def _clone_repo(repo_dir, repo_url, repo_type, clone_to_dir, checkout):
    subprocess.check_output(
        [repo_type, 'clone', repo_url], cwd=clone_to_dir, stderr=subprocess.STDOUT,
    )
    if checkout is not None:
        subprocess.check_output(
            [repo_type, 'checkout', checkout], cwd=repo_dir, stderr=subprocess.STDOUT,
        )


def _handle_clone_error(clone_error, repo_url, checkout):
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


def _backup_and_delete_repo(path, backup_path):
    logger.info('Backing up repo {} to {}'.format(path, backup_path))
    move(path, backup_path)
    logger.info('Moving repo {} to {}'.format(path, backup_path))


def _restore_old_repo(path, backup_path):
    try:
        rmtree(path)
        logger.info('Cleaning {}'.format(path))
    except FileNotFoundError:
        pass

    logger.info('Restoring backup repo {}'.format(backup_path))
    move(backup_path, path)
    logger.info('Restored {} successfully'.format(path))
