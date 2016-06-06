#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_real_hooks_acceptance
--------------------------

Additional tests for `cookiecutter.hooks` module.
"""

import os
import sys
import tempfile

from cookiecutter.utils import rmtree
from .support import SettingObject, Runner


class TestRealHooksAcceptance(object):
    repo_path = os.path.abspath(
        'tests/test-real-hooks-acceptance')
    templates_path = os.path.join(repo_path, 'templates')
    rcfile = os.path.join(repo_path, 'cookiecutterrc')
    default_project = 'Dummy Project'
    default_project_dir = 'dummy-project'

    def setup_method(self, method):
        self.runner = None
        self.settings = None
        self.__prepare_test_environment()

    def teardown_method(self, method):
        self.runner = None
        self.settings = None
        self.__cleanup_test_environment()

    def __prepare_test_environment(self):
        """
        helper method to prepare the test environment
        """
        self.output_dir = tempfile.mkdtemp()
        assert os.path.exists(self.output_dir)
        self.project_dir = os.path.join(
            self.output_dir, self.default_project_dir)

    def __cleanup_test_environment(self):
        """
        helper method to clean up the test environment
        """
        rmtree(self.output_dir)
        assert not os.path.exists(self.output_dir)

    def configure(self, template, extra_context=None, config_file=None):
        """
        configure the runtime environment
        :param template: name of the template
        :param extra_context: extra context dictionary
        :param config_file: path to the user cookiecutterrc file
        """
        template_dir = os.path.join(self.templates_path, template)
        assert os.path.exists(template_dir)
        context = {"project_name": self.default_project} if not extra_context \
            else extra_context
        config = self.rcfile if not config_file else config_file

        self.settings = SettingObject(
            template_dir, config, context, self.output_dir)
        self.runner = Runner(self.settings)

    def run(self, template=None):
        """
        run cookiecutter
        :param template: template name if a default configuration is sufficient
        """
        if template:
            self.configure(template)
        assert self.runner
        self.runner.run()

    def assert_real_hook_is_run_in_place(self, template):
        """
        assert that the real hook is run in place
        :param template: template id
        """
        template_dir = os.path.join(self.templates_path, template)
        file = os.path.join(self.project_dir, template)
        self.run(template)
        assert os.path.exists(file)
        content = open(file, 'r').read()
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
