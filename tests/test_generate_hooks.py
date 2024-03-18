"""Test work of python and shell hooks for generated projects."""

import errno
import os
import sys
from pathlib import Path

import pytest

from cookiecutter import generate, utils
from cookiecutter.exceptions import FailedHookException

WINDOWS = sys.platform.startswith('win')


@pytest.fixture(scope='function')
def remove_additional_folders(tmp_path):
    """Remove some special folders which are created by the tests."""
    yield
    directories_to_delete = [
        'tests/test-pyhooks/inputpyhooks',
        'inputpyhooks',
        'inputhooks',
        tmp_path.joinpath('test-shellhooks'),
        'tests/test-hooks',
    ]
    for directory in directories_to_delete:
        if os.path.exists(directory):
            utils.rmtree(directory)


@pytest.mark.usefixtures('clean_system', 'remove_additional_folders')
def test_ignore_hooks_dirs() -> None:
    """Verify hooks directory not created in target location on files generation."""
    generate.generate_files(
        context={'cookiecutter': {'pyhooks': 'pyhooks'}},
        repo_dir='tests/test-pyhooks/',
        output_dir='tests/test-pyhooks/',
    )
    assert not os.path.exists('tests/test-pyhooks/inputpyhooks/hooks')


@pytest.mark.usefixtures('clean_system', 'remove_additional_folders')
def test_run_python_hooks() -> None:
    """Verify pre and post generation python hooks executed and result in output_dir.

    Each hook should create in target directory. Test verifies that these files
    created.
    """
    generate.generate_files(
        context={'cookiecutter': {'pyhooks': 'pyhooks'}},
        repo_dir='tests/test-pyhooks/',
        output_dir='tests/test-pyhooks/',
    )
    assert os.path.exists('tests/test-pyhooks/inputpyhooks/python_pre.txt')
    assert os.path.exists('tests/test-pyhooks/inputpyhooks/python_post.txt')


@pytest.mark.usefixtures('clean_system', 'remove_additional_folders')
def test_run_python_hooks_cwd() -> None:
    """Verify pre and post generation python hooks executed and result in current dir.

    Each hook should create in target directory. Test verifies that these files
    created.
    """
    generate.generate_files(
        context={'cookiecutter': {'pyhooks': 'pyhooks'}}, repo_dir='tests/test-pyhooks/'
    )
    assert os.path.exists('inputpyhooks/python_pre.txt')
    assert os.path.exists('inputpyhooks/python_post.txt')


@pytest.mark.skipif(WINDOWS, reason='OSError.errno=8 is not thrown on Windows')
@pytest.mark.usefixtures('clean_system', 'remove_additional_folders')
def test_empty_hooks() -> None:
    """Verify error is raised on empty hook script. Ignored on windows.

    OSError.errno=8 is not thrown on Windows when the script is empty
    because it always runs through shell instead of needing a shebang.
    """
    with pytest.raises(FailedHookException) as excinfo:
        generate.generate_files(
            context={'cookiecutter': {'shellhooks': 'shellhooks'}},
            repo_dir='tests/test-shellhooks-empty/',
            overwrite_if_exists=True,
        )
    assert 'shebang' in str(excinfo.value)


@pytest.mark.usefixtures('clean_system', 'remove_additional_folders')
def test_oserror_hooks(mocker) -> None:
    """Verify script error passed correctly to cookiecutter error.

    Here subprocess.Popen function mocked, ie we do not call hook script,
    just produce expected error.
    """
    message = 'Out of memory'

    err = OSError(message)
    err.errno = errno.ENOMEM

    prompt = mocker.patch('subprocess.Popen')
    prompt.side_effect = err

    with pytest.raises(FailedHookException) as excinfo:
        generate.generate_files(
            context={'cookiecutter': {'shellhooks': 'shellhooks'}},
            repo_dir='tests/test-shellhooks-empty/',
            overwrite_if_exists=True,
        )
    assert message in str(excinfo.value)


@pytest.mark.usefixtures('clean_system', 'remove_additional_folders')
def test_run_failing_hook_removes_output_directory() -> None:
    """Verify project directory not created or removed if hook failed."""
    repo_path = os.path.abspath('tests/test-hooks/')
    hooks_path = os.path.abspath('tests/test-hooks/hooks')

    hook_dir = os.path.join(repo_path, 'hooks')
    template = os.path.join(repo_path, 'input{{cookiecutter.hooks}}')
    os.mkdir(repo_path)
    os.mkdir(hook_dir)
    os.mkdir(template)

    hook_path = os.path.join(hooks_path, 'pre_gen_project.py')

    with Path(hook_path).open('w') as f:
        f.write("#!/usr/bin/env python\n")
        f.write("import sys; sys.exit(1)\n")

    with pytest.raises(FailedHookException) as excinfo:
        generate.generate_files(
            context={'cookiecutter': {'hooks': 'hooks'}},
            repo_dir='tests/test-hooks/',
            overwrite_if_exists=True,
        )

    assert 'Hook script failed' in str(excinfo.value)
    assert not os.path.exists('inputhooks')


@pytest.mark.usefixtures('clean_system', 'remove_additional_folders')
def test_run_failing_hook_preserves_existing_output_directory() -> None:
    """Verify project directory not removed if exist before hook failed."""
    repo_path = os.path.abspath('tests/test-hooks/')
    hooks_path = os.path.abspath('tests/test-hooks/hooks')

    hook_dir = os.path.join(repo_path, 'hooks')
    template = os.path.join(repo_path, 'input{{cookiecutter.hooks}}')
    os.mkdir(repo_path)
    os.mkdir(hook_dir)
    os.mkdir(template)

    hook_path = os.path.join(hooks_path, 'pre_gen_project.py')

    with Path(hook_path).open('w') as f:
        f.write("#!/usr/bin/env python\n")
        f.write("import sys; sys.exit(1)\n")

    os.mkdir('inputhooks')
    with pytest.raises(FailedHookException) as excinfo:
        generate.generate_files(
            context={'cookiecutter': {'hooks': 'hooks'}},
            repo_dir='tests/test-hooks/',
            overwrite_if_exists=True,
        )

    assert 'Hook script failed' in str(excinfo.value)
    assert os.path.exists('inputhooks')


@pytest.mark.skipif(sys.platform.startswith('win'), reason="Linux only test")
@pytest.mark.usefixtures('clean_system', 'remove_additional_folders')
def test_run_shell_hooks(tmp_path) -> None:
    """Verify pre and post generate project shell hooks executed.

    This test for .sh files.
    """
    generate.generate_files(
        context={'cookiecutter': {'shellhooks': 'shellhooks'}},
        repo_dir='tests/test-shellhooks/',
        output_dir=tmp_path.joinpath('test-shellhooks'),
    )
    shell_pre_file = tmp_path.joinpath(
        'test-shellhooks', 'inputshellhooks', 'shell_pre.txt'
    )
    shell_post_file = tmp_path.joinpath(
        'test-shellhooks', 'inputshellhooks', 'shell_post.txt'
    )
    assert shell_pre_file.exists()
    assert shell_post_file.exists()


@pytest.mark.skipif(not sys.platform.startswith('win'), reason="Win only test")
@pytest.mark.usefixtures('clean_system', 'remove_additional_folders')
def test_run_shell_hooks_win(tmp_path) -> None:
    """Verify pre and post generate project shell hooks executed.

    This test for .bat files.
    """
    generate.generate_files(
        context={'cookiecutter': {'shellhooks': 'shellhooks'}},
        repo_dir='tests/test-shellhooks-win/',
        output_dir=tmp_path.joinpath('test-shellhooks-win'),
    )
    shell_pre_file = tmp_path.joinpath(
        'test-shellhooks-win', 'inputshellhooks', 'shell_pre.txt'
    )
    shell_post_file = tmp_path.joinpath(
        'test-shellhooks-win', 'inputshellhooks', 'shell_post.txt'
    )
    assert shell_pre_file.exists()
    assert shell_post_file.exists()


@pytest.mark.usefixtures("clean_system", "remove_additional_folders")
def test_ignore_shell_hooks(tmp_path) -> None:
    """Verify *.txt files not created, when accept_hooks=False."""
    generate.generate_files(
        context={"cookiecutter": {"shellhooks": "shellhooks"}},
        repo_dir="tests/test-shellhooks/",
        output_dir=tmp_path.joinpath('test-shellhooks'),
        accept_hooks=False,
    )
    shell_pre_file = tmp_path.joinpath("test-shellhooks/inputshellhooks/shell_pre.txt")
    shell_post_file = tmp_path.joinpath(
        "test-shellhooks/inputshellhooks/shell_post.txt"
    )
    assert not shell_pre_file.exists()
    assert not shell_post_file.exists()


@pytest.mark.usefixtures("clean_system", "remove_additional_folders")
def test_deprecate_run_hook_from_repo_dir(tmp_path) -> None:
    """Test deprecation warning in generate._run_hook_from_repo_dir."""
    repo_dir = "tests/test-shellhooks/"
    project_dir = Path(tmp_path.joinpath('test-shellhooks'))
    project_dir.mkdir()
    with pytest.deprecated_call():
        generate._run_hook_from_repo_dir(
            repo_dir=repo_dir,
            hook_name="pre_gen_project",
            project_dir=project_dir,
            context={},
            delete_project_on_failure=False,
        )
