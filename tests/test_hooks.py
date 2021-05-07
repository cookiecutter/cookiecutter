"""Tests for `cookiecutter.hooks` module."""
import errno
import stat
import sys
import textwrap
from pathlib import Path

import pytest

from cookiecutter import hooks, utils, exceptions


def make_test_repo(name, multiple_hooks=False):
    """Create test repository for test setup methods."""
    hook_dir = Path(name, 'hooks')
    template = Path(name, 'input{{hooks}}')
    Path(name).mkdir()
    hook_dir.mkdir()
    template.mkdir()

    with open(Path(template, 'README.rst'), 'w') as f:
        f.write("foo\n===\n\nbar\n")

    with open(Path(hook_dir, 'pre_gen_project.py'), 'w') as f:
        f.write("#!/usr/bin/env python\n")
        f.write("# -*- coding: utf-8 -*-\n")
        f.write("from __future__ import print_function\n")
        f.write("\n")
        f.write("print('pre generation hook')\n")
        f.write("f = open('python_pre.txt', 'w')\n")
        f.write("f.close()\n")

    if sys.platform.startswith('win'):
        post = 'post_gen_project.bat'
        with open(Path(hook_dir, post), 'w') as f:
            f.write("@echo off\n")
            f.write("\n")
            f.write("echo post generation hook\n")
            f.write("echo. >shell_post.txt\n")
    else:
        post = 'post_gen_project.sh'
        filename = Path(hook_dir, post)
        with open(filename, 'w') as f:
            f.write("#!/bin/bash\n")
            f.write("\n")
            f.write("echo 'post generation hook';\n")
            f.write("touch 'shell_post.txt'\n")
        # Set the execute bit
        filename.chmod(filename.stat().st_mode | stat.S_IXUSR)

    # Adding an additional pre script
    if multiple_hooks:
        if sys.platform.startswith('win'):
            pre = 'pre_gen_project.bat'
            with open(Path(hook_dir, pre), 'w') as f:
                f.write("@echo off\n")
                f.write("\n")
                f.write("echo post generation hook\n")
                f.write("echo. >shell_pre.txt\n")
        else:
            pre = 'pre_gen_project.sh'
            filename = Path(hook_dir, pre)
            with open(filename, 'w') as f:
                f.write("#!/bin/bash\n")
                f.write("\n")
                f.write("echo 'post generation hook';\n")
                f.write("touch 'shell_pre.txt'\n")
            # Set the execute bit
            filename.chmod(filename.stat().st_mode | stat.S_IXUSR)

    return post


class TestFindHooks(object):
    """Class to unite find hooks related tests in one place."""

    repo_path = 'tests/test-hooks'

    def setup_method(self, method):
        """Find hooks related tests setup fixture."""
        self.post_hook = make_test_repo(self.repo_path)

    def teardown_method(self, method):
        """Find hooks related tests teardown fixture."""
        utils.rmtree(self.repo_path)

    def test_find_hook(self):
        """Finds the specified hook."""
        with utils.work_in(self.repo_path):
            expected_pre = Path('hooks/pre_gen_project.py').resolve()
            actual_hook_path = hooks.find_hook('pre_gen_project')
            assert str(expected_pre) == actual_hook_path[0]

            expected_post = Path('hooks/{}'.format(self.post_hook)).resolve()
            actual_hook_path = hooks.find_hook('post_gen_project')
            assert str(expected_post) == actual_hook_path[0]

    def test_no_hooks(self):
        """`find_hooks` should return None if the hook could not be found."""
        with utils.work_in('tests/fake-repo'):
            assert None is hooks.find_hook('pre_gen_project')

    def test_unknown_hooks_dir(self):
        """`find_hooks` should return None if hook directory not found."""
        with utils.work_in(self.repo_path):
            assert hooks.find_hook('pre_gen_project', hooks_dir='hooks_dir') is None

    def test_hook_not_found(self):
        """`find_hooks` should return None if the hook could not be found."""
        with utils.work_in(self.repo_path):
            assert hooks.find_hook('unknown_hook') is None


class TestExternalHooks(object):
    """Class to unite tests for hooks with different project paths."""

    repo_path = Path('tests/test-hooks/').resolve()
    hooks_path = Path('tests/test-hooks/hooks').resolve()

    def setup_method(self, method):
        """External hooks related tests setup fixture."""
        self.post_hook = make_test_repo(self.repo_path, multiple_hooks=True)

    def teardown_method(self, method):
        """External hooks related tests teardown fixture."""
        utils.rmtree(self.repo_path)

        paths = [
            Path('python_pre.txt'),
            Path('shell_post.txt'),
            Path('shell_pre.txt'),
            Path('tests/shell_post.txt'),
            Path('tests/test-hooks/input{{hooks}}/python_pre.txt'),
            Path('tests/test-hooks/input{{hooks}}/shell_post.txt'),
            Path('tests/context_post.txt'),
        ]
        for path in paths:
            if path.exists():
                path.unlink()

    def test_run_script(self):
        """Execute a hook script, independently of project generation."""
        hooks.run_script(str(self.hooks_path.joinpath(self.post_hook)))
        assert Path('shell_post.txt').is_file()

    def test_run_failing_script(self, mocker):
        """Test correct exception raise if run_script fails."""
        err = OSError()

        prompt = mocker.patch('subprocess.Popen')
        prompt.side_effect = err

        with pytest.raises(exceptions.FailedHookException) as excinfo:
            hooks.run_script(str(self.hooks_path.joinpath(self.post_hook)))
        assert 'Hook script failed (error: {})'.format(err) in str(excinfo.value)

    def test_run_failing_script_enoexec(self, mocker):
        """Test correct exception raise if run_script fails."""
        err = OSError()
        err.errno = errno.ENOEXEC

        prompt = mocker.patch('subprocess.Popen')
        prompt.side_effect = err

        with pytest.raises(exceptions.FailedHookException) as excinfo:
            hooks.run_script(str(self.hooks_path.joinpath(self.post_hook)))
        assert 'Hook script failed, might be an empty file or missing a shebang' in str(
            excinfo.value
        )

    def test_run_script_cwd(self):
        """Change directory before running hook."""
        hooks.run_script(str(self.hooks_path.joinpath(self.post_hook)), 'tests')
        assert Path('tests/shell_post.txt').is_file()
        assert 'tests' not in str(Path.cwd())

    def test_run_script_with_context(self):
        """Execute a hook script, passing a context."""
        hook_path = self.hooks_path.joinpath('post_gen_project.sh')

        if sys.platform.startswith('win'):
            post = 'post_gen_project.bat'
            with open(self.hooks_path.joinpath(post), 'w') as f:
                f.write("@echo off\n")
                f.write("\n")
                f.write("echo post generation hook\n")
                f.write("echo. >{{cookiecutter.file}}\n")
        else:
            with open(hook_path, 'w') as fh:
                fh.write("#!/bin/bash\n")
                fh.write("\n")
                fh.write("echo 'post generation hook';\n")
                fh.write("touch 'shell_post.txt'\n")
                fh.write("touch '{{cookiecutter.file}}'\n")
                hook_path.chmod(hook_path.stat().st_mode | stat.S_IXUSR)

        hooks.run_script_with_context(
            self.hooks_path.joinpath(self.post_hook),
            'tests',
            {'cookiecutter': {'file': 'context_post.txt'}},
        )
        assert Path('tests/context_post.txt').is_file()
        assert 'tests' not in str(Path.cwd())

    def test_run_hook(self):
        """Execute hook from specified template in specified output \
        directory."""
        tests_dir = self.repo_path.joinpath('input{{hooks}}')
        with utils.work_in(self.repo_path):
            hooks.run_hook('pre_gen_project', str(tests_dir), {})
            assert tests_dir.joinpath('python_pre.txt').is_file()
            assert tests_dir.joinpath('shell_pre.txt').is_file()

            hooks.run_hook('post_gen_project', str(tests_dir), {})
            assert tests_dir.joinpath('shell_post.txt').is_file()

    def test_run_failing_hook(self):
        """Test correct exception raise if hook exit code is not zero."""
        hook_path = self.hooks_path.joinpath('pre_gen_project.py')
        tests_dir = self.repo_path.joinpath('input{{hooks}}')

        with open(hook_path, 'w') as f:
            f.write("#!/usr/bin/env python\n")
            f.write("import sys; sys.exit(1)\n")

        with utils.work_in(self.repo_path):
            with pytest.raises(exceptions.FailedHookException) as excinfo:
                hooks.run_hook('pre_gen_project', str(tests_dir), {})
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


def test_ignore_hook_backup_files(monkeypatch, dir_with_hooks):
    """Test `find_hook` correctly use `valid_hook` verification function."""
    # Change the current working directory that contains `hooks/`
    monkeypatch.chdir(dir_with_hooks)
    assert hooks.find_hook('pre_gen_project') is None
    assert hooks.find_hook('post_gen_project') is None
