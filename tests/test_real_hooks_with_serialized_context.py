#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_real_hooks_with_context_serialized
---------------------------------------

Additional tests for `cookiecutter.hooks` module.
"""

import os
import errno
import mock
import json

from cookiecutter import hooks, utils
from testfixtures import LogCapture, ShouldRaise


class TestRealHooks(object):
    repo_path = os.path.abspath(
        'tests/test-real-hooks-with-serialized-context')
    hooks_path = repo_path + '/hooks'

    def teardown_method(self, method):
        LogCapture.uninstall_all()

    def test_run_script_with_context_get_updated_context(self):
        """
        Execute a hook script, passing a serialized context object and
        getting the context updated
        """
        context = {
            "my_key": "my_val"
        }
        expected = {
            "my_key": "my_val_updated"
        }
        actual = hooks.run_script_with_context(
            os.path.join(
                self.repo_path,
                'update_context',
                'hooks',
                'pre_gen_project.py'
            ),
            'tests',
            context
        )

        assert actual == expected

    def test_run_script_with_context_returns_context(self):
        """
        Execute a hook script, passing a serialized context object
        """
        context = {
            "my_key": "my_val"
        }
        actual = hooks.run_script_with_context(
            os.path.join(
                self.repo_path, 'simple', 'hooks', 'pre_gen_project.py'),
            'tests',
            context
        )

        assert actual == context

    def test_run_hook_returns_context(self):
        """
        Execute a hook script, passing a serialized context object
        """
        context = {
            "my_key": "my_val"
        }

        with utils.work_in(os.path.join(self.repo_path, 'simple')):
            actual = hooks.run_hook(
                'pre_gen_project',
                os.path.join(
                    self.repo_path,
                    'simple',
                    'input{{simple_hooks}}'
                ),
                context
            )
            assert actual == context

        with utils.work_in(os.path.join(self.repo_path, 'update_context')):
            expected = {
                "my_key": "my_val_updated"
            }
            actual = hooks.run_hook(
                'pre_gen_project',
                os.path.join(
                    self.repo_path,
                    'update_context',
                    'input{{update_context_hooks}}'
                ),
                context
            )
            assert actual == expected

        with utils.work_in(os.path.join(self.repo_path, 'simple')):
            actual = hooks.run_hook(
                'not_handled_hook',
                os.path.join(
                    self.repo_path,
                    'simple',
                    'input{{simple_hooks}}'
                ),
                context
            )
            assert actual == context

    def test_run_script_with_context_runs_hook_in_place(self):
        """
        Execute a hook script in place, passing a serialized context object
        """
        hook = os.path.join(
            self.repo_path,
            'inplace',
            'hooks',
            'pre_gen_project.py'
        )
        context = {
            "_run_hook_in_place": True
        }
        expected = {
            "_run_hook_in_place": True,
            "inplace": hook
        }
        actual = hooks.run_script_with_context(hook, 'tests', context)

        assert actual == expected

    def test_getting_bad_json_returns_original_context(self):
        """
        Execute a hook script that returns bad json
        """
        context = {
            "my_key": "my_val",
        }

        actual = hooks.run_script_with_context(
            os.path.join(
                self.repo_path,
                'bad_json',
                'hooks',
                'pre_gen_project.py'
            ),
            'tests',
            context
        )

        assert actual == context

    @mock.patch('sys.platform')
    @mock.patch('subprocess.Popen', autospec=True)
    def test_handle_lost_stdin_during_communication_on_windows_os(
        self, mock_popen, mock_platform
    ):
        """
        Ensure that an OSError raised from Popen._stdin_write is correctly
        caught and logged, while not blocking the process on windows OS
        """
        context = {
            "my_key": "my_val"
        }

        log = LogCapture()

        proc = mock_popen.return_value
        proc.communicate.side_effect = OSError(
            errno.EINVAL, 'Invalid Argument'
        )
        proc.communicate.return_value = json.dumps(context).encode()
        proc.wait.return_value = 0

        platform = mock_platform.return_value
        platform.return_value = "win32"

        actual = hooks.run_script_with_context(
            os.path.join(
                self.repo_path, 'simple', 'hooks', 'pre_gen_project.py'),
            'tests',
            context
        )

        log.check(
            ('root', 'WARNING', 'Popen.communicate failed certainly ' +
                'because of the issue #19612')
        )
        assert actual == context

    @mock.patch('sys.platform')
    @mock.patch('subprocess.Popen', autospec=True)
    def test_handle_oserror_during_communication_on_non_windows_os(
        self, mock_popen, mock_platform
    ):
        """
        Ensure that an OSError raised on a non windows os is bubbled up
        """
        proc = mock_popen.return_value
        proc.communicate.side_effect = OSError(
            errno.EINVAL, 'Invalid Argument'
        )

        platform = mock_platform.return_value
        platform.return_value = "linux2"

        # with pytest.raises(OSError) as excinfo:
        with ShouldRaise() as s:
            hooks.run_script_with_context(
                os.path.join(
                    self.repo_path, 'simple', 'hooks', 'pre_gen_project.py'),
                'tests',
                {}
            )
            assert s.raised.code == errno.EINVAL
