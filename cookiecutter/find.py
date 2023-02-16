"""Functions for finding Cookiecutter templates and other components."""
import logging
import os
from pathlib import Path

from cookiecutter.exceptions import NonTemplatedInputDirException

logger = logging.getLogger(__name__)


def find_templates(repo_dir: "os.PathLike[str]") -> list[Path]:
    """Determine which child directories of ``repo_dir`` is a project template.

    :param repo_dir: Local directory of newly cloned repo.
    :return: List of relative path to project templates.
    """
    logger.debug('Searching %s for the project templates.', repo_dir)

    project_templates = []
    for str_path in os.listdir(repo_dir):
        if 'cookiecutter' in str_path and '{{' in str_path and '}}' in str_path:
            project_templates.append(Path(repo_dir, str_path))

    if not project_templates:
        raise NonTemplatedInputDirException

    logger.debug('The project templates appears to be {}'.format(project_templates))
    return project_templates
