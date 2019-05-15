import git
import logging

from .exceptions import InvalidGitRepository, RepositoryNoCKBranch, \
    RepositoryNotCleanError, UpdateException

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


def get_modified_files(repo):
    mod_files = []
    for item in repo.index.diff(None):
        mod_files.append(item.a_path)
    return mod_files


def is_dirty_repo(repo):
    logger.debug("repo has: {} and {}".format(
        repo.is_dirty(), repo.untracked_files))
    return repo.is_dirty() or repo.untracked_files


def commit_changes(repo):
    newfiles = repo.untracked_files

    modified_files = get_modified_files(repo)

    try:
        repo.git.add(newfiles + modified_files)
        logger.debug('files to commit: {}'.format(newfiles + modified_files))
        repo.git.commit(['-m', 'Cookiecutter Update'])
    except git.GitCommandError as e:
        head = 'HEAD'
        if 'commit' in e.command:
            head = 'HEAD^'
        # Simply removing changes added above.
        repo.git.reset('--hard', head)
        msg = 'Error trying to udpate cookiecutter branch, aborting update'
        raise UpdateException(msg, e)

    return repo.head.commit.hexsha


def apply_changes(repo, branch, update_commit):
    try:
        repo.git.cherry_pick(update_commit)
    except git.GitCommandError as e:
        # Rolling back the cherry-pick
        repo.git.reset('--hard', 'HEAD')
        msg = (
            'Cherry-pick failed due to conflicts.\n'
            'To manually finish the update from {}, do:\n'
            '`git cherry-pick {}`'
        ).format(branch, update_commit)
        logger.warning(msg)
        print(msg)


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


def apply_update(repo, branch='master'):
    if not repo.git.diff(None):
        msg = (
            'No update to do',
            'cookiecutter branch already at latest version'
        )
        print(msg)
        repo.git.checkout(branch)
        logger.debug('Move to branch {}'.format(branch))
    else:
        commit_sha = commit_changes(repo)
        repo.git.checkout(branch)
        logger.debug('Move to branch {}'.format(branch))
        apply_changes(repo, branch, commit_sha)
