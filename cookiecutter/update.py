import git
import logging

from .exceptions import InvalidGitRepository, RepositoryNoCKBranch, \
    RepositoryNotCleanError

DEFAULT_CK_BRANCH = 'cookiecutter'

logger = logging.getLogger(__name__)


def is_ck_branch(repo, ck_branch=DEFAULT_CK_BRANCH):
    for br in repo.branches:
        if br.name == DEFAULT_CK_BRANCH:
            return True
    return False


# Get git repo object from path
def get_repo(repo_path):
    try:
        repo = git.Repo(repo_path)
    except git.exc.InvalidGitRepositoryError as e:
        msg = 'Repository is not a git repo'
        raise InvalidGitRepository(msg, e)
    return repo


def is_dirty_repo(repo):
    logger.debug("repo has: {} and {}".format(
        repo.is_dirty(), repo.untracked_files))
    return repo.is_dirty() or repo.untracked_files


def prepare_update(repo_path, ck_branch=DEFAULT_CK_BRANCH):
    repo = get_repo(repo_path)

    if not is_ck_branch(repo, ck_branch):
        msg = 'Missing cookiecutter branch: {}'.format(ck_branch)
        raise RepositoryNoCKBranch(msg)

    # Only update clean repository.
    if is_dirty_repo(repo):
        msg = 'Repo {} is dirty, clean it before updating'.format(repo)
        raise RepositoryNotCleanError(msg)

    # Changing the HEAD is necessary to update a branch were only
    # cookiecutter changes resides.
    repo.git.checkout(ck_branch)
    logger.debug('Move to branch {}'.format(ck_branch))

    return repo
