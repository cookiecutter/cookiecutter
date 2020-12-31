"""Functions for finding Cookiecutter templates and other components."""
import logging
import os
import re

from cookiecutter import exceptions

logger = logging.getLogger(__name__)

_REGEX = r'{{.*cookiecutter.*}}'


def find_template(repo_dir):
    """Determine which child directory of `repo_dir` is the project template.

    :param repo_dir: Local directory of newly cloned repo.
    :returns project_template: Relative path to project template.
    """
    logger.debug('Searching %s for the project template.', repo_dir)
    candidates = []
    with os.scandir(repo_dir) as it:
        for entry in it:
            if not entry.is_dir():
                continue
            if re.search(_REGEX, entry.name):
                candidates.append(entry)
    if not candidates:
        raise exceptions.NonTemplatedInputDirException
    if len(candidates) > 1:
        raise exceptions.UnknownTemplateDirException
    entry, = candidates
    logger.debug('The project template appears to be %s', entry.path)
    return entry.path
