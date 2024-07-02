"""Test work of python and shell hooks on repository."""

import sys
from pathlib import Path

import pytest

from cookiecutter import hooks, utils
from cookiecutter.exceptions import FailedHookException

WINDOWS = sys.platform.startswith('win')


@pytest.fixture(scope='function')
def remove_tmp_repo_dir():
    """Remove the generate repo_dir."""

    def _func(repo_dir: Path) -> None:
        if repo_dir.exists():
            utils.rmtree(repo_dir)

    return _func


def test_run_pre_prompt_python_hook(remove_tmp_repo_dir) -> None:
    """Verify pre_prompt.py runs and creates a copy of cookiecutter.json."""
    new_repo_dir = hooks.run_pre_prompt_hook(repo_dir='tests/test-pyhooks/')
    assert new_repo_dir.exists()  # type: ignore[union-attr]
    bkp_config = new_repo_dir / "_cookiecutter.json"  # type: ignore[operator]
    assert bkp_config.exists()
    remove_tmp_repo_dir(new_repo_dir)


def test_run_pre_prompt_python_hook_fail(monkeypatch) -> None:
    """Verify pre_prompt.py will fail when a given env var is present."""
    message = 'Pre-Prompt Hook script failed'
    with monkeypatch.context() as m:
        m.setenv('COOKIECUTTER_FAIL_PRE_PROMPT', '1')
        with pytest.raises(FailedHookException) as excinfo:
            hooks.run_pre_prompt_hook(repo_dir='tests/test-pyhooks/')
    assert message in str(excinfo.value)


@pytest.mark.skipif(WINDOWS, reason='shell script will not run in Windows')
def test_run_pre_prompt_shell_hook(remove_tmp_repo_dir) -> None:
    """Verify pre_prompt.sh runs and creates a copy of cookiecutter.json."""
    new_repo_dir = hooks.run_pre_prompt_hook(repo_dir='tests/test-pyshellhooks/')
    assert new_repo_dir.exists()  # type: ignore[union-attr]
    bkp_config = new_repo_dir / "_cookiecutter.json"  # type: ignore[operator]
    assert bkp_config.exists()
    remove_tmp_repo_dir(new_repo_dir)
