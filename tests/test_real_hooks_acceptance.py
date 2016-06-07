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
