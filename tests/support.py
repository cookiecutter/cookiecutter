#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
support
-------

Add test support utilities which are globally available throughout the suite.
"""
import os
import tempfile

from abc import ABCMeta, abstractmethod
from cookiecutter.main import cookiecutter
from cookiecutter.utils import rmtree


def read_file(file):
    """
    helper method to get the content of a given file
    :param file: the file to read
    """
    fd = open(file, 'r')
    content = fd.read()
    fd.close()

    return content


class Runner(object):
    """
    helper class to run cookierunner main command
    """

    def __init__(self, settings):
        """
        :param settings: SettingObject instance
        """
        self.settings = settings

    def run(self):
        """
        run cookiecutter
        """
        cookiecutter(
            self.settings.template,
            self.settings.checkout,
            self.settings.no_input,
            self.settings.extra_context,
            self.settings.replay,
            self.settings.overwrite_if_exists,
            self.settings.output_dir,
            self.settings.config_file
        )


class SettingObject(object):
    """
    config object to pass to the runner instance to configure the cookiecutter
    runtime environment
    """

    def __init__(
        self, template_dir, config_file,
        extra_context=None, output_dir=u'.'
    ):
        """
        :param template_dir: the template directory
        :param config_file: path to the user cookiecutterrc file
        :param extra_context: extra context dictionary
        :output_dir: output directory
        """
        self.template = template_dir
        self.checkout = None
        self.no_input = True
        self.extra_context = extra_context
        self.replay = False
        self.overwrite_if_exists = False
        self.output_dir = output_dir
        self.config_file = config_file


class AbstractAcceptanceTest(object):
    """
    abstract base class to create acceptance tests

    to use this class, after having imported it :
    1. create a test class that inherits from this abstract class
    2. implement the abstract method _repo_id
    3. write your test methods as usual and consume the public api of
    this class

    eq.
    from .support import AbstractAcceptanceTest

    class TestFeatureAcceptance(AbstractAcceptanceTest):
        def _repo_id(self):
            # this means fixtures are set under ./tests/test-feature-acceptance
            return 'test-feature-acceptance'

        def test_some_behaviour(self):
            self.run('template')
            assert my_expected_behaviour_of_my_template
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def _repo_id(self):
        """
        abstract property to be implemented by acceptance tests
        it should return the directory basename in which are set the templates
        used to build the tests
        ie. return 'test-feature-acceptance'
        """

    def setup_method(self, method):
        """
        setup method
        take care of calling the super().setup_method() in case of overwriting
        """
        self.__setup()
        self.__reset_runtime()
        self.__prepare_test_environment()

    def teardown_method(self, method):
        """
        teardown method
        take care of calling the super().teardown_method() in case of
        overwriting
        """
        self.__reset_runtime()
        self.__cleanup_test_environment()

    @property
    def repo_path(self):
        """
        path of the test repository in which are set test fixtures
        read-only
        """
        return os.path.join(self.__tests_dir, self._repo_id())

    @property
    def user_config(self):
        """
        user configuration file
        taken from repo_path if it exists or from the main fixtures directory
        by default
        it has to be named: cookiecutterrc
        read-only
        """
        name = 'cookiecutterrc'
        rcfile = os.path.join(self.repo_path, name)

        return rcfile if os.path.exists(rcfile) else os.path.join(
            self.__tests_dir, 'fixtures', name)

    @property
    def templates_path(self):
        """
        path of the directory where lie templates fixtures
        read-only
        """
        return os.path.join(self.repo_path, 'templates')

    @property
    def project(self):
        """
        project name
        """
        return self.__project

    @project.setter
    def project(self, name):
        """
        project name setter
        :param name: name of the project
        """
        self.__project = name

    @property
    def project_dir(self):
        """
        output directory of the current project
        its name is automatically generated from the project name and is
        created under the output_dir
        read-only
        """
        return os.path.join(
            self.output_dir,
            self.project.strip().lower().replace(' ', '-')
        )

    @property
    def output_dir(self):
        """
        output diretory where the project under test is created
        read-only
        """
        if not self.__output_dir:
            self.__output_dir = tempfile.mkdtemp()

        return self.__output_dir

    @property
    def runner(self):
        """
        current cookiecutter runner instance
        read-only
        """
        return self.__runner

    @property
    def settings(self):
        """
        current cookiecutter runner configuration object
        read-only
        """
        return self.__settings

    def configure(self, template, extra_context=None, config_file=None):
        """
        configure the runtime environment
        :param template: name of the template
        :param extra_context: extra context dictionary
        :param config_file: path to the user cookiecutterrc file
        """
        template_dir = os.path.join(self.templates_path, template)
        assert os.path.exists(template_dir)
        context = {"project_name": self.project} if not extra_context \
            else extra_context
        config = self.user_config if not config_file else config_file

        self.__settings = SettingObject(
            template_dir, config, context, self.output_dir)
        self.__runner = Runner(self.settings)

    def run(self, template=None):
        """
        run cookiecutter
        :param template: template name if a default configuration is sufficient
        """
        if template:
            self.configure(template)
        assert self.runner
        self.runner.run()

    ###############
    # PRIVATE API #
    ###############

    def __setup(self):
        """
        helper method to initialize the test class internals
        """
        self.__tests_dir = os.path.abspath('tests')
        self.__output_dir = None
        self.project = 'Dummy Project'

    def __reset_runtime(self):
        """
        helper method to reset the runtime environment
        """
        self.__runner = None
        self.__settings = None

    def __prepare_test_environment(self):
        """
        helper method to prepare the test environment
        """
        assert os.path.exists(self.output_dir)

    def __cleanup_test_environment(self):
        """
        helper method to clean up the test environment
        """
        rmtree(self.output_dir)
        assert not os.path.exists(self.output_dir)
        self.__output_dir = None
