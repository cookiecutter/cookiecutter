"""Functions for finding Cookiecutter templates and other components."""
import logging
import os
from pathlib import Path

from cookiecutter.exceptions import NonTemplatedInputDirException

logger = logging.getLogger(__name__)


def find_template(
    repo_dir: "os.PathLike[str]",
    block_start_string: str = "{{",
    block_end_string: str = "}}",
) -> Path:
    """Determine which child directory of ``repo_dir`` is the project template.

    :param repo_dir: Local directory of newly cloned repo.
    :param block_start_string: Jinja2 block start string.
    :param block_end_string: Jinja2 block end string.
    :return: Relative path to project template.
    """
    logger.debug('Searching %s for the project template.', repo_dir)

    for str_path in os.listdir(repo_dir):
        if (
            'cookiecutter' in str_path
            and block_start_string in str_path
            and block_end_string in str_path
        ):
            project_template = Path(repo_dir, str_path)
            break
    else:
        raise NonTemplatedInputDirException

    logger.debug('The project template appears to be %s', project_template)
    return project_template
