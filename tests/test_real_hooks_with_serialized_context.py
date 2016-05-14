#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_real_hooks_with_context_serialized
---------------------------------------

Additional tests for `cookiecutter.hooks` module.
"""

import os

from cookiecutter import hooks, utils


class TestRealHooks(object):
    repo_path = os.path.abspath(
        'tests/test-real-hooks-with-serialized-context')
    hooks_path = repo_path + '/hooks'

    def test_run_script_with_context(self):
        """
        Execute a hook script, passing a serialized context object and
        getting the context not updated
        """

        context = {
            "my_key": "my_val"
        }
        actual = hooks.run_script(
            os.path.join(
                self.repo_path, 'simple', 'hooks', 'pre_gen_project.py'),
            context=context
        )

        assert actual == context

    def test_run_script_get_updated_context(self):
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
        actual = hooks.run_script(
            os.path.join(
                self.repo_path,
                'update_context',
                'hooks',
                'pre_gen_project.py'
            ),
            context=context
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
