"""Functions for finding Cookiecutter templates and other components."""
import logging
import os
from pathlib import Path
from typing import Dict

from cookiecutter.exceptions import NonTemplatedInputDirException

logger = logging.getLogger(__name__)


def find_template(repo_dir: "os.PathLike[str]", context: Dict) -> Path:
    """Determine which child directory of ``repo_dir`` is the project template.

    :param repo_dir: Local directory of newly cloned repo.
    :return: Relative path to project template.
    """
    logger.debug('Searching %s for the project template.', repo_dir)

    envvars = context.get('cookiecutter', {}).get('_jinja2_env_vars', {})

    variable_start_string = envvars.get(
        'variable_start_string', '{{'
    )  # {{ is the default jinja variable_start_string
    variable_end_string = envvars.get(
        'variable_end_string', '}}'
    )  # }} is the default jinja variable_end_string

    for str_path in os.listdir(repo_dir):
        if (
            'cookiecutter' in str_path
            and variable_start_string in str_path
            and variable_end_string in str_path
        ):
            project_template = Path(repo_dir, str_path)
            break
    else:
        raise NonTemplatedInputDirException

    logger.debug('The project template appears to be %s', project_template)
    return project_template
