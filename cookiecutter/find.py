"""Functions for finding Cookiecutter templates and other components."""
import logging
import os
from pathlib import Path

from cookiecutter.exceptions import NonTemplatedInputDirException
from pymonad.effects import Effect

logger = logging.getLogger(__name__)


def find_template(repo_dir: "os.PathLike[str]") -> Effect:
    """Determine which child directory of ``repo_dir`` is the project template.

    :param repo_dir: Local directory of newly cloned repo.
    :return: Effect representing the relative path to the project template.
    """
    def search_template():
        logger.debug('Searching %s for the project template.', repo_dir)

        for str_path in os.listdir(repo_dir):
            if 'cookiecutter' in str_path and '{{' in str_path and '}}' in str_path:
                project_template = Path(repo_dir, str_path)
                return project_template

        raise NonTemplatedInputDirException

    return Effect(search_template).map(lambda project_template: (
        logger.debug('The project template appears to be %s', project_template),
        project_template
    ))
