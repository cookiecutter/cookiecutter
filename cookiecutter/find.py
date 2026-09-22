"""Functions for finding Cookiecutter templates and other components."""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import TYPE_CHECKING

from cookiecutter.exceptions import NonTemplatedInputDirException

if TYPE_CHECKING:
    from jinja2 import Environment

logger = logging.getLogger(__name__)


def find_template(repo_dir: Path | str, env: Environment) -> Path:
    """Determine which child directory of ``repo_dir`` is the project template.

    :param repo_dir: Local directory of newly cloned repo.
    :return: Relative path to project template.
    """
    logger.debug('Searching %s for the project template.', repo_dir)

    candidates = []
    for str_path in sorted(os.listdir(repo_dir)):
        path = Path(repo_dir, str_path)
        if (
            'cookiecutter' in str_path
            and env.variable_start_string in str_path
            and env.variable_end_string in str_path
            and path.is_dir()
        ):
            candidates.append(path)

    if len(candidates) > 1 and Path(repo_dir, 'cookiecutter.json').is_file():
        # A repository may contain multiple sibling template directories. In
        # that layout the repository itself is the template root.
        project_template = Path(repo_dir)
    elif candidates:
        project_template = candidates[0]
    else:
        raise NonTemplatedInputDirException

    logger.debug('The project template appears to be %s', project_template)
    return project_template
