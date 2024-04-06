"""Tests for `cookiecutter.hooks` module."""

import errno
import os
import stat
import sys
import textwrap
from pathlib import Path

import pytest

from cookiecutter import exceptions, hooks, utils


def make_test_repo(name: str, multiple_hooks: bool = False) -> str:
    """Create test repository for test setup methods."""
    hook_dir = os.path.join(name, 'hooks')
    template = os.path.join(name, 'input{{hooks}}')
    os.mkdir(name)
    os.mkdir(hook_dir)
    os.mkdir(template)

    Path(template, 'README.rst').write_text("foo\n===\n\nbar\n")

    with Path(hook_dir, 'pre_gen_project.py').open('w') as f:
        f.write("#!/usr/bin/env python\n")
        f.write("# -*- coding: utf-8 -*-\n")
        f.write("from __future__ import print_function\n")
        f.write("\n")
        f.write("print('pre generation hook')\n")
        f.write("f = open('python_pre.txt', 'w')\n")
        f.write("f.close()\n")

    if sys.platform.startswith('win'):
        post = 'post_gen_project.bat'
        with Path(hook_dir, post).open('w') as f:
            f.write("@echo off\n")
            f.write("\n")
            f.write("echo post generation hook\n")
            f.write("echo. >shell_post.txt\n")
    else:
        post = 'post_gen_project.sh'
        filename = os.path.join(hook_dir, post)
        with Path(filename).open('w') as f:
            f.write("#!/bin/bash\n")
            f.write("\n")
            f.write("echo 'post generation hook';\n")
            f.write("touch 'shell_post.txt'\n")
        # Set the execute bit
        os.chmod(filename, os.stat(filename).st_mode | stat.S_IXUSR)

    # Adding an additional pre script
    if multiple_hooks:
        if sys.platform.startswith('win'):
            pre = 'pre_gen_project.bat'
            with Path(hook_dir, pre).open('w') as f:
                f.write("@echo off\n")
                f.write("\n")
                f.write("echo post generation hook\n")
                f.write("echo. >shell_pre.txt\n")
        else:
            pre = 'pre_gen_project.sh'
            filename = os.path.join(hook_dir, pre)
            with Path(filename).open('w') as f:
                f.write("#!/bin/bash\n")
                f.write("\n")
                f.write("echo 'post generation hook';\n")
                f.write("touch 'shell_pre.txt'\n")
            # Set the execute bit
            os.chmod(filename, os.stat(filename).st_mode | stat.S_IXUSR)

    return post


class TestFindHooks:
    """Class to unite find hooks related tests in one place."""

    repo_path = 'tests/test-hooks'

    def setup_method(self, _method) -> None:
        """Find hooks related tests setup fixture."""
        self.post_hook = make_test_repo(self.repo_path)

    def teardown_method(self, _method) -> None:
        """Find hooks related tests teardown fixture."""
        utils.rmtree(self.repo_path)

    def test_find_hook(self) -> None:
        """Finds the specified hook."""
        with utils.work_in(self.repo_path):
            expected_pre = os.path.abspath('hooks/pre_gen_project.py')
            actual_hook_path = hooks.find_hook('pre_gen_project')
            assert actual_hook_path
            assert expected_pre == actual_hook_path[0]

            expected_post = os.path.abspath(f'hooks/{self.post_hook}')
            actual_hook_path = hooks.find_hook('post_gen_project')
            assert actual_hook_path
            assert expected_post == actual_hook_path[0]

    def test_no_hooks(self) -> None:
        """`find_hooks` should return None if the hook could not be found."""
        with utils.work_in('tests/fake-repo'):
            assert None is hooks.find_hook('pre_gen_project')

    def test_unknown_hooks_dir(self) -> None:
        """`find_hooks` should return None if hook directory not found."""
        with utils.work_in(self.repo_path):
            assert hooks.find_hook('pre_gen_project', hooks_dir='hooks_dir') is None

    def test_hook_not_found(self) -> None:
        """`find_hooks` should return None if the hook could not be found."""
        with utils.work_in(self.repo_path):
            assert hooks.find_hook('unknown_hook') is None


class TestExternalHooks:
    """Class to unite tests for hooks with different project paths."""

    repo_path = os.path.abspath('tests/test-hooks/')
    hooks_path = os.path.abspath('tests/test-hooks/hooks')

    def setup_method(self, _method) -> None:
        """External hooks related tests setup fixture."""
        self.post_hook = make_test_repo(self.repo_path, multiple_hooks=True)

    def teardown_method(self, _method) -> None:
        """External hooks related tests teardown fixture."""
        utils.rmtree(self.repo_path)

        if os.path.exists('python_pre.txt'):
            os.remove('python_pre.txt')
        if os.path.exists('shell_post.txt'):
            os.remove('shell_post.txt')
        if os.path.exists('shell_pre.txt'):
            os.remove('shell_pre.txt')
        if os.path.exists('tests/shell_post.txt'):
            os.remove('tests/shell_post.txt')
        if os.path.exists('tests/test-hooks/input{{hooks}}/python_pre.txt'):
            os.remove('tests/test-hooks/input{{hooks}}/python_pre.txt')
        if os.path.exists('tests/test-hooks/input{{hooks}}/shell_post.txt'):
            os.remove('tests/test-hooks/input{{hooks}}/shell_post.txt')
        if os.path.exists('tests/context_post.txt'):
            os.remove('tests/context_post.txt')

    def test_run_script(self) -> None:
        """Execute a hook script, independently of project generation."""
        hooks.run_script(os.path.join(self.hooks_path, self.post_hook))
        assert os.path.isfile('shell_post.txt')

    def test_run_failing_script(self, mocker) -> None:
        """Test correct exception raise if run_script fails."""
        err = OSError()

        prompt = mocker.patch('subprocess.Popen')
        prompt.side_effect = err

        with pytest.raises(exceptions.FailedHookException) as excinfo:
            hooks.run_script(os.path.join(self.hooks_path, self.post_hook))
        assert f'Hook script failed (error: {err})' in str(excinfo.value)

    def test_run_failing_script_enoexec(self, mocker) -> None:
        """Test correct exception raise if run_script fails."""
        err = OSError()
        err.errno = errno.ENOEXEC

        prompt = mocker.patch('subprocess.Popen')
        prompt.side_effect = err

        with pytest.raises(exceptions.FailedHookException) as excinfo:
            hooks.run_script(os.path.join(self.hooks_path, self.post_hook))
        assert 'Hook script failed, might be an empty file or missing a shebang' in str(
            excinfo.value
        )

    def test_run_script_cwd(self) -> None:
        """Change directory before running hook."""
        hooks.run_script(os.path.join(self.hooks_path, self.post_hook), 'tests')
        assert os.path.isfile('tests/shell_post.txt')
        assert 'tests' not in os.getcwd()

    def test_run_script_with_context(self) -> None:
        """Execute a hook script, passing a context."""
        hook_path = os.path.join(self.hooks_path, 'post_gen_project.sh')

        if sys.platform.startswith('win'):
            post = 'post_gen_project.bat'
            with Path(self.hooks_path, post).open('w') as f:
                f.write("@echo off\n")
                f.write("\n")
                f.write("echo post generation hook\n")
                f.write("echo. >{{cookiecutter.file}}\n")
        else:
            with Path(hook_path).open('w') as fh:
                fh.write("#!/bin/bash\n")
                fh.write("\n")
                fh.write("echo 'post generation hook';\n")
                fh.write("touch 'shell_post.txt'\n")
                fh.write("touch '{{cookiecutter.file}}'\n")
                os.chmod(hook_path, os.stat(hook_path).st_mode | stat.S_IXUSR)

        hooks.run_script_with_context(
            os.path.join(self.hooks_path, self.post_hook),
            'tests',
            {'cookiecutter': {'file': 'context_post.txt'}},
        )
        assert os.path.isfile('tests/context_post.txt')
        assert 'tests' not in os.getcwd()

    def test_run_hook(self) -> None:
        """Execute hook from specified template in specified output \
        directory."""
        tests_dir = os.path.join(self.repo_path, 'input{{hooks}}')
        with utils.work_in(self.repo_path):
            hooks.run_hook('pre_gen_project', tests_dir, {})
            assert os.path.isfile(os.path.join(tests_dir, 'python_pre.txt'))
            assert os.path.isfile(os.path.join(tests_dir, 'shell_pre.txt'))

            hooks.run_hook('post_gen_project', tests_dir, {})
            assert os.path.isfile(os.path.join(tests_dir, 'shell_post.txt'))

    def test_run_failing_hook(self) -> None:
        """Test correct exception raise if hook exit code is not zero."""
        hook_path = os.path.join(self.hooks_path, 'pre_gen_project.py')
        tests_dir = os.path.join(self.repo_path, 'input{{hooks}}')

        with Path(hook_path).open('w') as f:
            f.write("#!/usr/bin/env python\n")
            f.write("import sys; sys.exit(1)\n")

        with utils.work_in(self.repo_path):
            with pytest.raises(exceptions.FailedHookException) as excinfo:
                hooks.run_hook('pre_gen_project', tests_dir, {})
            assert 'Hook script failed' in str(excinfo.value)


@pytest.fixture()
def dir_with_hooks(tmp_path):
    """Yield a directory that contains hook backup files."""
    hooks_dir = tmp_path.joinpath('hooks')
    hooks_dir.mkdir()

    pre_hook_content = textwrap.dedent(
        """
        #!/usr/bin/env python
        # -*- coding: utf-8 -*-
        print('pre_gen_project.py~')
        """
    )
    pre_gen_hook_file = hooks_dir.joinpath('pre_gen_project.py~')
    pre_gen_hook_file.write_text(pre_hook_content, encoding='utf8')

    post_hook_content = textwrap.dedent(
        """
        #!/usr/bin/env python
        # -*- coding: utf-8 -*-
        print('post_gen_project.py~')
        """
    )

    post_gen_hook_file = hooks_dir.joinpath('post_gen_project.py~')
    post_gen_hook_file.write_text(post_hook_content, encoding='utf8')

    # Make sure to yield the parent directory as `find_hooks()`
    # looks into `hooks/` in the current working directory
    yield str(tmp_path)

    pre_gen_hook_file.unlink()
    post_gen_hook_file.unlink()


def test_ignore_hook_backup_files(monkeypatch, dir_with_hooks) -> None:
    """Test `find_hook` correctly use `valid_hook` verification function."""
    # Change the current working directory that contains `hooks/`
    monkeypatch.chdir(dir_with_hooks)
    assert hooks.find_hook('pre_gen_project') is None
    assert hooks.find_hook('post_gen_project') is None
