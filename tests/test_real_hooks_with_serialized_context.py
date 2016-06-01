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
import sys
import subprocess
import pytest

from cookiecutter import hooks, utils


class TestRealHooks(object):
    repo_path = os.path.abspath(
        'tests/test-real-hooks-with-serialized-context')
    hooks_path = repo_path + '/hooks'

    def setup_method(self, method):
        self.old_popen = subprocess.Popen
        self.old_platform = sys.platform
        self.old_logging = hooks.logging

    def teardown_method(self, method):
        subprocess.Popen = self.old_popen
        sys.platform = self.old_platform
        hooks.logging = self.old_logging

    def run_script_with_context(self, repo_id, context):
        """
        Helper method to execute hooks.run_script_with_context on a given repo
        :param repo_id: repository identifier
        :param context: context dictionary
        """
        return hooks.run_script_with_context(
            os.path.join(
                self.repo_path,
                repo_id,
                'hooks',
                'pre_gen_project.py'
            ),
            'tests',
            context
        )

    def run_hook(self, repo_id, context, hook_name='pre_gen_project'):
        """
        Helper method to execute hooks.run_hook on a given repo
        :param repo_id: repository identifier
        :param context: context dictionary
        :param hook_name: hook name to run
        """
        return hooks.run_hook(
            hook_name,
            os.path.join(
                self.repo_path,
                repo_id,
                'input{{' + repo_id + '_hooks}}'
            ),
            context
        )

    def __new_patcher(self, to_be_mocked, configuration=None):
        """
        Helper factory method to create a configurable mock patcher
        of a given type
        :param to_be_mocked: the object type to get a mock from
        :param configuration: the configuration dictionary
        """
        patcher = mock.patch(to_be_mocked, new=mock.MagicMock())
        omock = patcher.start()
        if configuration is not None:
            omock.configure_mock(**configuration)

        return patcher

    def __configure_mock(self, mock_object, configuration):
        """
        Helper method to configure a given mock object
        :param mock_object: the mock to configure
        :param configuration: the configuration dictionary
        """
        omock = mock_object.return_value
        omock.configure_mock(**configuration)

        return omock

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
        actual = self.run_script_with_context('update_context', context)

        assert actual == expected

    def test_run_script_with_context_returns_context(self):
        """
        Execute a hook script, passing a serialized context object
        """
        context = {
            "my_key": "my_val"
        }
        actual = self.run_script_with_context('simple', context)

        assert actual == context

    def test_run_hook_returns_context(self):
        """
        Execute a hook script, passing a serialized context object
        """
        context = {
            "my_key": "my_val"
        }

        with utils.work_in(os.path.join(self.repo_path, 'simple')):
            actual = self.run_hook('simple', context)

            assert actual == context

        with utils.work_in(os.path.join(self.repo_path, 'update_context')):
            expected = {
                "my_key": "my_val_updated"
            }
            actual = self.run_hook('update_context', context)

            assert actual == expected

        with utils.work_in(os.path.join(self.repo_path, 'update_context')):
            actual = self.run_hook(
                'update_context',
                context,
                'not_handled_hook'
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

        actual = self.run_script_with_context('bad_json', context)

        assert actual == context

    @mock.patch('cookiecutter.hooks.logging')
    @mock.patch('subprocess.Popen', autospec=True)
    def test_handle_lost_stdin_during_communication_on_windows_os(
        self, mock_popen, mock_logging
    ):
        """
        Ensure that an OSError raised from Popen._stdin_write is correctly
        caught and logged, while not blocking the process on windows OS
        :param mock_popen: subprocess.Poper mock
        """
        context = {
            "my_key": "my_val"
        }

        self.__configure_mock(
            mock_popen,
            {
                'communicate.side_effect': OSError(
                    errno.EINVAL, 'Invalid Argument'
                ),
                'communicate.return_value': json.dumps(context).encode(),
                'wait.return_value': 0
            }
        )

        patcher_platform = self.__new_patcher(
            'sys.platform',
            {'startswith.return_value': True}
        )

        try:
            actual = self.run_script_with_context('simple', context)

            mock_logging.warn.assert_called_with(
                'Popen.communicate failed certainly ' +
                'because of the issue #19612'
            )
            assert actual == context

        finally:
            patcher_platform.stop()

    @mock.patch('subprocess.Popen', autospec=True)
    def test_handle_oserror_during_communication_on_non_windows_os(
        self, mock_popen
    ):
        """
        Ensure that an OSError raised on a non windows os is bubbled up
        :param mock_popen: subprocess.Poper mock
        """
        self.__configure_mock(
            mock_popen,
            {
                'communicate.side_effect': OSError(
                    errno.EINVAL, 'Invalid Argument'
                )
            }
        )

        patcher_platform = self.__new_patcher(
            'sys.platform',
            {'startswith.return_value': False}
        )

        try:
            with pytest.raises(OSError) as excinfo:
                self.run_script_with_context('simple', {})

            assert excinfo.value.errno == errno.EINVAL

        finally:
            patcher_platform.stop()
