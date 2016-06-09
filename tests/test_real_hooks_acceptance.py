#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_real_hooks_acceptance
--------------------------

Additional tests for `cookiecutter.hooks` module.
"""

import os
import sys


from .support import read_file, AbstractAcceptanceTest


class TestRealHooksAcceptance(AbstractAcceptanceTest):

    def _repo_id(self):
        return 'test-real-hooks-acceptance'

    def assert_real_hook_is_run_in_place(self, template):
        """
        assert that the real hook is run in place
        :param template: template id
        """
        template_dir = os.path.join(self.templates_path, template)
        file = os.path.join(self.project_dir, template)
        self.run(template)
        assert os.path.exists(file)
        content = read_file(file)
        assert template_dir == content.strip()

    def test_renderable_hooks_can_be_run(self):
        """
        regression test
        """
        template = 'renderable'
        self.run(template)
        assert os.path.exists(os.path.join(self.project_dir, template))

    def test_run_real_hook_in_place(self):
        """
        run a real hook in place: python file
        """
        self.assert_real_hook_is_run_in_place('inplace')

    def test_run_real_hook_in_place_shell(self):
        """
        run a real hook in place: bash or batch file depending on the OS
        """
        template = 'batch' if sys.platform.startswith('win') else 'bash'
        self.assert_real_hook_is_run_in_place(template)

    def test_run_pre_user_prompt_hook(self, mocker):
        """
        used to populate the context before the user is prompted for config
        """
        self.configure('pre_user_prompt')
        self.settings.no_input = False
        license = u'BSD-3'
        variables = {
            'project_name': self.project,
            'project_slug': self.project_dir
        }

        def _read_user_variable(*args, **kwargs):
            return variables[args[0]] if args[0] in variables else args[1]

        read_variable = mocker.patch('cookiecutter.prompt.read_user_variable')
        read_variable.side_effect = _read_user_variable
        read_choice = mocker.patch('cookiecutter.prompt.read_user_choice')
        read_choice.return_value = license

        self.run()
        assert os.path.exists(os.path.join(self.project_dir, license))
