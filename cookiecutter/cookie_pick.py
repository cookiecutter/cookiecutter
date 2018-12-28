# -*- coding: utf-8 -*-

"""
cookiecutter.generate_cookie_pick
------------------------
"""

from __future__ import unicode_literals

import logging
import os

from git import Repo
from git.exc import GitCommandError, NoSuchPathError
from jinja2 import FileSystemLoader

from .environment import StrictEnvironment
from .find import find_template

COMMIT_INFO_TEMPLATE = "  {}: {} by {} - {}"

logger = logging.getLogger(__name__)


def get_target_directory(repo_dir, context, output_dir, env):
    """Return the rendered target directory"""
    template_dir = find_template(repo_dir)
    unrendered_dir = os.path.split(template_dir)[1]
    name_tmpl = env.from_string(unrendered_dir)
    rendered_dirname = name_tmpl.render(**context)

    return os.path.normpath(
        os.path.join(output_dir, rendered_dirname)
    )


def show_commits(repository):
    """Log the last ten commits in the last month"""
    logger.info("Available commits:")
    for commit in repository.iter_commits(
        '--all',
        max_count=10,
        since='30.days.ago'
    ):
        logger.info(COMMIT_INFO_TEMPLATE.format(
            commit.hexsha,
            commit.committed_datetime,
            commit.committer.name,
            commit.summary
        ))


def generate_cookie_pick(repo_dir, context=None, output_dir='.',
                         cookie_pick=None, cookie_pick_parent=None):
    """Migrate a template change to a target directory

    1. Create a patch based on the source template repository
    2. Render the patchfile using the given context
    3. Apply the patch to the target repository
    """
    logger.debug("Generating patch for {}".format(repo_dir))
    logger.debug("Context: {}".format(context))

    env = StrictEnvironment(
        context=context,
        keep_trailing_newline=True,
    )
    target_dir = get_target_directory(
        repo_dir, context, output_dir, env)
    env.loader = FileSystemLoader(repo_dir)

    source_repo = Repo(repo_dir)

    # show available commits in the source repo
    if cookie_pick == 'list':
        show_commits(source_repo)
        return

    # get commits
    source_commit = source_repo.commit(cookie_pick)
    if cookie_pick_parent:
        target_commit = source_repo.commit(cookie_pick_parent)
    else:
        target_commit = source_commit.parents[0]

    logger.debug("Processing {} -> {}".format(
        source_commit.summary, target_commit.summary
    ))

    # create base patch
    source_patch = source_repo.git.diff([
        target_commit.hexsha,
        source_commit.hexsha,
        '--no-color',
        '-p'
    ])

    # render target patch
    target_patch = env.from_string(source_patch).render(**context)
    patch_file_name = 'cookiecutter_{}_{}.patch'.format(
        source_commit.hexsha,
        target_commit.hexsha
    )
    target_patch_path = os.path.join(target_dir, patch_file_name)

    logger.debug("Writing patch to {}".format(target_patch_path))
    with open(target_patch_path, 'w+') as patch_file:
        patch_file.write(target_patch)
        patch_file.write('\n')

    # target repository
    try:
        target_repo = Repo(target_dir)
    except NoSuchPathError:
        # might not be a repository
        logger.error(
            "{} is not a valid Git repository. "
            "The patchfile was created at {} to apply it manually."
            "".format(target_dir, target_patch_path)
        )
        raise

    try:
        target_repo.git.apply([
            '-p2',
            '--reject',
            '--whitespace=fix',
            patch_file_name
        ])
    except GitCommandError:
        logger.error(
            "The patch at {} could not be applied. "
            "The rejected parts are stored in the target repository at {}."
            "".format(target_patch_path, target_dir)
        )
        raise
    finally:
        os.remove(target_patch_path)
