"""Functions for finding Cookiecutter templates and other components."""
import logging
from pathlib import Path

from cookiecutter.exceptions import NonTemplatedInputDirException

logger = logging.getLogger(__name__)


def find_template(repo_dir):
    """Determine which child directory of `repo_dir` is the project template.

    :param repo_dir: Local directory of newly cloned repo.
    :returns project_template: Relative path to project template.
    """
    logger.debug('Searching %s for the project template.', repo_dir)

    repo_dir_contents = Path(repo_dir).iterdir()

    project_template = None
    for item in repo_dir_contents:
        item = str(item)
        if 'cookiecutter' in item and '{{' in item and '}}' in item:
            project_template = item
            break

    if project_template:
        logger.debug('The project template appears to be %s', project_template)
        return project_template
    else:
        raise NonTemplatedInputDirException
